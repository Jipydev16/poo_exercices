from abc import ABC, abstractmethod
from decimal import Decimal

def verifier(montant):
    d = Decimal(str(montant))
    if not d.is_finite() or d <= 0: raise ValueError("Montant strictement positif requis")
    return d

class MoyenPaiement(ABC):
    @abstractmethod
    def payer(self, montant): pass

class Especes(MoyenPaiement):
    def payer(self, montant): return f"ESP-{verifier(montant):.2f}"

class Carte(MoyenPaiement):
    def __init__(self, numero):
        if not numero: raise ValueError("Numéro requis")
        self.numero = str(numero)
    def payer(self, montant): return f"CB-{self.numero[-4:]}-{verifier(montant):.2f}"

class MobileMoney(MoyenPaiement):
    def __init__(self, numero): self.numero = numero
    def payer(self, montant): return f"MM-{self.numero}-{verifier(montant):.2f}"

class Virement(MoyenPaiement):
    def __init__(self, iban): self.iban = iban
    def payer(self, montant): return f"VIR-{self.iban}-{verifier(montant):.2f}"

class Caisse:
    def encaisser(self, moyen, montant):
        if not isinstance(moyen, MoyenPaiement): raise TypeError("MoyenPaiement requis")
        return moyen.payer(verifier(montant))

if __name__ == "__main__":
    assert Caisse().encaisser(Carte("1234"), 20) == "CB-1234-20.00"
