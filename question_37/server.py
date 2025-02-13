
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "&lt;"},
        {"tag": "false", "ans": "&gt;"},
        {"tag": "false", "ans": "&copy;"},
        {"tag": "false", "ans": "&amp;"}
    ]

    return data