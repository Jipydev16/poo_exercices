"""Ex. 15 — PROJET FINAL : ordonnancement topologique (algorithme de Kahn)."""

# ALGORITHME — Algorithme de Kahn : calcul des degrés entrants, tas des tâches libres, réduction des degrés.
# INVARIANT — Invariant : un identifiant unique par tâche, toutes dépendances connues, aucun cycle.
# COMPLEXITÉ — Temps : O((V+E) log V) au plus ; mémoire : O(V+E).
from dataclasses import dataclass, field
import heapq

@dataclass
class Tache:
    identifiant: str
    description: str
    dependances: set[str] = field(default_factory=set)

    def __post_init__(self):
        if not self.identifiant.strip() or not self.description.strip():
            raise ValueError('Identifiant et description requis')
        # Une copie évite qu'un set fourni par l'appelant soit modifié ensuite.
        self.dependances = set(self.dependances)
        if self.identifiant in self.dependances:
            raise ValueError('Auto-dépendance interdite')

class DependancesCycliques(ValueError):
    pass

class Projet:
    def __init__(self):
        self._taches: dict[str, Tache] = {}
        self._terminees: set[str] = set()

    def ajouter(self, tache: Tache) -> None:
        if not isinstance(tache, Tache) or tache.identifiant in self._taches:
            raise ValueError('Tâche invalide ou identifiant dupliqué')
        # Copier l'objet protège le graphe des modifications extérieures.
        self._taches[tache.identifiant] = Tache(tache.identifiant, tache.description, tache.dependances)

    def ordre_execution(self) -> list[str]:
        # Vérifier les arêtes avant de calculer les degrés entrants.
        ids = set(self._taches)
        for tache in self._taches.values():
            if not tache.dependances <= ids:
                raise ValueError('Une dépendance référence une tâche inconnue')
        degres = {i: 0 for i in ids}
        successeurs = {i: [] for i in ids}
        for tache in self._taches.values():
            degres[tache.identifiant] = len(tache.dependances)
            for parent in tache.dependances:
                successeurs[parent].append(tache.identifiant)
        # Un min-heap permet un ordre déterministe et des extractions O(log V).
        pretes = [i for i, degre in degres.items() if degre == 0]
        heapq.heapify(pretes)
        resultat: list[str] = []
        while pretes:
            actuelle = heapq.heappop(pretes)
            resultat.append(actuelle)
            for suivant in successeurs[actuelle]:
                degres[suivant] -= 1
                if degres[suivant] == 0:
                    heapq.heappush(pretes, suivant)
        if len(resultat) != len(ids):
            # Un cycle empêche au moins un nœud d'atteindre le degré zéro.
            raise DependancesCycliques('Cycle détecté entre les tâches')
        return resultat

    def taches_disponibles(self) -> list[str]:
        # Valider le graphe, même si certaines tâches semblent réalisables.
        self.ordre_execution()
        return sorted(t.identifiant for t in self._taches.values()
                      if t.identifiant not in self._terminees and t.dependances <= self._terminees)

    def terminer(self, identifiant: str) -> None:
        if identifiant not in self._taches:
            raise KeyError(identifiant)
        if identifiant not in self.taches_disponibles():
            raise ValueError('Tâche bloquée ou déjà terminée')
        self._terminees.add(identifiant)

if __name__ == '__main__':
    projet = Projet()
    projet.ajouter(Tache('A', 'Collecter les données'))
    projet.ajouter(Tache('B', 'Nettoyer', {'A'}))
    projet.ajouter(Tache('C', 'Analyser', {'B'}))
    print(projet.ordre_execution())  # ['A', 'B', 'C']
    print(projet.taches_disponibles())  # ['A']
