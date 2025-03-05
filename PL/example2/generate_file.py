import re
from jinja2 import Template
import os
import subprocess
import json
import uuid
import argparse  # Import argparse for handling command-line arguments

def generate_uuid():
    generated_uuid = str(uuid.uuid4())
    print(f"Generated UUID: {generated_uuid}")  # Debugging print
    return generated_uuid

# Function to load the content of a file
def load_files(file):
    with open(file, "r") as f:
        return f.read()

# Function to render a template with a given context
def render_files(file, context):
    template = Template(file)
    return template.render(context)

# Function to create a dictionary of question data from the markdown file
def create_data(file):
    data = []
    pattern = re.compile(r"(###.*?)(?=(?:\n###))", re.DOTALL)
    questions = pattern.findall(file)

    for question in questions:
        dic = {}
        lines = question.strip().split("\n")

        for line in lines:
            if line.strip() and line.strip() != "###":
                parts = line.split(": ", 1)  # Split only on first occurrence
                
                if len(parts) == 2:
                    key, value = parts
                    dic[key.strip()] = value.strip()
        
        if dic:
            data.append(dic)

    return data

# Function to delete a question's folder
def delete_question_folder(question_id):
    """Deletes the folder and its contents for a specific question."""
    folder_path = f"question_{question_id}"

    if os.path.exists(folder_path):
        subprocess.run(["rm", "-rf", folder_path])  # Deletes the folder
        print(f"Deleted folder: {folder_path}")
    else:
        print(f"Folder not found: {folder_path}")

# Function to create the question's context for template rendering
def createContext(question):
    context = {}
    i = 1

    for key in question:
        if question["type"] not in [ "Drop Down", "String Input"] or key == 'question':
            question[key].replace("<", "&lt;").replace(">", "&gt;")
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

# Function to generate question files
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

def templateType(file_content):
    """Splits template types and stores them in a dictionary."""
    dic = {}
    sections = re.split(r"###\n", file_content)  # Split based on '###\n'
    
    for section in sections:
        if section.strip():
            parts = section.split("@", 1)  # Split at the first '@' only
            if len(parts) == 2:
                type_name = parts[0].strip()
                template_content = parts[1].strip()
                dic[type_name] = template_content
    return dic

# Main function
def main():
    """Main function to process and regenerate questions."""
    parser = argparse.ArgumentParser(description="Generate or regenerate questions.")
    parser.add_argument("-regenerate", nargs="?", default=None, help="Regenerate a specific question or all (use 'all').")

    args = parser.parse_args()
    regenerate_id = args.regenerate  # Get the argument value

    q_bank = load_files("PL/example2/question_bank.md")
    data = create_data(q_bank)

    templates = load_files("PL/example2/template.md")
    typeDic = templateType(templates)  # Ensure this line exists
    info = typeDic.get("IJ", "")  # Get the 'IJ' template if it exists

    if regenerate_id:
        if regenerate_id.lower() == "all":
            print("♻️ Regenerating ALL questions...")
            for question in data:
                delete_question_folder(question["id"])
        else:
            try:
                question_id = int(regenerate_id)
                delete_question_folder(question_id)
                print(f"♻️ Regenerating question ID {question_id}...")
                data = [q for q in data if q["id"] == str(question_id)]
            except ValueError:
                print(f"❌ Invalid question ID: {regenerate_id}")
                return

    # Process each question type
    for question in data:
        q_type = question["type"]
        context = createContext(question)

        if q_type in ["Multiple Choice"]:
            generate_file(typeDic["MC"], info, context)
        elif q_type in ["Check Box"]:
            generate_file(typeDic["CB"], info, context)
        elif q_type in ["Drop Down"]:
            p = re.split("```", typeDic["DD"])
            generate_file(p[0], info, context, p[1])
        elif q_type in ["String Input"]:
            p = re.split("```", typeDic["SI"])
            generate_file(p[0], info, context, p[1])

    print("✅ Processing complete!")

if __name__ == "__main__":
    main()
