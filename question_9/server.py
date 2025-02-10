
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "<code>&lt;br&gt;</code>"},
        {"tag": "false", "ans": "<code>&lt;p&gt;</code>"},
        {"tag": "false", "ans": "<code>&lt;hr&gt;</code>"},
        {"tag": "false", "ans": "<code>&lt;h1&gt;</code>"}
    ]

    return data