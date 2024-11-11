# PDF editor
Cette application de bureau propose un certains nombres d'outils permettant de modifier des fichiers pdf. Les outils proposés ici sont tous gratuits et regroupent notamment :
<ul>
<li>Fusion de PDF</li>
<li>Séparation de PDF</li>
<li>Conversion de PDF vers JPG</li>
<li>Conversion de JPG vers PDF</li>
</ul>

# Motivation
L'objectif de cette application est de proposer une alternative aux éditeurs de PDF en ligne (comme IlovePDF) ou en version de bureau (comme Acrobat Reader). Cette application propose une confidentialité maximale des données étant donné que toutes les opérations se font sur la machine de l'utilisateur. Cette application ne restreint pas l'usage d'outils à un paiement, tous les outils sont gratuits.

# Auteur et conditions d'utilisation de l'application
Cette application a été créée par Antoine Thirion. Si d'autres projets similaires vous intéressent, vous pouvez consulter son site web <a href="https://anthirion.github.io/personal_website/">ici</a>En contrepartie de sa gratuité totale, l'auteur ne garantit pas d'évolutions futures. Il s'efforcera de corriger les bugs et d'ajouter des fonctionnalités jugées pertinentes, sans contrainte ni de résultats ni de délais.

# Choix techniques
Cette application est codée entièrement en python. Elle utilise la librairie <a href="https://pypdf.readthedocs.io/en/stable/index.html">pypdf</a> pour effectuer les différentes opérations sur les fichiers PDF et librairie graphique PySide6 pour l'interface graphique.
Les icones utilisées ont été reprises sur le repo GitHub de <a href="https://github.com/LibreOffice/core/tree/master/icon-themes/colibre/cmd">LibreOffice</a>. Certaines icones ont aussi été récupérées <a href="https://github.com/LibreOffice/core/tree/master/icon-themes/elementary/cmd">icic</a>.

# Installation

# Problèmes rencontrés et résolutions implémentées
<ul>
<li>Utiliser un IntEnum plutôt qu'un Enum lorsqu'on manipule des entiers</li>
<li>Un signal doit être attaché à une instance de classe et pas à une classe</li>
<li>Un signal doit être connecté dans la classe qui le définit (dans le constructeur par exemple). Le slot associé doit donc utilisé la classe parent.</li>
<li>L'affichage d'un message (d'erreur, d'avertissement ou d'information) bloque la prise en compte des évènements. Pour résoudre ce problème, mettre en place un timer avec un court délai (100 ms par exemple) au bout duquel le message sera affiché</li>
</ul>