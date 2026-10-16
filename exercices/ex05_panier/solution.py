"""Ex. 05 — Un Panier contient des Articles : c'est une composition."""

# ALGORITHME — Utiliser un dict pour retrouver une référence et agréger ou retirer une quantité.
# INVARIANT — Invariant : une seule entrée par référence ; quantités strictement positives.
# COMPLEXITÉ — Ajout/retrait : O(1) moyen ; total : O(n log n) à cause du tri des lignes.
from decimal import Decimal

class Article:
    def __init__(self, reference: str, nom: str, prix):
        if not reference.strip() or not nom.strip():
            raise ValueError("Article incomplet")
        montant = Decimal(str(prix))
        if not montant.is_finite() or montant < 0:
            raise ValueError("Prix invalide")
        self.reference, self.nom, self.prix = reference.strip(), nom.strip(), montant

class Panier:
    def __init__(self):
        # ref -> [Article, quantité] ; le dictionnaire assure l'unicité des refs.
        self._articles: dict[str, list] = {}

    def ajouter(self, article: Article, quantite: int = 1) -> None:
        if not isinstance(article, Article) or type(quantite) is not int or quantite <= 0:
            raise ValueError("Article / quantité invalide")
        ref = article.reference
        if ref in self._articles:
            ancien, total = self._articles[ref]
            if ancien.prix != article.prix or ancien.nom != article.nom:
                raise ValueError("Même référence, caractéristiques différentes")
            self._articles[ref][1] = total + quantite
        else:
            self._articles[ref] = [article, quantite]

    def retirer(self, reference: str, quantite: int = 1) -> None:
        if type(quantite) is not int or quantite <= 0:
            raise ValueError("Quantité invalide")
        if reference not in self._articles or self._articles[reference][1] < quantite:
            raise ValueError("Stock du panier insuffisant")
        self._articles[reference][1] -= quantite
        if self._articles[reference][1] == 0:
            del self._articles[reference]

    def lignes(self) -> list[tuple[str, int, Decimal]]:
        # On renvoie de nouvelles données : pas d'accès à l'état mutable interne.
        return [(ref, qte, art.prix * qte) for ref, (art, qte) in sorted(self._articles.items())]

    def total(self) -> Decimal:
        return sum((sous_total for _, _, sous_total in self.lignes()), Decimal('0'))

if __name__ == "__main__":
    panier = Panier()
    panier.ajouter(Article("A", "Stylo", 2.5), 3)
    panier.ajouter(Article("B", "Cahier", 4), 2)
    print(panier.total())  # 15.5
