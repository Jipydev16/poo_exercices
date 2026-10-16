from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum

class Statut(str, Enum):
    BROUILLON = "brouillon"
    CONFIRMEE = "confirmee"
    EXPEDIEE = "expediee"
    ANNULEE = "annulee"

@dataclass(frozen=True)
class LigneCommande:
    ref: str
    qte: int
    prix: Decimal
    def __post_init__(self):
        p = Decimal(str(self.prix))
        if not self.ref or type(self.qte) is not int or self.qte <= 0 or not p.is_finite() or p < 0:
            raise ValueError("Ligne invalide")
        object.__setattr__(self, "prix", p)

class Commande:
    def __init__(self, identifiant):
        self.identifiant = identifiant
        self._lignes = []
        self.statut = Statut.BROUILLON
        self.journal = [self.statut.value]
    @property
    def total(self): return sum((l.qte * l.prix for l in self._lignes), Decimal(0))
    def ajouter(self, ligne):
        if self.statut != Statut.BROUILLON: raise ValueError("Commande non modifiable")
        if not isinstance(ligne, LigneCommande): raise TypeError("LigneCommande attendue")
        self._lignes.append(ligne)
    def _transition(self, attendu, nouveau):
        if self.statut != attendu: raise ValueError("Transition interdite")
        self.statut = nouveau; self.journal.append(nouveau.value)
    def confirmer(self):
        if not self._lignes: raise ValueError("Commande vide")
        self._transition(Statut.BROUILLON, Statut.CONFIRMEE)
    def expedier(self): self._transition(Statut.CONFIRMEE, Statut.EXPEDIEE)
    def annuler(self):
        if self.statut not in (Statut.BROUILLON, Statut.CONFIRMEE): raise ValueError("Annulation interdite")
        self.statut = Statut.ANNULEE; self.journal.append(self.statut.value)

if __name__ == "__main__":
    c = Commande("C01"); c.ajouter(LigneCommande("P", 3, "5.50")); c.confirmer()
    assert c.total == Decimal("16.50") and c.statut == Statut.CONFIRMEE
