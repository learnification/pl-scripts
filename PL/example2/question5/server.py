
def generate(data):

    QUESTION1 = "HTML"

    data["params"][QUESTION1] = [
        {"tag": "false", "ans": "Style"},
        {"tag": "false", "ans": "Name"},
        {"tag": "true", "ans": "Id"},
        {"tag": "false", "ans": "Class"}
    ]

    return data