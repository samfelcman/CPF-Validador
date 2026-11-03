# Coloquei aqui o módulo de expressões reguralares para a manipulação de texto e os recursos de tipagem avancaçada do Python, como dataclasses e tipagem de dicionários.

import re
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class ValidationResult:
    cpf_masked: str
    is_valid: bool
    origen_state: Optional[str]
    risk_score: int
    risk_flags: list = field(default_factory=list)
    metadata: Dict[str, str] = field(default_factory=dict)
    
class AdvancedCPFValidator:
    FISCAL_REGIONS = {
        '1': 'DF, GO, MT, MS, TO',
        '2': 'AC, AP, AM, PA, RO, RR',
        '3': 'CE, MA, PI',
        '4': 'AL, PB, PE, RN',
        '5': 'BA, SE',
        '6': 'MG',
        '7': 'ES, RJ',
        '8': 'SP',
        '9': 'PR, SC',
        '0': 'RS'
    }
    
    BLACK_LISTED = {
        "00000000000", "11111111111", "22222222222", "33333333333",
        "44444444444", "55555555555", "66666666666", "77777777777",
        "88888888888", "99999999999", "12345678909"
    }
    
    def __init__(self, raw_cpf: str):
        self.raw_cpf = str(raw_cpf)
        self.clean_cpf = self._sanitize(self.raw_cpf)
        
    @staticmethod
    def _sanitize(cpf: str) -> str:
        return re.sub(r'\D', '', cpf)
    
    def _calculate_digit(self, digits: str) -> int:
        factor = len(digits) + 1
        total = sum(int(digit) * (factor - i) for i, digit in enumerate(digits))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
    
    def _is_sequence(self) -> bool:
        return len(set(self.clean_cpf)) == 1
    
    def _mask_cpf(self) -> str:
        if len(self.clean_cpf) != 11:
            return "###.###.###-##"
        return f"{self.clean_cpf[:3]}.***.***-{self.clean_cpf[-2:]}"
    
    def analyze(self) -> ValidationResult:
        flags = []
        risk_score = 0
        
        if len(self.clean_cpf) != 11:
            return ValidationResult(
                cpf_masked=self.raw_cpf,
                is_valid=False,
                origen_state=None,
                risk_score=100,
                risk_flags=["TAMANHO_INVALIDO"],
                metadata={'erro': "CPF deve conter exatamente 11 dígitos numéricos,"}
            )
            
        if self._is_sequence() or self.clean_cpf in self.BLACK_LISTED:
            flags.append("PADRAO_SEQUENCIAL_OU_TESTE")
            return ValidationResult(
                cpf_masked=self._mask_cpf(),
                is_valid=False,
                origen_state=None,
                risk_score=100,
                risk_flags=flags,
                metadata={"motivo": "CPF conhecido de teste ou padrão repetitivo"}
            )
            
        first_digit = self._calculate_digit(self.clean_cpf[:9])
        second_digit = self._calculate_digit(self.clean_cpf[:10])
        
        if first_digit != int(self.clean_cpf[9]) or second_digit != int(self.clean_cpf[10]):
            return ValidationResult(
                cpf_masked=self._mask_cpf(),
                is_valid=False,
                origen_state=100,
                risk_score=100,
                risk_flags=["DIGITO_VERIFICADOR_INVALIDO"],
                metadata={"motivo": "Falha na validação do módulo 11."}
            )
            
        region_digit = self.clean_cpf[8]
        origin = self.FISCAL_REGIONS.get(region_digit, "Desconhecido")
        
        if self.clean_cpf.startswith("00"):
            flags.append("PREFIXO_ZEROS_INICIAIS")
            risk_score += 15
            
        return ValidationResult(
            cpf_masked=self._mask_cpf(),
            is_valid=True,
            origen_state=origin,
            risk_score=risk_score,
            risk_flags=flags if flags else ["NENHUM_RISCO_DETECTADO"],
            metadata={
                "regiao_fiscal_digito": region_digit,
                "status_lgpd": "Mascara aplicada para conformidade"
            }
        )