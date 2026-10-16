"""Ex. 07 — ABC : définir un contrat commun et l'injecter."""

# ALGORITHME — Le service reçoit un objet conforme à l’interface et délègue le paiement.
# INVARIANT — Contrat ABC : tout moyen de paiement doit implémenter payer.
# COMPLEXITÉ — Caisse.encaisser : O(1) ici (simulations sans réseau).
from abc import ABC, abstractmethod
from decimal import Decimal

class MoyenPaiement(ABC):
    @abstractmethod
    def payer(self, montant: Decimal) -> str:
        """Retourne une référence de transaction après validation."""

class Especes(MoyenPaiement):
    def payer(self, montant: Decimal) -> str:
        return f"CASH-{montant:.2f}"

class Carte(MoyenPaiement):
    def __init__(self, quatre_derniers: str):
        if len(quatre_derniers) != 4 or not quatre_derniers.isdigit():
            raise ValueError("4 chiffres attendus")
        self.quatre_derniers = quatre_derniers

    def payer(self, montant: Decimal) -> str:
        # On ne journalise jamais le numéro de carte complet.
        return f"CB-{self.quatre_derniers}-{montant:.2f}"

class MobileMoney(MoyenPaiement):
    def __init__(self, telephone: str):
        if not telephone.strip():
            raise ValueError("Téléphone manquant")
        self.telephone = telephone.strip()

    def payer(self, montant: Decimal) -> str:
        return f"MOMO-{self.telephone[-4:]}-{montant:.2f}"

class Caisse:
    def encaisser(self, moyen: MoyenPaiement, montant) -> str:
        if not isinstance(moyen, MoyenPaiement):
            raise TypeError("Mode de paiement attendu")
        valeur = Decimal(str(montant))
        if not valeur.is_finite() or valeur <= 0:
            raise ValueError("Le montant doit être positif")
        # La caisse délègue l'action ; elle ne connaît pas les sous-classes.
        return moyen.payer(valeur)

if __name__ == "__main__":
    print(Caisse().encaisser(Carte('1234'), 20))  # CB-1234-20.00
