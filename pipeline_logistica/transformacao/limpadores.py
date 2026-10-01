def sanitize_string(raw_text: str) -> str:
    """
    Remove espaços extras nas extremidades e converte o texto para caixa alta.
    Se o valor não for uma string, dispara TypeError.
    """
    if not isinstance(raw_text, str):
        raise TypeError(f"Esperado tipo 'str', recebido '{type(raw_text).__name__}'")

    cleaned = raw_text.strip().upper()
    return cleaned


def clean_numeric_string(raw_text: str) -> str:
    """
    Remove caracteres não numéricos (espaços, traços, pontos) mantendo apenas dígitos.
    Exemplo: ' 12.345-678 ' -> '12345678'
    """
    cleaned = sanitize_string(raw_text)
    return "".join(char for char in cleaned if char.isdigit())