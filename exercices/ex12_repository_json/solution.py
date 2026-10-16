"""Ex. 12 — FICHIERS #2 : Repository et écriture atomique sur disque."""

# ALGORITHME — Préparer un nouvel état, écrire un temporaire, os.replace, publier le nouvel état en mémoire.
# INVARIANT — Invariant : identifiant client unique ; état mémoire cohérent avec le fichier.
# COMPLEXITÉ — CRUD lecture mémoire O(1) moyen ; écriture O(n log n) avec tri et sérialisation.
import json
import os
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass(frozen=True)
class Client:
    id: str
    nom: str
    email: str

    def __post_init__(self):
        if not self.id.strip() or not self.nom.strip() or '@' not in self.email:
            raise ValueError("Client invalide")

class Repository(ABC):
    @abstractmethod
    def ajouter(self, client: Client) -> None: ...
    @abstractmethod
    def obtenir(self, id: str) -> Client | None: ...
    @abstractmethod
    def lister(self) -> list[Client]: ...
    @abstractmethod
    def supprimer(self, id: str) -> bool: ...

class RepositoryClientsJSON(Repository):
    def __init__(self, chemin: str | Path):
        self.chemin = Path(chemin)
        # Lire n'est pas écrire : un nouveau repository n'écrase pas un ancien.
        self._clients: dict[str, Client] = {}
        if self.chemin.exists():
            donnees = json.loads(self.chemin.read_text(encoding='utf-8'))
            if not isinstance(donnees, list):
                raise ValueError("Le JSON doit contenir une liste")
            for item in donnees:
                client = Client(**item)
                if client.id in self._clients:
                    raise ValueError("Identifiants dupliqués dans le fichier")
                self._clients[client.id] = client

    def _persister(self, clients: dict[str, Client]) -> None:
        # Créer un fichier temporaire à côté de la cible, puis le remplacer.
        # Ainsi une exception avant os.replace préserve l'ancien fichier.
        self.chemin.parent.mkdir(parents=True, exist_ok=True)
        fd, temporaire = tempfile.mkstemp(prefix='.clients_', suffix='.tmp', dir=self.chemin.parent)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump([asdict(clients[k]) for k in sorted(clients)], f, ensure_ascii=False, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temporaire, self.chemin)
        finally:
            if os.path.exists(temporaire):
                os.unlink(temporaire)

    def ajouter(self, client: Client) -> None:
        if not isinstance(client, Client) or client.id in self._clients:
            raise ValueError("Client invalide ou identifiant déjà utilisé")
        nouveau = dict(self._clients)
        nouveau[client.id] = client
        # On ne publie le nouvel état en mémoire qu'après écriture réussie.
        self._persister(nouveau)
        self._clients = nouveau

    def obtenir(self, id: str) -> Client | None:
        return self._clients.get(id)

    def lister(self) -> list[Client]:
        return [self._clients[k] for k in sorted(self._clients)]

    def supprimer(self, id: str) -> bool:
        if id not in self._clients:
            return False
        nouveau = dict(self._clients)
        del nouveau[id]
        self._persister(nouveau)
        self._clients = nouveau
        return True

if __name__ == '__main__':
    from tempfile import TemporaryDirectory
    with TemporaryDirectory() as d:
        repo = RepositoryClientsJSON(Path(d) / 'clients.json')
        repo.ajouter(Client('C1', 'Amina', 'amina@example.org'))
        print(RepositoryClientsJSON(Path(d) / 'clients.json').obtenir('C1'))
