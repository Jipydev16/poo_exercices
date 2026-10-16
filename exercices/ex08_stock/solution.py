"""Ex. 08 — Exceptions de domaine et transfert sans perte."""

# ALGORITHME — Valider référence, quantité et disponibilité AVANT la mutation des deux stocks.
# INVARIANT — Invariant : quantités entières, non négatives ; transfert conservant les unités.
# COMPLEXITÉ — Dictionnaires : O(1) en moyenne par opération.
class StockErreur(Exception):
    """Base commune des erreurs métier de stock."""

class StockInsuffisant(StockErreur):
    pass

class ReferenceInconnue(StockErreur):
    pass

class Stock:
    def __init__(self):
        self._quantites: dict[str, int] = {}

    @staticmethod
    def _valider(reference: str, quantite: int) -> None:
        if not isinstance(reference, str) or not reference.strip():
            raise ValueError("Référence manquante")
        if type(quantite) is not int or quantite <= 0:
            raise ValueError("Quantité entière strictement positive attendue")

    def quantite(self, reference: str) -> int:
        return self._quantites.get(reference, 0)

    def ajouter(self, reference: str, quantite: int) -> None:
        self._valider(reference, quantite)
        self._quantites[reference] = self.quantite(reference) + quantite

    def sortir(self, reference: str, quantite: int) -> None:
        self._valider(reference, quantite)
        if reference not in self._quantites:
            raise ReferenceInconnue(reference)
        if self.quantite(reference) < quantite:
            raise StockInsuffisant(reference)
        self._quantites[reference] -= quantite

    def transferer(self, autre: 'Stock', reference: str, quantite: int) -> None:
        if not isinstance(autre, Stock) or autre is self:
            raise ValueError("Destination invalide")
        self._valider(reference, quantite)
        if reference not in self._quantites:
            raise ReferenceInconnue(reference)
        if self.quantite(reference) < quantite:
            raise StockInsuffisant(reference)
        # Préconditions validées avant de retirer ; le destinataire ne peut échouer.
        self._quantites[reference] -= quantite
        autre._quantites[reference] = autre.quantite(reference) + quantite

if __name__ == "__main__":
    depot, boutique = Stock(), Stock()
    depot.ajouter('P01', 10)
    depot.transferer(boutique, 'P01', 4)
    print(depot.quantite('P01'), boutique.quantite('P01'))  # 6 4
