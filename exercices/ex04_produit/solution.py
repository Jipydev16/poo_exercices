"""Ex. 04 — @classmethod et @staticmethod : construire et calculer."""

# ALGORITHME — Découper code;nom;prix, vérifier les champs, instancier via cls ; calculer TTC à part.
# INVARIANT — Invariant : code/nom non vides, prix non négatif.
# COMPLEXITÉ — Découpage de ligne : O(L), L étant la longueur du texte.
from decimal import Decimal, InvalidOperation

class Produit:
    def __init__(self, code: str, nom: str, prix_ht):
        if not code.strip() or not nom.strip():
            raise ValueError("Code et nom requis")
        self.code = code.strip()
        self.nom = nom.strip()
        try:
            self.prix_ht = Decimal(str(prix_ht))
        except InvalidOperation as exc:
            raise ValueError("Prix invalide") from exc
        if not self.prix_ht.is_finite() or self.prix_ht < 0:
            raise ValueError("Prix invalide")

    @classmethod
    def depuis_ligne(cls, ligne: str) -> 'Produit':
        # La fabrique convertit du texte en objet et réutilise __init__.
        parties = ligne.split(";")
        if len(parties) != 3:
            raise ValueError("Format attendu : code;nom;prix")
        return cls(parties[0], parties[1], parties[2])

    @staticmethod
    def prix_ttc(prix_ht, taux=0.16) -> Decimal:
        # Une méthode statique ne lit ni self ni cls.
        prix, taxe = Decimal(str(prix_ht)), Decimal(str(taux))
        if not prix.is_finite() or not taxe.is_finite() or prix < 0 or taxe < 0:
            raise ValueError("Prix ou taxe invalide")
        return (prix * (Decimal('1') + taxe)).quantize(Decimal('0.01'))

    def __repr__(self) -> str:
        return f"Produit(code={self.code!r}, nom={self.nom!r}, prix_ht={str(self.prix_ht)!r})"

if __name__ == "__main__":
    p = Produit.depuis_ligne("P01;Clavier;25")
    print(p, Produit.prix_ttc(p.prix_ht))  # 29.00
