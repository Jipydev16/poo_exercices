"""Ex. 02 — Encapsulation : dimensions toujours strictement positives."""

# ALGORITHME — Valider entièrement une nouvelle dimension avant de modifier les attributs.
# INVARIANT — Invariant : largeur > 0 et hauteur > 0.
# COMPLEXITÉ — Surface/périmètre/redimensionnement : O(1).
class Rectangle:
    def __init__(self, largeur: float, hauteur: float):
        # Utiliser une opération validée unique, évite les règles divergentes.
        self.redimensionner(largeur, hauteur)

    @staticmethod
    def _valider_dimension(valeur: float) -> float:
        if isinstance(valeur, bool) or not isinstance(valeur, (int, float)) or valeur <= 0:
            raise ValueError("Les dimensions doivent être strictement positives")
        return float(valeur)

    @property
    def largeur(self) -> float:
        # Lecture permise ; affecter rectangle.largeur directement est interdit.
        return self._largeur

    @property
    def hauteur(self) -> float:
        return self._hauteur

    @property
    def surface(self) -> float:
        return self.largeur * self.hauteur

    @property
    def perimetre(self) -> float:
        return 2 * (self.largeur + self.hauteur)

    def redimensionner(self, largeur: float, hauteur: float) -> None:
        # Valider les DEUX arguments avant toute mutation : opération atomique.
        l = self._valider_dimension(largeur)
        h = self._valider_dimension(hauteur)
        self._largeur, self._hauteur = l, h

if __name__ == "__main__":
    r = Rectangle(3, 4)
    print(r.surface, r.perimetre)  # 12.0 14.0
