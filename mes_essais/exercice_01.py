class Etudiant:
    def __init__(self, nom, prenom):
        self.nom, self.prenom = nom, prenom
        self.notes = []

    def ajouter_note(self, note):
        if not isinstance(note, (int, float)) or not 0 <= note <= 20:
            raise ValueError("Note attendue entre 0 et 20")
        self.notes.append(note)

    def moyenne(self):
        return sum(self.notes) / len(self.notes) if self.notes else None

    def est_admis(self, seuil=10):
        m = self.moyenne()
        return m is not None and m >= seuil

    def meilleure_note(self):
        return max(self.notes) if self.notes else None

if __name__ == "__main__":
    e = Etudiant("L", "J")
    for n in (12, 14, 10): e.ajouter_note(n)
    assert e.moyenne() == 12 and e.est_admis()
