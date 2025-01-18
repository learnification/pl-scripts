
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "font-family"},
        {"tag": "false", "ans": "font-size"},
        {"tag": "false", "ans": "font-style"},
        {"tag": "false", "ans": "font-variant"}
    ]

    return data