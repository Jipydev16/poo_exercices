# Cahier des 15 exercices — Programmation Orientée Objet en Python

## Mode d'emploi

Résolvez **dans l'ordre**, sans ouvrir `solution.py` avant d'avoir essayé. Les énoncés définissent le comportement attendu, mais vous devez trouver vous-même les algorithmes. Chaque exercice comporte une question de raisonnement et un défi supplémentaire facultatif. **Un fichier à compléter et un corrigé commenté** sont fournis pour chaque sujet.

### Objectifs par niveau

| Niveau | Exercices | Compétences |
|---|---|---|
| **Basique** | 01–05 | Instanciation, attributs, méthodes, propriétés, encapsulation, composition, `@classmethod`, `@staticmethod` |
| **Intermédiaire** | 06–10 | Héritage, polymorphisme, ABC, exceptions personnalisées, collection d'objets, fichiers JSON, package `tabulate` |
| **Avancé** | 11–15 | Dataclasses, états, Repository, persistance atomique, Strategy, validation `pydantic`, graphes et ordonnancement |

### Règles générales

- Ne pas utiliser d'`input()` dans les méthodes métier : elles doivent être facilement testables.
- Éviter les variables globales et les attributs de classe qui stockent des listes communes à toutes les instances.
- Valider les entrées avant de modifier l'état d'un objet.
- Utiliser `ValueError` ou les exceptions métier prévues au lieu de renvoyer silencieusement un faux résultat.
- Pour les montants, privilégier `decimal.Decimal` afin de contrôler les arrondis.
- Programmer avec **Python 3.10+** ; installer les dépendances dans `requirements.txt` pour les exercices 10 et 14.

---

## Exercice 01 — Carnet de notes d’un étudiant

**Niveau :** Basique · **Notions :** Classe, instance, liste, méthodes et invariants

### Situation et mission
Concevoir une classe `Etudiant` qui mémorise des notes, calcule une moyenne et décide si un étudiant est admis.

### Interface attendue
`Etudiant(nom, prenom)`, `ajouter_note(note)`, `moyenne()`, `est_admis(seuil=10)`

### Démonstration / sortie attendue
Notes 12, 14 et 10 → moyenne `12.0`, `est_admis()` → `True`.

### Cas limites et contraintes
Aucune note : `moyenne()` renvoie `None`. Note -1 ou 21 : exception `ValueError`.

### Question algorithmique à rédiger
Pourquoi une liste d’instances est-elle préférable à une variable globale pour les notes ?

### Défi supplémentaire (facultatif)
Ajouter une méthode `meilleure_note()` sans modifier les autres méthodes.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_01.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex01_etudiant/solution.py`

---

## Exercice 02 — Rectangle intelligent et propriétés

**Niveau :** Basique · **Notions :** Encapsulation, @property, validations

### Situation et mission
Empêcher un rectangle d’acquérir des dimensions négatives et calculer ses mesures.

### Interface attendue
`Rectangle(largeur, hauteur)`, propriétés `.largeur`, `.hauteur`, `.surface`, `.perimetre`, `redimensionner(l,h)`

### Démonstration / sortie attendue
`Rectangle(3,4)` → surface `12.0`, périmètre `14.0`.

### Cas limites et contraintes
Largeur 0 ou négative : exception ; redimensionnement invalide : anciennes dimensions conservées.

### Question algorithmique à rédiger
Pourquoi faut-il valider toutes les nouvelles dimensions avant de modifier les attributs ?

### Défi supplémentaire (facultatif)
Créer une propriété `est_carre` calculée sans la stocker.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_02.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex02_rectangle/solution.py`

---

## Exercice 03 — Compte bancaire sécurisé

**Niveau :** Basique · **Notions :** Méthodes métier, état, encapsulation, préconditions

### Situation et mission
Modéliser le dépôt, le retrait et le transfert d’argent sans solde négatif.

### Interface attendue
`CompteBancaire(titulaire, solde_initial=0)`, `.solde`, `deposer(somme)`, `retirer(somme)`, `transferer(destinataire,somme)`

### Démonstration / sortie attendue
De 100, transfert de 35 → soldes émetteur `65`, destinataire `35`.

### Cas limites et contraintes
Retrait supérieur au solde : aucune mutation. Transfert à soi-même ou somme nulle : refus.

