# -*- coding: utf-8 -*-
# Copyright (c) 2012 Andreas Klauer <Andreas.Klauer@metamorpher.de>
# Copyright (c) 2019 Luca Panno <panno.luca@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

'''
LilyPond (GNU Music Typesetter) integration addon for Anki 2.1.x

Code is based on / inspired by libanki's LaTeX integration.
'''
# http://lilypond.org/doc/Documentation/usage/lilypond-output-in-other-programs#inserting-lilypond-output-into-other-programs

# --- Imports: ---

from anki.hooks import addHook
from aqt import gui_hooks
from anki.utils import call, checksum, strip_html, tmpfile
from aqt import mw
from aqt.qt import *
from aqt.utils import getOnlyText, showInfo
from html.entities import entitydefs
import cgi, os, re, shutil

from typing import Any
from typing import Dict

from anki.cards import Card
from anki.media import MediaManager
from anki.models import NoteType
from aqt.editor import Editor

import subprocess
from . import i18n
_=i18n._
from PyQt5.QtWidgets import QMessageBox

# --- Globals: ---

editor=mw.addonManager.getConfig(__name__)["editor"]
lilypondTmpFile = tmpfile("lilypond", ".ly")
lilypondCmd = ["lilypond", "-dbackend=eps", "-dno-gs-load-fonts", "-dinclude-eps-fonts", "--o", lilypondTmpFile, "--png", lilypondTmpFile]
lilypondPattern = "%ANKI%"
lilypondSplit = "%%%"
lilypondTemplate = """\\paper{
  indent=0\\mm
  line-width=120\\mm
  oddFooterMarkup=##f
  oddHeaderMarkup=##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}

\\relative c'' { %s }
""" % (lilypondPattern,)
lilypondTemplates = {}
addonDir=__name__.split(".")[0]
tplDir = os.path.join(mw.pm.addonFolder(),addonDir,"user_files")
print("*** ly dir ***") ####debug
print(tplDir) ####debug
lilypondTagRegexp = re.compile(        # Match tagged code
    r"\[lilypond(=(?P<template>[a-z0-9_-]+))?\](?P<code>.+?)\[/lilypond\]", re.DOTALL | re.IGNORECASE)
lilypondFieldRegexp = re.compile(     # Match LilyPond field names
    r"^(?P<field>.*)-lilypond(-(?P<template>[a-z0-9_-]+))?$", re.DOTALL | re.IGNORECASE)
tplNameRegexp = re.compile(r"^[a-z0-9_-]+$", re.DOTALL | re.IGNORECASE) # Template names must match this
imgTagRegexp = re.compile("^<img.*>$", re.DOTALL | re.IGNORECASE)  # Detects if field already contains rendered img
imgFieldSuffix="-lilypondimg" # Suffix on LilyPond field destinations
cardEditorPrefix="clayout" # Prefix on `kind` parameter of card_will_show hook in card template previewer
lilypondCache = {}

# --- Templates: ---

def tplFile(name):
    '''Build the full filename for template name.'''
    return os.path.join(tplDir, "%s.ly" % (name,))

def setTemplate(name, content):
    '''Set and save a template.'''
    lilypondTemplates[name] = content
    f = open(tplFile(name), 'w')
    f.write(content)

def getTemplate(name, code):
    '''Load template by name and fill it with code.'''
    if name is None:
        name="default"

    tpl = None

    if name not in lilypondTemplates:
        try:
            tpl = open(tplFile(name)).read()
            if tpl and lilypondPattern in tpl:
                lilypondTemplates[name] = tpl
        except:
            if name == "default":
                tpl = lilypondTemplate
                setTemplate("default", tpl)
        finally:
            if name not in lilypondTemplates:
                raise IOError("LilyPond Template %s not found or not valid." % (name,))

    # Replace one or more occurences of lilypondPattern

    codes = code.split(lilypondSplit)

    r = lilypondTemplates[name]

    for code in codes:
        r = r.replace(lilypondPattern, code, 1)

    return r

# --- GUI: ---

def templatefiles():
    '''Produce list of template files.'''
    return [f for f in os.listdir(tplDir)
            if f.endswith(".ly")]

def editFile(filename):
    subprocess.run([editor,filename], stdout=subprocess.PIPE)

def removeFile(filename):
    qm = QMessageBox
    title="Template: "+os.path.basename(os.path.normpath(filename))
    res=qm.question(mw, title, "Are you sure to delete this template?", qm.Yes | qm.No)
    if res==qm.Yes:
        os.remove(filename)

def addtemplate():
    '''Dialog to add a new template file.'''
    name = getOnlyText("Please choose a name for your new LilyPond template:")

    if not tplNameRegexp.match(name):
        showInfo("Empty template name or invalid characters.")
        return

    if os.path.exists(tplFile(name)):
        showInfo("A template with that name already exists.")

    setTemplate(name, lilypondTemplate)
    editFile(tplFile(name))

