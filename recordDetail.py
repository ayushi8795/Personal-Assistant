from config import personalConfig
import resend

def record_user_details(email, name ="notProvided", notes="notProvided"):
    send_alert (
        subject = "New Interested User — Personal Assistant",
        message = f"Email: {email}\nName: {name}\nNotes: {notes}"
    )
    return {"recorded":"OK"}

def record_Unkonwn_questions(email, question, name ="notProvided"):
    send_alert (
        subject = "Unknown Question Asked — Personal Assistant",
        message = f"Email: {email}\nName: {name}\nQuestion: {question}",
    )
    return {"recorded":"OK"}


def  send_alert(subject:str, message:str, priority:str = "default"):
    resend.api_key = personalConfig.RESEND_API_KEY
    sender = str(personalConfig.RESEND_EMAIL_DEFAULT_SENDER)
    receiver = str(personalConfig.RECEIVER_EMAIL)

    response = resend.Emails.send(
        {
            "from": sender,
            "to": receiver,
            "subject": subject,
            "html": message
        }
    )


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name":  {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {"type": "string", "description": "Any additional context worth recording"},
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_Unkonwn_questions",
    "description": "Always use this tool to record any question that couldn't be answered",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of the user who asked the question"},
            "name":  {"type": "string", "description": "The user's name, if they provided it"},
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["email", "question"],
        "additionalProperties": False,
    },
}
   