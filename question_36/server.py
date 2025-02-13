
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "<ol>"},
        {"tag": "false", "ans": "<ul>"},
        {"tag": "false", "ans": "<dl>"},
        {"tag": "false", "ans": "<li>"}
    ]

    return data