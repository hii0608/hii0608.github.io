# 안녕하세요, hii0608 입니다 👋

- 🔬 **그래프 기반 머신러닝**(장면 그래프·서브그래프 학습)으로 이미지 검색을 연구했습니다.
- ⚙️ **MLOps 파이프라인**(Airflow·MLflow·Docker)으로 모델의 학습–추적–서빙을 다룹니다.
- 🤖 센싱·로보틱스부터 시계열 예측까지, 데이터가 흐르는 문제를 좋아합니다.

```mermaid
flowchart TD
    ME([hii0608])

    ME --> GML[그래프 머신러닝]
    ME --> OPS[MLOps]
    ME --> ROB[로보틱스·센싱]

    GML --> P1[CBIR-SubSG · 장면 그래프 이미지 검색]
    GML --> P2[서브그래프 기반 표현 학습]
    OPS --> P3[실시간 객체 검출·재학습 파이프라인]
    OPS --> P4[자전거 수요 예측 · MLflow]
    ROB --> P5[2D LiDAR 매핑]

    classDef hub fill:#6366f1,stroke:#4f46e5,color:#fff;
    classDef proj fill:#eef0f7,stroke:#c9cee0,color:#1b1f2a;
    class GML,OPS,ROB hub;
    class P1,P2,P3,P4,P5 proj;
```

🔗 **인터랙티브 포트폴리오:** <https://hii0608.github.io>