def lilypondMenu(lm):
    '''Extend "lilypond" menu with lilypond template entries.'''
    a = QAction("Add template...", mw)
    a.triggered.connect(addtemplate)
    lm.addAction(a)

    for f in templatefiles():
        m = lm.addMenu(os.path.splitext(f)[0])
        a = QAction(_("Edit..."), mw)
        p = os.path.join(tplDir, f)
        a.triggered.connect(lambda b,p=p: editFile(p))
        m.addAction(a)
        a = QAction(_("Delete..."), mw)
        a.triggered.connect(lambda b,p=p: removeFile(p))
        m.addAction(a)

# --- Functions: ---

def _lyFromHtml(ly):
    '''Convert entities and fix newlines.'''

    ly = re.sub(r"<(br|div|p) */?>", "\n", ly)
    ly = strip_html(ly)

    ly = ly.replace("&nbsp;", " ")

    for match in re.compile(r"&([a-zA-Z]+);").finditer(ly):
        if match.group(1) in entitydefs:
            ly = ly.replace(match.group(), entitydefs[match.group(1)])

    return ly

def _buildImg(ly, fname):
    '''Build the image PNG file itself and add it to the media dir.'''
    lyfile = open(lilypondTmpFile, "w")
    lyfile.write(ly.decode("utf-8"))
    lyfile.close()

    log = open(lilypondTmpFile+".log", "w")

    if call(lilypondCmd, stdout=log, stderr=log):
        return _errMsg("lilypond")

    # add to media
    try:
        shutil.move(lilypondTmpFile+".png", os.path.join(mw.col.media.dir(), fname))
    except:
        return _("Could not move LilyPond PNG file to media dir. No output?<br>")+_errMsg("lilypond")

def _imgLink(template, ly):
    '''Build an <img src> link for given LilyPond code.'''

    # Finalize LilyPond source.
    ly = getTemplate(template, ly)
    ly = ly.encode("utf8")

    # Derive image filename from source.
    fname = "lilypond-%s.png" % (checksum(ly),)
    link = '<img src="%s" alt=%s>' % (fname,ly,)

    # Build image if necessary.
    if os.path.exists(fname):
        return link
    else:
        # avoid errornous cards killing performance
        if fname in lilypondCache:
            return lilypondCache[fname]

        err = _buildImg(ly, fname)
        if err:
            lilypondCache[fname] = err
            return err
        else:
            return link

def _errMsg(type):
    '''Error message, will be displayed in the card itself.'''
    msg = (_("Error executing %s.") % type) + "<br>"
    try:
        log = open(lilypondTmpFile+".log", "r").read()
        if log:
            msg += """<small><pre style="text-align: left">""" + cgi.escape(log) + "</pre></small>"
    except:
        msg += _("Have you installed lilypond? Is your lilypond code correct?")
    return msg

def _getfields(notetype: Union[NoteType,Dict[str,Any]]):
    '''Get list of field names for given note type'''
    return list(field['name'] for field in notetype['flds'])

# --- Hooks: ---

def _mungeString(text: str) -> str:
    """
        Replaces tagged LilyPond code with rendered images
    :return: Text with tags substituted in-place
    """
    for match in lilypondTagRegexp.finditer(text):
        lyCode = _lyFromHtml(match.group(lilypondTagRegexp.groupindex['code']))
        tplName = match.group(lilypondTagRegexp.groupindex['template'])
        text = text.replace(
            match.group(), _imgLink(tplName, lyCode)
        )

    return text

def mungeCard(html: str, card: Card, kind: str):
    if kind.startswith(cardEditorPrefix):
        # In card editor, may contain invalid but tagged LilyPod code
        return html
    return _mungeString(html)

gui_hooks.card_will_show.append(mungeCard)

def mungeFields(txt: str, editor: Editor):#fields, model, data, col):
    '''Parse lilypond tags before they are displayed.'''
    # Fallback if can't identify current field
    # Substitute LilyPond tags
    if editor.currentField is None:
        return txt
    
    fields: list[str] = _getfields(editor.note.model())
    field: str = fields[editor.currentField]
    if fieldMatch := lilypondFieldRegexp.match(field):
        tplName = fieldMatch.group(lilypondFieldRegexp.groupindex['template'])
        imgLink= _imgLink(tplName, _lyFromHtml(txt)) if txt != "" else "" # Check to avoid compiling empty templates
        if (destField := fieldMatch.group(lilypondFieldRegexp.groupindex['field']) + imgFieldSuffix) in fields:
            # Target field exists, populate it
            editor.note[destField] = imgLink
            return txt
        else:
            # Substitute in-place
            if imgTagRegexp.match(txt):
                # Field already contains rendered image
                return txt
            else:
                return imgLink
    elif field.endswith(imgFieldSuffix):
        # Field is a destination for rendered images, won't contain code
        return txt
    else:
        # Normal field
        # Substitute LilyPond tags
        return _mungeString(txt)

addHook("mungeFields", mungeFields)

def profileLoaded():
    '''Create "lilypond" menu'''
    getTemplate(None, "") # creates default.ly if does not exist
    menu=QMenu("lilypond",mw)
    menu.setIcon(QIcon(os.path.join(os.path.join(mw.pm.addonFolder(), addonDir),"lilypond.png")))
    mw.form.menuTools.addSeparator()
    mw.form.menuTools.insertMenu(mw.form.menuTools.menuAction(),menu)
    lilypondMenu(menu)

addHook("profileLoaded", profileLoaded)

# --- End of file. ---
