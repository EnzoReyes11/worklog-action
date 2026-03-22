#!/bin/bash

# Load environment variables from .env if it exists
if [ -f .env ]; then
  # Load each line from .env, ignoring comments and exporting the variables
  export $(grep -v '^#' .env | xargs)
fi

# Secret configuration (if not set in .env or environment, fallback to defaults)
SECRET_NAME=${SECRET_NAME:-"WORKLOG_ACTION_PAT"}
# SECRET_VALUE must be provided via the environment
if [ -z "$SECRET_VALUE" ]; then
    echo "Error: SECRET_VALUE is not set. Please set it in your .env file or environment."
    exit 1
fi

# Read repository list from a file (e.g., repos.txt)
while IFS= read -r REPO; do
    echo "Adding secret $SECRET_NAME to $REPO..."
    # Use gh secret set with the --repo flag
    # The --body flag is used to pass the secret value directly
    gh secret set $SECRET_NAME --repo $REPO --body "$SECRET_VALUE"
    if [ $? -eq 0 ]; then
        echo "Successfully added secret to $REPO"
    else
        echo "Failed to add secret to $REPO"
    fi
done < repos.txt
