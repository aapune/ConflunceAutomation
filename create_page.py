import requests
import json
from requests.auth import HTTPBasicAuth

def create_confluence_page(base_url, username, api_token, space_key, title, parent_id=None):
    """
    Create a blank page in Confluence using REST API
    
    Parameters:
    base_url (str): Your Confluence base URL (e.g., 'https://your-domain.atlassian.net/wiki')
    username (str): Your Confluence username (email)
    api_token (str): Your Confluence API token
    space_key (str): The key of the space where the page will be created
    title (str): The title of the new page
    parent_id (str, optional): ID of the parent page if you want to create it as a child page
    
    Returns:
    dict: Response from the API containing the created page details
    """
    
    # API endpoint for creating pages
    api_endpoint = f"{base_url}/rest/api/content"
    
    # Basic page content structure
    page_data = {
        "type": "page",
        "title": title,
        "space": {
            "key": space_key
        },
        "body": {
            "storage": {
                "value": " ",  # Blank content
                "representation": "storage"
            }
        }
    }
    
    # Add parent page reference if provided
    if parent_id:
        page_data["ancestors"] = [{"id": parent_id}]
    
    # Headers for the request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    try:
        # Make the API request
        response = requests.post(
            api_endpoint,
            auth=HTTPBasicAuth(username, api_token),
            headers=headers,
            json=page_data
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating page: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Replace these with your actual values
    CONFLUENCE_BASE_URL = "https://your-domain.atlassian.net/wiki"
    USERNAME = "your-email@domain.com"
    API_TOKEN = "your-api-token"
    SPACE_KEY = "SPACEKEY"
    PAGE_TITLE = "My New Blank Page"
    
    # Optional: Parent page ID if you want to create the page as a child
    PARENT_ID = None
    
    result = create_confluence_page(
        CONFLUENCE_BASE_URL,
        USERNAME,
        API_TOKEN,
        SPACE_KEY,
        PAGE_TITLE,
        PARENT_ID
    )
    
    if result:
        print(f"Page created successfully! Page ID: {result['id']}")
        print(f"Page URL: {result['_links']['base'] + result['_links']['webui']}")
    else:
        print("Failed to create page.")