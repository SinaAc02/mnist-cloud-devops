# Interactive Step-by-Step Instructions for Codex

Build this project interactively, one stage at a time.

The main goal is not to finish the whole project as quickly as possible. The goal is for me to understand every major decision, every technology used, and every step of the deployment pipeline.

## Core rule

Do NOT build the whole project at once.

For every stage:

1. Explain what we are about to build in a few sentences.
2. Show the important decisions/options available at that stage.
3. Ask me which option I want whenever there is a meaningful choice.
4. Explain the practical difference between the options briefly.
5. Wait for my decision before implementing that part.
6. Implement only that stage.
7. Show me exactly what you created or changed.
8. Show me the important files/code/configuration.
9. Explain what each new file or major section does.
10. Tell me how to run/test that stage myself.
11. Verify that the stage works.
12. Summarize what we now have.
13. Only then move to the next stage.

Do not silently make important architectural decisions for me.

You may make trivial implementation decisions yourself, but any choice that changes the architecture, technology, user experience, deployment strategy, cost, security model, or learning path should be presented to me first.

---

# Stage 1 — Decide the ML model

First explain the available choices.

For example:

### Option A — FFNN
- Simple
- Uses flattened 28×28 MNIST images
- Good for learning
- Similar to a model I have built before

### Option B — CNN
- More appropriate for image classification
- Usually better accuracy
- More realistic computer-vision architecture
- Slightly more complex

### Option C — modified/custom network
- Build something between the two or create our own architecture

Ask me which I want.

Also ask about important training choices where appropriate, such as:
- simple vs more advanced architecture
- dropout or no dropout
- batch normalization or not
- target accuracy
- CPU vs GPU training
- whether to show training graphs
- whether to save only the best model

Do not train anything until I choose.

Then implement the chosen model, train it, evaluate it and save it.

Show:
- architecture
- parameter count
- training result
- validation/test accuracy
- saved model location

---

# Stage 2 — Decide prediction output

Before building the API, ask what I want the model to return.

Possible options could include:

### Minimal
```text
Prediction: 7
```

### Confidence
```text
Prediction: 7
Confidence: 98.4%
```

### Full probabilities
```text
0: 0.1%
1: 0.0%
2: 0.2%
...
7: 98.4%
```

### Top predictions
```text
7 — 98.4%
1 — 1.0%
9 — 0.4%
```

Let me choose.

Then design the inference output around that choice.

---

# Stage 3 — Image preprocessing

Explain the important issue:

The browser drawing will not automatically look exactly like an MNIST image.

Present options for preprocessing, such as:
- basic resize to 28×28
- resize + grayscale + normalize
- crop around the drawn digit
- center the digit
- preserve aspect ratio
- invert colors to match MNIST
- optionally reproduce MNIST-style centering

Recommend sensible options, but let me decide how advanced we want preprocessing to be.

Then implement and test it.

Show me examples of what the model actually receives after preprocessing.

---

# Stage 4 — Backend/API

Explain the backend options.

For example:

### FastAPI
Recommended for this project.

### Flask
Simpler but less modern for API-focused work.

Ask me before choosing if there is a meaningful alternative.

Then decide together:
- API framework
- input format
- output format
- error responses
- whether the frontend and backend run as one application or separately

Implement:

```text
GET /health
POST /predict
```

Show me:
- request example
- response example
- backend structure
- how model loading works
- how inference works

Run and test both endpoints.

---

# Stage 5 — Frontend/UI

Before implementation, ask how I want the UI.

Decisions should include things such as:

### UI technology

Option A:
- plain HTML
- CSS
- JavaScript

Option B:
- React

Option C:
- another reasonable frontend if useful

Explain why plain JavaScript may be enough for this project.

Then ask about features such as:
- canvas size
- Clear button
- Predict button
- automatic prediction while drawing or manual prediction
- confidence display
- probability bars
- dark/light design
- prediction history
- model information
- drawing thickness
- touch support for phones

Do not add every possible feature automatically.

Let me choose.

