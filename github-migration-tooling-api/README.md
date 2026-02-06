# GitHub Migration Tooling: GraphQL Edition
This repository contains the automation scripts and GraphQL queries required to migrate repositories from Azure DevOps (ADO) to GitHub Enterprise.

## Project Structure
 * collections/: Postman collections for manual API testing.
 * queries/: Raw .graphql files for version-controlled mutations.
 * scripts/: Automation scripts for bulk migration and identity mapping.

## Prerequisites
  * GitHub PAT: Scopes: repo, admin:org, read:enterprise.
  * Azure DevOps PAT: Scopes: Code (Read & Write).
  * Environment Variables:
        * export GH_PAT="your_github_token"
        * export ADO_PAT="your_ado_token"
        * export ORG_ID="O_kgDOD3SQGQ"
        * export SOURCE_ID="MS_kgDaACQ4MzJiM2M4Yy01ZjUwLTQwMGMtYmY1OC04NDNjYmE4YmIyM2Q"

## Step-by-Step Execution Guide
  * Step 1: Prepare the New Repository Metadata
  - Identify the Azure DevOps repository URL you wish to migrate.
        * ADO Repo: https://dev.azure.com/Mahesh61076963/Project/_git/NewRepoName
        * Target GitHub Name: new-repo-name

  * Step 2: Update the GraphQL Mutation
  - Open queries/03-start-migration.graphql and ensure the parameters are set.

  * Step 3: Execute via Postman (Manual)
    * Import collections/GitHub_Migration.postman_collection.json into Postman.
    * Select the 01-Start-Migration.graphql request.
    * Paste the mutation from your queries/ folder into the Body.
    * Click Send.
    * Copy the id (RM_...) from the response.
    * Select 04-check-status.graphql
    * Once the state is SUCCEEDED, Start 05-generate-mannequin.graphql
  
  * Step 5: Post-Migration Identity Mapping
    * Update scripts/mannequins.csv with the mapping.
    * Run the script: 
            python3 scripts/reclaim_mannequins.py
