
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "text-color"},
        {"tag": "false", "ans": "background-color"},
        {"tag": "false", "ans": "font-color"},
        {"tag": "true", "ans": "color"}
    ]

    return data