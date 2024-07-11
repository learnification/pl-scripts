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

def create_data(file):
    data = []
    pattern = re.compile(r'(type:.*?)(?=(?:\ntype:.|$))', re.DOTALL)
    questions = pattern.findall(file)
    for question in questions:
        dic = {}
        lines = question.split("\n")
        for line in lines:
            key, value = line.split(": ")
            dic[key] = value
        data.append(dic)

    return data

def multiChoice(question):
    context = {}
    i = 1
    for key, value in question.items():
        value = value.replace('<', '&lt;').replace('>', '&gt;')
        if key == "question":
            context['question'] = value
        elif key not in ["type", "question"]:
            context[f"option{i}"] = value
            context[f"flag{i}"] = "false"

            if key == 'answer':
                
                context[f"flag{i}"] = "true"
            

                
            i += 1


    return context


def check_type(data):
    mcq_question = []
    for question in data:
        if question["type"] == "Multiple Choice":
            mcq_question.append(question)
    return mcq_question

def generate_file(file, context):
    html_content = render_files(file, context)
    global index 
    index += 1
    with open(f"question{index}.html", "w") as f:
        
        f.write(html_content)

       
   

def main():
    j = 1
    x = load_files("question_bank.md")
    y = load_files("template.md")
    
    data = create_data(x)
    mc_questions = check_type(data)

    for question in mc_questions:
        context = multiChoice(question)
        generate_file(y, context)

    #print(multiChoice(i))

if __name__ == "__main__":
    main()

   
