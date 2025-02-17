
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "<strong> <p>HTML</p> </strong>"},
        {"tag": "true", "ans": "<p> <strong>HTML</strong> </p>"},
        {"tag": "false", "ans": "<p> <em>HTML</em> </p>"},
        {"tag": "false", "ans": "<p>HTML<p> <strong> </strong>"}
    ]

    return data