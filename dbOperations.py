from sqlalchemy.exc import OperationalError
from models import BugReport
from db_config import db
import json

def is_bug_report_table_empty():
    try:
        first_bug_report = BugReport.query.first()
        return first_bug_report is None
    except OperationalError:
        return True
    


def insert_issue_to_db(issue_id, issue_title, issue_body, issue_url, embedding):
    try:
        embedding_list = embedding.tolist()
        embedding_json = json.dumps(embedding_list)

        bug_report = BugReport(
            issueId=issue_id,
            issueTitle=issue_title,
            issueBody=issue_body,
            issueURL=issue_url,
            embedding=embedding_json
        )

        db.session.add(bug_report)
        db.session.commit()
        print('post success')
        return True
    except Exception as e:
        print(f"Error inserting data into the database: {str(e)}")
        return False