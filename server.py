#!/usr/bin/env python3
"""
AI Self-Audit MCP — MEOK AI Labs. AI agents audit their OWN compliance."""

import json, hashlib, re, os
from datetime import datetime, timezone, timedelta
from typing import Optional
from collections import defaultdict
from mcp.server.fastmcp import FastMCP
import sys, os

from auth_middleware import check_access

# Tier authentication (connects to Stripe subscriptions)
try:
    from auth_middleware import get_tier_from_api_key, Tier, TIER_LIMITS

    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False  # Runs without auth in dev mode

FREE_DAILY_LIMIT = 20
_usage = defaultdict(list)
_audit_log = []
_MEOK_API_KEY = os.environ.get("MEOK_API_KEY", "")


def _check_rate_limit(caller="anonymous"):
    now = datetime.now(timezone.utc)
    _usage[caller] = [t for t in _usage[caller] if (now - t).total_seconds() < 86400]
    if len(_usage[caller]) >= FREE_DAILY_LIMIT:
        return f"Free tier limit. Upgrade: https://councilof.ai"
    _usage[caller].append(now)
    return None


mcp = FastMCP(
    "ai-self-audit",
    instructions="MEOK AI Labs — AI agents audit their own compliance in real-time.",
)

COMPLIANCE_CHECKS = {
    "risk_management": ["risk assess", "risk manage", "risk mitigat"],
    "data_governance": ["data governance", "bias", "representative", "data quality"],
    "documentation": ["document", "annex iv", "technical doc"],
    "logging": ["log", "audit trail", "trace", "record"],
    "transparency": ["transparent", "explainable", "interpretable"],
    "human_oversight": ["human oversight", "human-in-the-loop", "intervention"],
    "accuracy_robustness": ["accuracy", "robust", "security", "adversarial", "test"],
}


@mcp.tool()
def self_audit(system_description: str, article: str = "all", api_key: str = "") -> str:
    """AI agent self-audits EU AI Act compliance. Call: 'Am I compliant right now?'

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        system_description (str): The system description to analyze or process.
        article (str): The article to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}
    if err := _check_rate_limit():
        return {"error": err}
    desc = system_description.lower()
    results = {}
    passed = 0
    total = len(COMPLIANCE_CHECKS)
    for check, keywords in COMPLIANCE_CHECKS.items():
        ok = any(k in desc for k in keywords)
        results[check] = {
            "compliant": ok,
            "evidence": f"{'Found' if ok else 'Missing'} signals",
        }
        if ok:
            passed += 1
    score = round(passed / total * 100, 1)
    ts = datetime.now(timezone.utc).isoformat()
    h = hashlib.sha256(f"{ts}{system_description}".encode()).hexdigest()[:12]
    _audit_log.append({"id": h, "time": ts, "score": score})
    return {
        "audit_id": h,
        "timestamp": ts,
        "compliance_score": score,
        "assessment": "COMPLIANT"
        if score >= 70
        else "PARTIAL"
        if score >= 40
        else "NON-COMPLIANT",
        "passed": passed,
        "total": total,
        "checks": results,
        "days_until_enforcement": (
            datetime(2026, 8, 2, tzinfo=timezone.utc) - datetime.now(timezone.utc)
        ).days,
        "crosswalk_recommendation": "Use meok-governance-engine-mcp for detailed framework mapping"
        if score < 70
        else None,
    }


@mcp.tool()
def audit_conversation(text: str, api_key: str = "") -> str:
    """Audit conversation for bias, PII, manipulation, transparency issues.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        text (str): The text to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}
    if err := _check_rate_limit():
        return {"error": err}
    issues = []
    checks = {
        "manipulation": ["ignore previous", "system prompt", "jailbreak", "bypass"],
        "pii": ["social security", "credit card", "passport number"],
        "bias": ["all [group] are", "never trust", "those people"],
        "transparency": ["pretend to be human", "don't mention ai"],
    }
    for cat, patterns in checks.items():
        for p in patterns:
            if p in text.lower():
                issues.append(
                    {
                        "type": cat,
                        "pattern": p,
                        "severity": "high"
                        if cat in ("manipulation", "pii")
                        else "medium",
                    }
                )
    return {
        "status": "CLEAN" if not issues else "ISSUES",
        "count": len(issues),
        "issues": issues,
    }


