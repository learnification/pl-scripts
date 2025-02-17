
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "It creates a line break in the text"},
        {"tag": "false", "ans": "It has no content without a closing tag"},
        {"tag": "true", "ans": "It must be placed within a <p> tag"},
        {"tag": "false", "ans": "It does not have an end tag"}
    ]

    return data