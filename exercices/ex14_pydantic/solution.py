"""Ex. 14 — PAQUET EXTERNE #2 : Pydantic v2 et validation métier."""

# ALGORITHME — Pydantic valide les champs puis model_validator effectue un parcours avec set.
# INVARIANT — Invariant : commande non vide, quantités positives, références uniques.
# COMPLEXITÉ — Détection des doublons : O(n) en moyenne ; total O(n).
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, model_validator

class LigneAPI(BaseModel):
    reference: str = Field(min_length=1)
    quantite: int = Field(strict=True, gt=0)
    prix_unitaire: Decimal = Field(ge=0, allow_inf_nan=False)

    @field_validator('reference')
    @classmethod
    def reference_non_vide(cls, reference: str) -> str:
        # min_length=1 ne rejette pas une chaîne ne contenant que des espaces.
        reference = reference.strip()
        if not reference:
            raise ValueError('Référence vide')
        return reference

class CommandeAPI(BaseModel):
    client_id: str = Field(min_length=1)
    lignes: list[LigneAPI] = Field(min_length=1)

    @field_validator('client_id')
    @classmethod
    def client_non_vide(cls, valeur: str) -> str:
        if not valeur.strip():
            raise ValueError('Identifiant client vide')
        return valeur.strip()

    @model_validator(mode='after')
    def sans_references_dupliquees(self) -> 'CommandeAPI':
        # Algorithme avec ensemble (set) : O(n) en moyenne.
        deja_vues: set[str] = set()
        for ligne in self.lignes:
            if ligne.reference in deja_vues:
                raise ValueError('Référence dupliquée dans une commande')
            deja_vues.add(ligne.reference)
        return self

    @property
    def total(self) -> Decimal:
        return sum((l.quantite * l.prix_unitaire for l in self.lignes), Decimal('0'))

if __name__ == '__main__':
    c = CommandeAPI.model_validate({'client_id':'C1','lignes':[{'reference':'P1','quantite':2,'prix_unitaire':'12.50'}]})
    print(c.total)  # 25.00
