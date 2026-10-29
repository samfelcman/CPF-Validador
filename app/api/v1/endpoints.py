from fastapi import APIRouter, status
from app.core.validator import AdvancedCPFValidator
from app.schemes.cpf_schema import CPFValidateRequest, CPFValidateResponse

router = APIRouter()

@router.post(
    "/validate",
    response_model=CPFValidateResponse,
    status_code=status.HTTP_200_OK,
    summary="Valida e analisa um documento CPF",
    description="Executa validação via algoritmo Módulo 11, detecta fiscal de emissão e avalia risco de fraude."
)
def validate_cpf(payload: CPFValidateRequest):
    validator = AdvancedCPFValidator(payload.cpf)
    result = validator.analyze()
    
    return CPFValidateResponse(
        cpf_masked=result.cpf_masked,
        is_valid=result.is_valid,
        origin_state=result.origen_state,
        risk_score=result.risk_score,
        risk_flags=result.risk_flags,
        metadata=result.metadata
    )