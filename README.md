# Agentic System For Trading

## [Context Diagram](./docs/context-diagram.mmd)

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Segoe UI, Roboto, Arial, sans-serif", "fontSize": "22px", "textColor": "#0f172a", "lineColor": "#475569", "edgeLabelBackground": "#ffffff", "primaryTextColor": "#0f172a"}, "flowchart": {"curve": "basis", "nodeSpacing": 40, "rankSpacing": 130, "padding": 30, "htmlLabels": false}}}%%
flowchart LR
    subgraph canvas [" "]
        direction LR
        user(["User"])
        system["Crypto analyst agent (answers market questions, produces validated signals)"]
        llm["LLM API (Claude)"]
        emb["Embeddings API (Gemini or OpenAI)"]
        news["News sources (RSS)"]
        market["Market data APIs (Binance, CoinGecko)"]
        exchange["Exchange (Binance testnet)"]

        user -->|"Asks questions, confirms signals · HTTPS"| system
        system -->|"Sends prompts to · HTTPS"| llm
        system -->|"Embeds text via · HTTPS"| emb
        system -->|"Fetches articles from · HTTPS"| news
        system -->|"Requests prices from · HTTPS"| market
        system -->|"Places paper orders on · HTTPS"| exchange
    end

    classDef person fill:#0b3d6f,stroke:#082a4d,color:#ffffff,stroke-width:2px
    classDef ours fill:#1f7ae0,stroke:#145ab0,color:#ffffff,stroke-width:2px
    classDef external fill:#8b949e,stroke:#5b636b,color:#ffffff,stroke-width:2px
    class user person
    class system ours
    class llm,emb,news,market,exchange external
    style canvas fill:#ffffff,stroke:#ffffff
```

## [Container Diagram](./docs/container-diagram.mmd)

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Segoe UI, Roboto, Arial, sans-serif", "fontSize": "22px", "textColor": "#0f172a", "lineColor": "#475569", "edgeLabelBackground": "#ffffff", "primaryTextColor": "#0f172a"}, "flowchart": {"curve": "basis", "nodeSpacing": 40, "rankSpacing": 110, "padding": 30, "htmlLabels": false}}}%%
flowchart LR
    subgraph canvas [" "]
        direction LR
        user(["User"])
        agents["Agent service (Python, FastAPI)"]
        ingest["Data pipeline (Python job)"]
        llm["LLM API (Claude)"]
        embA["Embeddings API (Gemini or OpenAI)"]
        db[("Database (Postgres + pgvector)")]
        embI["Embeddings API (Gemini or OpenAI)"]
        news["News sources (RSS)"]
        exchange["Market APIs (Binance, CoinGecko)"]

        user -->|"Asks questions · HTTPS"| agents
        agents -->|"Sends prompts to · HTTPS"| llm
        agents -->|"Embeds queries via · HTTPS"| embA
        agents -->|"Reads and writes · SQL"| db
        ingest -->|"Writes data to · SQL"| db
        ingest -->|"Embeds news via · HTTPS"| embI
        ingest -->|"Fetches articles from · HTTPS"| news
        ingest -->|"Requests prices from · HTTPS"| exchange
    end

    classDef person fill:#0b3d6f,stroke:#082a4d,color:#ffffff,stroke-width:2px
    classDef container fill:#1f7ae0,stroke:#145ab0,color:#ffffff,stroke-width:2px
    classDef external fill:#8b949e,stroke:#5b636b,color:#ffffff,stroke-width:2px
    class user person
    class agents,ingest,db container
    class llm,embA,embI,news,exchange external
    style canvas fill:#ffffff,stroke:#ffffff
```

