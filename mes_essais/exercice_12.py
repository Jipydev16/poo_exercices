from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from pathlib import Path
import json, os, tempfile

@dataclass(frozen=True)
class Client:
    id: str
    nom: str
    email: str

class Repository(ABC):
    @abstractmethod
    def ajouter(self, client): pass
    @abstractmethod
    def obtenir(self, identifiant): pass
    @abstractmethod
    def lister(self): pass
    @abstractmethod
    def supprimer(self, identifiant): pass

class RepositoryClientsMemoire(Repository):
    def __init__(self): self._clients = {}
    def ajouter(self, client):
        if client.id in self._clients: raise ValueError("Identifiant dupliqué")
        self._clients[client.id] = client
    def obtenir(self, identifiant): return self._clients.get(identifiant)
    def lister(self): return list(self._clients.values())
    def supprimer(self, identifiant): return self._clients.pop(identifiant, None) is not None

class RepositoryClientsJSON(RepositoryClientsMemoire):
    def __init__(self, chemin):
        super().__init__(); self.chemin = Path(chemin)
        if self.chemin.exists():
            try:
                donnees = json.loads(self.chemin.read_text(encoding="utf-8"))
                if not isinstance(donnees, list): raise ValueError("Liste JSON attendue")
                for item in donnees: super().ajouter(Client(**item))
            except (ValueError, TypeError, KeyError) as e:
                raise ValueError("Fichier clients corrompu") from e

    def _sauver(self):
        self.chemin.parent.mkdir(parents=True, exist_ok=True)
        nom = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=self.chemin.parent, delete=False) as f:
                nom = f.name
                json.dump([asdict(c) for c in self.lister()], f, ensure_ascii=False, indent=2)
                f.flush(); os.fsync(f.fileno())
            os.replace(nom, self.chemin)
        finally:
            if nom and os.path.exists(nom): os.unlink(nom)

    def ajouter(self, client):
        super().ajouter(client)
        try: self._sauver()
        except Exception:
            del self._clients[client.id]
            raise

    def supprimer(self, identifiant):
        if identifiant not in self._clients: return False
        ancien = self._clients.pop(identifiant)
        try: self._sauver()
        except Exception:
            self._clients[identifiant] = ancien
            raise
        return True

if __name__ == "__main__":
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as d:
        chemin = Path(d) / "clients.json"
        r = RepositoryClientsJSON(chemin); r.ajouter(Client("C1", "Alice", "a@example.org"))
        assert RepositoryClientsJSON(chemin).obtenir("C1").nom == "Alice"
