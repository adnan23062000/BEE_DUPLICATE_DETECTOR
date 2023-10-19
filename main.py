from flask import Flask, request
import sqlalchemy
from createComment import create_comment
from db_config import configure_database
from models import BugReport

app = Flask(__name__)

configure_database(app)


@app.route('/')
def api_root():
    return 'Hello World'

@app.route('/github', methods=['POST'])
def api_git_msg():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        action = data.get('action', '')

        if action == 'opened':
            issue_title = data['issue']['title']
            issue_body = data['issue']['body']
            print(f"Issue Title: {issue_title}")
            print(f"Issue Body: {issue_body}")

            repo_full_name = data['repository']['full_name']
            issue_number = data['issue']['number']

            # Create a comment on the GitHub issue
            create_comment(repo_full_name, issue_number, "test comment")

            return "Issue title and body printed."

        return "Not a new issue, no action required."
    else:
        return "415 Unsupported Media Type ;)"

if __name__ == '__main__':
    app.run(debug=True, port=5000)