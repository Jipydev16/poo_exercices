"""Ex. 06 — Polymorphisme : même méthode, calcul différent."""

# ALGORITHME — Parcourir la liste et appeler remuneration() sans inspecter les classes.
# INVARIANT — Contrat : toute sous-classe d’Employe calcule sa rémunération.
# COMPLEXITÉ — Masse salariale : O(n) pour n employés.
from decimal import Decimal

class Employe:
    def __init__(self, nom: str):
        if not nom.strip():
            raise ValueError("Nom obligatoire")
        self.nom = nom.strip()

    def remuneration(self) -> Decimal:
        # Un type de base définit un contrat que ses enfants redéfinissent.
        raise NotImplementedError("Spécialiser la méthode")

class Salarie(Employe):
    def __init__(self, nom: str, mensuel):
        super().__init__(nom)
        self.mensuel = Decimal(str(mensuel))
        if not self.mensuel.is_finite() or self.mensuel < 0:
            raise ValueError("Salaire invalide")

    def remuneration(self) -> Decimal:
        return self.mensuel

class Freelance(Employe):
    def __init__(self, nom: str, heures: int, taux):
        super().__init__(nom)
        if type(heures) is not int or heures < 0:
            raise ValueError("Heures invalides")
        self.heures, self.taux = heures, Decimal(str(taux))
        if not self.taux.is_finite() or self.taux < 0:
            raise ValueError("Taux invalide")

    def remuneration(self) -> Decimal:
        return self.heures * self.taux

def masse_salariale(personnel: list[Employe]) -> Decimal:
    # Pas de if isinstance(...) : le polymorphisme choisit la formule.
    return sum((employe.remuneration() for employe in personnel), Decimal('0'))

if __name__ == "__main__":
    equipe = [Salarie("Anne", 1000), Freelance("Junior", 20, 15)]
    print(masse_salariale(equipe))  # 1300
