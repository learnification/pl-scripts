import re
from jinja2 import Template
import html
import os
import requests
def generate_uuid():
    url = "https://www.uuidtools.com/api/generate/v4/count/1"
    response = requests.get(url)
    if response.status_code == 200:
        uuid = response.json()[0]
        return uuid
    else:
        raise Exception(f"Failed to generate UUID. Status code: {response.status_code}")

index = 0
def load_files(file):
    with open(file, "r") as f:
        return f.read()
    
def render_files(file, context):
    template = Template(file)
    return template.render(context)

def templateType(file):
    dic = {}
    
    
    section = re.split("###\n", file)
    for i in section:
        if i != "":

            type, template = i.split("@")
            type.strip()
            dic[type] = template
    return dic

def create_data(file):
    data = []
    pattern = re.compile(r'(###.*?)(?=(?:\n###))', re.DOTALL)
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
    context = {}
    i = 1
    for key in question:
        question[key] = question[key].replace('<', '&lt;').replace('>', '&gt;')
        if question["type"] in ["Drop Down", "Multiple Choice", "Check Box"]:
            if "___" in question["question"]:
                question1, question2 = question["question"].split("___")
                context["question1"] = question1.strip()
                context["question2"] = question2.strip()
            else:
                context["question"] = question["question"].strip()

            if key not in ["type", "question", "title", "topic"]:
                context[f"option{i}"] = question[key]
                context[f"flag{i}"] = "false"

                if key.startswith("*"):
                
                    context[f"flag{i}"] = "true"

            
                i += 1
            if key in ["title", "topic"]:
                context[key] = question[key]
            uuid = generate_uuid()
            context["uuid"] = uuid

    return context


def process_questions(data, file, info, question_type, html_file=None, py_file=None):
    questions = [question for question in data if question["type"] == question_type]
    
    for question in questions:
        context = createContext(question)
        generate_file(file, info, context)
        
        # For Drop Down questions, generate an additional file if specified
        if question_type == "Drop Down" and html_file and py_file:
            generate_file(html_file, info, context, py_file)
            

# Usage example
def createMultipleChoice(data, file, info):
    process_questions(data, file,info, "Multiple Choice")

def createCheckBox(data, file, info):
    process_questions(data, file, info, "Check Box")

def createDropDown(data, html_file, py_file, info):
    process_questions(data, html_file,info, "Drop Down", html_file, py_file)


def generate_file(html_file, info_file, context, py_file=None,):

    html_content = render_files(html_file, context)
    info_content = render_files(info_file, context)
    
    global index 
    index += 1
   
    folder_path = f"question{index}"
    
    os.makedirs(folder_path, exist_ok=True)
   
    
    if py_file:
        py_content = render_files(py_file, context)
        file_path = os.path.join(folder_path, "server.py")
        with open(file_path, "w") as f:
                
            f.write(py_content)
        
    file_path = os.path.join(folder_path, "question.html")
    with open(file_path, "w") as f:
                
        f.write(html_content)
    file_path = os.path.join(folder_path, "info.json")
    with open(file_path, "w") as f:
                
        f.write(info_content)

       
   

def main():
    j = 1
    x = load_files("question_bank.md")
    data = create_data(x)

    y = load_files("template.md")
    typeDic = templateType(y)
    info = typeDic["IJ"]
    for type, template in typeDic.items():
        if type == "MC":
            createMultipleChoice(data, template, info )
        elif type == "CB":
            createCheckBox(data, template, info)
        elif type == "DD":
            
            p = re.split("```", template)
            createDropDown( data, p[0],p[1], info )


   

    #print(multiChoice(i))

if __name__ == "__main__":
    main()

   
