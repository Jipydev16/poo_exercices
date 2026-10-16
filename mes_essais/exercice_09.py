from dataclasses import dataclass, asdict
from pathlib import Path
import json

@dataclass(frozen=True)
class Livre:
    isbn: str
    titre: str
    auteur: str

class Bibliotheque:
    def __init__(self): self._livres = {}
    def ajouter(self, livre):
        if livre.isbn in self._livres: raise ValueError("ISBN dupliqué")
        self._livres[livre.isbn] = livre
    def rechercher(self, isbn): return self._livres.get(isbn)
    def supprimer(self, isbn):
        if isbn not in self._livres: raise KeyError(isbn)
        del self._livres[isbn]
    def rechercher_titre(self, mot):
        return [l for l in self._livres.values() if mot.casefold() in l.titre.casefold()]
    def sauvegarder(self, chemin):
        Path(chemin).write_text(json.dumps([asdict(l) for l in self._livres.values()], ensure_ascii=False, indent=2), encoding="utf-8")
    @classmethod
    def charger(cls, chemin):
        donnees = json.loads(Path(chemin).read_text(encoding="utf-8"))
        if not isinstance(donnees, list): raise ValueError("Liste JSON attendue")
        b = cls()
        for entree in donnees: b.ajouter(Livre(**entree))
        return b

if __name__ == "__main__":
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as d:
        chemin = Path(d) / "livres.json"
        b = Bibliotheque(); b.ajouter(Livre("1", "Python", "A")); b.ajouter(Livre("2", "POO", "B"))
        b.sauvegarder(chemin)
        assert Bibliotheque.charger(chemin).rechercher("2").titre == "POO"
