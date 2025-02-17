
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "p { }"},
        {"tag": "false", "ans": ".p { }"},
        {"tag": "false", "ans": "#p { }"},
        {"tag": "false", "ans": "p() { }"}
    ]

    return data