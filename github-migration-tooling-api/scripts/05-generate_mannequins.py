import requests
import csv
import os

def load_env_file(filepath):
    """Loads variables from your migrate_repo.env file"""
    if os.path.exists(filepath):
        with open(filepath) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    line = line.replace("export ", "").strip()
                    if "=" in line:
                        key, value = line.split("=", 1)
                        os.environ[key] = value.strip('"').strip("'")

def fetch_mannequins():
    # 1. Load settings
    load_env_file("migrate_repo.env")
    token = os.getenv("GH_PAT")
    org_name = os.getenv("GITHUB_ORG_NAME")
    
    if not token or not org_name:
        print("❌ Error: GH_PAT or GITHUB_ORG_NAME not found in env file.")
        return

    url = "https://api.github.com/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    # 2. GraphQL Query
    query = """
    query($org: String!) {
      organization(login: $org) {
        mannequins(first: 100) {
          nodes {
            id
            login
          }
        }
      }
    }
    """
    
    variables = {"org": org_name}
    
    print(f"🔍 Fetching mannequins for {org_name}...")
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    data = response.json()

    if "errors" in data:
        print(f"❌ Error: {data['errors'][0]['message']}")
        return

    mannequins = data['data']['organization']['mannequins']['nodes']

    if not mannequins:
        print("⚠️ No mannequins found. This usually means all users are already linked.")
        return

    # 3. Write to CSV
    # We provide placeholders for target-user so you can fill them in
    with open('mannequins.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['mannequin-user', 'mannequin-id', 'target-user'])
        
        for m in mannequins:
            writer.writerow([m['login'], m['id'], '']) # Leave target-user blank for you to fill

    print(f"✅ Created mannequins.csv with {len(mannequins)} entries.")
    print("👉 Now, open mannequins.csv and add the GitHub usernames to the 'target-user' column.")

if __name__ == "__main__":
    fetch_mannequins()