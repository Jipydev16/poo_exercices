from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Article:
    reference: str
    nom: str
    prix: Decimal
    def __post_init__(self):
        p = Decimal(str(self.prix))
        if not p.is_finite() or p < 0: raise ValueError("Prix invalide")
        object.__setattr__(self, "prix", p)

class Panier:
    def __init__(self):
        self._articles = {}
        self._coupon = Decimal("0")

    @staticmethod
    def _qte(q):
        if type(q) is not int or q <= 0: raise ValueError("Quantité positive entière requise")

    def ajouter(self, article, qte):
        self._qte(qte)
        if article.reference in self._articles:
            ancien, q = self._articles[article.reference]
            if ancien != article: raise ValueError("Référence déjà associée à un autre article")
            self._articles[article.reference] = (ancien, q + qte)
        else: self._articles[article.reference] = (article, qte)

    def retirer(self, reference, qte):
        self._qte(qte)
        if reference not in self._articles: raise ValueError("Référence inconnue")
        article, ancienne = self._articles[reference]
        if qte > ancienne: raise ValueError("Quantité insuffisante")
        if qte == ancienne: del self._articles[reference]
        else: self._articles[reference] = (article, ancienne - qte)

    def appliquer_coupon(self, pourcentage):
        d = Decimal(str(pourcentage))
        if not d.is_finite() or not 0 <= d <= 1: raise ValueError("Coupon entre 0 et 1")
        self._coupon = d

    def lignes(self):
        return [(a.reference, a.nom, q, a.prix * q) for a, q in self._articles.values()]

    def total(self):
        return sum((a.prix * q for a, q in self._articles.values()), Decimal(0)) * (1 - self._coupon)

if __name__ == "__main__":
    p = Panier(); p.ajouter(Article("S", "Stylo", "2.50"), 3)
    p.ajouter(Article("C", "Cahier", 4), 2)
    assert p.total() == Decimal("15.50")
