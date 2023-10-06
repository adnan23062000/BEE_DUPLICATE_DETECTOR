from flask import Flask, request
import json
import requests
import jwt
import time

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Hello World'

@app.route('/github', methods=['POST'])
def api_git_msg():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        if 'issue' in data and 'title' in data['issue'] and 'body' in data['issue']:
            issue_title = data['issue']['title']
            issue_body = data['issue']['body']
            print(f"Issue Title: {issue_title}")
            print(f"Issue Body: {issue_body}")

            # Extract repository full name and issue number
            repo_full_name = data['repository']['full_name']
            issue_number = data['issue']['number']

            # Create a comment on the GitHub issue
            create_comment(repo_full_name, issue_number, "test comment")

            return "Issue title and body printed."
        else:
            return "Invalid JSON format; missing issue title or body."
    else:
        return "415 Unsupported Media Type ;)"

def create_comment(repo_full_name, issue_number, comment_text):
    # Construct the API URL based on the extracted details
    # the repo_full_name is in the format "owner/repo"
    url = f'https://api.github.com/repos/{repo_full_name}/issues/{issue_number}/comments'

    # Generate a fine grained access token and give read and write permission to it for issues in order to comment on issues
    private_key = "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"
    
    headers = {
        'Authorization': f'Bearer {private_key}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28'
    }

    data = {
        'body': comment_text
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Comment created successfully.")
    else:
        print("Failed to create comment:", response.status_code, response.text)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
