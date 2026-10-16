class Rectangle:
    def __init__(self, largeur, hauteur):
        self.redimensionner(largeur, hauteur)

    @staticmethod
    def _valider(x):
        if isinstance(x, bool) or not isinstance(x, (int, float)) or not 0 < x < float("inf"):
            raise ValueError("Dimension strictement positive requise")
        return float(x)

    @property
    def largeur(self): return self._largeur
    @largeur.setter
    def largeur(self, valeur): self._largeur = self._valider(valeur)
    @property
    def hauteur(self): return self._hauteur
    @hauteur.setter
    def hauteur(self, valeur): self._hauteur = self._valider(valeur)
    @property
    def surface(self): return self.largeur * self.hauteur
    @property
    def perimetre(self): return 2 * (self.largeur + self.hauteur)
    @property
    def est_carre(self): return self.largeur == self.hauteur
    def redimensionner(self, l, h):
        l, h = self._valider(l), self._valider(h)
        self._largeur, self._hauteur = l, h

if __name__ == "__main__":
    r = Rectangle(3, 4)
    assert r.surface == 12 and r.perimetre == 14
