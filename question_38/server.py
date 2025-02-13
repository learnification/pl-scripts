
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "<div>"},
        {"tag": "false", "ans": "<span>"},
        {"tag": "false", "ans": "<section>"},
        {"tag": "false", "ans": "<p>"}
    ]

    return data