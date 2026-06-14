import requests
import json
import argparse

def get_page_insights(page_id, access_token, metric="page_impressions", period="day"):
    """
    Fetches insights for a given Facebook Page.
    """
    url = f"https://graph.facebook.com/v19.0/{page_id}/insights"
    
    params = {
        'metric': metric,
        'period': period,
        'access_token': access_token
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        data = response.json()
        print("\n=== Meta Page Insights Data ===")
        print(json.dumps(data, indent=2))
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"\nError fetching data from Meta API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response details: {e.response.text}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test Meta Graph API /insights endpoint.')
    parser.add_argument('--page-id', required=True, help='Your Facebook Page ID')
    parser.add_argument('--token', required=True, help='Your long-lived Page Access Token')
    parser.add_argument('--metric', default='page_impressions', help='Metric to query (default: page_impressions)')
    
    args = parser.parse_args()
    
    get_page_insights(args.page_id, args.token, args.metric)
