"""Ex. 01 — Classe et objet : gérer les notes d'un étudiant."""

# ALGORITHME — Parcourir les notes et calculer la somme, puis diviser par le nombre d’éléments.
# INVARIANT — Invariant : chaque note appartient à [0,20].
# COMPLEXITÉ — moyenne() : O(n) temps ; stockage : O(n).
class Etudiant:
    def __init__(self, nom: str, prenom: str):
        # Les attributs appartiennent à chaque instance, pas à la classe.
        if not nom.strip() or not prenom.strip():
            raise ValueError("Le nom et le prénom sont obligatoires")
        self.nom = nom.strip()
        self.prenom = prenom.strip()
        self.notes: list[float] = []

    def ajouter_note(self, note: float) -> None:
        # Invariant : une note doit rester dans l'intervalle fermé [0, 20].
        if isinstance(note, bool) or not isinstance(note, (int, float)) or not 0 <= note <= 20:
            raise ValueError("Une note doit être comprise entre 0 et 20")
        self.notes.append(float(note))

    def moyenne(self) -> float | None:
        # Aucune note : ne pas diviser par zéro ; None signifie « inconnue ».
        if not self.notes:
            return None
        return sum(self.notes) / len(self.notes)

    def est_admis(self, seuil: float = 10) -> bool:
        # Une moyenne absente ne peut jamais mener à une admission.
        resultat = self.moyenne()
        return resultat is not None and resultat >= seuil

if __name__ == "__main__":
    eleve = Etudiant("Kasongo", "Amina")
    for note in (12, 14, 10):
        eleve.ajouter_note(note)
    print(eleve.moyenne(), eleve.est_admis())  # 12.0 True
