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

    response_text = create_similarity_string(comment_text)
    comment_body = response_text[0]
    isDuplicate = response_text[1]

    print("-------------------")
    print(comment_body)
    print("-------------------")
    print(isDuplicate)
    print("-------------------")

    if(isDuplicate):
        create_label(repo_full_name, issue_number)

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
    similarity_string = "The most similar 3 bug report issues are given below:\n\n\n"

    isDuplicate = False
    # Loop through the first 3 elements in sorted_results
    for result in sorted_results[:3]:
        issue_id = result['issueId']
        issue_title = result['issueTitle']
        similarity = result['similarity'] * 100
        issue_body = result['issueBody']
        issue_url = result['issueURL']

        if similarity > 85:
            isDuplicate = True

        similarity_string += f"**Issue ID:** {issue_id}\n"
        similarity_string += f"**Issue Title:** {issue_title}\n"
        similarity_string += f"**Similarity Score:** {similarity:.2f}%\n"
        similarity_string += f"**Issue URL:** {issue_url}\n"
        

        similarity_string += "\n\n\n"

    
    print(similarity_string)

    return similarity_string, isDuplicate



def create_label(repo_full_name, issue_number):
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/labels'

    private_key = os.environ.get('GITHUB_PRIVATE_KEY')

    if private_key is None:
        raise ValueError("GitHub private key is not set in the .env file")

    headers = {
        'Authorization': f'Bearer {private_key}',
        'Accept': 'application/vnd.github.v3+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    label_name = "Duplicate"

    data = {
        'labels': [label_name]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print(f"Label '{label_name}' created successfully on issue #{issue_number}.")
    else:
        print(f"Failed to create label '{label_name}':", response.status_code, response.text)