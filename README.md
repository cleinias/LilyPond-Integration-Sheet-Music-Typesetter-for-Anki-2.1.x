# LilyPond-Integration-Sheet-Music-Typesetter-for-Anki-2.1.x
LilyPond Integration (Sheet Music Typesetter) for Anki 2.1.x (tested on versions >=2.1.54)

<b><i>LilyPond - music notation for everyone - <a href="http://lilypond.org/" rel="nofollow">http://lilypond.org/</a> </i></b>
With this addon, you can add sheet music snippets to your deck, wrapped in <code>[lilypond]c d e[/lilypond]</code> tags.
For this addon to work, you have to install <b>LilyPond</b> first. For Windows and Mac, please follow the installation instructions for running <b>LilyPond</b> on the command line. (<b>LilyPond</b> needs to be in your <i>PATH</i>).
<ul><li><b>LilyPond</b> homepage: <a href="http://lilypond.org" rel="nofollow">http://lilypond.org</a> </li><li><b>LilyPond</b> download: <a href="http://lilypond.org/download.html" rel="nofollow">http://lilypond.org/download.html</a> </li><li><b>LilyPond</b> tutorial: <a href="http://lilypond.org/doc/v2.16/Documentation/learning/index.html" rel="nofollow">http://lilypond.org/doc/v2.16/Documentation/learning/index.html</a> </li></ul>Original addon for <b>Anki 2</b> on GitHub: <a href="https://github.com/frostschutz/lilypond-anki" rel="nofollow">https://github.com/frostschutz/lilypond-anki</a> (this addon for Anki 2.1.x is not hosted on GitHub and it is only available on the Anki 2.1.x addons website).

<b>How to use</b>
This addon understands <code>[lilypond]</code> tags:<code>
[lilypond]c d e[/lilypond]</code>
Alternatively, you can create fields dedicated to LilyPond, e.g. <i>front-lilypond</i> or <i>back-lilypond</i>, and omit the <code>
[lilypond]</code> tags for them:<code>
c d e</code>
With <i>lilypond</i> in the field name, it will act as if the entire field content was wrapped in <code>[lilypond][/lilypond]</code> tags.
This addon allows the creation of custom templates (see below), and specifying which template to use:<code>[lilypond=default]c d e[/lilypond]</code>
<code>[lilypond=yourtemplate]c d e[/lilypond]</code>
The name of the default template is <i>default</i>, so <code>[lilypond=default]</code> is identical to <code>[lilypond]</code>.
You can also use templates in <i>lilypond</i> fields by giving them names like <i>front-lilypond-yourtemplate</i>, <i>back-lilypond-yourtemplate</i>.

<b>Mobile/Web support</b>
Anki addons are desktop only, so by default, LilyPond images won't appear on other platforms since those platforms won't know what to make of a <code>[lilypond]</code> tag or how to treat a <i>lilypond</i> field.
However, if you are using <i>lilypond</i> fields, and for each field create another field called <i>lilypondimg</i>, the desktop plugin will autofill it with the <code>[image]</code> tag.
For example, if your field is <i>front-lilypond</i>, with content <code>c d e</code>, and you have another field <i>front-lilypondimg</i>, and use only the <i>front-lilypondimg</i> field in your card template, the image will appear on all platforms (provided that the desktop plugin generated the image once and the images were synced to the other platforms as well).
Note: Please do not add any other text to a <i>lilypondimg</i> field, as it will be overwritten and discarded by the addon.

<b>LilyPond Templates</b>
The <b>addons21/123418104/lilypond</b> directory holds template files for LilyPond.
Templates can be created and edited from Anki, using the Tools-&gt;lilypond menu. An external editor is used. The default editor is <b>xed</b>, but you surely must adapt it for your specific setup: menu Tools-&gt;Addons, select this addon in the list, then click on Config. Modify the JSON config with the editor command (it may be necessary to include the path).
Please restart Anki when you change templates.
The default template is <b>default</b><b>.ly</b> and used by:<code>
[lilypond]code[/lilypond]</code><code>
[lilypond=default]code[/lilypond]</code>
<i>somefield-lilypond</i>
All other templates have to be specified by name:<code>
[lilypond=templatename]code[/lilypond]</code>
<i>somefield-lilypond-templatename</i>
In the template, <code>%ANKI%</code> will be replaced with code.
Multiple codes can be specified, by separating them with <code>%%%</code>:<code>
[lilypond]
code1
%%%
code2
[/lilypond]</code>
In the template, the first occurence of <code>%ANKI%</code> will be replaced with <code>code1</code>, the second occurence of <code>%ANKI%</code> with <code>code2</code>.
The number of <code>%ANKI%</code> in the template has to match the number of codes used for this template always, otherwise the remaining occurences of <code>%ANKI%</code> will not be replaced, or the surplus specified codes will not be inserted.
The default template looks like this:<code>
\paper{
    indent=0\mm
    line-width=120\mm
    oddFooterMarkup=##f
    oddHeaderMarkup=##f
    bookTitleMarkup = ##f
    scoreTitleMarkup = ##f
}
\relative c'' { %ANKI% }</code>
Please refer to the LilyPond homepage and documentation for details on how to write LilyPond code.
