from decimal import Decimal, ROUND_HALF_UP

class Produit:
    def __init__(self, code, nom, prix_ht, devise="USD"):
        self.code, self.nom, self.devise = code, nom, devise
        self.prix_ht = Decimal(str(prix_ht))
        if not self.prix_ht.is_finite() or self.prix_ht < 0: raise ValueError("Prix invalide")

    @classmethod
    def depuis_ligne(cls, ligne):
        champs = ligne.split(";")
        if len(champs) != 3: raise ValueError("Trois champs attendus")
        return cls(champs[0], champs[1], champs[2])

    @staticmethod
    def prix_ttc(prix, taxe=0.16):
        p, t = Decimal(str(prix)), Decimal(str(taxe))
        if not p.is_finite() or not t.is_finite() or p < 0 or t < 0: raise ValueError("Prix/taxe invalide")
        return (p * (1 + t)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def __repr__(self):
        return f"Produit({self.code!r}, {self.nom!r}, {self.prix_ht:.2f} {self.devise})"

if __name__ == "__main__":
    p = Produit.depuis_ligne("P01;Clavier;25")
    assert p.prix_ttc(p.prix_ht) == Decimal("29.00")
