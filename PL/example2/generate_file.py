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
    """Parses the git diff output to identify added, removed, and modified questions."""
    addDic = {}       # Stores newly added questions
    removeList = []   # Stores removed question IDs
    modifiedList = [] # Stores modified question IDs

    lines = diff.splitlines()
    
    added_ids = set()
    removed_ids = set()

    for line in lines:
        # Detect added lines
        if re.match(r"^\+[^+].*?:.*", line):
            parts = line[1:].split(": ", 1)  # Split on the first occurrence only
            if len(parts) == 2:  # Ensure valid key-value pair
                key, value = parts
                key = key.strip()
                value = value.strip()

                if key == "id":
                    added_ids.add(value)  # Track added question ID

                if key in addDic:
                    addDic[key].append(value)
                else:
                    addDic[key] = [value]            
            key = key.strip()
            value = value.strip()

            if key == "id":
                added_ids.add(value)  # Track added question ID

            if key in addDic:
                addDic[key].append(value)
            else:
                addDic[key] = [value]
        
        # Detect removed question IDs
        if re.search(r"-id:\s*(\d+)", line):
            match = re.search(r"-id:\s*(\d+)", line)
            id_number = match.group(1)
            removed_ids.add(id_number)
            removeList.append(id_number)

    # Identify modified questions: If an ID is both removed & added, it was modified
    modifiedList = list(added_ids & removed_ids)

    return removeList, addDic, modifiedList

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
    remove, addDic, modified = parse_diff(diff_output)
    
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
    """Generates question artifacts and saves them in their respective folders."""
    html_content = render_files(html_file, context)
    info_content = render_files(info_file, context)

    id = context["id"]
    folder_path = f"question_{id}"  # Each question has its own folder

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    print(f"Generating files in: {folder_path}")

    # Define file paths inside the folder
    html_filename = os.path.join(folder_path, "question.html")
    info_filename = os.path.join(folder_path, "info.json")
    py_filename = os.path.join(folder_path, "server.py") if py_file else None

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
    print("Git diff output:")
    print(diff_output)

    # Parse added, removed, and modified questions
    remove, addDic, modified = parse_diff(diff_output)

    print(f"Removed questions: {remove}")
    print(f"Added questions: {list(addDic.keys())}")  # Only keys for debugging
    print(f"Modified questions: {modified}")

    # Delete removed questions
    if remove:
        for id in remove:
            delete_question_folder(id)

    # Delete & regenerate modified questions
    if modified:
        for id in modified:
            delete_question_folder(id)  # Delete old folder
            print(f"Regenerating modified question: {id}")

    # If there are no new or modified questions, exit
    if not addDic and not modified:
        print("No new or modified questions detected. Exiting.")
        return

    # Load question bank
    q_bank = load_files("PL/example2/question_bank.md")
    data = create_data(q_bank)

    # Load templates
    templates = load_files("PL/example2/template.md")
    typeDic = templateType(templates)
    info = typeDic["IJ"]

    # Process each question type
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

    print("✅ Processing complete!")

if __name__ == "__main__":
    main()