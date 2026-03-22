# Project & Worklog Sync Action

A reusable GitHub Action that automatically syncs `WORKLOG.md` and `PROJECT.md` files from multiple source repositories into a single centralized repository via pull requests.

Designed for maintaining a portfolio or blog (e.g. Astro): each project repo holds its own documentation, and this action funnels it all into one place automatically.

---

## What Gets Synced

| File | Purpose | Destination in target repo |
|---|---|---|
| `PROJECT.md` | Describes the project (portfolio entry) | `<destination_path>/project/<repo-name>-PROJECT.md` |
| `WORKLOG.md` | Work diary / blog entries with dated items | `<destination_path>/worklog/<repo-name>-WORKLOG.md` |

Both files are **overwritten** on each sync (not appended). The sync only triggers and opens a PR when file content actually changes.

---

## How It Works

1. A push to `main` in a source repo modifies `WORKLOG.md` or `PROJECT.md`
2. The caller workflow triggers and runs this action
3. The action clones your central (target) repository
4. It creates a branch named `update/<source-repo-name>-<sha>`
5. It copies the changed files to the appropriate subdirectory
6. It opens a pull request in the target repo for review

---

## Quick Start

### Step 1 — Set up the central repository

Designate one GitHub repository to collect all synced files. No special setup is needed inside it.

### Step 2 — Generate a Personal Access Token (PAT)

1. Go to **GitHub Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**
2. Generate a new token with the full **`repo`** scope
3. Copy the token value — you'll need it in the next step

### Step 3 — Add the secret to each source repository

In **every source repository** that will use this action:

1. Go to **Settings** > **Secrets and variables** > **Actions**
2. Click **New repository secret**
3. Name: `WORKLOG_ACTION_TOKEN`
4. Value: paste your PAT

### Step 4 — Add the workflow file to each source repository

Create the following file in each source repository:

#### `.github/workflows/sync-files.yml`

```yaml
name: 'Sync Project Files on Change'

on:
  push:
    branches:
      - main
    paths:
      - 'WORKLOG.md'
      - 'PROJECT.md'

jobs:
  sync_files_job:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v6

      - name: Sync Files
        uses: EnzoReyes11/worklog-action@main
        with:
          target_repo: 'your-owner/central-repo'   # <-- your central repository
          token: ${{ secrets.WORKLOG_ACTION_TOKEN }}
          # destination_path: 'files'              # optional, defaults to 'files'
          # target_branch: 'main'                  # optional, defaults to 'main'
```

That's it. The next time `WORKLOG.md` or `PROJECT.md` is pushed on `main`, a PR will be opened in your central repo.

---

## Action Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `target_repo` | Yes | — | Central repo in `owner/repo` format |
| `token` | Yes | — | PAT with `repo` scope for the target repo |
| `target_branch` | No | `main` | Branch in the target repo to open the PR against |
| `destination_path` | No | `files` | Base folder in the target repo where files land |

---

## Bulk Setup Utility

If you have many repositories to configure, use the included `sync.sh` script to set the PAT secret across all of them at once using the GitHub CLI.

> **Note:** This script only sets the secret. You still need to add the workflow file (Step 4 above) to each repository manually or via automation.

### Prerequisites

- [GitHub CLI](https://cli.github.com/) installed and authenticated:
  ```bash
  gh auth login
  ```

### Configuration

1. Create `repos.txt` listing one repository per line (see `repos.txt.example`):
   ```
   your-username/repo-one
   your-username/repo-two
   ```

2. Create a `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```
   Set the following in `.env`:
   ```
   SECRET_NAME=WORKLOG_ACTION_TOKEN
   SECRET_VALUE=ghp_your_token_here
   ```

### Run

```bash
chmod +x sync.sh
./sync.sh
```

The script iterates through `repos.txt` and runs `gh secret set` for each repository.