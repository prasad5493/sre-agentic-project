"""Turns agent/incident_report.json into a static status page for GitHub or GitLab Pages."""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(BASE_DIR, "agent", "incident_report.json")
OUT_DIR = os.path.join(BASE_DIR, "public")

STATUS_COLORS = {"healthy": "#2ecc71", "warning": "#f39c12", "critical": "#e74c3c"}

CONCEPTS = [
    (
        "Infrastructure as Code",
        "The AWS permission role in this project is written as a CloudFormation "
        "template instead of being created by hand in the AWS console. This means "
        "the infrastructure can be reviewed, reused, and recreated reliably.",
    ),
    (
        "Configuration Management with Ansible",
        "Ansible is used to install and configure the web service, and to apply "
        "the fix that the agent decides on, such as restarting the service.",
    ),
    (
        "Least Privilege Identity and Access Management",
        "The IAM role created for this project only allows reading monitoring "
        "data and basic managed server access. It does not include permission to "
        "change or delete other resources in the AWS account.",
    ),
    (
        "Continuous Integration and Deployment",
        "Every time code is pushed, an automated pipeline checks the files for "
        "mistakes, runs the agent, and publishes this page, with no manual steps.",
    ),
    (
        "Agentic Automation",
        "The agent follows a simple loop of observing information, reasoning "
        "about it, deciding what to do, and then acting on that decision. This "
        "is the same basic pattern used by more advanced AI driven agents.",
    ),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(REPORT) as f:
        report = json.load(f)

    color = STATUS_COLORS.get(report["severity"], "#95a5a6")
    findings_html = "".join(f"<li>{line}</li>" for line in report["reasoning_trace"])
    concepts_html = "".join(
        f"<li><strong>{title}.</strong> {desc}</li>" for title, desc in CONCEPTS
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SRE Agentic Project</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, sans-serif; max-width: 680px;
          margin: 60px auto; color: #222; padding: 0 20px; }}
  .badge {{ display: inline-block; padding: 6px 14px; border-radius: 20px;
            color: white; background: {color}; font-weight: 600;
            text-transform: uppercase; font-size: 13px; }}
  h1 {{ font-size: 24px; margin-bottom: 4px; }}
  h2 {{ font-size: 18px; margin-top: 40px; }}
  h3 {{ font-size: 15px; margin-bottom: 6px; }}
  ul {{ line-height: 1.7; padding-left: 20px; }}
  .author {{ color: #555; font-size: 13px; margin-top: 6px; }}
  .description {{ background: #f6f8fa; border-radius: 6px; padding: 16px 18px;
                   font-size: 14px; line-height: 1.6; margin: 20px 0; }}
  .concepts {{ background: #ffffff; border: 1px solid #e1e4e8; border-radius: 6px;
               padding: 16px 22px; font-size: 14px; line-height: 1.6; }}
  .concepts li {{ margin-bottom: 10px; }}
  .status-box {{ border: 1px solid #e1e4e8; border-radius: 6px; padding: 18px 20px;
                 margin: 24px 0; background: #fafbfc; }}
  .status-item {{ margin-bottom: 18px; }}
  .status-item:last-child {{ margin-bottom: 0; }}
  .status-label {{ font-size: 12px; text-transform: uppercase; letter-spacing: 0.4px;
                    color: #777; font-weight: 600; }}
  .status-value {{ font-size: 15px; margin: 4px 0 4px 0; }}
  .status-note {{ font-size: 13px; color: #555; line-height: 1.5; }}
  .meta {{ color: #777; font-size: 13px; margin-top: 30px; }}
</style>
</head>
<body>
  <h1>SRE Agentic Project</h1>
  <div class="author">Built by Prasad Bhor</div>

  <p class="description">
    This project watches a website and checks whether it is running well. It
    looks at information such as how busy the server is, how many errors are
    happening, and how slow it is responding. Based on what it finds, it
    decides whether everything is fine or whether action is needed, and it
    tells another tool to apply the fix. This page shows the result of that
    check, and it updates automatically every time new code is pushed.
  </p>

  <h2>Key Concepts Used In This Project</h2>
  <ul class="concepts">{concepts_html}</ul>

  <h2>Current Status</h2>
  <h1>{report['service']} <span class="badge">{report['severity']}</span></h1>

  <div class="status-box">
    <div class="status-item">
      <div class="status-label">Checkout Api</div>
      <div class="status-value">{report['service']}</div>
      <div class="status-note">
        This is the name of the sample website or service that the agent is
        watching in this project. In a real setup, this could be any service
        running on a company server.
      </div>
    </div>

    <div class="status-item">
      <div class="status-label">Action Taken By Agent</div>
      <div class="status-value">{report['action_taken']}</div>
      <div class="status-note">
        This shows what the agent decided to do after checking the service
        information. It could be no action if everything looks healthy, or a
        fix such as restarting the service if a problem was found.
      </div>
    </div>

    <div class="status-item">
      <div class="status-label">Agent Reasoning Trace</div>
      <ul class="status-value">{findings_html}</ul>
      <div class="status-note">
        This is the list of checks the agent performed and what it found
        during each one, so anyone reading this page can see exactly why the
        agent reached its decision.
      </div>
    </div>
  </div>

  <div class="meta">Generated {report['generated_at']} by the automated pipeline</div>
</body>
</html>"""

    with open(os.path.join(OUT_DIR, "index.html"), "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
