
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "true", "ans": "<code>target="_blank"</code>"},
        {"tag": "false", "ans": "<code>href="_newtab"</code>"},
        {"tag": "false", "ans": "<code>open="new"</code>"},
        {"tag": "false", "ans": "<code>newtab="true"</code>"}
    ]

    return data