flowchart LR
    %% ===== 스타일 정의 =====
    classDef node fill:#f9f9f9,stroke:#333,stroke-width:1px,rx:8px,ry:8px
    classDef meta fill:#d9f7ff,stroke:#007acc,stroke-width:1px,rx:8px,ry:8px
    classDef tool fill:#fff7d9,stroke:#b59f00,stroke-width:1px,rx:8px,ry:8px
    classDef group fill:#f2f2f2,stroke:#aaa,stroke-width:1px,rx:10px,ry:10px

    %% ===== 노드 정의 =====
    subgraph G1["📤 Channel 단계"]
        channel["channel\n📥 input_value"]:::node
        metaExtract["meta 추출기\n(input_value 중 일부를 meta 로 분리)"]:::meta
        channel --> metaExtract
    end

    subgraph G2["📦 BA 단계"]
        BA["BA\n📥 input_value + meta 수신"]:::node
    end

    subgraph G3["🧠 commonAgent 단계"]
        commonAgent["commonAgent\n📥 input_value + meta 수신"]:::node
        toolSelect["tool 선택 로직\n(meta 값 활용 가능)"]:::meta
        commonAgent --> toolSelect
    end

    subgraph G4["🧩 Tool 단계"]
        toolA["tool A\n(meta 중 필요한 값만 사용)"]:::tool
        toolB["tool B\n(meta 중 필요한 값만 사용)"]:::tool
    end

    %% ===== 흐름 연결 =====
    metaExtract -->|meta| BA
    channel -->|input_value| BA
    BA -->|input_value + meta| commonAgent
    toolSelect --> toolA
    toolSelect --> toolB

    %% ===== 설명 =====
    note right of toolB
        commonAgent는 여러 tool 중 하나를 선택하여 호출합니다.\n
        각 tool은 meta 항목 중 필요한 값만 전달받습니다.\n
        tool 선택과 호출은 반복적으로 수행될 수 있습니다.
    end note
