FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the project files
COPY . /app

# Set working directory
WORKDIR /app

# Install dependencies
RUN uv sync --frozen --no-install-project

# Expose the port
EXPOSE 5002

# Run the MCP server
CMD ["uv", "run", "mcp_server.py"]