"""
Testes unitários para as regras de validação de domínio (validadores.py).
"""

import pytest
from pipeline_logistica.exceptions import ValidationError
from pipeline_logistica.transformacao.validadores import (
    validate_document,
    validate_freight_value,
    validate_zip_code,
)


def test_validate_document_success() -> None:
    """Valida formato correto de CPF (11 dígitos)."""
    assert validate_document("123.456.789-01", line_number=2) == "12345678901"


def test_validate_document_invalid_length() -> None:
    """Valida se documento com tamanho incorreto dispara ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validate_document("12345", line_number=3)

    assert exc_info.value.field_name == "document"
    assert exc_info.value.line_number == 3


def test_validate_freight_value_negative() -> None:
    """Valida se valor de frete negativo dispara ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validate_freight_value("-50.00", line_number=4)

    assert exc_info.value.field_name == "freight_value"
    assert "maior que zero" in exc_info.value.message


def test_validate_freight_value_non_numeric() -> None:
    """Valida se texto em campo numérico dispara ValidationError."""
    with pytest.raises(ValidationError):
        validate_freight_value("INVALID_VALUE", line_number=5)


def test_validate_zip_code_with_letters() -> None:
    """Garante que CEP contendo letras é rejeitado com ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        validate_zip_code("01001A00", line_number=8)

    assert exc_info.value.field_name == "zip_code"
    assert "8 dígitos numéricos" in exc_info.value.message