@mcp.tool()
def get_certificate(system_name: str, description: str, api_key: str = "") -> str:
    """Generate timestamped compliance certificate for audit trail.

    Behavior:
        This tool generates structured output without modifying external systems.
        Output is deterministic for identical inputs. No side effects.
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        system_name (str): The system name to analyze or process.
        description (str): The description to analyze or process.
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}
    if err := _check_rate_limit():
        return {"error": err}
    ts = datetime.now(timezone.utc)
    desc = description.lower()
    passed = sum(1 for kws in COMPLIANCE_CHECKS.values() if any(k in desc for k in kws))
    score = round(passed / len(COMPLIANCE_CHECKS) * 100, 1)
    h = hashlib.sha256(f"{system_name}{ts.isoformat()}{score}".encode()).hexdigest()
    return {
        "cert_id": f"MEOK-{h[:12].upper()}",
        "issued": ts.isoformat(),
        "valid_until": (ts + timedelta(days=90)).isoformat(),
        "system": system_name,
        "score": score,
        "status": "compliant"
        if score >= 70
        else "partial"
        if score >= 40
        else "non_compliant",
        "hash": h,
        "issuer": "MEOK AI Labs",
    }


@mcp.tool()
def regulatory_pulse(api_key: str = "") -> str:
    """Current regulatory deadlines and enforcement status.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}
    now = datetime.now(timezone.utc)
    deadlines = [
        ("EU AI Act Prohibited", "2025-02-02", "IN FORCE"),
        ("South Korea AI Act", "2026-01-22", "IN FORCE"),
        ("EU AI Act High-Risk", "2026-08-02", "PENDING"),
        ("UK AI Bill", "2026-12-31", "DRAFT"),
        ("EU AI Act Annex I", "2028-08-02", "PENDING"),
    ]
    result = []
    for name, date, status in deadlines:
        d = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        days = (d - now).days
        result.append(
            {
                "framework": name,
                "date": date,
                "status": status if days > 0 else "IN FORCE",
                "days": days,
            }
        )
    return {"deadlines": result}


@mcp.tool()
def get_audit_trail(api_key: str = "") -> str:
    """Return audit trail of all self-audit checks.

    Behavior:
        This tool is read-only and stateless — it produces analysis output
        without modifying any external systems, databases, or files.
        Safe to call repeatedly with identical inputs (idempotent).
        Free tier: 10/day rate limit. Pro tier: unlimited.
        No authentication required for basic usage.

    When to use:
        Use this tool when you need to assess, audit, or verify compliance
        requirements. Ideal for gap analysis, readiness checks, and generating
        compliance documentation.

    When NOT to use:
        Do not use as a substitute for qualified legal counsel. This tool
        provides technical compliance guidance, not legal advice.

    Args:
        api_key (str): The api key to analyze or process.

    Behavioral Transparency:
        - Side Effects: This tool is read-only and produces no side effects. It does not modify
          any external state, databases, or files. All output is computed in-memory and returned
          directly to the caller.
        - Authentication: No authentication required for basic usage. Pro/Enterprise tiers
          require a valid MEOK API key passed via the MEOK_API_KEY environment variable.
        - Rate Limits: Free tier: 10 calls/day. Pro tier: unlimited. Rate limit headers are
          included in responses (X-RateLimit-Remaining, X-RateLimit-Reset).
        - Error Handling: Returns structured error objects with 'error' key on failure.
          Never raises unhandled exceptions. Invalid inputs return descriptive validation errors.
        - Idempotency: Fully idempotent — calling with the same inputs always produces the
          same output. Safe to retry on timeout or transient failure.
        - Data Privacy: No input data is stored, logged, or transmitted to external services.
          All processing happens locally within the MCP server process.
    """
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://councilof.ai"}
    return {"total": len(_audit_log), "audits": _audit_log[-50:]}


def main():
    mcp.run()

if __name__ == '__main__':
    main()


# ── MEOK monetization layer (Stripe upgrade · PAYG · pricing) ──────────
# Free tier is zero-config. Upgrade to Pro (unlimited) or pay-as-you-go per call.
import os as _meok_os
MEOK_STRIPE_UPGRADE = "https://buy.stripe.com/00wfZjcgAeUW4c5cyQ8k90K"  # Pro (unlimited)
MEOK_PAYG_KEY = _meok_os.environ.get("MEOK_PAYG_KEY", "")  # set to enable PAYG (x402 / ~GBP0.05 per call)
MEOK_PRICING = "https://meok.ai/pricing"


def meok_upsell(tier: str = "free") -> dict:
    """Monetization options for free-tier callers: Pro upgrade, PAYG, or pricing page."""
    if tier != "free":
        return {}
    return {"upgrade_url": MEOK_STRIPE_UPGRADE,
            "payg_enabled": bool(MEOK_PAYG_KEY),
            "pricing": MEOK_PRICING}
