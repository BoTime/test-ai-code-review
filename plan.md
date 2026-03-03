# AI Automated Code Review Plan (GitHub Actions MVP First)

## 1) Objective
Ship a working automated PR review in about 30 minutes, then harden for production.

Success for MVP:
- GitHub PR event triggers a GitHub Actions workflow.
- Workflow runs Qodo PR-Agent with OpenAI.
- PR-Agent posts review comments back to the PR.

## 2) Simplest Architecture (MVP)
GitHub PR Event -> GitHub Actions Workflow -> PR-Agent -> OpenAI API -> Comment on GitHub PR

MVP components only:
- GitHub Actions workflow (`.github/workflows/pr-review.yml`)
- GitHub repository secret (`OPENAI_API_KEY`)
- Default `GITHUB_TOKEN` permissions for PR comments

This intentionally skips AWS services for fastest setup.

## 3) 30-Minute Implementation Plan

## Step 1: Add repository secret (5 min)
Create:
- `OPENAI_API_KEY`

## Step 2: Add workflow (10 min)
File path:
- `.github/workflows/pr-review.yml`

Use this configuration:

```yaml
name: PR Review (PR-Agent)

on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install PR-Agent
        run: pip install -U pr-agent

      - name: Run review
        env:
          OPENAI__KEY: ${{ secrets.OPENAI_API_KEY }}
          CONFIG__GIT_PROVIDER: github
          GITHUB__USER_TOKEN: ${{ github.token }}
          PR_URL: ${{ github.event.pull_request.html_url }}
        run: python -m pr_agent.cli --pr_url "$PR_URL" review
```

## Step 3: Validate end-to-end (10-15 min)
1. Open or update a small PR.
2. Confirm workflow run starts in Actions tab.
3. Confirm PR-Agent comments appear on the PR.
4. If no comment appears, inspect the workflow logs first.

## 4) MVP Acceptance Criteria
- One PR event triggers one workflow run.
- PR-Agent posts at least one review comment on a test PR.
- No plaintext API keys in repository files.
- Typical run time is under ~5 minutes for small PRs.

## 5) Known MVP Tradeoffs
- Minimal observability (GitHub Actions logs only).
- Limited queue/concurrency controls by default.
- Secret management is in GitHub, not centralized AWS secrets.

These tradeoffs are acceptable for a same-day trial.

## 6) Hardening Path After MVP (Production)

## Phase A: Security hardening
1. Move to GitHub App credentials if needed for org policy.
2. Restrict workflow permissions further if possible.
3. Add secret rotation and ownership documentation.

## Phase B: Reliability and control
1. Add concurrency groups to avoid duplicate runs.
2. Add PR size/file filters to control cost and noise.
3. Add retry/failure notification strategy.

## Phase C: Observability and KPIs
1. Track workflow failure rate and latency.
2. Track review usefulness, false positives, and cost per PR.

## Phase D: Optional AWS migration (when needed)
If requirements grow, move to AWS CodeBuild or ECS Fargate for:
- Centralized secrets and IAM controls
- Custom networking/compliance constraints
- Advanced scaling and operational policies

## 7) Immediate Next Actions
1. Set `OPENAI_API_KEY` repository secret.
2. Commit and push `.github/workflows/pr-review.yml`.
3. Open/update one test PR and verify comment output.
4. Tune rules/prompts based on first trial results.
