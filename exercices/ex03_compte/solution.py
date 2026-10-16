"""Ex. 03 — Compte bancaire : respecter les invariants du solde."""

# ALGORITHME — Valider montant et solde puis retirer et créditer ; aucune mutation en cas de refus.
# INVARIANT — Invariant : solde non négatif ; somme des deux soldes conservée par transfert.
# COMPLEXITÉ — Opérations élémentaires : O(1).
from decimal import Decimal

class CompteBancaire:
    def __init__(self, titulaire: str, solde_initial=0):
        if not titulaire.strip():
            raise ValueError("Titulaire vide")
        self.titulaire = titulaire.strip()
        self._solde = Decimal("0")
        montant = self._montant(solde_initial)
        self._solde = montant  # Un solde initial peut être nul.

    @staticmethod
    def _montant(somme) -> Decimal:
        # Decimal(str(...)) évite certaines imprécisions binaires des floats.
        if isinstance(somme, bool):
            raise ValueError("Montant invalide")
        try:
            montant = Decimal(str(somme))
        except Exception as exc:
            raise ValueError("Montant invalide") from exc
        if not montant.is_finite() or montant < 0:
            raise ValueError("Montant négatif ou non fini")
        return montant

    @property
    def solde(self) -> Decimal:
        return self._solde

    def deposer(self, somme) -> None:
        montant = self._montant(somme)
        if montant == 0:
            raise ValueError("Le dépôt doit être positif")
        self._solde += montant

    def retirer(self, somme) -> None:
        montant = self._montant(somme)
        if montant == 0:
            raise ValueError("Le retrait doit être positif")
        if montant > self.solde:
            raise ValueError("Solde insuffisant")
        self._solde -= montant

    def transferer(self, destinataire: 'CompteBancaire', somme) -> None:
        if not isinstance(destinataire, CompteBancaire) or destinataire is self:
            raise ValueError("Destinataire invalide")
        montant = self._montant(somme)
        if montant == 0 or montant > self.solde:
            raise ValueError("Transfert impossible")
        # Valider avant mutation assure l'absence de transfert partiel.
        self._solde -= montant
        destinataire._solde += montant

if __name__ == "__main__":
    a, b = CompteBancaire("Alice", 100), CompteBancaire("Benoît")
    a.transferer(b, 35)
    print(a.solde, b.solde)  # 65 35
