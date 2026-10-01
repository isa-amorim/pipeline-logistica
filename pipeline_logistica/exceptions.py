"""
Módulo de Exceções Customizadas do Pipeline de Logística.
Define a hierarquia de erros para garantir rastreabilidade na quarentena.
"""


class PipelineError(Exception):
    """Exceção base para todas as falhas mapeadas do pipeline."""

    pass


class ValidationError(PipelineError):
    """Disparada quando um registro falha nas regras de sanitização ou validação."""

    def __init__(self, message: str, line_number: int, field_name: str) -> None:
        self.message = message
        self.line_number = line_number
        self.field_name = field_name

        # Constrói mensagem detalhada para rastreamento no relatório de quarentena
        full_message = (
            f"[Linha {self.line_number}] Falha no campo '{self.field_name}': "
            f"{self.message}"
        )

        super().__init__(full_message)