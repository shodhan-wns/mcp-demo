# MCP Demo Project

This project demonstrates the concepts of the **Model Context Protocol (MCP)** by implementing a simple MCP server and client setup.


## Overview

- **Data**: We are using fake, static data stored in JSON files (see the `data/` folder). The data was created and fetched from https://mockapi.io/clone/69c4cea08a5b6e2dec2b2b55.
- **MCP Server**: Built using `FastMCP` (via the MCP SDK), this server exposes `tools` that would let any MCP Client fetch data that is exposed.
- **MCP Client**: For the sake of this PoC, we are using Claude CLI as the Client, and configuring the MCP server in it. This lets us use the powers of Claude conversational AI while interacting with the MCP server without writing any additional code.


## Setup

### MCP server

1. **Clone or navigate to the project directory**:
   ```
   cd /path/to/mcp_demo
   ```

2. **Install dependencies**:
   Make sure `uv` is installed. Refer [this guide](https://docs.astral.sh/uv/getting-started/installation/) based on your OS.
   
   Ensure you have Python 3.12 or higher installed. Then run:
   ```
   uv sync
   ```
   This will create a virtual environment and install the required packages from `pyproject.toml`, including `mcp[cli]`, `anthropic`, etc.

3. **Verify installation**:
   Activate the virtual environment and check that MCP CLI is installed:
   ```
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   `mcp version`
   ```

4. **Run the MCP server**:
Start the MCP server in a terminal. Make sure the virtual environment is activated:
```
uv run mcp_server.py
```

The server will run on `http://127.0.0.1:5002` and expose the tools defined in it.

### MCP Client

To interact with the MCP server, we are using Claude CLI as client. To configure it to connect to the MCP server:

1. **Install Claude CLI** (if not already installed):
   Follow the instructions at [Anthropic's Claude CLI documentation](https://code.claude.com/docs/en/quickstart). Once installed, run `claude` and login into your account.

2. **Configure MCP server in Claude**:
Add the abive MCP server in Claude by:
```
claude mcp add --transport stdio mcp_demo --scope local http:/127.0.0.1:5002/mcp
```

3. **Run Claude CLI**:
Run Claude CLI and check if the MCP server was registered and enabled successfully. This can be done using `/mcp` in Claude CLI.

Once this is established, you can then start to converse normally with Claude, asking questions about the data. It will deduce what tools to use, invoke them and return the results. You can see what tools were called in the console itself.
