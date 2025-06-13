# Agentic Chatbot Using MCP
This example simulates a simple Chatbot using MCP (Model Context Protocol) for an online shoe retailer. This chatbot provides a natural language interface to the shoppers to ask questions about products, check availability, etc.

This example has the following components:
- `mcp_chatbot.py`: The MCP host that access to mcp servers via `MCPClient` and communicates with the LLM.
- `mcp_client.py`: The MCP client that connects to the MCP servers and manages the sessions.
- `product_mcp_server.py`: The MCP server that provides primitives.
- `server_config.json`: The configuration for the MCP servers.
