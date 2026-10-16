from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP

def montant(x):
    d = Decimal(str(x))
    if not d.is_finite() or d < 0: raise ValueError("Montant invalide")
    return d

class Remise(ABC):
    @abstractmethod
    def appliquer(self, total): pass

class Pourcentage(Remise):
    def __init__(self, taux):
        self.taux = montant(taux)
        if self.taux > 1: raise ValueError("Taux supérieur à 1")
    def appliquer(self, total): return montant(total) * (1 - self.taux)

class MontantFixe(Remise):
    def __init__(self, somme): self.somme = montant(somme)
    def appliquer(self, total): return max(Decimal(0), montant(total) - self.somme)

class Seuil(Remise):
    def __init__(self, minimum, remise):
        self.minimum = montant(minimum)
        if not isinstance(remise, Remise): raise TypeError("Stratégie requise")
        self.remise = remise
    def appliquer(self, total):
        total = montant(total)
        return self.remise.appliquer(total) if total >= self.minimum else total

class RemiseFidelite(Remise):
    def __init__(self, annees, taux_par_an=0.01):
        if type(annees) is not int or annees < 0: raise ValueError("Ancienneté invalide")
        self.strategie = Pourcentage(min(Decimal(1), annees * montant(taux_par_an)))
    def appliquer(self, total): return self.strategie.appliquer(total)

class Tarificateur:
    def calculer(self, total, strategies):
        total = montant(total)
        for strategie in strategies:
            if not isinstance(strategie, Remise): raise TypeError("Stratégie requise")
            total = montant(strategie.appliquer(total))
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    assert Tarificateur().calculer(100, [Pourcentage("0.10"), MontantFixe(5)]) == Decimal("85.00")
