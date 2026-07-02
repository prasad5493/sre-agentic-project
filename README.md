# SRE Agentic Project

Built by Prasad Bhor

## What This Project Does

Imagine you run a website and you want to know the moment something goes wrong with it, such as the site becoming slow or errors starting to pile up. You will also want the fix to happen automatically, instead of staying up late to restart a server yourself.

This project is a small robot that does exactly that. It checks the website health information, decides whether things look fine, need attention, or are broken, tells another tool what to do about it, such as restarting the service, and publishes a simple status page showing what it found and why. All of this happens automatically every time new code is pushed to the repository.

This project was built to practice and demonstrate a few important DevOps and Site Reliability Engineering skills together in one small working example. These include infrastructure as code, configuration management, continuous integration and deployment, and the observe, decide, act pattern that agentic automation is built on. The project does not use real AWS resources or cost any money to explore, since the health information used by the agent comes from a sample file rather than a live AWS account.

## How The Different Parts Work Together

The file `agent/mock_metrics.json` contains sample health information that stands in for real AWS CloudWatch data. It includes values such as CPU usage, error rate, response time, and how many servers are currently healthy.

The file `agent/sre_agent.py` acts as the brain of the project. It reads the health information, compares each value against a set of thresholds, and decides how serious the situation is. It then records its reasoning and writes down what action should be taken.

The `ansible` folder contains the automation that acts on the agent decision. If the agent decides the service should be restarted, this is the part that actually performs the restart. The variable used to pass this decision is named `remediation_action`, since the word `action` is reserved by Ansible itself and cannot be used as a custom variable name. Every task in this folder also uses the full module name, such as `ansible.builtin.service`, instead of a shortened name. This is a modern best practice that removes any confusion about which collection a module belongs to.

The file `infra/iam-role.yaml` defines an AWS permission template. It gives the agent only the two permissions it actually needs, which are reading monitoring data and basic managed server access, instead of full access to the AWS account. This follows the security principle known as least privilege, meaning a system should only be given the access it truly needs to do its job.

The file `pages/build_dashboard.py` takes the agent decision and turns it into a simple webpage that anyone can view.

The files `.gitlab-ci.yml` and `.github/workflows/deploy.yml` describe the automated pipeline that runs all of the steps above every time code is pushed, and then publishes the resulting webpage. Both pipelines run the same four steps in order, checking the Ansible files for style issues, checking the AWS permission template for mistakes, running the agent, and publishing the final page.

The project also includes a `.yamllint` configuration file. By default, the tool that checks YAML formatting only allows lines up to eighty characters, which is often too strict for real Ansible files. This file raises that limit to a more realistic one hundred and twenty characters, which is a common setting used by real Ansible projects.

## Why It Is Built This Way

The permissions given to the agent are intentionally limited. The AWS role only allows reading monitoring information and basic managed access, and nothing that could change or delete other resources in the account. This is the least privilege principle in practice.

The agent currently uses simple rule based logic rather than a live artificial intelligence model. A clear extension point named `call_llm_for_triage` is included in the code to show exactly where a real AI model, such as Claude, could be added later to handle cases that do not fit clean rules. This project aims to show a clear understanding of how an agentic system is structured, rather than presenting a more advanced system than what has actually been built.

Every part of this project is automated from start to finish. The status page is never updated by hand. Pushing code is the only action needed, and the pipeline takes care of checking the code, running the agent, and publishing the updated page every time.
