
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "&lt;br&gt;"},
        {"tag": "false", "ans": "&lt;p&gt;"},
        {"tag": "false", "ans": "&lt;hr&gt;"},
        {"tag": "false", "ans": "&lt;h1&gt;"}
    ]

    return data