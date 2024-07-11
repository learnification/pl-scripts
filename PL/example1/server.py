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
