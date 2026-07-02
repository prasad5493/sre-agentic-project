"""
SRE Agent - a minimal agentic system that observes infrastructure
metrics, reasons about system health, decides on a remediation action,
and acts by generating the inputs Ansible needs to apply a fix.

This mirrors a classic agent loop: Observe -> Reason -> Decide -> Act -> Log.
In production, the reasoning step could be swapped for an LLM call
(e.g. Claude) to triage ambiguous cases that don't fit clean thresholds.
A stub for that is included below but left disabled so the pipeline
runs with zero external dependencies or API keys.
"""

import json
import os
from datetime import datetime, timezone

METRICS_FILE = os.path.join(os.path.dirname(__file__), "mock_metrics.json")
REPORT_FILE = os.path.join(os.path.dirname(__file__), "incident_report.json")
VARS_FILE = os.path.join(os.path.dirname(__file__), "remediation_vars.json")

THRESHOLDS = {
    "cpu_utilization": 85,
    "error_rate_percent": 5,
    "p95_latency_ms": 1000,
}


def observe():
    with open(METRICS_FILE) as f:
        return json.load(f)


def reason(data):
    """Compare each metric to its threshold and build a reasoning trace."""
    metrics = data["metrics"]
    findings = []
    breached = []

    for key, limit in THRESHOLDS.items():
        value = metrics[key]
        if value > limit:
            findings.append(f"{key}={value} exceeds threshold {limit}")
            breached.append(key)
        else:
            findings.append(f"{key}={value} within threshold {limit}")

    unhealthy = metrics["total_instances"] - metrics["healthy_instances"]
    if unhealthy > 0:
        findings.append(f"{unhealthy} unhealthy instance(s) detected")

    return findings, breached, unhealthy


def decide(breached, unhealthy):
    """Simple severity model that drives the agent's chosen action."""
    if len(breached) >= 2 or unhealthy >= 2:
        return "critical", "restart_service"
    if len(breached) == 1 or unhealthy == 1:
        return "warning", "scale_out"
    return "healthy", "no_action"


def act(severity, action, service):
    """
    The agent 'acts' by writing an Ansible extra-vars file rather than
    calling AWS directly - this keeps the demo safe while showing the
    real hand-off point between "agent decides" and "automation
    executes". Run it with:
      ansible-playbook -i ansible/inventory.ini ansible/site.yml \
        -e @agent/remediation_vars.json
    """
    payload = {"service": service, "remediation_action": action, "severity": severity}
    if action != "no_action":
        with open(VARS_FILE, "w") as f:
            json.dump(payload, f, indent=2)
    return payload


def call_llm_for_triage(findings):
    """
    Extension point: replace/augment rule-based reasoning with an LLM
    call for cases that don't cleanly fit fixed thresholds (e.g.
    correlated, unusual, or multi-service failures). Left unimplemented
    so this pipeline has no external API dependency.
    """
    raise NotImplementedError("Wire this up to the Claude API for richer triage")


def main():
    data = observe()
    findings, breached, unhealthy = reason(data)
    severity, action = decide(breached, unhealthy)
    result = act(severity, action, data["service"])

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "service": data["service"],
        "severity": severity,
        "action_taken": action,
        "reasoning_trace": findings,
        "remediation": result,
    }

    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
