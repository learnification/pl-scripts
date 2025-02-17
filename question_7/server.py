
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "To refresh the web page every specified number of seconds"},
        {"tag": "false", "ans": "To set keywords for search engine optimization"},
        {"tag": "true", "ans": "To provide a brief summary of the web page’s content"},
        {"tag": "false", "ans": "To define the author of a page"}
    ]

    return data