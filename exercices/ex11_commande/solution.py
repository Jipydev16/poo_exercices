"""Ex. 11 — State machine : contrôler les transitions d'une commande."""

# ALGORITHME — Chaque transition contrôle l’état courant et ne modifie rien si elle est impossible.
# INVARIANT — États autorisés : BROUILLON → CONFIRMEE → EXPEDIEE ; annulation avant expédition.
# COMPLEXITÉ — Changement d’état : O(1) ; total : O(n) lignes.
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class Statut(str, Enum):
    BROUILLON = 'brouillon'
    CONFIRMEE = 'confirmee'
    EXPEDIEE = 'expediee'
    ANNULEE = 'annulee'

@dataclass(frozen=True)
class LigneCommande:
    reference: str
    quantite: int
    prix_unitaire: Decimal

    def __post_init__(self):
        if not self.reference.strip() or type(self.quantite) is not int or self.quantite <= 0:
            raise ValueError("Ligne invalide")
        prix = Decimal(str(self.prix_unitaire))
        if not prix.is_finite() or prix < 0:
            raise ValueError("Prix invalide")
        # frozen=True : normaliser l'attribut via object.__setattr__.
        object.__setattr__(self, 'prix_unitaire', prix)

    @property
    def montant(self) -> Decimal:
        return self.quantite * self.prix_unitaire

class Commande:
    def __init__(self, identifiant: str):
        if not identifiant.strip():
            raise ValueError("Identifiant vide")
        self.identifiant = identifiant
        self._statut = Statut.BROUILLON
        self._lignes: list[LigneCommande] = []

    @property
    def statut(self) -> Statut:
        return self._statut

    @property
    def total(self) -> Decimal:
        return sum((l.montant for l in self._lignes), Decimal('0'))

    def ajouter(self, ligne: LigneCommande) -> None:
        if self.statut != Statut.BROUILLON or not isinstance(ligne, LigneCommande):
            raise ValueError("Modification interdite")
        self._lignes.append(ligne)

    def confirmer(self) -> None:
        if self.statut != Statut.BROUILLON or not self._lignes:
            raise ValueError("Confirmation impossible")
        self._statut = Statut.CONFIRMEE

    def expedier(self) -> None:
        if self.statut != Statut.CONFIRMEE:
            raise ValueError("Expédition impossible")
        self._statut = Statut.EXPEDIEE

    def annuler(self) -> None:
        if self.statut not in (Statut.BROUILLON, Statut.CONFIRMEE):
            raise ValueError("Annulation impossible après expédition")
        self._statut = Statut.ANNULEE

if __name__ == '__main__':
    c = Commande('C01')
    c.ajouter(LigneCommande('P01', 3, '5.5'))
    c.confirmer()
    print(c.total, c.statut.value)  # 16.5 confirmee
