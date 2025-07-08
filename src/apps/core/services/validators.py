import re
from validate_docbr import CPF, CNPJ
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class ValidatorService:
    """
    Classe de serviço para validação de dados.
    Fornece métodos estáticos para validar dados comuns como CPF, CNPJ, e-mails, CEPs e telefones.
    """
    _cpf_validator = CPF()
    _cnpj_validator = CNPJ()

    @staticmethod
    def _clean_doc_number(doc: str) -> str:
        """Método auxiliar para remover formatação de documentos."""
        if not isinstance(doc, str):
            return ""
        return doc.replace('.', '').replace('-', '').replace('/', '')

    @classmethod
    def is_valid_cpf(cls, cpf: str) -> bool:
        """
        Valida um CPF usando a biblioteca validate_docbr.
        Aceita CPF com ou sem formatação.
        """
        # A biblioteca lida com a formatação
        return cls._cpf_validator.validate(cpf)

    @classmethod
    def is_valid_cnpj(cls, cnpj: str) -> bool:
        """
        Valida um CNPJ usando a biblioteca validate_docbr.
        Aceita CNPJ com ou sem formatação.
        """
        return cls._cnpj_validator.validate(cnpj)

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Valida um e-mail usando o validador robusto do Django.
        """
        if not email:
            return False
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    @staticmethod
    def is_valid_phone(phone: str) -> bool:
        """
        Valida se o número de telefone contém 10 ou 11 dígitos numéricos.
        Remove formatações como '()', '-', e espaços antes de validar.
        """
        if not phone:
            return False
            
        # 1. Limpa a string de todos os caracteres não numéricos
        cleaned_phone = re.sub(r'\D', '', phone)

        # 2. Verifica se o resultado tem 10 (fixo) ou 11 (móvel) dígitos
        return len(cleaned_phone) in (10, 11)

    @staticmethod
    def is_valid_cep(cep: str) -> bool:
        """
        Valida se o CEP contém 8 dígitos numéricos.
        Remove a formatação antes de validar.
        """
        if not cep:
            return False
        
        # 1. Limpa a string de todos os caracteres não numéricos
        cleaned_cep = re.sub(r'\D', '', cep)
        
        # 2. Verifica se o resultado tem exatamente 8 dígitos
        return len(cleaned_cep) == 8
    