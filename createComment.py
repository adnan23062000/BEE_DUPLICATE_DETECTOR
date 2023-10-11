import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_comment(repo_full_name, issue_number, comment_text):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'

    private_key = os.environ.get('GITHUB_PRIVATE_KEY')

    if private_key is None:
        raise ValueError("GitHub private key is not set in the .env file")

    headers = {
        'Authorization': f'Bearer {private_key}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    data = {
        'body': comment_text
    }

    response = requests.post(url, headers=headers, json=data)
    print(response)

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print("Failed to create comment:", response.status_code, response.text)