### Question algorithmique à rédiger
Comment garantir que l’argent n’est ni perdu ni créé pendant un transfert ?

### Défi supplémentaire (facultatif)
Créer un historique de transactions avec date et motif.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_03.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex03_compte/solution.py`

---

## Exercice 04 — Usine de produits et taxes

**Niveau :** Basique · **Notions :** Méthodes d’instance, de classe, statiques, représentation

### Situation et mission
Construire des produits à partir de texte et calculer le prix TTC.

### Interface attendue
`Produit(code,nom,prix_ht)`, `Produit.depuis_ligne("P01;Clavier;25.0")`, `Produit.prix_ttc(prix,taxe=0.16)`, `__repr__`

### Démonstration / sortie attendue
`Produit.depuis_ligne("P01;Clavier;25")` et taxe 16 % → `29.00`.

### Cas limites et contraintes
Ligne avec deux champs : exception. Prix négatif : refus.

### Question algorithmique à rédiger
Distinguer un constructeur, une fabrique de classe et une fonction utilitaire statique.

### Défi supplémentaire (facultatif)
Permettre une devise paramétrable lors de l’affichage du produit.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_04.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex04_produit/solution.py`

---

## Exercice 05 — Panier et composition d’objets

**Niveau :** Basique · **Notions :** Composition, dictionnaire, agrégation, cohérence des quantités

### Situation et mission
Regrouper plusieurs produits et calculer un ticket sans doublons de référence.

### Interface attendue
`Article(reference, nom, prix)`, `Panier.ajouter(article,qte)`, `retirer(reference,qte)`, `total()`, `lignes()`

### Démonstration / sortie attendue
3 stylos à 2,50 et 2 cahiers à 4 → total `15.5`.

### Cas limites et contraintes
Ajouter deux fois la même référence cumule les quantités. Retirer trop d’articles : exception.

### Question algorithmique à rédiger
Pourquoi un dictionnaire indexé par référence évite-t-il un parcours systématique de la liste ?

### Défi supplémentaire (facultatif)
Ajouter des coupons applicables au total du panier.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_05.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex05_panier/solution.py`

---

## Exercice 06 — Calculateur de rémunération polymorphe

**Niveau :** Intermédiaire · **Notions :** Héritage, override, polymorphisme, agrégation

### Situation et mission
Calculer une masse salariale en faisant varier la formule selon le type d’employé.

### Interface attendue
`Employe(nom)`, `Salarie(nom,mensuel)`, `Freelance(nom,heures,taux)`, `masse_salariale(personnel)`

### Démonstration / sortie attendue
Un salarié à 1000 et un freelance à 20 h × 15 → masse salariale `1300`.

### Cas limites et contraintes
Heures négatives, taux négatif : exception. Équipe vide : total 0.

### Question algorithmique à rédiger
En quoi le polymorphisme facilite-t-il l’ajout d’un troisième type d’employé ?

### Défi supplémentaire (facultatif)
Ajouter un `Stagiaire` rémunéré par indemnité fixe sans modifier `masse_salariale`.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_06.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex06_personnel/solution.py`

---

## Exercice 07 — Système de paiement extensible

**Niveau :** Intermédiaire · **Notions :** Classe abstraite ABC, injection de dépendances, polymorphisme

### Situation et mission
Appliquer plusieurs modes de paiement à travers un même contrat abstrait.

### Interface attendue
`MoyenPaiement(ABC).payer(montant)`, `Especes`, `Carte`, `MobileMoney`, `Caisse.encaisser(moyen,montant)`

### Démonstration / sortie attendue
`Caisse().encaisser(Carte("1234"),20)` → `"CB-1234-20.00"`.

### Cas limites et contraintes
Une classe abstraite ne peut pas être instanciée ; un paiement négatif doit être rejeté.

### Question algorithmique à rédiger
Pourquoi `Caisse` dépend-elle d’une abstraction et non d’une sous-classe ?

