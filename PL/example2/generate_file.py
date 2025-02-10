import re
from jinja2 import Template
import os
import subprocess
import json
import uuid

def generate_uuid():
    generated_uuid = str(uuid.uuid4())
    print(f"Generated UUID: {generated_uuid}")  # Debugging print
    return generated_uuid


index = 0


# Function to load the content of a file
def load_files(file):
    with open(file, "r") as f:
        return f.read()

# Function to render a template with a given context
def render_files(file, context):
    template = Template(file)
    return template.render(context)

# Function to split template types and store them in a dictionary
def templateType(file):
    dic = {}
    section = re.split("###\n", file)
    for i in section:
        if i != "":
            type, template = i.split("@")
            type.strip()
            dic[type] = template
    return dic

def get_diff():
    """Gets the git diff output to determine added and removed questions."""
    try:
        diff_output = subprocess.check_output(
            ["git", "diff", "--unified=0", "HEAD~1", "PL/example2/question_bank.md"]
        )
        return diff_output.decode("utf-8")
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return ""

def parse_diff(diff):
    """Parses the git diff output to identify added and removed questions."""
    addDic = {}
    removeList = []
    lines = diff.splitlines()
    
    for line in lines:
        if re.match(r"^\+[^+].*?:.*", line):
            key, value = line[1:].split(": ")
            key = key.strip()
            value = value.strip()

            if key in addDic:
                addDic[key].append(value)
            else:
                addDic[key] = [value]
        
        if re.search(r"-id:\s*(\d+)", line):
            match = re.search(r"-id:\s*(\d+)", line)
            id_number = match.group(1)
            removeList.append(id_number)

    return removeList, addDic

def create_data(file):
    """Creates a list of question data from the markdown file."""
    data = []
    pattern = re.compile(r"(###.*?)(?=(?:\n###))", re.DOTALL)
    questions = pattern.findall(file)

    for question in questions:
        dic = {}
        lines = question.split("\n")
        for line in lines:
            if line != "###":
                key, value = line.split(": ")
                dic[key] = value

        data.append(dic)
    return data

def createContext(question):
    """Creates a context dictionary for template rendering."""
    context = {}
    i = 1

    for key in question:
        if question["type"] in ["Drop Down", "Multiple Choice", "Check Box", "String Input"]:
            if "___" in question["question"]:
                question1, question2 = question["question"].split("___")
                context["question"] = question1.strip()
                context["question2"] = question2.strip()
            else:
                context["question"] = question["question"].strip()

            if key not in ["type", "question", "title", "topic", "answer", "id", "tags"]:
                context[f"option{i}"] = question[key]
                context[f"flag{i}"] = "false"
                if key.startswith("*"):  # Mark correct options with *
                    context[f"flag{i}"] = "true"
                i += 1
            
            if key in ["title", "topic", "answer", "id"]:
                context[key] = question[key]
            
            if key == "tags":
                tg = question[key].split(", ")
                context["tags"] = json.dumps(tg)
            
            context["uuid"] = generate_uuid()

    return context

def delete_question_folder(question_id):
    """Deletes question-related files from the root directory."""
    files_to_delete = [
        f"question_{question_id}.html",
        f"question_{question_id}.json",
        f"question_{question_id}.py"
    ]

    for file_path in files_to_delete:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        else:
            print(f"File not found: {file_path}")

def process_questions(data, file, info, question_type, html_file=None, py_file=None):
    """Processes questions and generates necessary files."""
    diff_output = get_diff()
    remove, addDic = parse_diff(diff_output)

    questions = [question for question in data if question["type"] == question_type]

    for question in questions:
        try:
            matches_all = True  # Assume all will match

            for key, values in addDic.items():
                if key in question:
                    if isinstance(question[key], str):
                        if question[key].strip() not in values:
                            print("-----------DEBUGGING START-----------")
                            print(question)
                            print(question[key])
                            print(values)
                            print("-----------DEBUGGING END-----------")
                            matches_all = False  # Found a mismatch
                            break  # No need to check further for this question

            if matches_all:
                context = createContext(question)
            else:
                continue

        except KeyError:
            continue

        if question_type in ["Drop Down", "String Input"] and html_file and py_file:
            generate_file(html_file, info, context, py_file)
        else:
            generate_file(file, info, context)

def createMultipleChoice(data, file, info):
    process_questions(data, file, info, "Multiple Choice")

def createCheckBox(data, file, info):
    process_questions(data, file, info, "Check Box")

def createDropDown(data, html_file, py_file, info):
    process_questions(data, html_file, info, "Drop Down", html_file, py_file)

def createStringInput(data, html_file, py_file, info):
    process_questions(data, html_file, info, "String Input", html_file, py_file)

def generate_file(html_file, info_file, context, py_file=None):
    """Generates question artifacts and saves them in the root directory."""
    html_content = render_files(html_file, context)
    info_content = render_files(info_file, context)

    id = context["id"]

    html_filename = f"question_{id}.html"
    info_filename = f"question_{id}.json"
    py_filename = f"question_{id}.py" if py_file else None

    print(f"Generating files: {html_filename}, {info_filename}, {py_filename if py_file else 'No Python file'}")

    with open(html_filename, "w") as f:
        f.write(html_content)

    with open(info_filename, "w") as f:
        f.write(info_content)

    if py_file:
        py_content = render_files(py_file, context)
        with open(py_filename, "w") as f:
            f.write(py_content)

def main():
    """Main function to process the question bank and generate output files."""
    diff_output = get_diff()
    print(diff_output)
    remove, addDic = parse_diff(diff_output)
    print(remove)
    print(addDic)

    if remove:
        for id in remove:
            delete_question_folder(id)
    
    if not addDic:
        return

    q_bank = load_files("PL/example2/question_bank.md")
    data = create_data(q_bank)

    templates = load_files("PL/example2/template.md")
    typeDic = templateType(templates)
    info = typeDic["IJ"]

    for type, template in typeDic.items():
        if type == "MC":
            createMultipleChoice(data, template, info)
        elif type == "CB":
            createCheckBox(data, template, info)
        elif type == "DD":
            p = re.split("```", template)
            createDropDown(data, p[0], p[1], info)
        elif type == "SI":
            p = re.split("```", template)
            createStringInput(data, p[0], p[1], info)

if __name__ == "__main__":
    main()