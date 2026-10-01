from pipeline_logistica.exceptions import ValidationError
from pipeline_logistica.transformacao.limpadores import clean_numeric_string, sanitize_string


def validate_document(raw_doc: str, line_number: int) -> str:
    """
    Valida e higieniza documentos (CPF/CNPJ).
    Regra: Deve conter apenas números e ter tamanho igual a 11 (CPF) ou 14 (CNPJ).
    """
    doc_digits = clean_numeric_string(raw_doc)

    if len(doc_digits) not in (11, 14):
        raise ValidationError(
            message=f"Documento com tamanho inválido ({len(doc_digits)} dígitos). Esperado 11 ou 14.",
            line_number=line_number,
            field_name="document",
        )

    return doc_digits


def validate_zip_code(raw_zip: str, line_number: int) -> str:
    """
    Valida e sanitiza o CEP.
    Regra: Deve conter exatamente 8 dígitos numéricos.
    """
    zip_digits = clean_numeric_string(raw_zip)

    if len(zip_digits) != 8:
        raise ValidationError(
            message=f"CEP inválido ({raw_zip}). Esperado exatamente 8 dígitos numéricos.",
            line_number=line_number,
            field_name="zip_code",
        )

    return zip_digits


def validate_freight_value(raw_freight: str, line_number: int) -> float:
    """
    Valida e converte o valor do frete.
    Regra: Deve ser um número flutuante positivo (> 0).
    """
    try:
        cleaned_str = sanitize_string(raw_freight)
        freight_value = float(cleaned_str)
    except (ValueError, TypeError):
        raise ValidationError(
            message=f"Valor de frete não-numérico recebido: '{raw_freight}'.",
            line_number=line_number,
            field_name="freight_value",
        )

    if freight_value <= 0:
        raise ValidationError(
            message=f"Valor de frete deve ser maior que zero. Recebido: {freight_value}.",
            line_number=line_number,
            field_name="freight_value",
        )

    return freight_value


def process_and_validate_record(record: dict, line_number: int) -> dict:
    """
    Orquestra a sanitização e validação completa de um único registro.
    Retorna o dicionário com os campos transformados e validados.
    """
    processed_record = {
        "delivery_id": sanitize_string(record.get("delivery_id", "")),
        "document": validate_document(record.get("document", ""), line_number),
        "zip_code": validate_zip_code(record.get("zip_code", ""), line_number),
        "freight_value": validate_freight_value(record.get("freight_value", ""), line_number),
        "status": sanitize_string(record.get("status", "")),
    }

    return processed_record