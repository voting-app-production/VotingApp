import csv
import requests
import os

def reclaim_users(csv_path):
    token = os.getenv("GH_PAT")
    org_name = "voting-app-production" 
    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Get the Organization ID
    org_query = f'{{ organization(login: "{org_name}") {{ id }} }}'
    org_resp = requests.post(url, json={'query': org_query}, headers=headers).json()
    org_id = org_resp['data']['organization']['id']

    with open(csv_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader((line.replace(' ', '') for line in file))
        for row in reader:
            target_username = row['target-user']
            print(f"🔄 Processing {target_username}...")

            # 2. Convert Username to Global Node ID
            user_query = f'{{ user(login: "{target_username}") {{ id }} }}'
            user_resp = requests.post(url, json={'query': user_query}, headers=headers).json()
            
            if 'errors' in user_resp:
                print(f"❌ Could not find GitHub user: {target_username}")
                continue
            
            target_node_id = user_resp['data']['user']['id']

            # 3. Run the Reclamation Mutation
            reclaim_mutation = """
            mutation($orgId: ID!, $mannequinId: ID!, $targetUserId: ID!) {
              createAttributionInvitation(input: {
                ownerId: $orgId,
                sourceId: $mannequinId,
                targetId: $targetUserId
              }) {
                source { ... on Mannequin { login } }
                target { ... on User { login } }
              }
            }
            """
            
            variables = {
                "orgId": org_id,
                "mannequinId": row['mannequin-id'],
                "targetUserId": target_node_id # Now sending the ID, not the name
            }

            response = requests.post(url, json={'query': reclaim_mutation, 'variables': variables}, headers=headers)
            result = response.json()

            if "errors" in result:
                print(f"❌ Failed for {row['mannequin-user']}: {result['errors'][0]['message']}")
            else:
                print(f"✅ Success! Invitation sent to {target_username}")

if __name__ == "__main__":
    reclaim_users("mannequins.csv")