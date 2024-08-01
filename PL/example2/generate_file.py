import re
from jinja2 import Template
import html
import os
import requests
import time

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

# Function to create a list of question data from the file content
def create_data(file):
    data = []
    
    pattern = re.compile(r'(###.*?)(?=(?:\n###))', re.DOTALL)
    questions = pattern.findall(file) # Find all sections starting with ###
    for question in questions:
        if check(question):
            return
        dic = {}
       
        
       
        lines = question.split("\n")
        for line in lines:
            if line != "###":
                key, value = line.split(": ")
                
                dic[key] = value
                
        data.append(dic)
       

    return data

def save_question(question):
    with open("uuid.txt", "a") as f:
                
        f.write(f"{question}\n")

def check(question):
    file = load_files("PL/example2/uuid.txt")
    list = file.split("\n")
    for q in list:
        if q.strip() == question:
            return True
    return False
    
        
    


# Function to create a context dictionary for a given question
def createContext(question):
    save_question(question["question"].strip())
    
    context = {}
    i = 1
    for key in question:
        print(key)
        
        if question["type"] in ["Drop Down", "Multiple Choice", "Check Box", "String Input"]:

            question["question"] = question["question"].replace('<', '&lt;').replace('>', '&gt;')
            if "___" in question["question"]:
                question1, question2 = question["question"].split("___")
                context["question1"] = question1.strip()
                context["question2"] = question2.strip()
            else:
                context["question"] = question["question"].strip()

            if key not in ["type", "question", "title", "topic", "answer"]:
                context[f"option{i}"] = question[key]
                context[f"flag{i}"] = "false"

                if key.startswith("*"): # Check for correct options marked with *
                
                    context[f"flag{i}"] = "true"

            
                i += 1
            if key in ["title", "topic", "answer"]:
                context[key] = question[key]
            uuid = generate_uuid()
            
            context["uuid"] = uuid
           
          

    return context

# Function to process questions of a specific type and generate files
def process_questions(data, file, info, question_type, html_file=None, py_file=None):
    questions = [question for question in data if question["type"] == question_type]

   
        
    
    for question in questions:
        
        q = question["question"].strip()
        print(check(q))
        if check(q):
            continue
        context = createContext(question)
        
      
        # For Drop Down questions, generate an additional file if specified
        if question_type in ["Drop Down, String Input"] and html_file and py_file:
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
    
    global index 
    index += 1
   
    folder_path = f"PL/example2/question{index}"
    
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

   
