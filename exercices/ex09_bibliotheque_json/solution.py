"""Ex. 09 — FICHIERS #1 : sauvegarder et charger une bibliothèque JSON."""

# ALGORITHME — Convertir chaque Livre en dict, sérialiser UTF-8, puis recréer des Livre au chargement.
# INVARIANT — Invariant : les ISBN restent uniques dans le catalogue.
# COMPLEXITÉ — Recherche : O(1) moyen ; sauvegarde : O(n log n) pour trier les ISBN.
import json
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class Livre:
    isbn: str
    titre: str
    auteur: str

    def __post_init__(self):
        if not all((self.isbn.strip(), self.titre.strip(), self.auteur.strip())):
            raise ValueError("Tous les champs du livre sont obligatoires")

class Bibliotheque:
    def __init__(self):
        self._livres: dict[str, Livre] = {}

    def ajouter(self, livre: Livre) -> None:
        if not isinstance(livre, Livre):
            raise TypeError("Un objet Livre est attendu")
        if livre.isbn in self._livres:
            raise ValueError("ISBN déjà présent")
        self._livres[livre.isbn] = livre

    def rechercher(self, isbn: str) -> Livre | None:
        return self._livres.get(isbn)

    def lister(self) -> list[Livre]:
        return [self._livres[isbn] for isbn in sorted(self._livres)]

    def sauvegarder(self, chemin: str | Path) -> None:
        # asdict convertit les objets métiers en dictionnaires sérialisables.
        contenu = [asdict(livre) for livre in self.lister()]
        # utf-8 + ensure_ascii=False préservent les accents en clair.
        Path(chemin).write_text(json.dumps(contenu, ensure_ascii=False, indent=2), encoding='utf-8')

    @classmethod
    def charger(cls, chemin: str | Path) -> 'Bibliotheque':
        # L'erreur FileNotFoundError n'est pas masquée : elle est informative.
        donnees = json.loads(Path(chemin).read_text(encoding='utf-8'))
        if not isinstance(donnees, list):
            raise ValueError("Fichier JSON : une liste de livres est attendue")
        bibliotheque = cls()
        for item in donnees:
            if not isinstance(item, dict):
                raise ValueError("Chaque livre doit être un objet JSON")
            bibliotheque.ajouter(Livre(**item))
        return bibliotheque

if __name__ == '__main__':
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as d:
        p = Path(d) / 'livres.json'
        b = Bibliotheque()
        b.ajouter(Livre('978-001', 'Python pas à pas', 'M. A.'))
        b.sauvegarder(p)
        print(Bibliotheque.charger(p).rechercher('978-001'))
