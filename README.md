# VotingApp Migration: Azure DevOps to GitHub Enterprise

This repository represents the successful migration of the VotingApp from Azure DevOps (ADO) to GitHub Enterprise (GHE). This document summarizes the technical steps taken to move the source code, preserve history, and maintain CI/CD continuity.

# Prerequisites
- Azure DevOps: * Access Level: Basic access or higher in the source organization.
    * Permissions: Project Administrator or Build Administrator (to configure Service Connections and Pipelines)

- GitHub Enterprise:
    * Role: Organization Owner or a user with the Migrator role in the voting-app-production organization.

Permissions: Project Administrator or Build Administrator (to configure Service Connections and Pipelines)
# Migration Overview
- Source: Azure DevOps Services [VotingApp Project](https://dev.azure.com/Mahesh61076963/VotingApp)
- Destination: GitHub Enterprise [voting-app-production]https://github.com/enterprises/mahesh-migration-sandbox/organizations
- Strategy: Hybrid Migration (GitHub for Source, Azure DevOps & Actions for CI/CD)

# Steps:
## 1. Installations & configuration
 - GitHub CLI
 - GEI Extension
    * gh extension install github/gh-ado2gh

 - Personal Access Tokens (PATs)
    * ADO PAT: Needs Code (Read/Write/Manage) and Identity (Read)
    * GitHub PAT: Needs repo, workflow, and admin:org 

## 2. Migration
#### Set your environment variables (Replace the values in quotes)
export GH_PAT="<ghp_your_github_token_here>"
export ADO_PAT="<your_ado_token_here>"

#### Perform the migration
--wait ensures the terminal stays open until the migration finishes

* gh ado2gh migrate-repo \
    --ado-org "<ADO_ORG>" \
    --ado-team-project "<ADO_PROJECT>" \
    --ado-repo "<ADO_REPO>" \
    --github-org "<GH_ORG>" \
    --github-repo "<GH_REPO>" \
    --wait

* sample screen of success message 
 ![Alt Text](images/Migration-success-msg.png)

## 3. Reclaiming Mannequin
- A mannequin is a placeholder identity used by the GitHub Enterprise Importer. It preserves the history of who did what in Azure DevOps, but it isn't linked to a real GitHub account yet.

#### Generate a Mannequin List
- Basically getting the list of users associated with the Repo
- Generate the list in CSV with below command

* gh ado2gh generate-mannequin-csv \
    --github-org "<GH_ORG>" \
    --output mannequins.csv

- Edit mannequins.csv with target-user as GitHub username

*  gh ado2gh reclaim-mannequin \
    --github-org "<GH_ORG>" \
    --csv mannequins.csv

- Sample screen of successful mannequin reclaim
 ![Alt Text](images/mannequin-reclaim-success-msg.png)

- For Security reason it has to be re-atrributes and approved. You finally see githu user details on commit history and other places.
![Alt Text](images/Github-user-details.png)

## 4. ADO Pipeline rewiring
- To ensure zero downtime for the build process, we "rewired" our existing Azure Pipelines to listen to the new GitHub repository
- Integration: Installed the [Azure Pipelines GitHub App](https://github.com/marketplace/azure-pipelines).
- Result: Every commit pushed to GitHub now triggers action on azo pipeline.

- Sample screen of successful mannequin reclaim
  ![Alt Text](images/pipeline-rewiring.png)