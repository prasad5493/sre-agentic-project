"""Turns agent/incident_report.json into a static status page for GitLab Pages."""

import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = os.path.join(BASE_DIR, "agent", "incident_report.json")
OUT_DIR = os.path.join(BASE_DIR, "public")

STATUS_COLORS = {"healthy": "#2ecc71", "warning": "#f39c12", "critical": "#e74c3c"}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(REPORT) as f:
        report = json.load(f)

    color = STATUS_COLORS.get(report["severity"], "#95a5a6")
    findings_html = "".join(f"<li>{line}</li>" for line in report["reasoning_trace"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SRE Agent Status</title>
<style>
  body {{ font-family: -apple-system, Segoe UI, sans-serif; max-width: 640px;
          margin: 60px auto; color: #222; padding: 0 20px; }}
  .badge {{ display: inline-block; padding: 6px 14px; border-radius: 20px;
            color: white; background: {color}; font-weight: 600;
            text-transform: uppercase; font-size: 13px; }}
  h1 {{ font-size: 22px; }}
  ul {{ line-height: 1.7; }}
  .explainer {{ background: #f6f8fa; border-left: 4px solid #999; padding: 14px 18px;
                border-radius: 4px; font-size: 14px; line-height: 1.6; margin: 24px 0; }}
  .meta {{ color: #777; font-size: 13px; margin-top: 30px; }}
  .author {{ color: #555; font-size: 13px; margin-top: 6px; }}
</style>
</head>
<body>
  <p class="explainer">
    <strong>What am I looking at?</strong> This little robot checks my website's
    vitals (how busy it is, how many errors it's throwing, how slow it's
    responding), decides if that's fine or a problem, and if it's a problem,
    tells another tool (Ansible) to fix it &mdash; like restarting the service.
    This page is that decision, explained in its own words, and it rebuilds
    itself automatically every time I push new code.
  </p>
  <h1>{report['service']} &mdash; <span class="badge">{report['severity']}</span></h1>
  <p><strong>Action taken by agent:</strong> {report['action_taken']}</p>
  <h3>Agent reasoning trace</h3>
  <ul>{findings_html}</ul>
  <div class="meta">Generated {report['generated_at']} by the SRE Agent CI pipeline</div>
  <div class="author">Built by Prasad Bhor</div>
</body>
</html>"""

    with open(os.path.join(OUT_DIR, "index.html"), "w") as f:
        f.write(html)


if __name__ == "__main__":
    main()
