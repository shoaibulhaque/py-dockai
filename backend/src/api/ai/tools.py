from langchain_core.tools import tool

from api.myemailer.sender import send_email
from api.myemailer.inbox_reader import read_inbox
from api.ai.services import generate_email_message


@tool
def research_email(query: str):
    """
    performs research based on query

    Arguments:
    - query: str - Topic of research
    """
    response = generate_email_message(query)
    msg = f"Subject {response.subject}:\nBody: {response.content}"
    return msg


@tool
def send_me_email(subject: str, content: str) -> str:
    """send an email to myself with a subject and content

    Arguments:
    - subject: str - Text subject of the email
    - content: str - Text body content of the email
    """

    try:
        send_email(subject=subject, content=content)

    except:
        return "Not sent"

    return "Sent email"


@tool
def get_unread_email(hours_ago: int = 72) -> str:
    """
    Read all emails from my inbox withing the last N hours

    Arguments:
    - hours_ago: int - Number of hours to look back for unread emails (default: 72 hours)

    Returns:
    A string of emails separated by a line "---"
    """
    try:
        emails = read_inbox(hours_ago=hours_ago, verbose=False)

    except:
        return "Error getting latest emails"

    cleaned = []
    for email in emails:
        print(email)
        data = email.copy()
        if "html_body" in data:
            data.pop("html_body")
        msg = ""
        for k, v in data.items():
            msg += f"{k}:\t{v}"
        cleaned.append(msg)

    return "\n-------\n".join(cleaned)
