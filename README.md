Automating question generation in PrairieLearn project:
Overview:

This project focuses on developing a question bank for the CIS 145 course at the University of Fraser Valley. The course is an introduction to web publishing, and the questions will help students practice various concepts such as HTML, CSS, and JavaScript. We are building and automating the creation of a diverse range of questions using PrairieLearn, an open-source platform that supports various question formats (Multiple Choice, Short Answer, Dropdown, etc.). The project aims to simplify the process of generating and authoring questions while ensuring a wide array of question types and topics to cover the course material.

What is PrairieLearn?
PrairieLearn is an innovative educational platform designed to enhance the learning experience through interactive and personalized assessments. It offers a wide range of tools and features that allow educators to create, manage, and deliver assessments effectively. PrairieLearn supports various question types, including multiple-choice, coding questions, and more, making it a versatile tool for different educational contexts. For more information refer to https://prairielearn.readthedocs.io/en/latest/.

Question Configuration:

Each question directory consists of three files: 
1. info.json: For each question defines properties of the question.
2. question.html: The question.html is a template used to render the question to the students.
3. Server.py: The server.py file for each question creates randomized question variants by generating random parameters and the corresponding correct answer.
For a more detailed explanation of each file and its examples, please refer to https://prairielearn.readthedocs.io/en/latest/question/.

How to generate a Question:
-Go to the Questions tab and click "Add question".
-Change the question ID and edit info.json to set the question title, topic, and tags.
-Modify question.html to create the question content.
-Save and sync the question, then preview it to test.

Main project outline:
human ---> .md files ---> pyhton script ---> .pl files ---> Github ---> PrairieLearn
The workflow starts with humans drafting questions in markdown files, which are then processed by a Python script that generates PrairieLearn-compatible files; these files are committed to GitHub and deployed to the PrairieLearn platform for student assessments.

File explaination:
1- Template.md: Defines the structure and format for each type of question and contains templates for info.json file and multiple choice, drop down, check box and string input question types. (For detailed information on these question types visit )
2- Question_bank.md: Markdown format with specific structure which stores a list of questions to be added to PrairieLearn.
Each question in the question bank must be followed by "###" which helps in seperating questions from one another. Questions must also include:
Type (specifies the type of question)
Title (A brief description of the question's focus)
Topic (The subject category of the question)
Question (The prompt or query posed to the student)
Answer Choices (List of possible answers, with the correct one marked by *)

3- geneate.py: This is the main script that automates the creation of questions for the PrairieLearn platform by processing Markdown files and generating the corresponding HTML, JSON, and Python files. Here's a brief explanation of the key components:

UUID Generation: The script uses an external API to generate unique UUIDs for each question. If the API request fails, it retries with exponential backoff. 
* For more information on UUIDs refer to https://prairielearn.readthedocs.io/en/latest/uuid/.
File Loading and Rendering: The script reads templates and question data from Markdown files, processes them using the Jinja2 templating engine, and renders the final content.
Template Handling: Questions are categorized by type (e.g., Multiple Choice, Check Box, Drop Down). The script splits templates into sections and matches them with question data to create the final output.
Data Processing: It extracts questions from the input file, parses the content, and generates the necessary context for rendering the templates.
File Generation: For each question, the script creates a dedicated folder and writes the HTML, JSON (info.json), and optionally Python (server.py) files into it.
Question Type Handling: Different functions are defined to handle specific question types like Multiple Choice, Check Box, Drop Down, and String Input, ensuring the appropriate files are generated for each type.
Main Workflow: The main function orchestrates the entire process by loading the question bank and templates, processing the data, and generating files for each question type.
This automation ensures that new questions can be quickly added to PrairieLearn with the required file structure, reducing manual work and minimizing errors.















 


