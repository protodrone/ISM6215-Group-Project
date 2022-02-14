# ISM6215-Group-Project

ISM6215 Spring 2022 Group Project

# Introduction

Python utility I wrote to generate and load ramdom sample data for the project.
JobNames.csv was sourced from https://www.onetcenter.org/database.html#individual-files.
Cities.txt was sourced from https://www.britannica.com/topic/list-of-cities-and-towns-in-the-United-States-2023068. RandomNames.csv was sourced from
http://random-name-generator.info. Company names were sourced from https://fauxid.com/tools/fake-company-generator. Random comments were sourced from https://hipsum.co api, which remains
my favorite Lorem Ipsum generator.

# Setup Quickstart

Best to use the app in a Python Virtual Environment (Python best practice). If you aren't 
familiar with VENV, the docs are at https://docs.python.org/3/library/venv.html. 

TL;DR
* git clone https://github.com/protodrone/ISM6215-Group-Project.git
* cd ISM6215-Group-Project
* python3 -m venv .venv
* source .venv/bin/activate
* pip install --upgrade pip
* pip install -r requirements.txt

The app uses the Python ConfigParser and looks for config.ini. Copy example_config.ini
to config.ini then update it with your database credentials.

# App Usage

Option 1) 
Edit DBTools.py to call the desired function(s). Examples included inline.

Option 2)
Use the functions interactively in a Python shell. Import DBTools.py and call the functions
à la carte as needed. 

Functions include:
* getPersonIdMax()
    * Returns the highest PersonId for use in random person selection with the presumption of a starting record Id of 1 and contiguous Ids to the max. This works so long as the Person table has only been truncated, which resets the AUTO_INCREMENT of the PK, and not deleted from. Not a great concern, as this function is generally used in the intial population of an empty schema.
* getCompanyIdMax()
    * Returns the highest CompanyId for use in random company selection. Same caveat as getPersonIdMax().
* randomizeParentCompanies(numParents)
* generateReviews(numReviews)
* getRandomComment()
    * Will be used in generateCommentAnswer(numAnsers). Need the questions first, so waiting on those for now.
* generateQuestionTypes()
    * generates default question types of Star and Comment
* generateQuestions()
    * Generates default Star and Comment Questions 1-5
* generateAnswers()
    * Generates an answer record for each question for each review
* generateCommentAnswers()
    * Generates a comment answer for each answer for question of type comment
* generateStarAnswers()
    * Generates a star answer for each answer for question of type star
* printCompanyTree()
    * Recursively print the Company tree
