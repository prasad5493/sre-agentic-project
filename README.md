# SRE Agentic Project

Built by Prasad Bhor

## What This Project Does

Imagine you run a website and you want to know the moment something goes wrong with it, such as the site becoming slow or errors starting to pile up. You will also want the fix to happen automatically, instead of staying up late to restart a server yourself.

This project is a small robot that does exactly that. It checks the website health information, decides whether things look fine, need attention, or are broken, tells Ansible what to do about it, such as restarting the service, and publishes a simple status page showing what it found and why. All of this happens automatically every time new code is pushed to the repository. This project follows the agentic AI concept, where a system observes information, reasons about it, decides on an action, and carries out that action on its own.

This project was built to demonstrate a few important DevOps and Site Reliability Engineering skills in one small example, including infrastructure as code, configuration management, and continuous integration and deployment. The project does not use real AWS resources or cost any money to explore, since the health information used by the agent comes from a sample file rather than a live AWS account.

## How The Different Parts Work Together

The file `agent/mock_metrics.json` contains sample health information that stands in for real AWS CloudWatch data - CPU usage, error rate, response time, and how many servers are healthy.

The file `agent/sre_agent.py` is the brain of the project. It reads the health information, compares it against a set of thresholds, decides how serious the situation is, and records its reasoning along with the action to take.

The `ansible` folder contains the automation that acts on the agent's decision. If the agent decides the service should be restarted, this is the part that performs the restart.

The file `infra/iam-role.yaml` defines an AWS permission role using a CloudFormation template. It gives the agent only two permissions - reading monitoring data and basic managed server access - instead of full access to the AWS account. This template is checked automatically by `cfn-lint` on every push, though deploying it to a real AWS account is still a manual step, run using the AWS CLI.

The file `pages/build_dashboard.py` turns the agent's decision into a simple webpage that anyone can view.

The files `.gitlab-ci.yml` and `.github/workflows/deploy.yml` describe the automated pipeline that runs everything above every time code is pushed - checking the Ansible files, checking the AWS permission template, running the agent, and publishing the final page.

The project also includes a `.yamllint` file that raises the maximum line length allowed in YAML files, since the default limit of eighty characters is too strict for real Ansible projects.

## Conclusion

Every part of this project is automated from start to finish. The status page is never updated by hand. Pushing code is the only action needed, and the pipeline takes care of checking the code, running the agent, and publishing the updated page every time.