### Défi supplémentaire (facultatif)
Ajouter `Virement` en respectant le contrat sans toucher au code de la caisse.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_07.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex07_paiements/solution.py`

---

## Exercice 08 — Gestion de stock et exceptions personnalisées

**Niveau :** Intermédiaire · **Notions :** Exception métier, dictionnaire, transactions, invariants

### Situation et mission
Gérer des stocks par référence avec erreurs explicites et opérations fiables.

### Interface attendue
`Stock.ajouter(ref,quantite)`, `sortir(ref,quantite)`, `transferer(autre,ref,quantite)`, `quantite(ref)`

### Démonstration / sortie attendue
10 unités au dépôt ; transfert de 4 → dépôt `6`, boutique `4`.

### Cas limites et contraintes
Sortie sur référence inconnue : `ReferenceInconnue`. Quantité excessive : `StockInsuffisant` sans mutation.

### Question algorithmique à rédiger
À quel moment une exception doit-elle être levée pour éviter un transfert partiellement exécuté ?

### Défi supplémentaire (facultatif)
Ajouter une journalisation des mouvements de stock et un seuil d’alerte.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_08.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex08_stock/solution.py`

---

## Exercice 09 — Bibliothèque persistante au format JSON

**Niveau :** Intermédiaire · **Notions :** Composition, sérialisation, pathlib, json, gestion des erreurs

### Situation et mission
Concevoir un catalogue de livres sauvegardé sur disque et rechargé sans perte.

### Interface attendue
`Livre(isbn,titre,auteur)`, `Bibliotheque.ajouter(livre)`, `rechercher(isbn)`, `sauvegarder(chemin)`, `charger(chemin)`

### Démonstration / sortie attendue
Sauvegarder deux livres puis recharger : retrouver les mêmes ISBN, titres et auteurs.

### Cas limites et contraintes
ISBN dupliqué : refus ; fichier absent : `FileNotFoundError` ; JSON invalide : erreur.

### Question algorithmique à rédiger
Pourquoi les objets `Livre` doivent-ils être convertis en dictionnaires avant `json.dumps` ?

### Défi supplémentaire (facultatif)
Ajouter la suppression d’un livre et une recherche par mot contenu dans le titre.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_09.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex09_bibliotheque_json/solution.py`

---

## Exercice 10 — Catalogue formaté avec tabulate

**Niveau :** Intermédiaire · **Notions :** Installation de paquet externe, reporting, séparation métier / présentation

### Situation et mission
Installer `tabulate`, créer un catalogue orienté objet et produire un tableau terminal.

### Interface attendue
`pip install -r requirements.txt`, `FicheProduit`, `Catalogue.ajouter`, `par_categorie`, `valeur_totale`, `tableau()`

### Démonstration / sortie attendue
Deux produits : tableau Markdown lisible + valeur du stock = somme `prix × quantité`.

### Cas limites et contraintes
Catalogue vide : total 0, tableau avec entêtes ; références dupliquées : refus.

### Question algorithmique à rédiger
Pourquoi faut-il séparer la logique de calcul de la bibliothèque d’affichage ?

### Défi supplémentaire (facultatif)
Ajouter un tri par valeur décroissante du stock et un filtre de prix.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_10.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex10_catalogue_tabulate/solution.py`

---

## Exercice 11 — Commande et machine à états

**Niveau :** Avancé · **Notions :** Dataclass immuable, Enum, machine à états, invariants

### Situation et mission
Faire évoluer une commande entre des états autorisés et calculer son montant.

### Interface attendue
`LigneCommande(ref,qte,prix)`, `Commande(identifiant)`, `ajouter(ligne)`, `confirmer()`, `expedier()`, `annuler()`, `total`

### Démonstration / sortie attendue
Commande `C01`, 3 × 5,50 → `16.5`, statut `confirmee` après confirmation.

### Cas limites et contraintes
Impossible de confirmer sans lignes, de modifier une commande confirmée ou d’annuler une commande expédiée.

### Question algorithmique à rédiger
Comment représenter un diagramme des transitions permises plutôt qu’un ensemble de booléens ?

