from flask import Flask, request
from createComment import create_comment
from db_config import db, configure_database
from models import BugReport
from getAllIssues import fetch_repository_issues
from dbOperations import is_bug_report_table_empty, insert_issue_to_db, fetch_all_bug_reports
from textModel import calculate_embeddings, calculate_similarity

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
        repo_full_name = data['repository']['full_name']
        issue_number = data['issue']['number']

        if action == 'opened':
            if not is_bug_report_table_empty():
                id = data['issue']['number']
                title = data['issue']['title']
                body = data['issue']['body']
                embedding = calculate_embeddings(title+body)
                url = data['issue']['html_url']
                bug_reports = fetch_all_bug_reports()
                insert_issue_to_db(id, title, body, url, embedding)
                output = calculate_similarity(body, bug_reports)
                create_comment(repo_full_name, issue_number, output)



            if is_bug_report_table_empty():
                issues_data = fetch_repository_issues(repo_full_name)
                for issue in issues_data:
                    issue_id = issue['number']
                    issue_title = issue['title']
                    issue_body = issue['body']
                    embedding = calculate_embeddings(issue_body)
                    issue_url = issue['html_url']
                    insert_issue_to_db(issue_id, issue_title, issue_body, issue_url, embedding)


            return "Issue title and body printed."

        return "Not a new issue, no action required."
    else:
        return "415 Unsupported Media Type ;)"

if __name__ == '__main__':
    app.run(debug=True, port=5000)