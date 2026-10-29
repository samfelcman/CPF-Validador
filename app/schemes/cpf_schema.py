from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class CPFValidateRequest(BaseModel):
    cpf: str = Field(
        ...,
        example="165.948.507-09",
        description="CPF a ser validado (pode conter pontuação ou apenas números)"
    )
    
class CPFValidateResponse(BaseModel):
    cpf_masked: str = Field(..., example="165.***.***-09")
    is_valid: bool = Field(..., example=True)
    origin_state: Optional[str] = Field(None, example="ES, RJ")
    risk_score: int = Field(..., example=0, description="Score de 0 (Seguro) a 100 (Inválido/Risco)")
    risk_flags: List[str] = Field(..., example=["NENHUM_RISCO_DETECTADO"])
    metadata: Dict[str, str] = Field(default_factory=dict)