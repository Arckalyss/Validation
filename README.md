# Description du projet

Ce projet implémente un cadre générique d’exploration et de vérification de modèles pour des systèmes dynamiques discrets, fondé sur :

une sémantique abstraite des systèmes (LanguageSemantics),

la composition synchrone de plusieurs systèmes indépendants (Soup semantics),

la conversion automatique en graphe enraciné,

et l’exploration exhaustive de l’espace d’états par recherche en largeur (BFS).

Le cadre permet à la fois :

de résoudre des problèmes (ex. Tours de Hanoï),

et de vérifier des propriétés de sûreté et de vivacité (ex. exclusion mutuelle, deadlocks) par exploration explicite de l’espace d’états, avec génération de contre-exemples minimaux.


Cette séparation permet de réutiliser les mêmes algorithmes d’exploration pour des modèles très différents.

## Organisation des fichiers : 
### languagesemantics.py

Définit l’interface abstraite LanguageSemantics d’un système dynamique discret :

états initiaux,

actions activables,

fonction de transition,

prédicat de solution (ou d’état “mauvais” dans un contexte de vérification).

Cette interface découple complètement la définition des systèmes de leur exploration.

### hanoilanguagesemantics.py

Implémente une sémantique concrète du problème des Tours de Hanoï, conforme à LanguageSemantics.
Les états représentent la configuration des tours, les actions sont des déplacements légaux, et la condition de solution correspond à la résolution complète du problème.

### soupsemantics.py

Implémente la sémantique composée (Soup semantics), permettant de coupler plusieurs sémantiques indépendantes.

Un état global est un produit cartésien d’états locaux.

Les actions sont partagées entre les sous-systèmes.

Les transitions résultent de l’application simultanée d’une action à chaque composant.

Un état global est solution si tous les sous-systèmes sont en état solution.

Cette sémantique permet d’étudier des systèmes synchrones composés.

### rootedgraph.py

Définit l’interface minimale d’un graphe enraciné :

sommets initiaux (roots),

successeurs (neighbors).

Cette abstraction permet de rendre les algorithmes de parcours indépendants du modèle étudié.

### ls2rg.py

Adaptateur générique transformant une LanguageSemantics en RootedGraph.
Il automatise la construction du graphe d’états à partir des fonctions actions et execute.

### BFS_definition.py

Implémente un algorithme de recherche en largeur (BFS) générique.
Un callback permet :

d’accumuler des informations pendant le parcours,

d’arrêter l’exploration dès qu’une propriété est violée ou satisfaite.

### soup_validation.py

Script de démonstration pour les Tours de Hanoï :

instancie plusieurs sémantiques de Hanoï,

les compose via SoupSemantics,

explore l’espace d’états par BFS,

et détecte les configurations solutions.

### alicebob_languagesemantics.py

Implémente les protocoles Alice & Bob (AB1, AB2, AB3) sous forme de LanguageSemantics.
Ces modèles sont utilisés pour la vérification de propriétés concurrentes :

exclusion mutuelle,

deadlocks.

### alicebob_validation.py

Script de vérification de modèles basé sur BFS :

explore exhaustivement l’espace d’états atteignables,

vérifie l’exclusion mutuelle (propriété de sûreté),

détecte les deadlocks (propriété de vivacité négative),

reconstruit automatiquement des traces minimales menant à un contre-exemple ou à un état bloqué.

## Exécution
Validation de la composition (Tours de Hanoï)
python -m soup.soup_validation

Vérification de modèles (Alice & Bob)
python -m soup.alicebob_validation