## [Component Diagram (Agent Service)](./docs/component-diagram.mmd)

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Segoe UI, Roboto, Arial, sans-serif", "fontSize": "20px", "textColor": "#0f172a", "lineColor": "#475569", "edgeLabelBackground": "#ffffff", "primaryTextColor": "#0f172a"}, "flowchart": {"curve": "basis", "nodeSpacing": 35, "rankSpacing": 100, "padding": 30, "htmlLabels": false}}}%%
flowchart LR
    subgraph canvas [" "]
        direction LR
        routes["HTTP routes (FastAPI)"]
        orch["Orchestrator (analyst-validator loop)"]
        exec["Execution service"]
        analyst["Analyst agent"]
        validator["Validator agent"]
        risk["Risk engine (plain code)"]
        pLLM["LLMClient (interface)"]
        pStore["VectorStore (interface)"]
        pRepo["Repository (interface)"]
        pBroker["Broker (interface)"]
        pRule["RiskRule (interface)"]
        claude["ClaudeClient (Anthropic SDK)"]
        pgv["PgVectorStore (pgvector, SQL)"]
        pgrepo["PostgresRepository (SQL)"]
        paper["PaperBroker (ccxt, testnet)"]
        rules["Risk rules (position size, drawdown, kill switch)"]

        routes -->|"Runs question"| orch
        routes -->|"Confirms signal"| exec
        orch -->|"Delegates draft to"| analyst
        orch -->|"Sends draft to"| validator
        orch -->|"Loads and saves history via"| pRepo
        analyst -->|"Calls model via"| pLLM
        analyst -->|"Searches news via"| pStore
        analyst -->|"Reads prices via"| pRepo
        validator -->|"Calls model via"| pLLM
        validator -->|"Checks sources via"| pRepo
        exec -->|"Checks order with"| risk
        exec -->|"Places order via"| pBroker
        exec -->|"Saves order via"| pRepo
        risk -->|"Applies rules via"| pRule
        pLLM -.->|"implemented by"| claude
        pStore -.->|"implemented by"| pgv
        pRepo -.->|"implemented by"| pgrepo
        pBroker -.->|"implemented by"| paper
        pRule -.->|"implemented by"| rules
    end

    classDef api fill:#0b3d6f,stroke:#082a4d,color:#ffffff,stroke-width:2px
    classDef core fill:#1f7ae0,stroke:#145ab0,color:#ffffff,stroke-width:2px
    classDef port fill:#ffffff,stroke:#1f7ae0,color:#0f172a,stroke-width:2px,stroke-dasharray:6 4
    classDef adapter fill:#0f766e,stroke:#0b5a54,color:#ffffff,stroke-width:2px
    class routes api
    class orch,exec,analyst,validator,risk core
    class pLLM,pStore,pRepo,pBroker,pRule port
    class claude,pgv,pgrepo,paper,rules adapter
    style canvas fill:#ffffff,stroke:#ffffff
```

## [Sequence Diagram](./docs/sequence-diagram.mmd)

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Segoe UI, Roboto, Arial, sans-serif", "fontSize": "16px", "textColor": "#0f172a", "lineColor": "#475569", "primaryTextColor": "#0f172a", "primaryColor": "#dbeafe", "primaryBorderColor": "#1f7ae0", "noteBkgColor": "#fef9c3", "noteTextColor": "#0f172a", "actorBkg": "#dbeafe", "actorBorder": "#1f7ae0", "actorTextColor": "#0f172a", "signalColor": "#475569", "signalTextColor": "#0f172a"}, "sequence": {"mirrorActors": false, "messageMargin": 40, "boxMargin": 10, "width": 170}}}%%
sequenceDiagram
    autonumber
    actor U as User (web client)
    participant API as Agent service (FastAPI)
    participant AN as Analyst agent (Python + Claude)
    participant EM as Embeddings API
    participant DB as Postgres + pgvector
    participant VA as Validator agent (Python + Claude)
    participant BR as Broker (Python, ccxt)
    participant EX as Exchange (Binance testnet)

    U->>API: POST /sessions/{id}/messages (HTTPS, JSON)
    API->>DB: Load session history (SQL)
    DB-->>API: Previous messages
    API->>AN: Question + history
    AN->>EM: Embed the question
    EM-->>AN: Query vector
    AN->>DB: Vector search + price query (SQL)
    DB-->>AN: News chunks and candles
    AN-->>API: Draft answer with sources

    loop Up to 3 rounds, until approved
        API->>VA: Draft answer + cited sources
        VA-->>API: Verdict (approved or remarks)
        opt Remarks
            API->>AN: Fix these issues
            AN-->>API: Revised answer
        end
    end

    Note over API: After 3 failed rounds the answer is returned with an unverified flag
    API->>DB: Save run, signal, verdict, messages (SQL)
    API-->>U: Answer with sources

    opt User confirms an approved signal
        U->>API: POST /signals/{id}/confirm
        API->>BR: Execute signal
        BR->>BR: Check risk rules (plain code, no LLM)
        BR->>EX: Place order (paper trading)
        EX-->>BR: Order status
        BR->>DB: Save order and audit record (SQL)
        BR-->>API: Result
        API-->>U: Order status
    end
```

