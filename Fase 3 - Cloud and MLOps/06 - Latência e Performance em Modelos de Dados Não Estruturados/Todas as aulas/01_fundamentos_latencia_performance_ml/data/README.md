# Datasets — Aula 01: Fundamentos de Latência e Performance em ML

## Caso de Uso: Detecção de Fraude Bancária em Tempo Real

Toda a aula gira em torno de um **único cenário aplicado**: um sistema antifraude
que analisa cada transação de cartão no momento em que ela acontece. Se uma
transação fraudulenta demora a ser sinalizada (latência alta), o banco perde
dinheiro — o débito já foi efetivado — e perde credibilidade junto ao cliente.
O objetivo do produto é simples: **reduzir a latência da decisão a praticamente
zero do ponto de vista do usuário**, mantendo qualidade adequada de detecção.

## Dataset Principal

### Descrição

Dataset **sintético** de transações bancárias gerado com
`sklearn.datasets.make_classification` e renomeado com termos do domínio
antifraude (Bahnsen et al., 2016; Carcillo et al., 2018). Cada linha é uma
transação; a coluna `target` indica se a transação é fraude (1) ou legítima (0).

### Estrutura

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| tx_amount_z | float | Valor da transação normalizado (z-score) |
| amount_to_avg_ratio | float | Razão entre o valor atual e a média do cliente |
| hour_sin | float | Hora do dia codificada (componente seno) |
| hour_cos | float | Hora do dia codificada (componente cosseno) |
| time_since_last_tx_s | float | Segundos desde a última transação do cartão |
| distance_from_home_km | float | Distância geográfica do endereço cadastrado |
| distance_from_last_tx_km | float | Distância da transação imediatamente anterior |
| merchant_risk_score | float | Score de risco do estabelecimento |
| mcc_risk_score | float | Score de risco da categoria do comércio (MCC) |
| velocity_1h | float | Nº de transações na última hora (informativa) |
| velocity_24h | float | Nº de transações nas últimas 24h (redundante) |
| avg_amount_30d | float | Ticket médio nos últimos 30 dias (redundante) |
| card_age_days | float | Tempo de uso do cartão (ruído) |
| cross_border_score | float | Indicador de operação internacional (ruído) |
| device_anomaly_score | float | Anomalia do dispositivo/IP usado (ruído) |
| target | int | **0 = legítima, 1 = fraude** |

### Estatísticas

- **Transações:** 10.000
- **Features:** 15 numéricas (10 informativas, 2 redundantes, 3 ruidosas)
- **Classes:** 2 — desbalanceadas (~95% legítimas, ~5% fraudes)
- **Missing values:** Nenhum
- **Seed de reprodução:** 42

### Reprodução

```bash
python -c "from src.data_preprocessing import DataPreprocessor; DataPreprocessor.generate_synthetic_dataset('data/raw/dataset.csv')"
```

### Propósito Pedagógico

O dataset foi projetado especificamente para o caso de uso de fraude:

1. **15 features** — mistura de sinais informativos, redundantes e ruidosos,
   típica de pipelines antifraude reais.
2. **10K transações** — volume suficiente para medir P95/P99 de latência
   sem inflar o tempo de execução das aulas.
3. **Desbalanceamento ~5%** — reflete a natureza rara da fraude e força o
   aluno a olhar para precision/recall, não apenas accuracy.
4. **Foco em latência** — todas as etapas (I/O, normalização, inferência,
   batching) são cronometradas porque, neste cenário, **cada milissegundo
   adicional é dinheiro que escapa**.