### Défi supplémentaire (facultatif)
Ajouter un journal des événements de changement de statut.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_11.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex11_commande/solution.py`

---

## Exercice 12 — Repository de clients et persistance JSON

**Niveau :** Avancé · **Notions :** Repository pattern, ABC, séparation des couches, fichiers, sauvegarde atomique

### Situation et mission
Créer une couche de stockage indépendante des règles métier et assurer une écriture JSON fiable.

### Interface attendue
`Client(id,nom,email)`, `Repository(ABC)`, `RepositoryClientsJSON(chemin).ajouter`, `.obtenir`, `.lister`, `.supprimer`

### Démonstration / sortie attendue
Créer `C1`, recharger un nouvel objet Repository depuis le même fichier → client `C1` retrouvé.

### Cas limites et contraintes
Identifiant en double : exception ; JSON corrompu : erreur explicite ; suppression inconnue : `False`.

### Question algorithmique à rédiger
Pourquoi écrire dans un temporaire puis utiliser `os.replace` ? Que se passe-t-il si le programme plante ?

### Défi supplémentaire (facultatif)
Créer un `RepositoryClientsMemoire` qui implémente la même interface sans disque.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_12.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex12_repository_json/solution.py`

---

## Exercice 13 — Moteur de promotions (Strategy)

**Niveau :** Avancé · **Notions :** Design pattern Strategy, ABC, injection, composition de règles

### Situation et mission
Changer dynamiquement l’algorithme de remise sans modifier le service de tarification.

### Interface attendue
`Remise(ABC).appliquer(total)`, `Pourcentage`, `MontantFixe`, `Seuil`, `Tarificateur.calculer(total,strategies)`

### Démonstration / sortie attendue
Prix 100, réduction 10 %, puis remise de 5 → `85.00`.

### Cas limites et contraintes
Taux > 1 : refus ; remise fixe > total : prix plafonné à zéro ; stratégies dans l’ordre fourni.

### Question algorithmique à rédiger
Pourquoi une liste de stratégies est-elle plus extensible que quinze conditions `if` ?

### Défi supplémentaire (facultatif)
Ajouter `RemiseFidelite` (ancienneté) et comparer deux ordres de promotions.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_13.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex13_strategies/solution.py`

---

## Exercice 14 — Validation d’objets avec Pydantic

**Niveau :** Avancé · **Notions :** Installation de package, BaseModel, Field, validateurs v2, intégrité métier

### Situation et mission
Valider des commandes provenant d’une API comme des objets fortement contraints.

### Interface attendue
`pip install -r requirements.txt`, `LigneAPI(BaseModel)`, `CommandeAPI(BaseModel)`, validateurs `field_validator` / `model_validator`

### Démonstration / sortie attendue
Client C1, 2 articles P1 à 12,50 → total `25.00`.

### Cas limites et contraintes
Quantité zéro, doublon de référence, liste vide ou identifiant blanc : `ValidationError`.

### Question algorithmique à rédiger
Quelle différence entre la validation des champs et la validation croisée de l’objet complet ?

### Défi supplémentaire (facultatif)
Ajouter la validation d’un code promotionnel facultatif et de sa date d’expiration.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_14.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex14_pydantic/solution.py`

---

## Exercice 15 — Mini-projet : ordonnanceur de tâches (DAG)

**Niveau :** Avancé · **Notions :** Composition, graphes, parcours topologique, dépendances, détection de cycles

### Situation et mission
Construire un ordonnanceur orienté objet qui détecte les dépendances circulaires et produit un ordre d’exécution.

### Interface attendue
`Tache(id,description,dependances=set())`, `Projet.ajouter(tache)`, `ordre_execution()`, `taches_disponibles()`, `terminer(id)`

### Démonstration / sortie attendue
Dépendances A → B → C : ordre `["A", "B", "C"]` et tâches disponibles au départ `["A"]`.

### Cas limites et contraintes
Cycle A ↔ B : `DependancesCycliques`. Dépendance inconnue : exception. Terminer C avant B : refus.

### Question algorithmique à rédiger
Pourquoi un tri topologique est-il impossible lorsqu’il existe un cycle ? Quelle est sa complexité ?

### Défi supplémentaire (facultatif)
Ajouter des durées d’exécution et calculer le chemin critique d’un projet.

### Fichiers de travail
- Votre tentative : `mes_essais/exercice_15.py`
- Solution commentée (à consulter **après** votre essai) : `exercices/ex15_ordonnanceur/solution.py`

---

## Évaluation finale — mini-oral technique

Expliquez, pour trois exercices de votre choix : **(a)** le rôle de chaque classe, **(b)** les invariants, **(c)** l'algorithme principal en pseudo-code, **(d)** un test inattendu, **(e)** ce qui changerait si l'application devait traiter un million d'éléments. Réécrivez au moins un exercice sans regarder votre corrigé.
