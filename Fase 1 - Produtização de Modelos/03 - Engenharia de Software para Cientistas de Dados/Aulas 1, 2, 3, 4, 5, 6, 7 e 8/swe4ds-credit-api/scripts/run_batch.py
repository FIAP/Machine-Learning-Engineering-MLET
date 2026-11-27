"""Script para processamento em batch."""

import json
from pathlib import Path

from src.services.model_service import predict_one


def process_batch(input_file: Path, output_file: Path) -> None:
    """
    Processa um arquivo batch de requisições.
    
    Args:
        input_file: Caminho para arquivo de entrada (JSON lines)
        output_file: Caminho para arquivo de saída (JSON lines)
    """
    print(f"Processing batch from: {input_file}")
    
    processed = 0
    approved = 0
    rejected = 0
    
    with input_file.open("r", encoding="utf-8") as fin:
        with output_file.open("w", encoding="utf-8") as fout:
            for line in fin:
                data = json.loads(line)
                result = predict_one(data)
                
                # Adiciona resultado ao registro original
                data["prediction"] = result["prediction"]
                data["confidence"] = result["confidence"]
                
                fout.write(json.dumps(data) + "\n")
                
                processed += 1
                if result["prediction"] == "approved":
                    approved += 1
                else:
                    rejected += 1
    
    print(f"\nBatch processing completed!")
    print(f"Total processed: {processed}")
    print(f"Approved: {approved} ({approved/processed*100:.1f}%)")
    print(f"Rejected: {rejected} ({rejected/processed*100:.1f}%)")
    print(f"\nOutput saved to: {output_file}")


def create_sample_input(output_file: Path) -> None:
    """
    Cria arquivo de exemplo para processamento batch.
    
    Args:
        output_file: Caminho para salvar o arquivo
    """
    samples = [
        {"age": 30, "income": 5000, "loan_amount": 10000, "credit_history": "good"},
        {"age": 25, "income": 3000, "loan_amount": 15000, "credit_history": "fair"},
        {"age": 45, "income": 8000, "loan_amount": 5000, "credit_history": "good"},
        {"age": 22, "income": 2000, "loan_amount": 20000, "credit_history": "poor"},
        {"age": 35, "income": 6000, "loan_amount": 8000, "credit_history": "good"},
    ]
    
    with output_file.open("w", encoding="utf-8") as f:
        for sample in samples:
            f.write(json.dumps(sample) + "\n")
    
    print(f"Sample input created: {output_file}")


if __name__ == "__main__":
    # Criar diretório de dados se não existir
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Criar arquivo de exemplo
    input_path = data_dir / "batch_input.jsonl"
    create_sample_input(input_path)
    
    # Processar batch
    output_path = data_dir / "batch_output.jsonl"
    process_batch(input_path, output_path)
