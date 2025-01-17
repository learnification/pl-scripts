
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "target="_blank""},
        {"tag": "false", "ans": "href="_newtab""},
        {"tag": "false", "ans": "open="new""},
        {"tag": "false", "ans": "newtab="true""}
    ]

    return data