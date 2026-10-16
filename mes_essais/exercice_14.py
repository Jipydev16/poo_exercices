from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

class LigneAPI(BaseModel):
    model_config = ConfigDict(extra="forbid")
    reference: str
    quantite: int = Field(strict=True, gt=0)
    prix: Decimal = Field(ge=0, allow_inf_nan=False)

    @field_validator("reference")
    @classmethod
    def reference_non_vide(cls, v):
        if not v.strip(): raise ValueError("Référence vide")
        return v.strip()

class CommandeAPI(BaseModel):
    model_config = ConfigDict(extra="forbid")
    client_id: str
    lignes: list[LigneAPI] = Field(min_length=1)
    code_promo: str | None = None
    expiration_promo: date | None = None

    @field_validator("client_id")
    @classmethod
    def client_non_vide(cls, v):
        if not v.strip(): raise ValueError("Client vide")
        return v.strip()

    @model_validator(mode="after")
    def verifier_commande(self):
        refs = [l.reference for l in self.lignes]
        if len(refs) != len(set(refs)): raise ValueError("Référence dupliquée")
        if self.code_promo is not None:
            if not self.code_promo.strip(): raise ValueError("Code promo vide")
            if self.expiration_promo is None or self.expiration_promo < date.today():
                raise ValueError("Promotion expirée ou date absente")
        elif self.expiration_promo is not None:
            raise ValueError("Date sans code promotionnel")
        return self

    @property
    def total(self): return sum((l.prix * l.quantite for l in self.lignes), Decimal(0))

if __name__ == "__main__":
    c = CommandeAPI(client_id="C1", lignes=[{"reference":"P1", "quantite":2, "prix":"12.50"}])
    assert c.total == Decimal("25.00")
