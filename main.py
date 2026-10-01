"""
Ponto de Entrada Principal (Orquestrador) do Pipeline de Logística.
"""

from pathlib import Path
from pipeline_logistica.exceptions import PipelineError, ValidationError
from pipeline_logistica.ingestao.leitor import read_raw_csv
from pipeline_logistica.transformacao.validadores import process_and_validate_record
from pipeline_logistica.armazenamento.escritor import write_processed_data, write_quarantine_data

# Mapeamento estático de caminhos no sistema operacional
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

RAW_FILE = DATA_DIR / "raw" / "deliveries_raw.csv"
PROCESSED_FILE = DATA_DIR / "processed" / "deliveries_processed.csv"
QUARANTINE_FILE = DATA_DIR / "quarantine" / "deliveries_quarantine.csv"


def run_pipeline() -> None:
    print("=== INICIANDO PIPELINE DE LOGÍSTICA ===")

    # 1. Fase de Ingestão
    print("\n[1/3] Lendo arquivo bruto...")
    try:
        raw_data = read_raw_csv(RAW_FILE)
        print(f"[OK] Ingestão concluída. Total de registros lidos: {len(raw_data)}")
    except PipelineError as exc:
        print(f"[FALHA CRÍTICA] {exc}")
        return

    # 2. Fase de Transformação e Validação
    processed_records = []
    quarantine_records = []

    print("\n[2/3] Processando e validando registros...")
    for index, record in enumerate(raw_data, start=2):
        try:
            valid_record = process_and_validate_record(record, line_number=index)
            processed_records.append(valid_record)
        except ValidationError as val_err:
            quarantine_records.append({
                "line_number": val_err.line_number,
                "field_name": val_err.field_name,
                "error_message": val_err.message,
                "raw_record": record,
            })

    print(f"[OK] Registros Válidos: {len(processed_records)}")
    print(f"[OK] Registros em Quarentena: {len(quarantine_records)}")

    # 3. Fase de Armazenamento
    print("\n[3/3] Gravando arquivos de saída...")
    try:
        write_processed_data(PROCESSED_FILE, processed_records)
        print(f"[OK] Dados válidos salvos em: {PROCESSED_FILE.relative_to(BASE_DIR)}")

        write_quarantine_data(QUARANTINE_FILE, quarantine_records)
        print(f"[OK] Relatório de quarentena salvo em: {QUARANTINE_FILE.relative_to(BASE_DIR)}")

    except PipelineError as exc:
        print(f"[FALHA DE ESCRITA] {exc}")
        return

    print("\n=== PIPELINE EXECUTADO COM SUCESSO ===")


if __name__ == "__main__":
    run_pipeline()