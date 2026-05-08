<div align="center">

# Ai Self Audit MCP

**MCP server for ai self audit mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-ai-self-audit-mcp)](https://pypi.org/project/meok-ai-self-audit-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Ai Self Audit MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `self_audit` | AI agent self-audits EU AI Act compliance. Call: 'Am I compliant right now?' |
| `audit_conversation` | Audit conversation for bias, PII, manipulation, transparency issues. |
| `get_certificate` | Generate timestamped compliance certificate for audit trail. |
| `regulatory_pulse` | Current regulatory deadlines and enforcement status. |
| `get_audit_trail` | Return audit trail of all self-audit checks. |

## Installation

```bash
pip install meok-ai-self-audit-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "ai-self-audit-mcp": {
      "command": "python",
      "args": ["-m", "meok_ai_self_audit_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 5 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
