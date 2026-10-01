"""
Testes unitários para as funções de sanitização de dados (limpadores.py).
"""

import pytest
from pipeline_logistica.transformacao.limpadores import clean_numeric_string, sanitize_string


def test_sanitize_string_success() -> None:
    """Garante que espaços nas extremidades são removidos e a string vira caixa alta."""
    raw_input = "  dados_entrega  "
    expected = "DADOS_ENTREGA"
    assert sanitize_string(raw_input) == expected


def test_sanitize_string_invalid_type() -> None:
    """Garante que passar um valor não-string dispara TypeError."""
    with pytest.raises(TypeError):
        sanitize_string(12345)  # type: ignore


def test_clean_numeric_string_success() -> None:
    """Garante que apenas os caracteres numéricos são mantidos."""
    raw_zip = " 01.001-000 "
    expected = "01001000"
    assert clean_numeric_string(raw_zip) == expected