"""Ex. 13 — Strategy : interchanger des algorithmes sans if/elif géants."""

# ALGORITHME — Appliquer les stratégies dans l’ordre fourni ; le prix intermédiaire devient l’entrée suivante.
# INVARIANT — Contrat : chaque stratégie reçoit un total non négatif et retourne un total non négatif.
# COMPLEXITÉ — Calcul : O(k) pour k règles de promotion.
from abc import ABC, abstractmethod
from decimal import Decimal

class Remise(ABC):
    @abstractmethod
    def appliquer(self, total: Decimal) -> Decimal:
        """Retourne le nouveau montant, jamais négatif."""

class Pourcentage(Remise):
    def __init__(self, taux):
        self.taux = Decimal(str(taux))
        if not self.taux.is_finite() or not 0 <= self.taux <= 1:
            raise ValueError("Taux entre 0 et 1 requis")

    def appliquer(self, total: Decimal) -> Decimal:
        return total * (1 - self.taux)

class MontantFixe(Remise):
    def __init__(self, remise):
        self.remise = Decimal(str(remise))
        if not self.remise.is_finite() or self.remise < 0:
            raise ValueError("Réduction invalide")

    def appliquer(self, total: Decimal) -> Decimal:
        # Une réduction ne peut pas rendre un prix négatif.
        return max(Decimal('0'), total - self.remise)

class Seuil(Remise):
    def __init__(self, minimum, remise):
        self.minimum = Decimal(str(minimum))
        self._strategie = MontantFixe(remise)
        if not self.minimum.is_finite() or self.minimum < 0:
            raise ValueError("Seuil invalide")

    def appliquer(self, total: Decimal) -> Decimal:
        return self._strategie.appliquer(total) if total >= self.minimum else total

class Tarificateur:
    def calculer(self, montant, strategies: list[Remise]) -> Decimal:
        prix = Decimal(str(montant))
        if not prix.is_finite() or prix < 0:
            raise ValueError("Prix initial invalide")
        for strategie in strategies:
            if not isinstance(strategie, Remise):
                raise TypeError("Une stratégie Remise est attendue")
            # L'ordre compte : chaque règle utilise le total après la précédente.
            prix = strategie.appliquer(prix)
        return prix.quantize(Decimal('0.01'))

if __name__ == '__main__':
    print(Tarificateur().calculer(100, [Pourcentage('0.10'), MontantFixe('5')]))  # 85.00
