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

    comment_body = create_similarity_string(comment_text)

    data = {
        'body': comment_body
    }

    response = requests.post(url, headers=headers, json=data)
    print(response)

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print("Failed to create comment:", response.status_code, response.text)




def create_similarity_string(sorted_results):
    similarity_string = ""

    # Loop through the first 3 elements in sorted_results
    for result in sorted_results[:3]:
        issue_id = result['issueId']
        issue_title = result['issueTitle']
        similarity = result['similarity']
        issue_body = result['issueBody']
        issue_url = result['issueURL']


        similarity_string += f"**Issue ID:** {issue_id}\n"
        similarity_string += f"**Issue Title:** {issue_title}\n"
        similarity_string += f"**Similarity Score:** {similarity:.4f}\n"
        similarity_string += f"\n**Issue URL:** {issue_url}\n"
        similarity_string += f"\n**Issue Body:** {issue_body}\n"
        

        similarity_string += "\n\n\n"

    return similarity_string