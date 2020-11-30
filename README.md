## Survey Template
#### November 2020
#### Description: 
Python3 command line interface program to give users an interactive survey experience and allow them to create json objects after completion.
#### Usage: 
```python
python3 survey.py
```
#### Current Dependencies: 
	termcolor - pip3 install termcolor
	progress.bar - pip3 install progress
	crypto - pip3 install pycryptodome
#### Instructions: 
> To create a survey first provide a questions text file with a list of questions where each question has the following format:
> 
> ***question-type*** ~ ***question-prompt*** ~ ***question-choices***
> 
> There are four types of questions:
> 1. text i.e. "text ~ What is your favorite color? ~ "
> 2. number i.e. "number ~ How old are you? ~ "
> 3. choice i.e. "choice ~ Which comic universe? ~ DC, Marvel"
> 4. list i.e. "list ~ List your favorite foods: ~ "
> Only choice requires the third argument, others still require the '~' but no argument to follow it. After creating a text file, edit the two variables at the top of the program called 'survey_source' and 'survey_description'.