"""Ex. 10 — PAQUET EXTERNE #1 : tabulate pour la présentation uniquement."""

# ALGORITHME — Calculer les données dans Catalogue et déléguer uniquement le rendu à tabulate.
# INVARIANT — Invariant : référence unique ; stocks et prix non négatifs.
# COMPLEXITÉ — Filtre : O(n) ; affichage trié : O(n log n).
from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class FicheProduit:
    reference: str
    categorie: str
    prix: Decimal
    stock: int

    def __post_init__(self):
        if not self.reference.strip() or not self.categorie.strip():
            raise ValueError("Référence / catégorie vide")
        prix = Decimal(str(self.prix))
        if not prix.is_finite() or prix < 0 or type(self.stock) is not int or self.stock < 0:
            raise ValueError("Prix / stock invalide")
        object.__setattr__(self, 'prix', prix)

class Catalogue:
    def __init__(self):
        self._produits: dict[str, FicheProduit] = {}

    def ajouter(self, produit: FicheProduit) -> None:
        if produit.reference in self._produits:
            raise ValueError("Référence déjà utilisée")
        self._produits[produit.reference] = produit

    def par_categorie(self, categorie: str) -> list[FicheProduit]:
        return sorted((p for p in self._produits.values() if p.categorie == categorie), key=lambda p: p.reference)

    def valeur_totale(self) -> Decimal:
        return sum((p.prix * p.stock for p in self._produits.values()), Decimal('0'))

    def tableau(self) -> str:
        try:
            from tabulate import tabulate  # Dépendance installée via pip.
        except ImportError as exc:
            raise RuntimeError("Installez 'tabulate' : python -m pip install -r requirements.txt") from exc
        lignes = [(p.reference, p.categorie, str(p.prix), p.stock) for p in sorted(self._produits.values(), key=lambda p: p.reference)]
        # La bibliothèque ne décide PAS du calcul métier : elle ne fait qu'afficher.
        return tabulate(lignes, headers=['Réf.', 'Catégorie', 'Prix', 'Stock'], tablefmt='github')

if __name__ == '__main__':
    c = Catalogue()
    c.ajouter(FicheProduit('A', 'Papeterie', '2.5', 4))
    print(c.tableau())
