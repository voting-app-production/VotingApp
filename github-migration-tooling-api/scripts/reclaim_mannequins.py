import csv
import requests
import os

# High-level logic:
# 1. Open the mapping CSV.
# 2. For each row, grab the 'Mannequin ID' and the 'Target GitHub User'.
# 3. Send a POST request to the 'reclaim' endpoint.

def reclaim_users(csv_path):
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Logic to call GitHub GraphQL Mutation 'reclaimMannequin'
            print(f"Mapping {row['login']} to {row['github_user']}")
            # API request goes here...

if __name__ == "__main__":
    reclaim_users("mannequins.csv")