## [Entity Relationship Diagram](./docs/er-diagram.mmd)

```mermaid
%%{init: {"theme": "base", "themeVariables": {"fontFamily": "Inter, Segoe UI, Roboto, Arial, sans-serif", "fontSize": "16px", "textColor": "#0f172a", "lineColor": "#475569", "primaryColor": "#dbeafe", "primaryTextColor": "#0f172a", "primaryBorderColor": "#1f7ae0", "secondaryColor": "#f1f5f9", "tertiaryColor": "#ffffff", "edgeLabelBackground": "#ffffff"}}}%%
erDiagram
    ASSET ||--o{ JOB : "requested for"
    ASSET ||--o{ MARKET_SNAPSHOT : "has"
    ASSET ||--o{ NEWS_DOC_ASSET : "mentioned in"
    ASSET ||--o{ SIGNAL : "subject of"
    JOB ||--o| MARKET_SNAPSHOT : "produces"
    JOB ||--o{ NEWS_DOC : "produces"
    NEWS_DOC ||--|{ NEWS_CHUNK : "split into"
    NEWS_DOC ||--o{ NEWS_DOC_ASSET : "mentions"
    SESSION ||--o{ MESSAGE : "contains"
    SESSION ||--o{ AGENT_RUN : "has"
    AGENT_RUN ||--o{ MESSAGE : "answers with"
    AGENT_RUN ||--o{ VALIDATION : "checked by"
    AGENT_RUN ||--o{ SIGNAL : "produces"
    SIGNAL ||--o{ SIGNAL_SOURCE : "cites"
    NEWS_CHUNK ||--o{ SIGNAL_SOURCE : "cited by"
    SIGNAL |o--o| SIGNAL : "supersedes"
    SIGNAL ||--o{ TRADE_ORDER : "executed as"

    ASSET {
        int id PK
        string ticker
        string name
    }
    JOB {
        int id PK
        int asset_id FK
        string job_type
        string source
        jsonb params
        string status
        int attempts
        int max_attempts
        datetime next_retry_at
        datetime created_at
        datetime started_at
        datetime finished_at
        string error
    }
    MARKET_SNAPSHOT {
        int id PK
        int asset_id FK
        int job_id FK
        string source
        datetime captured_at
        decimal bid
        decimal ask
        decimal low_24h
        decimal high_24h
        decimal volume_24h
        decimal change_pct_24h
    }
    NEWS_DOC {
        int id PK
        int job_id FK
        string source
        string url
        string title
        datetime published_at
        text body
        string content_hash
        jsonb extra
    }
    NEWS_DOC_ASSET {
        int doc_id FK
        int asset_id FK
    }
    NEWS_CHUNK {
        int id PK
        int doc_id FK
        int position
        text text
        vector embedding
    }
    SESSION {
        int id PK
        datetime created_at
        datetime last_active_at
    }
    MESSAGE {
        int id PK
        int session_id FK
        int run_id FK
        string role
        text content
        datetime created_at
    }
    AGENT_RUN {
        int id PK
        int session_id FK
        string question
        text answer
        string status
        int rounds
        string model
        string prompt_version
        int tokens_in
        int tokens_out
        decimal cost_usd
        int latency_ms
        datetime created_at
    }
    VALIDATION {
        int id PK
        int run_id FK
        int round_no
        string verdict
        text remarks
        string model
        datetime created_at
    }
    SIGNAL {
        int id PK
        int run_id FK
        int asset_id FK
        int supersedes_id FK
        string action
        decimal confidence
        text reason
        string status
        datetime confirmed_at
        datetime created_at
    }
    SIGNAL_SOURCE {
        int signal_id FK
        int chunk_id FK
    }
    TRADE_ORDER {
        int id PK
        int signal_id FK
        string exchange
        string mode
        string side
        decimal quantity
        string status
        boolean risk_passed
        jsonb risk_details
        string exchange_order_id
        datetime created_at
        datetime filled_at
    }
```