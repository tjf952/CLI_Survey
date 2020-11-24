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

import sys, os, time, json
from termcolor import colored, cprint
from progress.bar import FillingCirclesBar
from datetime import datetime

############################################################################################
# Program Functions
############################################################################################

survey_questions = []

survey_description = '''
Welcome to the developer incentive and job satisfaction survey! This survey will help senior leaders increase
the visibility and job satisfaction of our developer community. It is our goal to recruit, cultivate, and retain a
highly qualified developer community that collaboratively and creatively overcomes some of our most difficult
technical problems. This survey will help us determine how we should recognize and reward these developers.\n
Do not discuss sensitive operational information, or information injurious to the Army or any individuals, or
subjects mentioned in AR 360-1, paragraphs 5-3a(1) through 5-3a(20).\n
'''

timestamp = None

# Question Class

class Question:
    def __init__(self, category, prompt, choices):
        self.category = category
        self.prompt = prompt
        self.choices = choices
        self.answer = None

# Print Functions

def printd(s, c='blue'):
    cprint(s, c, attrs=['bold'])

def printc(s):
    cprint(s, 'magenta', attrs=['bold'])

def printe(s):
    cprint(s, 'red', attrs=['bold', 'reverse', 'blink'])

def printr(s):
    colors = ['red', 'yellow', 'green', 'cyan', 'blue', 'magenta']
    for i, l in enumerate(s): cprint(l, colors[i%len(colors)], attrs=['bold'], end='')

# Menu Functions

def main_menu():
    clear()
    printd(survey_description)
    printc('[1] Take Survey')
    printc('[2] View Answers')
    printc('[3] Change Answers')
    printc('[4] Submit')
    printc('[0] Exit')
    c = input('\n >> ')
    exec_menu(c)

def clear():
    os.system('clear')
    print()

def exec_menu(s):
    clear()
    print()
    try: 
        actions[s]()
    except KeyError:
        printe('Invalid selection, try again.')
        actions['main_menu']()

def take_survey():
    printd('Welcome to the beginning of the survey. Please answer to the best of your ability!\n')
    printd('There are '+str(len(survey_questions))+' questions in this survey. Press [Enter] to begin...\n', 'cyan')
    input()
    for i,q in enumerate(survey_questions):
        give_answer(i,q)
    clear()
    printr('You have completed the survey! Press [Enter] to return to the Main Menu...\n')
    input()
    actions['main_menu']()

def view_answers():
    printd('View Survey!\n')
    printd('Press [Enter] to return to the Main Menu...\n', 'cyan')
    printd('\nSurvey Questions\n')
    for i,q in enumerate(survey_questions):
        printd('—'*50, 'white')
        printd('Question ' + str(i+1) + ' of ' + str(len(survey_questions)) + '\n')
        printd(str(i+1) + '. ' + q.prompt)
        if q.category == 'choice':
            print()
            for choice in q.choices:
                printc('\t'+choice)
        printd('\nAnswer: ' + str(q.answer), 'white')
        printd('—'*50+'\n', 'white')
    printd('Press [Enter] to return to the Main Menu...\n', 'cyan')
    input()
    actions['main_menu']()

def change_answers():
    c = None
    while True:
        clear()
        printd('Change Menu!\n')
        printd('Please enter the question number to edit a question:')
        printd('(Please enter a valid number)', 'cyan')
        try:
            c = int(input('\n >> '))
            if c < 1 or c > len(survey_questions): raise ValueError
        except ValueError:
            printe('\nInvalid input! Please try again.')
            continue
        clear()
        printd('Is this the question you want to edit?\n')
        printd('[' + survey_questions[c-1].prompt + ']\n', 'cyan')
        printc('[1] Yes')
        printc('[2] No')
        choice = input('\n >> ')
        if choice == '1': break
    give_answer(c-1, survey_questions[c-1])
    clear()
    printr('You have changed your answer! Press [Enter] to return to the Main Menu...\n')
    input()
    actions['main_menu']()

def submit():
    printr('Turning file into json format!\n')
    write_json()
    loading_bar()
    printd('Press [Enter] to return to the Main Menu...\n', 'cyan')
    input()
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

def loading_bar():
    with FillingCirclesBar('Loading', max=20) as bar:
        for i in range(20):
            time.sleep(0.1)
            bar.next()

actions = {
    'main_menu': main_menu,
    '1': take_survey,
    '2': view_answers,
    '3': change_answers,
    '4': submit,
    '0': exit,
}

# Survey Functions

def get_questions():
    read_file = 'data/questions.txt'
    with open(read_file, 'r') as f:
        for line in f.readlines():
            c, q, a = map(str.strip, line.split('~'))
            a = a.split(',')
            if c == 'choice':
                for i, choice in enumerate(a):
                    a[i] = '('+str(i+1)+') '+choice.strip()
            else:
                a = None
            if c: survey_questions.append(Question(c, q, a))

def give_answer(i,q):
    os.system('clear')
    printd('Question ' + str(i+1) + ' of ' + str(len(survey_questions)) + '\n')
    printd(str(i+1) + '. ' + q.prompt)
    c = None
    if q.category == 'number':
        while True:
            printd('(Please enter a valid number)', 'cyan')
            try:
                c = int(input('\n >> '))
                if c < 0: raise ValueError
                break
            except ValueError:
                printe('\nInvalid input! Please try again.')
    elif q.category == 'text':
        c = input('\n >> ')
    elif q.category == 'choice':
        printd('(Choose one of the following by entering the corresponding number)\n', 'cyan')
        for choice in q.choices:
            printc('\t'+choice)
        while True:
            try:
                c = int(input('\n >> '))
                if c < 1 or c > len(q.choices): raise ValueError
                break
            except ValueError:
                printe('\nInvalid choice! Please try again.')
    elif q.category == 'list':
        printd('(This is a list question, press [Enter] to add an entry or to end the list)', 'cyan')
        l = []
        while True:
            c = input('\n >> ')
            if not c: 
                printd('\nDo you want to end the list?\n')
                printc('[1] Yes')
                printc('[2] No')
                choice = input('\n >> ')
                if choice == '1':
                    c = l
                    break
                else:
                    printd('(Continuing to add to list)', 'cyan')
                    continue
            l.append(c)
            printc('\"' + c + '\" was added to the current list.')
    q.answer = c


def write_json():
    outfile = 'responses/entry-' + timestamp + '.txt'
    data = []
    for q in survey_questions:
        data.append({
            'type': q.category,
            'question': q.prompt,
            'choices': q.choices,
            'answer': q.answer
        })
    with open(outfile, 'w') as f:
        json.dump(data, f)

############################################################################################
# Main Function
############################################################################################

if __name__ == "__main__":
    # Set timestamp
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    # Setup survey
    get_questions()
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
