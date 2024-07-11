{% if flag %}
# Info
- uuid: 28ce6a5e-8ad6-44d2-b454-19cd50dc1d8a
- title: CIS 145
- topic: Demo
- tags: [summer2024, cis145]
- type: v3

# Question
{% endif %}
<pl-question-panel>
  <p>Which one of the tags below represent {{params.var}} list in HTML:</p>
</pl-question-panel>

<pl-multiple-choice answers-name="acc" weight="1">
  <pl-answer correct="false">{{params.c0}}</pl-answer>
  <pl-answer correct="false">{{params.c1}}</pl-answer>
  <pl-answer correct="false">{{params.c2}}</pl-answer>
  <pl-answer correct="true">{{params.ans}}</pl-answer>
</pl-multiple-choice>

{% if flag %}
```python
import random

def generate(data):

  # Create a list of choices
  choices = ["<li>", "<ol>", "<dl>", "<lis>", "<unordered>", "<ul>"]
  # Create a list of variables
  variables = ["unordered", "ordered", "detailed"]
   
  var = random.choice(variables)
  data["params"]["var"] = var
    
  # Determine the correct answer
  if var == "unordered":

    answer = "<ul>"
  elif var == "ordered":
    answer = "<ol>"
  else:  
   
    answer = "<dl>"
        
  data["params"]["ans"] = answer
    
  # Create a new list without the answer
  choices2 = [choice for choice in choices if choice != answer]
    
  # Randomly select 3 incorrect choices
  incorrect_choices = random.sample(choices2, 3)
  for j in range(3):  
    data["params"][f"c{j}"] = incorrect_choices[j]
```
{% endif %}