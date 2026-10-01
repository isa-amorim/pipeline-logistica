"""
Módulo de Persistência do Pipeline de Logística.
Gerencia a gravação física dos dados processados e da quarentena em disco.
"""

import csv
from pathlib import Path
from typing import Any, Dict, List
from pipeline_logistica.exceptions import PipelineError


def write_processed_data(file_path: Path, records: List[Dict[str, Any]]) -> None:
    """
    Grava os registros validados no diretório de destino (processed).
    """
    if not records:
        print("[Aviso] Nenhum registro válido para gravar em processed.")
        return

    try:
        # Extrai os cabeçalhos diretamente das chaves do primeiro dicionário
        fieldnames = list(records[0].keys())

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)

    except PermissionError:
        raise PipelineError(f"Sem permissão de escrita no arquivo: {file_path}")
    except Exception as exc:
        raise PipelineError(f"Falha ao gravar dados processados: {str(exc)}")


def write_quarantine_data(file_path: Path, records: List[Dict[str, Any]]) -> None:
    """
    Grava os registros rejeitados no diretório de quarentena com metadados do erro.
    """
    if not records:
        print("[Aviso] Nenhum registro em quarentena para gravar.")
        return

    try:
        # Define estrutura plana para o relatório de quarentena
        fieldnames = ["line_number", "field_name", "error_message", "raw_record"]

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # Achata o dicionário para gravação limpa no CSV
            for item in records:
                writer.writerow({
                    "line_number": item["line_number"],
                    "field_name": item["field_name"],
                    "error_message": item["error_message"],
                    "raw_record": str(item["raw_record"]),  # Converte dict original para string
                })

    except PermissionError:
        raise PipelineError(f"Sem permissão de escrita no arquivo de quarentena: {file_path}")
    except Exception as exc:
        raise PipelineError(f"Falha ao gravar dados de quarentena: {str(exc)}")