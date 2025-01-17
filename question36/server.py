
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "&lt;ol&gt;"},
        {"tag": "false", "ans": "&lt;ul&gt;"},
        {"tag": "false", "ans": "&lt;dl&gt;"},
        {"tag": "false", "ans": "&lt;li&gt;"}
    ]

    return data