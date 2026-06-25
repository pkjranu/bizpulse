import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_salesforce_token():
    url = "https://nagarro227-dev-ed.develop.my.salesforce.com/services/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': os.environ.get('SF_CONSUMER_KEY'),
        'client_secret': os.environ.get('SF_CONSUMER_SECRET'),
    }
    response = requests.post(url, data=payload)
    data = response.json()
    print("Auth response:", data)
    return data.get('access_token'), data.get('instance_url')

def query_salesforce(token, instance_url, query):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = f"{instance_url}/services/data/v59.0/query"
    response = requests.get(url, headers=headers, params={'q': query})
    return response.json()

token, instance_url = get_salesforce_token()
if token:
    print("✅ Connected to Salesforce!")
    result = query_salesforce(token, instance_url,
        "SELECT Id, Name, Amount, StageName FROM Opportunity LIMIT 5")
    print(f"Opportunities: {result.get('totalSize', 0)}")
    for opp in result.get('records', []):
        print(f"  - {opp['Name']}: ${opp['Amount']} ({opp['StageName']})")
else:
    print("❌ Failed - no token received")