Then build the UI and show how frontend → API communication works.

---

# Stage 6 — Local integration

Connect:

```text
Browser
   ↓
Frontend
   ↓
FastAPI
   ↓
Preprocessing
   ↓
PyTorch model
   ↓
Prediction
```

Run the complete application locally.

Test multiple digits manually.

Show me what commands start the app and where everything is running.

---

# Stage 7 — Automated tests

Before adding tests, explain what kinds are useful:

- unit tests
- API tests
- preprocessing tests
- model-loading tests
- integration tests

Ask how extensive I want the first test setup to be.

Then add the selected tests with `pytest`.

At minimum we will eventually want tests for:
- `/health`
- `/predict`
- invalid input
- model loading
- preprocessing

Run the tests and show the output.

---

# Stage 8 — Git structure

Before changing Git workflow, explain:

- repository
- commits
- branches
- main branch
- feature branches
- pull requests

Ask whether I want:
- simple `main` workflow
- feature branches + pull requests

Then initialize/organize the repository accordingly.

Show the resulting repository structure.

---

# Stage 9 — Docker

Explain first:

```text
Dockerfile
Docker image
Docker container
port mapping
environment variables
```

Before implementation, ask about relevant decisions such as:
- Python base image
- single-container application vs frontend/backend separation
- development vs production container
- whether the trained model is copied into the image or mounted separately

Then Dockerize it.

Show:
- complete Dockerfile
- what every section does
- build command
- run command

Test the container.

---

# Stage 10 — Docker Compose

Explain why Docker Compose exists.

Then ask whether we want to keep only the application initially or introduce another service.

Possible options:

### Option A
Application only.

### Option B
Application + PostgreSQL.

If PostgreSQL is added, ask whether prediction history should be stored.

Possible stored information:
- timestamp
- prediction
- confidence
- processing time

Do not store user drawings by default.

Then create Docker Compose.

Explain:
- services
- Docker network
- volumes
- environment variables
- service names

Run and test it.

---

# Stage 11 — Choose the cloud provider

Stop before creating any cloud resources.

Present reasonable choices such as:

### Azure
Good because I specifically want Azure/cloud experience.

### Azure for Students
Use if available and appropriate.

### Google Cloud
Useful alternative.

### Oracle Cloud
Possible free VM option.

### Hetzner Cloud
Simple and cheap, but generally not free.

For each option briefly explain:
- cost/free allowance
- difficulty
- relevance for learning
- whether a payment card is required
- major limitations

Use current information when evaluating cloud pricing/free tiers.

Ask me which provider I want.

Do not create anything until I choose.

---

# Stage 12 — Create the first VM manually

Once I choose a provider, guide me through the cloud UI manually first.

At every important choice ask me or explain the options, including:
- region
- VM size
- CPU
- RAM
- Ubuntu version
- disk size
- public IP
- SSH key
- username
- firewall/security rules

Do not simply say "create a VM."

Explain what each setting means while we configure it.

The first VM should be created manually so I understand what Terraform later automates.

---

# Stage 13 — SSH and Linux

Once the VM exists:

Teach me how to connect using SSH.

Explain:
- public IP
- username
- SSH public key
- SSH private key
- port 22

Then practice essential Linux commands.

Do not dump hundreds of commands.

Teach only what we need while deploying the application.

---

# Stage 14 — Manual deployment

Deploy the application manually first.

Process:

```text
Linux VM
↓
Install Docker
↓
Get application
↓
Run Docker Compose
↓
Access application remotely
```

Explain each action.

Verify that the app works from my own browser through the VM's public IP.

---

# Stage 15 — Firewall/security

Review what ports are currently exposed.

Explain:
- inbound traffic
- outbound traffic
- ports
- firewall rules

Decide which ports should remain open.

Target eventually:

```text
22 SSH
80 HTTP
443 HTTPS
```

Everything unnecessary should stay closed.

---

# Stage 16 — Domain decision

Ask whether I want:

### Option A
Continue using the server IP.

