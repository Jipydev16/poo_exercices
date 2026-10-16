from dataclasses import dataclass, field
from collections import deque

class DependancesCycliques(Exception): pass

@dataclass
class Tache:
    id: str
    description: str
    dependances: set[str] = field(default_factory=set)
    duree: float = 1
    def __post_init__(self):
        self.dependances = set(self.dependances)
        if not self.id or not isinstance(self.duree, (int, float)) or not 0 <= self.duree < float("inf"):
            raise ValueError("Tâche invalide")

class Projet:
    def __init__(self): self._taches = {}; self._terminees = set()
    def ajouter(self, tache):
        if tache.id in self._taches: raise ValueError("Identifiant dupliqué")
        self._taches[tache.id] = tache

    def ordre_execution(self):
        indegres = {id: 0 for id in self._taches}
        suivants = {id: [] for id in self._taches}
        for id, t in self._taches.items():
            for dep in t.dependances:
                if dep not in self._taches: raise ValueError(f"Dépendance inconnue : {dep}")
                indegres[id] += 1; suivants[dep].append(id)
        file = deque(id for id in self._taches if indegres[id] == 0)
        ordre = []
        while file:
            id = file.popleft(); ordre.append(id)
            for suivant in suivants[id]:
                indegres[suivant] -= 1
                if indegres[suivant] == 0: file.append(suivant)
        if len(ordre) != len(self._taches): raise DependancesCycliques("Cycle détecté")
        return ordre

    def taches_disponibles(self):
        ordre = self.ordre_execution()
        return [id for id in ordre if id not in self._terminees and self._taches[id].dependances <= self._terminees]

    def terminer(self, id):
        if id not in self._taches: raise KeyError(id)
        if id not in self.taches_disponibles(): raise ValueError("Tâche non disponible")
        self._terminees.add(id)

    def chemin_critique(self):
        ordre = self.ordre_execution()
        fins, chemins = {}, {}
        for id in ordre:
            t = self._taches[id]
            pred = max(t.dependances, key=lambda x: fins[x]) if t.dependances else None
            fins[id] = t.duree + (fins[pred] if pred else 0)
            chemins[id] = (chemins[pred] if pred else []) + [id]
        if not ordre: return (0, [])
        dernier = max(ordre, key=lambda x: fins[x])
        return fins[dernier], chemins[dernier]

if __name__ == "__main__":
    p = Projet()
    p.ajouter(Tache("A", "Début")); p.ajouter(Tache("B", "Suite", {"A"})); p.ajouter(Tache("C", "Fin", {"B"}))
    assert p.ordre_execution() == ["A", "B", "C"] and p.taches_disponibles() == ["A"]
