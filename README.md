# Project & Worklog Sync Action

A reusable GitHub Action that automatically syncs `WORKLOG.md` and `PROJECT.md` files from multiple source repositories to a single, centralized repository. 

***

## How It Works 📋

This action is designed to be used in multiple "source" repositories. When triggered, it performs the following steps:

1.  **Detects Changes**: The action runs whenever a push or pull request modifies `WORKLOG.md` or `PROJECT.md` in a source repository.
1.  **Creates a Branch**: It clones the central "target" repository and creates a unique, temporary branch for the incoming update (e.g., `update/my-repo-name-a1b2c3d`).
1.  **Processes Files Conditionally**: It checks which file triggered the workflow:
    * If `WORKLOG.md` was changed, it copies it to the `<destination_path>/worklog/` subdirectory in the target repo.
    * If `PROJECT.md` was changed, it copies it to the `<destination_path>/project/` subdirectory.
1.  **Opens a Pull Request**: Finally, it pushes the new branch and opens a single pull request in the target repository containing all the file changes from the run. This allows you to review and approve the updates before they are merged.

***

## Usage 🚀

To use this action, you need to set up two things: the prerequisites in your target repository and a caller workflow in each source repository.

### ## Prerequisites

1.  **Create a Central Repository**: Designate a GitHub repository that will collect all the synced files.
1.  **Generate a Personal Access Token (PAT)**:
    * Go to **Settings** > **Developer settings** > **Personal access tokens** > **Tokens (classic)**.
    * Generate a new token with the full **`repo`** scope. This is required for the action to create branches and open pull requests.
1.  **Store the PAT as a Secret**:
    * In **each source repository** that will use this action, go to **Settings** > **Secrets and variables** > **Actions**.
    * Create a new repository secret named `SYNC_ACTION_PAT` and paste your PAT as the value.

### ## Caller Workflow Example

In every source repository where you want to monitor `WORKLOG.md` or `PROJECT.md`, create the following file:

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
  pull_request:
    paths:
      - 'WORKLOG.md'
      - 'PROJECT.md'

jobs:
  sync_files_job:
    runs-on: ubuntu-latest
    steps:
      # Step 1: Check out the repository's code so the action can find the files
      - name: Checkout Code
        uses: actions/checkout@v4

      # Step 2: Use the reusable sync action
      -

