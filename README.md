# Atelier Python — 15 défis de Programmation Orientée Objet

**Public :** débutants ayant déjà vu variables, fonctions, listes et dictionnaires.  
**Objectif :** savoir concevoir des classes fiables et résoudre de vrais problèmes algorithmiques grâce à la POO.  
**Format :** 5 exercices basiques + 5 intermédiaires + 5 avancés ; énoncés, fichiers à compléter, solutions COMMENTÉES, tests et données d'exemple.

## Démarrage rapide

1. Extraire le ZIP, ouvrir le dossier `poo_python_15_exercices` dans VS Code.
2. Depuis le répertoire racine, vérifier : `python --version` (**Python 3.10+**).
3. Créer un environnement virtuel (recommandé) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Sur Linux/macOS : `source .venv/bin/activate` (puis les mêmes commandes pip).  
**Si l'activation PowerShell est bloquée**, utiliser directement `.venv\Scripts\python.exe -m pip install -r requirements.txt`.

4. Lire `EXERCICES.md`. Écrire votre code dans `mes_essais/exercice_01.py`, puis comparer au corrigé `exercices/ex01_etudiant/solution.py`.
5. Tester les solutions livrées : `python -m unittest discover -s tests -v`.
6. Lancer une solution : `python -m exercices.ex01_etudiant.solution`.

> Les tests inclus évaluent les **corrigés fournis**, pas vos fichiers `mes_essais`. Pour tester vos tentatives, importez votre module dans vos propres tests ou adaptez les imports des tests existants.

## Organisation

```text
poo_python_15_exercices/
├── README.md                 ← installation + méthode
├── EXERCICES.md              ← 15 énoncés complets (sans solution)
├── INDICES.md                ← indices progressifs (sans code résolu)
├── requirements.txt         ← tabulate et pydantic (seulement 10 et 14)
├── exercices/
│   ├── ex01_etudiant/
│   │   └── solution.py       ← corrigé commenté
│   └── ... jusqu'à ex15_ordonnanceur/
├── mes_essais/
│   ├── exercice_01.py        ← TODO à compléter
│   └── ... exercice_15.py
├── data/
│   ├── bibliotheque_exemple.json
│   └── clients_exemple.json
└── tests/
    └── test_exercices.py
```

## Dépendances et accès au disque

- **Exercice 10** : `tabulate` (mise en forme tabulaire terminal).
- **Exercice 14** : `pydantic` version 2 (validation de données externes).
- **Exercice 09** : lecture / écriture d'une bibliothèque dans un fichier JSON.
- **Exercice 12** : persistance d'un repository JSON avec remplacement atomique du fichier.
- Les autres exercices ne nécessitent **que la bibliothèque standard de Python**.
- Aucun exercice n'exige d'accès réseau ni de clés API, même après installation des dépendances.
- Les tests de fichiers utilisent des dossiers temporaires : ils n'altèrent pas vos données d'exemple.

## Méthode d'étude pour chaque problème

**1. Comprendre :** formuler entrées, sorties, règles métier et cas limites.  
**2. Dessiner :** choisir les objets, leurs responsabilités et leurs relations.  
**3. Décomposer :** écrire un pseudo-code de chaque méthode avant Python.  
**4. Implémenter :** commencer par le scénario nominal puis refuser les cas invalides.  
**5. Tester :** au moins un cas normal, un cas vide, un cas invalide, un cas de frontière.  
**6. Expliquer :** justifier la structure de données et la complexité, puis consulter la solution.

**Barème indicatif (sur 20)** : conception des classes (5), raisonnement algorithmique (6), validations (4), tests (3), clarté (2).

> Ce projet est pédagogique : les montants financiers, comptes et paiements ne sont PAS adaptés à un service bancaire ou transactionnel réel sans contrôles supplémentaires, concurrence et transactions persistantes.
