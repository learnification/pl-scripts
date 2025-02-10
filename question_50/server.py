
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "<code>rgb(255, 0, 0)</code>"},
        {"tag": "false", "ans": "<code>hsl(120, 100%, 50%)</code>"},
        {"tag": "false", "ans": "<code>#0000ff</code>"},
        {"tag": "false", "ans": "<code>None of the options</code>"}
    ]

    return data