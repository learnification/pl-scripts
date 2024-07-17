import re
from jinja2 import Template
import html
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

            if key not in ["type", "question"]:
                context[f"option{i}"] = question[key]
                context[f"flag{i}"] = "false"

                if key.startswith("*"):
                
                    context[f"flag{i}"] = "true"

             
                i += 1


    return context


def createMultipleChoice(data, file):
    mcq_questions = []
    
    for question in data:
        if question["type"] == "Multiple Choice":
            mcq_questions.append(question)
       

    for question in mcq_questions:
        context = createContext(question)
        generate_file(file, context)
   

def createCheckBox(data, file):
    CB_questions = []
    for question in data:
        
        if question["type"] == "Check Box":
            CB_questions.append(question)

    for question in CB_questions:
        context = createContext(question)
        generate_file(file, context)

def createDropDown(data, HTML, py):
    DD_question = []
    for question in data:
        if question["type"] == "Drop Down":
            DD_question.append(question)
    for question in DD_question:
        context = createContext(question)
        generate_file(HTML, context)
        generate_file(py, context, True )

def generate_file(file, context, flag=False):
    html_content = render_files(file, context)
    global index 
    index += 1
   
    if flag:
        index = index - 1
        with open(f"server{index}.py", "w") as f:
        
            f.write(html_content)
    else:
        with open(f"question{index}.html", "w") as f:
        
            f.write(html_content)

       
   

def main():
    j = 1
    x = load_files("question_bank.md")
    data = create_data(x)

    y = load_files("template.md")
    typeDic = templateType(y)

    for type, template in typeDic.items():
        if type == "MC":
            createMultipleChoice(data, template)
        elif type == "CB":
            createCheckBox(data, template)
        elif type == "DD":
            
            p = re.split("```", template)
            createDropDown( data, p[0],p[1] )


   

    #print(multiChoice(i))

if __name__ == "__main__":
    main()

   
