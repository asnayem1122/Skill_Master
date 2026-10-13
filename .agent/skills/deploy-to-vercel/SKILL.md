---
name: deploy-to-vercel
description: >-
  Deploy and manage web applications on Vercel using Git integration or the
  Vercel CLI with token-based or interactive authentication. Use when deploying
  apps, creating preview deployments, configuring environment variables, or
  setting up headless CI deployment.
metadata:
  version: "3.1.0"
---

# Deploy to Vercel (CLI & Token-Based Workflow)

Deploy any web project to Vercel safely. **Always deploy as preview** unless the user explicitly requests production. Supports both interactive local development and headless, token-based CI/agent environments.

---

## When to Use This Skill

- User says "deploy my app", "deploy to vercel", "give me a preview link", "push this live"
- Setting up or managing Vercel projects headlessly via access tokens (`VERCEL_TOKEN`)
- Configuring production or preview environment variables via Vercel CLI
- Inspecting deployment logs, domains, and build statuses

---

## Step 1: Authentication & Token Discovery

Identify the authentication mechanism before executing commands:

### A. Environment Token Check
```bash
# Check if token exists in environment
echo $VERCEL_TOKEN
```
- If `VERCEL_TOKEN` is found, the CLI reads it natively from environment variables.
- **Security Rule**: Never pass `--token "vca_..."` in CLI flags; keep secrets out of shell history.

### B. Project & Team IDs
If deploying headlessly without an interactive `.vercel/` folder:
```bash
export VERCEL_ORG_ID="<org-id>"
export VERCEL_PROJECT_ID="<project-id>"
```
*(Both must be exported together if used).*

### C. Interactive Local CLI
If working interactively without tokens:
```bash
vercel whoami
vercel teams list --format json
```

---

## Step 2: Determine Deployment Strategy

```mermaid
flowchart TD
    Check[Check Project State] --> Linked{Is .vercel/ configured?}
    Linked -->|Yes| GitRemote{Has Git Remote Origin?}
    GitRemote -->|Yes| StrategyGit[Strategy A: Git Commit & Push (Recommended)]
    GitRemote -->|No| StrategyCLI[Strategy B: vercel deploy --no-wait]
    Linked -->|No| StrategyLink[Strategy C: vercel link or Headless Env]
```

### Strategy A: Git-Integrated Deployment (Preferred)
When connected to GitHub/GitLab:
1. Always confirm with the user before pushing:
   > *"This project is connected to Vercel via Git. Would you like me to commit and push to trigger a preview deployment?"*
2. Commit and push:
   ```bash
   git add .
   git commit -m "deploy: update application"
   git push origin <feature-branch>
   ```
3. Retrieve deployment URL:
   ```bash
   vercel ls --format json
   ```

### Strategy B: Direct CLI Deployment
For unlinked Git repos or immediate direct bundle uploads:

```bash
# Deploy preview (non-blocking)
vercel deploy -y --no-wait

# Deploy to production (ONLY if explicitly requested by user)
vercel deploy --prod -y --no-wait
```

### Strategy C: Inspecting & Polling Status
Once initiated, monitor the build without locking terminal processes:
```bash
vercel inspect <deployment-url>
```

---

## Managing Environment Variables

Add or synchronize environment variables without exposing secrets in chat:

```bash
# Add variable for preview and development
echo "my-secret-val" | vercel env add DATABASE_URL preview,development

# Pull project environment variables locally
vercel env pull .env.local
```

---

## Safety Checklist

- [ ] Deploying as **preview** by default; production flag (`--prod`) used only on explicit request
- [ ] No tokens exposed in command line flags or public logs
- [ ] Working tree checked for uncommitted sensitive files before bundling
- [ ] Build output inspected via `vercel inspect` to confirm green status
