
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "src "},
        {"tag": "true", "ans": "href "},
        {"tag": "false", "ans": "alt "},
        {"tag": "false", "ans": "title"}
    ]

    return data