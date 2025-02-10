
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "<br>"},
        {"tag": "false", "ans": "<p>"},
        {"tag": "false", "ans": "<hr>"},
        {"tag": "false", "ans": "<h1>"}
    ]

    return data