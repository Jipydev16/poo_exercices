from abc import ABC, abstractmethod
from decimal import Decimal

def positif(x):
    d = Decimal(str(x))
    if not d.is_finite() or d < 0: raise ValueError("Valeur négative ou non finie")
    return d

class Employe(ABC):
    def __init__(self, nom): self.nom = nom
    @abstractmethod
    def remuneration(self): pass

class Salarie(Employe):
    def __init__(self, nom, mensuel):
        super().__init__(nom); self.mensuel = positif(mensuel)
    def remuneration(self): return self.mensuel

class Freelance(Employe):
    def __init__(self, nom, heures, taux):
        super().__init__(nom); self.heures, self.taux = positif(heures), positif(taux)
    def remuneration(self): return self.heures * self.taux

class Stagiaire(Employe):
    def __init__(self, nom, indemnite):
        super().__init__(nom); self.indemnite = positif(indemnite)
    def remuneration(self): return self.indemnite

def masse_salariale(personnel):
    return sum((e.remuneration() for e in personnel), Decimal(0))

if __name__ == "__main__":
    assert masse_salariale([Salarie("A", 1000), Freelance("B", 20, 15)]) == 1300