### Option B
Use a real domain/subdomain.

If I choose a domain, explain:
- DNS
- A record
- domain → IP mapping

Then configure it.

---

# Stage 17 — Reverse proxy

Explain why FastAPI should not normally be directly exposed as:

```text
SERVER_IP:8000
```

Introduce Nginx.

Architecture:

```text
Internet
↓
Nginx
↓
FastAPI
```

Ask if we want Nginx or another reasonable reverse proxy if alternatives matter.

Then configure it.

---

# Stage 18 — HTTPS

Explain:
- HTTP
- HTTPS
- TLS
- certificates
- Let's Encrypt

Then enable HTTPS.

Verify:
- HTTPS works
- HTTP redirects to HTTPS if appropriate

---

# Stage 19 — Terraform

Only after I understand the manually-created infrastructure should we introduce Terraform.

Explain:

```text
Manual infrastructure
vs
Infrastructure as Code
```

Show which things Terraform will replace.

Ask decisions where relevant, including:
- what resources Terraform should manage
- whether networking should be explicit
- variable structure
- where secrets should live

Then create Terraform gradually.

Use:

```text
terraform init
terraform plan
terraform apply
```

Show me the plan before applying.

Explain what Terraform is about to create.

---

# Stage 20 — Terraform destroy/recreate exercise

Once Terraform works:

Explain the purpose of:

```text
terraform destroy
```

Ask me before destroying anything.

Then deliberately destroy the test environment and recreate it with:

```text
terraform apply
```

This should demonstrate reproducible infrastructure.

---

# Stage 21 — Ansible

Explain clearly:

```text
Terraform = creates infrastructure
Ansible = configures servers
```

Show what we previously configured manually.

Decide what should now be automated by Ansible.

Possible tasks:
- users
- Docker installation
- Nginx
- directories
- configuration files
- services

Then implement incrementally.

---

# Stage 22 — CI

Explain CI before writing GitHub Actions.

Show the desired flow:

```text
git push
↓
checkout
↓
install dependencies
↓
run tests
↓
pass/fail
```

Ask about optional checks such as:
- linting
- formatting
- type checking
- security scanning

Let me choose what to include.

Then create GitHub Actions.

Run/test the workflow.

---

# Stage 23 — Container registry

Explain why the server should pull an already-built Docker image rather than build everything itself.

Present registry options such as:
- GitHub Container Registry
- Docker Hub
- cloud-provider registry

Let me choose.

Then configure image publishing.

---

# Stage 24 — Image tagging/versioning

Before deciding tags, present options:

### `latest`

### semantic version
```text
v1.0.0
```

### Git commit hash
```text
a4b19ef
```

### combination

Explain advantages/disadvantages.

Let me choose.

---

# Stage 25 — CD

Explain CD.

Target pipeline:

```text
git push
↓
tests
↓
Docker build
↓
push image
↓
deploy
↓
health check
```

Before implementation, explain deployment strategy options.

For example:
- SSH into VM and update Docker Compose
- another deployment mechanism

Then implement the selected approach.

---

# Stage 26 — Pipeline failure experiments

Do controlled failure experiments.

Before each experiment tell me what we expect to happen.

Experiments:

1. Break a unit test.
2. Push.
3. Confirm deployment stops.

Then:

1. Fix test.
2. Break Docker build.
3. Confirm deployment stops.

Then test failed health checks.

Show exactly where the pipeline detects each problem.

---

# Stage 27 — Rollback strategy

Explain rollback options.

Decide how we want to return to a previous Docker version.

Then deliberately deploy a bad version in the test environment and roll back.

Verify the old version works.

---

# Stage 28 — Logging

Explain what logs are and what we actually need.

Ask which application information should be logged.

Possible useful information:
- timestamp
- prediction
- confidence
- request latency
- status
- error

Do not log unnecessary sensitive data.

Implement structured logging.

Show how to inspect logs.

---

# Stage 29 — Metrics

Explain difference between:

```text
logs
vs
metrics
```

Decide what metrics to expose.

