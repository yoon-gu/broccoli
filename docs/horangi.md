# Horangi 한국어 LLM 벤치마크

호랑이 LLM 리더보드는 거대언어모델(LLM)의 한국어 능력을 평가하기 위한 도구로써 또 다른 대안을 제시합니다. 우리는 두 가지 방법을 통해 한국어에 대한 종합적인 평가를 수행하고자 합니다.
Q&A 형식의 언어이해 llm-kr-eval: 일본어 버전인 llm-jp-eval 기반에서 한국어 버전으로 개발되었습니다.
Multi-turn 대화를 통해 생성 능력을 평가하는 MT-Bench

호랑이 LLM 리더보드는 Weight & Biases (W&B)의 테이블 기능을 활용하여 평가 결과를 다양한 시각에서 쉽게 분석할 수 있도록 합니다. 이 기능을 활용하면 각 모델 별 비교를 손쉽게 수행할 수 있으며, 기존 실험들을 추적하고 기록할 수 있습니다.
이 문서는 호랑이 LLM 리더보드의 평가 결과와, 평가 방법론, 각 평가 query에 대한 세부 분석을 제공하며, 이를 통해 사용자에게 최신 LLM에 대한 이해도를 높일 수 있도록 하고자 합니다.

## Radar Plots

```plotly
--8<-- "./assets/horangi_radar.json"
```

## Benchmarks

=== "AVG"

    {{ read_csv('assets/horangi_benchmark_avg.csv') }}

=== "Abilities"

    {{ read_csv('assets/horangi_benchmark_3.csv') }}

=== "EL,FA,NLI,QA,RC"

    {{ read_csv('assets/horangi_benchmark_2.csv') }}

=== "ALL"

    {{ read_csv('assets/horangi_benchmark.csv') }}
