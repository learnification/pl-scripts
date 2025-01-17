import re
from jinja2 import Template
import html
import os
import requests
import subprocess 
import time
import shutil

import json

# Function to generate a UUID using an external API
def generate_uuid(retries=3, backoff_factor=0.3):
    url = "https://www.uuidtools.com/api/generate/v4/count/1"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status() # This will raise an HTTPError for bad responses
            uuid = response.json()[0]
            return uuid
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(backoff_factor * (2 ** attempt)) # Exponential back
                
            else:
                raise Exception(f"Failed to generate UUID after {retries} attempts. Last error: {e}")




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
    try:
        diff_output = subprocess.check_output(['git', 'diff', '--unified=0', 'HEAD~1', 'PL/example2/question_bank.md'])
        return diff_output.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"Error running git diff: {e}")
        return ""

def parse_diff(diff):
    addDic = {}
    removeList = []
    lines = diff.splitlines()
    for line in lines:
        
        
       
        if re.match(r'^\+[^+].*?:.*', line):
            
            
            key, value = line[1:].split(": ")
            key = key.strip()
            value = value.strip()
            
            # If the key already exists, append the new value to the list
            if key in addDic:
                addDic[key].append(value)
            else:
                addDic[key] = [value]
        if re.search(r"-id:\s*(\d+)", line):
            match = re.search(r"-id:\s*(\d+)", line)
            id_number = match.group(1)
            removeList.append(id_number)
        
        
        
    
    return removeList, addDic

# Function to create a list of question data from the file content
def create_data(file):
    data = []
    
    pattern = re.compile(r'(###.*?)(?=(?:\n###))', re.DOTALL)
    questions = pattern.findall(file) # Find all sections starting with ###
    for question in questions:
       ## if check(question):
            ##return
        dic = {}
       
        
       
        lines = question.split("\n")
        for line in lines:
            if line != "###":
                key, value = line.split(": ")

               
                
                dic[key] = value
                
        data.append(dic)
       

    return data
        
  
# Function to create a context dictionary for a given question
def createContext(question):
   ## save_question(question["id"].strip())
    
    context = {}
    i = 1
    for key in question:
        
        if question["type"] in ["Drop Down", "Multiple Choice", "Check Box", "String Input"]:

            ##question["question"] = question["question"].replace('<', '&lt;').replace('>', '&gt;')
            if "___" in question["question"]:
                question1, question2 = question["question"].split("___")
                context["question"] = question1.strip()
                context["question2"] = question2.strip()
            else:
                context["question"] = question["question"].strip()

            if key not in ["type", "question", "title", "topic", "answer", "id", "tags"]:
                context[f"option{i}"] = question[key]
                context[f"flag{i}"] = "false"

                if key.startswith("*"): # Check for correct options marked with *
                
                    context[f"flag{i}"] = "true"

            
                i += 1
            if key in ["title", "topic", "answer", "id",]:
                context[key] = question[key]
            if key == "tags":
                tg = question[key].split(", ")
                context["tags"] = json.dumps(tg)
            uuid = generate_uuid()
            
            context["uuid"] = uuid

    return context


def delete_question_folder(question_id):
    folder_path = f"PL/example2/question{question_id}"
    
    print(folder_path)

    

# Function to process questions of a specific type and generate files
def process_questions(data, file, info, question_type, html_file=None, py_file=None):
    diff_output = get_diff()
    
    remove, addDic = parse_diff(diff_output)
    
   
            
    questions = [question for question in data if question["type"] == question_type]


    for question in questions:
        
        try:
        # Check if all key-value pairs in addDic match in the question
            matches_all = True  # Assume all will match unless proven otherwise
        
            for key, values in addDic.items():
                if key in question:
            # Check if the question has the key and matches one of the values in addDic
                    if isinstance(question[key], str): 
                        if question[key].strip() not in values:
                            print(question)
                            print(question[key])
                            print(values)
                            matches_all = False  # Found a mismatch
                            break  # No need to check further for this question

        # If everything matches, process the question
            if matches_all:
                context = createContext(question)  # Process the question
            else:
                continue  # Skip to the next question if there was a mismatch

        except KeyError:
        # Skip this question if a key was missing
            continue
        # Generate file if context is set
        if question_type in ["Drop Down", "String Input"] and html_file and py_file:
            generate_file(html_file, info, context, py_file)
            pass
        else:
            generate_file(file, info, context)
            
           
            
        
        
      
       
        
            

# Function to create multiple choice questions
def createMultipleChoice(data, file, info):
    process_questions(data, file,info, "Multiple Choice")

# Function to create checkbox questions
def createCheckBox(data, file, info):
    process_questions(data, file, info, "Check Box")

# Function to create drop down questions
def createDropDown(data, html_file, py_file, info):
    process_questions(data, html_file,info, "Drop Down", html_file, py_file)

def createStringInput(data, html_file, py_file, info):
    process_questions(data, html_file,info, "String Input", html_file, py_file)

# Function to generate HTML, info, and optionally Python files based on templates
def generate_file(html_file, info_file, context, py_file=None,):

    

    html_content = render_files(html_file, context) # Render HTML content
    info_content = render_files(info_file, context) # Render info content
    
    id = context["id"]
   
    folder_path = f"PL/example2/question{id}"
    
    os.makedirs(folder_path, exist_ok=True) # Create directory for the question
   
    
    if py_file:
       
        py_content = render_files(py_file, context) # Render Python content
        file_path = os.path.join(folder_path, "server.py")
        with open(file_path, "w") as f:
           
            f.write(py_content)
        
    file_path = os.path.join(folder_path, "question.html")
    with open(file_path, "w") as f:
                
        f.write(html_content)
    file_path = os.path.join(folder_path, "info.json")
    with open(file_path, "w") as f:
                
        f.write(info_content)


       
   
# Main function to load files, create data, and generate questions based on templates
def main():
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
  
    q_bank = load_files('PL/example2/question_bank.md')
    data = create_data(q_bank)

    templates = load_files("PL/example2/template.md")
    typeDic = templateType(templates)
    info = typeDic["IJ"]
    for type, template in typeDic.items():
        if type == "MC":
            createMultipleChoice(data, template, info )
        elif type == "CB":
            createCheckBox(data, template, info)
        elif type == "DD":
            
            p = re.split("```", template)
            createDropDown( data, p[0],p[1], info )
        elif type == "SI":

       

            p = re.split("```", template)
            
            createStringInput( data, p[0],p[1], info )
       
       

   

   

if __name__ == "__main__":
    main()

   
