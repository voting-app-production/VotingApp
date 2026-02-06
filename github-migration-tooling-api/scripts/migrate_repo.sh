#!/bin/bash
# Usage: ./migrate_repo.sh <repo_name>

QUERY=$(cat <<EOF
mutation {
  startRepositoryMigration(input: {
    sourceId: "$SOURCE_ID",
    sourceRepositoryUrl: "https://dev.azure.com/org/proj/_git/$1",
    repositoryName: "$1",
    ownerId: "$ORG_ID",
    accessToken: "$ADO_PAT",
    githubPat: "$GH_PAT",
    targetRepoVisibility: "public"
  }) {
    repositoryMigration { id state }
  }
}
EOF
)

curl -H "Authorization: Bearer $GH_PAT" \
     -X POST -d "{\"query\": \"$QUERY\"}" \
     https://api.github.com/graphql