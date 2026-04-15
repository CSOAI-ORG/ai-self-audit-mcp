# AI Self-Audit MCP Server

> By [MEOK AI Labs](https://meok.ai) — AI agents audit their own EU AI Act compliance in real-time

## Installation

```bash
pip install ai-self-audit-mcp
```

## Usage

```bash
# Run standalone
python server.py

# Or via MCP
mcp install ai-self-audit-mcp
```

## Tools

### `self_audit`
AI agent self-audits EU AI Act compliance. Checks risk management, data governance, documentation, logging, transparency, human oversight, and accuracy/robustness.

**Parameters:**
- `system_description` (str): Description of your AI system
- `article` (str): Specific article to check (default 'all')

### `audit_conversation`
Audit conversation for bias, PII, manipulation, and transparency issues.

**Parameters:**
- `text` (str): Conversation text to audit

### `get_certificate`
Generate timestamped compliance certificate for audit trail. Valid for 90 days.

**Parameters:**
- `system_name` (str): Name of the system
- `description` (str): System description

### `regulatory_pulse`
Current regulatory deadlines and enforcement status for EU AI Act, South Korea AI Act, UK AI Bill, and more.

### `get_audit_trail`
Return audit trail of all self-audit checks performed.

## Authentication

Free tier: 20 calls/day. Upgrade at [meok.ai/pricing](https://meok.ai/pricing) for unlimited access.

## License

MIT — MEOK AI Labs
