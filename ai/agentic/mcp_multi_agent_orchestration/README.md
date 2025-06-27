# Multi-Agent Orchestration Using MCP
This example implements a **central orchestrator** (the `ChatBot`) that treats each MCP server as a *tool* or *sub-agent*, dynamically invoking their capabilities (tools, prompts, resources) to fulfill user queries. This pattern of multi-agent orchestration are commonly refer to as **agent-as-tool**, and is different from the **hand-off** pattern where peer agents hand off control among themselves. In here, the orchestrator retains full control, querying sub-agents in parallel (or as needed), and then synthesizing their outputs into a coherent response.

**Orchestrator Agent (`ChatBot`)**
  - Uses the `AnthropicBedrock` LLM to drive dialogue and decide when to call tools.
  - Collects all available tools, prompts, and resources via its `MCPClient`.
  - In `process_query()`, it sends conversation history + user query to the LLM, reads any tool-use actions, invokes those tools through the client, feeds back tool results.

**Domain-Specific Sub-Agents (MCP Servers)**

  - **Order Server (`order_mcp_server.py`)**
    - Exposes shipping info as a resource, an `order_instructions` prompt, and a `place_order` tool to simulate order placement.
    - Encapsulates all order-management logic behind a simple API surface.

  - **Product Server (`product_mcp_server.py`)**
    - Provides resources for categories and individual product listings, a `product_instructions` prompt, and a `search_products` tool for inventory queries.
    - Contains all product-catalog logic and stock data.
