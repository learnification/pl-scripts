
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "selector"},
        {"tag": "false", "ans": "size"},
        {"tag": "false", "ans": "distance"},
        {"tag": "true", "ans": "value"}
    ]

    return data