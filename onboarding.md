### Guidline on generating different question types:
- id: Each question should have a unique id. Make sure that you don’t duplicate question IDs.
- type: The type of question should be one of the predefined types (e.g., Multiple Choice, String Input, Drop Down, Check Box).
- title: The title is a brief description of the question's focus and will be used for identifying the question.
- topic: Specify the relevant topic for categorization (e.g., HTML Basics, HTML Attributes).
- question: Provide a clear question prompt.
- Answer Choices: For Multiple Choice and Drop Down, include the correct answer by marking it with an asterisk (*). For Check Box questions, mark all correct answers with an asterisk (*).
- The right option in each question must start with "*".  
- Each ":" must be followed by a space.
- Each question must end with "###".
- Refer to question_bank.md file to find examples of each question type.

1. **Multiple Choice Question (MCQ)**
Description: A multiple choice question offers four options, and only one of them is correct. The correct answer is marked with an asterisk (*).

**Format**:  
id: (id of the last question in the question_bank.md + 1)  
type: Multiple Choice  
title: (Brief description of the question's focus)  
topic: (Relevant topic)  
question: (The question prompt)  
A: (Option A)  
*B: (Option B)  (* correct answer)  
C: (Option C)  
D: (Option D)  
###  

2. **String Input Question** 
Description: A string input question requires the user to type in a correct answer in the form of text. The expected answer is predefined in the answer field.  

**Format**:  
id: (Unique number)  
type: String Input  
title: (Brief description of the question's focus)   
topic: (Relevant topic)    
question: (The question prompt)    
answer: (The correct answer)   
###   

3. **Drop Down Question** 
Description: A drop down question provides multiple choices, but only one is correct. Users can choose one option from a dropdown menu. The correct answer is marked with an asterisk (*).  

**Format**:  

id: (Unique number)  
type: Drop Down  
title: (Brief description of the question's focus)  
topic: (Relevant topic)  
question: (The question prompt)  
A: (Option A)  
B: (Option B)  
*C: (Option C)  (* correct answer)  
D: (Option D)  
###  

4. **Check Box Question**  
Description: A check box question allows multiple correct answers. Users can select more than one answer. There must be 5 options and the correct answers are marked with an asterisk (*).  

**Format**:

id: (Unique number)  
type: Check Box  
title: (Brief description of the question's focus)  
topic: (Relevant topic)  
question: (The question prompt)  
*A: (Option A) (* correct answer)  
B: (Option B)  
*C: (Option C) (* correct answer)  
D: (Option D)  
*E: (Option E) (* correct answer)  
###  

### How to add questions into Github repo:
1. Clone the Repository:
Use the following command to clone the repo:

```bash
git clone https://github.com/learnification/pl-scripts.git
```
2. Navigate into the project directory:
```bash
cd pl-scripts
```
3. Creat a new branch:
Create and checkout a new branch for your question:
```bash
git checkout -b new-question
```
4. Add Your Question in question_bank.md:
Open the question_bank.md file and write your question following the above formating for each question type.
5. Generate the Question Using the Script:
Run the provided generate.py script:
```bash
python generate.py
```
The script will create a folder with the necessary files (info.json, question.html, and server.py) based on your question. 

6. Check if the Question is Valid:  
Review the generated files in the output directory.  
Make sure question.html displays the question properly, and the answer choices or logic are correctly formatted.  
Check the info.json for the correct metadata (e.g., topic, tags).  

7. Push Your Changes to GitHub:
Add your changes:

```bash
git add question_bank.md 
```
Commit the changes:
```bash
git commit -m "Added new [] question"
```
You can write the question title inside the bracket.  
Push your changes to GitHub:

```bash
git push origin new-question
```
8. Submit a Pull Request:
Go to GitHub and open a pull request from your branch to the main branch.
Add reviewers and wait for approval.

