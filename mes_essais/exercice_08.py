from datetime import datetime, timezone

class ReferenceInconnue(Exception): pass
class StockInsuffisant(Exception): pass

class Stock:
    def __init__(self, seuil_alerte=0):
        self._quantites = {}; self.journal = []; self.seuil_alerte = seuil_alerte

    @staticmethod
    def _valider(q):
        if type(q) is not int or q <= 0: raise ValueError("Quantité entière positive requise")

    def _log(self, action, ref, q):
        self.journal.append((datetime.now(timezone.utc).isoformat(), action, ref, q))

    def quantite(self, ref): return self._quantites.get(ref, 0)

    def ajouter(self, ref, quantite):
        self._valider(quantite)
        if not ref: raise ValueError("Référence vide")
        self._quantites[ref] = self.quantite(ref) + quantite
        self._log("entrée", ref, quantite)

    def sortir(self, ref, quantite):
        self._valider(quantite)
        if ref not in self._quantites: raise ReferenceInconnue(ref)
        if self.quantite(ref) < quantite: raise StockInsuffisant(ref)
        self._quantites[ref] -= quantite
        self._log("sortie", ref, quantite)

    def transferer(self, autre, ref, quantite):
        if not isinstance(autre, Stock) or autre is self: raise ValueError("Destination invalide")
        self._valider(quantite)
        if ref not in self._quantites: raise ReferenceInconnue(ref)
        if self.quantite(ref) < quantite: raise StockInsuffisant(ref)
        self._quantites[ref] -= quantite
        autre._quantites[ref] = autre.quantite(ref) + quantite
        self._log("transfert sortant", ref, quantite)
        autre._log("transfert entrant", ref, quantite)

    def alertes(self):
        return [ref for ref, q in self._quantites.items() if q <= self.seuil_alerte]

if __name__ == "__main__":
    a, b = Stock(), Stock(); a.ajouter("P", 10); a.transferer(b, "P", 4)
    assert (a.quantite("P"), b.quantite("P")) == (6, 4)
