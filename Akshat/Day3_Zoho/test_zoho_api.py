import os
import requests
import json


from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

CLIENT_ID = os.environ.get("ZOHO_CLIENT_ID")
CLIENT_SECRET = os.environ.get("ZOHO_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("ZOHO_REFRESH_TOKEN")
DOMAIN = os.environ.get("ZOHO_DC", "in")

def get_access_token():
    """Generates a short-lived access token using the refresh token."""
    url = f"https://accounts.zoho.{DOMAIN}/oauth/v2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json().get("access_token")

def test_zoho_books_invoices(access_token):
    """Fetches the list of invoices from Zoho Books."""
    url = f"https://www.zohoapis.{DOMAIN}/books/v3/invoices"
    headers = {"Authorization": f"Zoho-oauthtoken {access_token}"}
    
    # Intentionally omitting organization_id to see if Zoho defaults to the only org
    print("\n--- Testing Zoho Books: /invoices ---")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed: {response.text}")
        return
        
    data = response.json()
    print("Success! Connection to Zoho Books established.")
    print(f"Total Invoices found: {len(data.get('invoices', []))}")
    if data.get('invoices'):
        print("\nSample Data (First Invoice):")
        print(json.dumps(data['invoices'][0], indent=2))

if __name__ == "__main__":
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN]):
        print("Missing Zoho credentials in .env file.")
        exit(1)
        
    try:
        print("Generating Access Token...")
        access_token = get_access_token()
        print("Access Token generated successfully!")
        
        test_zoho_books_invoices(access_token)
        
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
