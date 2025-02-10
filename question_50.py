
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "rgb(255, 0, 0)"},
        {"tag": "false", "ans": "hsl(120, 100%, 50%)"},
        {"tag": "false", "ans": "#0000ff"},
        {"tag": "false", "ans": "None of the above"}
    ]

    return data