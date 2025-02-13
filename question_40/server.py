
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "<img>"},
        {"tag": "false", "ans": "<image>"},
        {"tag": "false", "ans": "<media>"},
        {"tag": "false", "ans": "<figure>"}
    ]

    return data