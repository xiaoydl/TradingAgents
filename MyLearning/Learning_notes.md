# Embeddings and LLM Models Configuration
## Embeddings
- Using Google's PaLM Embeddings via langchain-google-genai
- RAG Vector Store: ChromaDB
  - In-memory storage only, no persistence, Only while the application is running
- Collections: 5 separate memory stores:
    - bull_memory - Bullish scenarios
    - bear_memory - Bearish scenarios
    - trader_memory - Trading decisions
    - invest_judge_memory - Investment judgments
    - risk_manager_memory - Risk management
- Stock Data Cache added in: `tradingagents/dataflows/data_cache/NVDA-YFin-data-2010-11-22-2025-11-22.csv`


## LLM Models
- Deep Thinking: gemini-2.5-pro
- Quick Thinking: gemini-2.5-flash