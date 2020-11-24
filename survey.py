#!/usr/bin/env python3

############################################################################################
#
# Title: Developer Survey
# Date: 23 November 2020
# Description: 
# Usage: 
# Instructions: 
#
############################################################################################

############################################################################################
# Imports
############################################################################################

import sys, os, json
from termcolor import colored, cprint
from datetime import datetime
import question

############################################################################################
# Program Functions
############################################################################################

survey_questions = []
survey_answers = []

survey_description = '''
Welcome to the developer incentive and job satisfaction survey! This survey will help senior leaders increase
the visibility and job satisfaction of our developer community. It is our goal to recruit, cultivate, and retain a
highly qualified developer community that collaboratively and creatively overcomes some of our most difficult
technical problems. This survey will help us determine how we should recognize and reward these developers.\n
Do not discuss sensitive operational information, or information injurious to the Army or any individuals, or
subjects mentioned in AR 360-1, paragraphs 5-3a(1) through 5-3a(20).\n
'''

# Question Class

class Question:
    def __init__(self, category, prompt, choices):
        self.category = category
        self.prompt = prompt
        self.choices = choices
        self.answer = ''

# Print Functions

def printd(s):
    cprint(s, 'blue', attrs=['bold', 'dark'])

def printc(s):
    cprint(s, 'blue', attrs=['bold'])

def printe(s):
    cprint(s, 'red', attrs=['bold', 'reverse', 'blink'])

# Menu Functions

def main_menu():
    os.system('clear')
    printd(survey_description)
    printc('[1] Take Survey')
    printc('[2] View Answers')
    printc('[3] Change Answers')
    printc('[4] Submit')
    printc('[0] Exit')
    c = input('\n >> ')
    exec_menu(c)

def exec_menu(s):
    os.system('clear')
    try: 
        actions[s]()
    except KeyError:
        printe('Invalid selection, try again')
        actions['main_menu']()

def take_survey():
    printd('Menu A!\n')
    printd('There are '+str(len(survey_questions))+' questions in this survey. Press [Enter] to begin...')
    input()
    for q in survey_questions:
        os.system('clear')
        # CONTINUE HERE

def view_answers():
    printd('Menu A!\n')
    printc('[9] Back to Main Menu')
    printc('[0] Exit')
    c = input('\n >> ')
    exec_menu(c)

def change_answers():
    printd('Menu A!\n')
    printc('[9] Back to Main Menu')
    printc('[0] Exit')
    c = input('\n >> ')
    exec_menu(c)

def submit():
    printd('Menu A!\n')
    printc('[9] Back to Main Menu')
    printc('[0] Exit')
    c = input('\n >> ')
    exec_menu(c)

def back():
    actions['main_menu']()

def exit():
    printe('Are you sure you want to exit?\n')
    printc('[1] Yes')
    printc('[2] No')
    choice = input('\n >> ')
    if choice == '1':
        os.system('clear')
        sys.exit()
    else:
        actions['main_menu']()

actions = {
    'main_menu': main_menu,
    '1': take_survey,
    '2': view_answers,
    '3': change_answers,
    '4': submit,
    '9': back,
    '0': exit,
}

# Survey Functions

def get_questions():
    read_file = 'data/questions.txt'
    with open(read_file, 'r') as f:
        for line in f.readlines():
            c, q, a = map(str.strip, line.split('~'))
            a = a.split(',')
            for i, choice in enumerate(a):
                a[i] = '('+str(i+1)+') '+choice.strip()
            if c: survey_questions.append(Question(c, q, a))

def write_json():
    outfile = 'responses/entry-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.txt'
    with open(file, 'w') as f:
        json.dump(results, outfile)


############################################################################################
# Main Function
############################################################################################

if __name__ == "__main__":
    # Setup survey
    # Launch survey
    main_menu()

############################################################################################
# Resources
############################################################################################

# Termcolor: https://pypi.org/project/termcolor/
# JSON: https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
# Interactive Menu: https://www.bggofurther.com/2015/01/create-an-interactive-command-line-menu-using-python/

############################################################################################
# Example
############################################################################################