Possible metrics:
- total prediction requests
- errors
- request latency
- prediction count by digit
- CPU
- RAM

Then add Prometheus.

---

# Stage 30 — Grafana

Explain Grafana's role.

Ask which dashboard panels I want.

Then create a useful dashboard.

Do not make a huge dashboard just because we can.

---

# Stage 31 — Kubernetes decision

Before introducing Kubernetes, review what Docker Compose currently does.

Explain why Kubernetes exists.

Ask whether I want to continue to Kubernetes at this point.

If yes, use a lightweight environment such as k3s unless another option is selected.

Explain alternatives if relevant.

---

# Stage 32 — Kubernetes basics

Introduce concepts gradually:

```text
Cluster
Node
Pod
Deployment
Service
Ingress
ConfigMap
Secret
Volume
```

Do not introduce them all abstractly at once.

Introduce each when the application needs it.

---

# Stage 33 — Kubernetes deployment

Convert the existing deployment into Kubernetes resources.

Show how each Kubernetes resource corresponds to something we already understand from Docker Compose.

Deploy and verify the application.

---

# Stage 34 — Kubernetes replicas

Ask how many replicas I want.

For example:

```text
1
2
3
```

Explain why multiple replicas exist.

Then deploy the selected number.

---

# Stage 35 — Self-healing experiment

Delete a pod manually.

Before doing it, explain what should happen.

Then observe Kubernetes automatically recreate it.

Show me the result.

---

# Stage 36 — Scaling experiment

Change replica count.

Show:

```text
2 → 4
```

or whatever I choose.

Explain what Kubernetes changes.

---

# Stage 37 — Helm

Only introduce Helm after I have seen the raw Kubernetes YAML.

Explain what problem Helm solves.

Then convert the current Kubernetes deployment into a Helm chart.

Ask which configuration values should be customizable.

---

# Stage 38 — GitOps

Explain the difference between our current CD approach and GitOps.

Introduce Argo CD.

Target:

```text
Git
↓
Argo CD
↓
Kubernetes
```

Ask whether deployment configuration should live:
- in the same repository
- in a separate deployment repository

Explain the difference.

Then implement the chosen structure.

---

# Stage 39 — GitOps experiment

Change something simple in Git, such as:

```text
replicas: 2
```

to:

```text
replicas: 3
```

Push it.

Observe Argo CD synchronize the cluster.

Show exactly what happened.

---

# Stage 40 — Final review

At the end, show me the complete architecture.

Explain the full path:

```text
Developer
↓
Git
↓
CI
↓
Tests
↓
Docker build
↓
Container Registry
↓
CD / GitOps
↓
Cloud infrastructure
↓
Application
↓
Monitoring
```

Also explain:

```text
Terraform
→ infrastructure

Ansible
→ server configuration

Docker
→ application packaging

GitHub Actions
→ CI/CD automation

Nginx
→ reverse proxy

Prometheus
→ metrics

Grafana
→ visualization

Kubernetes
→ container orchestration

Helm
→ Kubernetes packaging

Argo CD
→ GitOps
```

---

# Important behavior rules

At every stage:

- Do not rush ahead.
- Do not implement future stages prematurely.
- Do not hide decisions from me.
- Do not give me ten choices for trivial details.
- Ask only about decisions that actually matter.
- Recommend an option when useful, but let me choose.
- Clearly mark your recommendation.
- Explain tradeoffs briefly.
- After I choose, implement it.
- Show all important changes.
- Show commands that were run.
- Show test results.
- Explain errors if something fails.
- Never pretend something worked if it was not tested.
- Keep a running checklist showing which stages are complete.
- Keep the repository runnable after every major stage.
- Do not delete working functionality just to move to the next stage.
- Prefer simple solutions first, then introduce more advanced tooling when there is a reason for it.

Most importantly:

This project is a learning exercise.

Do not behave like an autonomous agent whose objective is simply "finish the project."

Behave like a technical mentor building the project together with me, where I make the important decisions and understand why each technology is being introduced.
