# SRE Agentic Toolkit

Built by **Prasad Bhor**

## What is this, actually?

Imagine you run a website and you want to know the moment something
goes wrong with it — like it getting slow, or errors piling up. You'd
also love it if the fix could happen automatically instead of you
staying up at 2am to restart a server.

That's what this project is: a tiny robot that

1. **checks** your website's health stats (CPU load, error rate,
   response time),
2. **decides** whether things look fine, a bit worrying, or broken,
3. **tells another tool what to do about it** (like "restart the
   service"),
4. and **publishes a simple status page** showing what it found and
   why — automatically, every time I push new code.

I built this to practice (and demonstrate) a few core DevOps/SRE
skills together in one small, working example: infrastructure as
code, config management, CI/CD, and the "observe → decide → act" loop
that agentic automation is built on. Nothing here touches real AWS
money — the "health stats" are a mock JSON file, so anyone can clone
this and run it with zero cloud account needed.

## How the pieces fit together

- `agent/mock_metrics.json` — fake health stats standing in for real
  AWS CloudWatch data (CPU%, error rate, latency, how many instances
  are healthy).
- `agent/sre_agent.py` — the "brain." Reads the stats, checks them
  against thresholds, decides how serious it is, and writes down its
  reasoning plus what it decided to do about it.
- `ansible/` — the "hands." If the agent says "restart the service,"
  this is the Ansible playbook that actually does it.
- `infra/iam-role.yaml` — an AWS permissions template. Gives the agent
  only the two permissions it actually needs (read monitoring data,
  basic server access) instead of a master key to everything.
- `pages/build_dashboard.py` — takes the agent's decision and turns it
  into a simple webpage.
- `.gitlab-ci.yml` / `.github/workflows/deploy.yml` — the automation
  that runs all of the above every time I push code, and publishes the
  resulting webpage.

## Important commands (the ones that actually matter)

Run the agent and see what it decided:
```bash
python agent/sre_agent.py
```

Have Ansible act on the agent's decision (e.g. restart the service):
```bash
ansible-playbook -i ansible/inventory.ini ansible/site.yml -e @agent/remediation_vars.json
```

Build the status page locally, to see it before pushing:
```bash
python pages/build_dashboard.py
```

Check the Ansible playbook for mistakes before running it:
```bash
ansible-lint ansible/site.yml
```

Check the AWS permissions template for mistakes:
```bash
cfn-lint infra/iam-role.yaml
```

Deploy the real IAM role to AWS (only if you actually want it in your
own AWS account):
```bash
aws cloudformation deploy --template-file infra/iam-role.yaml --stack-name sre-agent-role --capabilities CAPABILITY_NAMED_IAM
```

## Why I built it this way

- **The permissions are locked down on purpose.** The IAM role only
  gets two abilities — reading monitoring data and basic managed
  server access — nothing that could change or delete other things in
  the account. That's the "least privilege" principle: give a thing
  only the access it needs to do its one job.
- **The "AI" part is honest about what it is.** Right now the agent
  uses simple if/then rules, not a live language model. I left a clear
  spot in the code (`call_llm_for_triage`) where a real model like
  Claude could take over for trickier cases that don't fit clean
  thresholds. I'd rather show I understand the shape of an agentic
  system than fake a fancier version of it.
- **Everything is automated end-to-end.** I never manually upload the
  status page — pushing code is the only step. The pipeline lints the
  config, validates the AWS template, runs the agent, and republishes
  the page every single time.
