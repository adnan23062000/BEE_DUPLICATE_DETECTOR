from dbModel import db, BugReport
from sqlalchemy import inspect


def table_exists():
    with db.engine.connect() as connection:
        inspector = inspect(connection)
        return 'bug_report' in inspector.get_table_names()


def insert_bug_report(id, title, body, embeddings, issue_link):
    existing_bug_report = BugReport.query.get(id)
    
    if existing_bug_report is not None:
        return "A row with the same 'id' already exists."

    bug_report = BugReport(id=id, title=title, body=body, embeddings=embeddings, issue_link=issue_link)
    db.session.add(bug_report)
    db.session.commit()

    return "Bug report inserted successfully."


def get_all_bug_reports():
    bug_reports = BugReport.query.all()

    for bug_report in bug_reports:
        print(f'ID: {bug_report.id}')
        print(f'Title: {bug_report.title}')
        print('\n\n')

    return 'Data Fetched successfully.'