from dataclasses import dataclass
from decimal import Decimal
from tabulate import tabulate

@dataclass(frozen=True)
class FicheProduit:
    reference: str
    nom: str
    categorie: str
    prix: Decimal
    quantite: int
    def __post_init__(self):
        p = Decimal(str(self.prix))
        if not p.is_finite() or p < 0 or type(self.quantite) is not int or self.quantite < 0:
            raise ValueError("Prix ou quantité invalide")
        object.__setattr__(self, "prix", p)
    @property
    def valeur(self): return self.prix * self.quantite

class Catalogue:
    def __init__(self): self._produits = {}
    def ajouter(self, produit):
        if produit.reference in self._produits: raise ValueError("Référence dupliquée")
        self._produits[produit.reference] = produit
    def par_categorie(self, categorie):
        return [p for p in self._produits.values() if p.categorie == categorie]
    def valeur_totale(self):
        return sum((p.valeur for p in self._produits.values()), Decimal(0))
    def filtrer_prix(self, maximum):
        return [p for p in self._produits.values() if p.prix <= Decimal(str(maximum))]
    def tableau(self, tri_valeur=False):
        produits = list(self._produits.values())
        if tri_valeur: produits.sort(key=lambda p: p.valeur, reverse=True)
        lignes = [[p.reference, p.nom, p.categorie, f"{p.prix:.2f}", p.quantite, f"{p.valeur:.2f}"] for p in produits]
        return tabulate(lignes, headers=["Réf", "Nom", "Catégorie", "Prix", "Qté", "Valeur"], tablefmt="github")

if __name__ == "__main__":
    c = Catalogue(); c.ajouter(FicheProduit("A", "Stylo", "Papeterie", "2.5", 3))
    c.ajouter(FicheProduit("B", "Cahier", "Papeterie", 4, 2))
    assert c.valeur_totale() == Decimal("15.5")
    print(c.tableau())
