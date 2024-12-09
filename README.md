# PDF editor

Cette application de bureau propose un certains nombres d'outils permettant de modifier des fichiers pdf. Les outils
proposés ici sont tous gratuits et regroupent notamment :
<ul>
<li>Fusion de PDF</li>
<li>Conversion de PDF vers JPG</li>
<li>Conversion de JPG vers PDF</li>
</ul>

Plus de détails sont donnés dans <a href="https://anthirion.github.io/personal_website/pdf_editor.html">l'article</a>
dédié sur mon site perso.

# Auteur et conditions d'utilisation de l'application

Cette application a été créée par Antoine Thirion. En contrepartie de sa gratuité
totale, l'auteur ne garantit pas d'évolutions futures. Il s'efforcera de corriger les bugs et d'ajouter des
fonctionnalités jugées pertinentes, sans contrainte ni de résultats ni de délais.

# Installation

Pour installer l'application, télécharger la dernière version présente dans
les <a href="https://github.com/anthirion/pdf_editor/tags">tags</a>.
Ensuite, installer les dépendances du projet en tapant dans un terminal :

```python
pip install -r requirements.txt
```

Lancer le programme en lancant le main :
```python
python main.py
```

<!-- 
# Problèmes rencontrés et résolutions implémentées

<ul>
<li>Utiliser un IntEnum plutôt qu'un Enum lorsqu'on manipule des entiers</li>
<li>Un signal doit être attaché à une instance de classe et pas à une classe</li>
<li>Un signal doit être connecté dans la classe qui le définit (dans le constructeur par exemple). Le slot associé doit donc utilisé la classe parent.</li>
<li>L'affichage d'un message d'erreur, d'avertissement ou d'information) bloque la prise en compte des évènements. Pour résoudre ce problème, mettre en place un timer avec un court délai (100 ms par exemple) au bout duquel le message sera affiché</li>
<li>L'utilisation de protocoles pour définir des sous-classes spécifiques</li>
<li>Différer les imports pour éviter les erreurs d'importations circulaires</li>
<li>Utiliser un QThread pour effectuer des tâches longues ou lourdes. Possibilité d'utiliser des messages</li>
</ul>
-->