
def generate(data):

    QUESTION1 = "HTML1"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "Inside the main content area"},
        {"tag": "true", "ans": "As the title in the browser tab, bookmarks, and search engine results"},
        {"tag": "false", "ans": "As the title"},
        {"tag": "false", "ans": "At the beginning of each paragraph"}
    ]

    return data