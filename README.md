## Project overview

This project implements the models AB1, AB2, and AB3 as rooted graphs and
uses a generic BFS exploration to answer questions 4 and 5 of the assignment.

- **Question 4**: verification of mutual exclusion and deadlock properties
  by exhaustive state-space exploration.
- **Question 5**: construction of explicit counterexample traces
  (violation of mutual exclusion or deadlock).

The entry point is `main.py`.

## Description du projet

Ce projet implémente un cadre générique de composition de systèmes dynamiques discrets et de parcours d’états à l’aide d’un algorithme de recherche en largeur (BFS).

L’objectif principal est de pouvoir combiner plusieurs sémantiques de systèmes indépendants (par exemple plusieurs tours de Hanoï) dans une sémantique globale, puis d’explorer automatiquement l’espace d’états résultant afin de détecter des configurations solutions.

Organisation des fichiers

languagesemantics.py
Définit l’interface générique LanguageSemantics d’un système dynamique : états initiaux, actions possibles, transition d’état et condition de solution.

hanoilanguagesemantics.py
Implémente une sémantique concrète du problème des tours de Hanoï conforme à l’interface LanguageSemantics.

soupsemantics.py
Implémente la sémantique composée (ou “soupe”) permettant de coupler plusieurs systèmes.
Les états sont des configurations produit, les actions sont partagées, et les transitions résultent de l’application simultanée d’une action à chaque sous-système.

rootedgraph.py
Définit l’interface d’un graphe enraciné (racines + voisins), utilisée comme abstraction pour les algorithmes de parcours.

ls2rg.py
Adaptateur transformant une LanguageSemantics en graphe enraciné exploitable par un algorithme de recherche.

BFS_definition.py
Implémente un algorithme de parcours en largeur (BFS) générique, avec callback permettant la détection et l’arrêt sur une configuration solution.

soup_validation.py
Script principal de test : il instancie plusieurs sémantiques de Hanoï, les compose via SoupSemantics, puis explore l’espace d’états par BFS afin de valider le modèle et détecter les solutions.


