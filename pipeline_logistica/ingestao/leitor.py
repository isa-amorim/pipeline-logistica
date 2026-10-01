import csv
from pathlib import Path
from typing import Dict, List
from pipeline_logistica.exceptions import PipelineError


def read_raw_csv(file_path: Path) -> List[Dict[str, str]]:
    """
    Lê um arquivo CSV bruto e retorna uma lista de dicionários.
    Cada linha do CSV se torna um dicionário onde a chave é o cabeçalho.
    """
    if not file_path.exists():
        raise PipelineError(f"Arquivo não encontrado no caminho: {file_path}")

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            
            if not data:
                raise PipelineError("O arquivo CSV está vazio ou sem dados validos.")
                
            return data

    except PermissionError:
        raise PipelineError(f"Sem permissão de leitura para o arquivo: {file_path}")
    except Exception as exc:
        raise PipelineError(f"Erro inesperado ao ler o arquivo CSV: {str(exc)}")