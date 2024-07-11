import re
import json
from jinja2 import Template

#open the file
def loat_template(file):
    with open(file, 'r') as f:
        loaded_file = f.read()
        return loaded_file
    
#render the html 
def render_template(file, context):
    template = Template(file)
    return template.render(context)
    

def create_content(md_file):
    info = {}
    params = {}
   

    lines = md_file.split('\n')
    for line in lines:
        if line.startswith('- uuid:'):
            info['uuid'] = line.split(': ')[1]
        elif line.startswith('- title:'):
            info['title'] = line.split(': ')[1]
        elif line.startswith('- topic:'):
            info['topic'] = line.split(': ')[1]
        elif line.startswith('- tags:'):
            tags = line.split(': ')[1].strip('[]').split(', ')
            info['tags'] = tags
        elif line.startswith('- type:'):
            info['type'] = line.split(': ')[1]

        else:
            matches = re.findall(r'\{\{params\.(.*?)\}\}', line)
            for match in matches:
                params[match] = "{{params." + match + "}}"

    return params, info

def generate_question_html(template_content, params, flag=False):
    context = {'params': params, 'flag': flag}
    html_content = render_template(template_content, context)
    with open('question.html', 'w') as f:
        f.write(html_content)

def generate_info_json(dict):
    with open('info.json', 'w') as f:
        json.dump(dict, f, indent=4)


def extract_python(file):
    python_code = ""
    include_line = False
    md_content = file.split('\n')
    for line in md_content:
        if line.startswith('```python'):
            include_line = True

        elif line.startswith('```') and include_line:
            include_line = False
          
        elif include_line:
        
            python_code += line + '\n'
          
    return python_code

def generate_server(python_code):
    with open('server.py', 'w') as f:
        f.write(python_code)

def main():
    x = loat_template('template.md')
    p, i = create_content(x)
    generate_question_html(x, p)
    generate_info_json(i)
    a = extract_python(x)
    generate_server(a)
   


if __name__ == "__main__":
    main()

   
        