from decimal import Decimal
from datetime import datetime, timezone

def argent(x):
    d = Decimal(str(x))
    if not d.is_finite(): raise ValueError("Montant non fini")
    return d

class CompteBancaire:
    def __init__(self, titulaire, solde_initial=0):
        self.titulaire = titulaire
        self._solde = argent(solde_initial)
        if self._solde < 0: raise ValueError("Solde négatif")
        self.historique = []

    @property
    def solde(self): return self._solde

    @staticmethod
    def _montant(somme):
        d = argent(somme)
        if d <= 0: raise ValueError("Montant strictement positif requis")
        return d

    def _journal(self, motif, somme):
        self.historique.append((datetime.now(timezone.utc).isoformat(), motif, somme))

    def deposer(self, somme):
        d = self._montant(somme)
        self._solde += d
        self._journal("dépôt", d)

    def retirer(self, somme):
        d = self._montant(somme)
        if d > self._solde: raise ValueError("Solde insuffisant")
        self._solde -= d
        self._journal("retrait", -d)

    def transferer(self, destinataire, somme):
        if not isinstance(destinataire, CompteBancaire) or destinataire is self:
            raise ValueError("Destinataire invalide")
        d = self._montant(somme)
        if d > self._solde: raise ValueError("Solde insuffisant")
        self._solde -= d
        destinataire._solde += d
        self._journal("transfert sortant", -d)
        destinataire._journal("transfert entrant", d)

if __name__ == "__main__":
    a, b = CompteBancaire("A", 100), CompteBancaire("B")
    a.transferer(b, 35)
    assert (a.solde, b.solde) == (65, 35)
