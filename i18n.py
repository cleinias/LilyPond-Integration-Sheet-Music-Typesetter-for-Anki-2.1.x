# -*- coding: utf-8 -*-
# Copyright (c) 2019 Luca Panno <panno.luca@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# internationalisation for LilyPond add-on (Anki 2.1.x)
from anki import lang
txt={
  "LilyPond Template %s not found or not valid.":{
    "fr":"Le modèle LilyPond %s n'a pas été trouvé ou n'est pas valide.",
    "it":"Il modello LilyPond %s non è stato trovato o non è valido."
  },
  "Template: ":{
    "fr":"Modèle : ",
    "it":"modello: "
  },
  "Are you sure to delete this template?":{
    "fr":"Etes-vous sûr de vouloir supprimer ce modèle ?",
    "it":"È certa/o di voler eliminare questo modello?"
  },
  "Please choose a name for your new LilyPond template:":{
    "fr":"Veuillez choisir un nom pour votre nouveau modèle LilyPond :",
    "it":"Scegliete un nome per il suo nuovo modello LilyPond:"
  },
  "Empty template name or invalid characters.":{
    "fr":"Nom de modèle vide ou caractères non valides.",
    "it":"Nome del modello vuoto o caratteri non validi."
  },
  "A template with that name already exists.":{
    "fr":"Un modèle portant ce nom existe déjà.",
    "it":"Esiste già un modello con questo nome."
  },
  "Add template...":{
    "fr":"Ajouter un modèle...",
    "it":"Aggiungere un modello..."
  },
  "Edit...":{
    "fr":"Éditer...",
    "it":"Editare..."
  },
  "Delete...":{
    "fr":"Effacer...",
    "it":"Eliminare..."
  },
  "Could not move PNG file to media dir. No output?<br>":{
    "fr":"Ne peut pas déplacer le fichier PNG vers le répertoire des média. Pas de résultat ?<br>",
    "it":"Impossibile spostare il file MP3 nella cartella dei media. Nessun risultato?<br>"
  },
  "Error executing %s.":{
    "fr":"Erreur en exàcutant %s.",
    "it":"Errore eseguendo %s."
  },
  "Have you installed lilypond? Is your lilypond code correct?":{
    "fr":"Avez-vous installé lilypond? Votre code LilyPond est-il correct ?",
    "it":"Ha installato lilipond? Il suo codice lilypond è corretto?"
  }
}
def _(s):
    l=lang.current_lang
    if l=="en":
        return s
    return txt[s][l]
