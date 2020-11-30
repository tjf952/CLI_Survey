#!/usr/bin/env python3

############################################################################################
#
# Title: Survey Template
# Date: 23 November 2020
# Description: Python3 command line interface program to give users an interactive survey
#               experience and allow them to create json objects after completion.
# Usage: python3 survey.py
# Current Dependencies: termcolor - pip3 install termcolor
#                       progress.bar - pip3 install progress
#                       crypto - pip3 install pycryptodome
# Instructions: To create a survey first provide a questions text file with a list of 
#               questions where each question has the following format:
#                   <question-type> ~ <question-prompt> ~ <question-choices>
#               There are four types of questions:
#                   1. text i.e. "text ~ What is your favorite color? ~ "
#                   2. number i.e. "number ~ How old are you? ~ "
#                   3. choice i.e. "choice ~ Which comic universe? ~ DC, Marvel"
#                   4. list i.e. "list ~ List your favorite foods: ~ "
#               Only choice requires the third argument, others still require the '~' but 
#               no argument to follow it. After creating a text file, edit the two variables
#               at the top of the program called 'survey_source' and 'survey_description'.
#
############################################################################################

############################################################################################
# Imports
############################################################################################

import sys, os, time, json, b64
from termcolor import colored, cprint
from progress.bar import FillingCirclesBar
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from datetime import datetime

############################################################################################
# Program Functions
############################################################################################

### CHANGE THIS ###
survey_source = 'data/questions.txt'
survey_description = '''
Welcome to the developer incentive and job satisfaction survey! This survey will help senior leaders increase
the visibility and job satisfaction of our developer community. It is our goal to recruit, cultivate, and retain a
highly qualified developer community that collaboratively and creatively overcomes some of our most difficult
technical problems. This survey will help us determine how we should recognize and reward these developers.

Do not discuss sensitive operational information, or information injurious to the Army or any individuals, or
subjects mentioned in AR 360-1, paragraphs 5-3a(1) through 5-3a(20).
'''
###################

survey_questions = []
timestamp = None

# Question Class

class Question:
    def __init__(self, category, prompt, choices):
        self.category = category
        self.prompt = prompt
        self.choices = choices
        self.answer = None

# Print Functions

# May need to choose a different color than white if terminal is white
def printd(s, c='white'):
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
    data = write_json()
    encrypt_message_and_send(data)
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
    with open(survey_source, 'r') as f:
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
    clear()
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
        while True:
            c = input('\n >> ')
            if c == '':
                printe('\nInvalid answer! Please try again.')
            else: break
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
    data = []
    for q in survey_questions:
        data.append({
            'type': q.category,
            'question': q.prompt,
            'choices': q.choices,
            'answer': q.answer
        })
    return data

def encrypt_message_and_send(data):
    outfile = 'responses/entry-' + timestamp + '.bin'
    # Reads public key
    key = RSA.importKey(open('rsa.pub').read())
    cipher = PKCS1_OAEP.new(key)
    # Creates random symmetric key
    symkey = get_random_bytes(16)
    symcipher = AES.new(symkey, AES.MODE_EAX)
    # Encode data with symmetric key
    message = json.dumps(data).encode()
    ciphertext, tag = symcipher.encrypt_and_digest(message)
    # Encrypts symmetric key
    ekey = cipher.encrypt(symkey)
    # Writes to file
    with open(outfile, 'wb') as f: 
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ekey)
        f.write(ciphertext)

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
# Progress Bar: https://pypi.org/project/progress/
# JSON: https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
# Interactive Menu: https://www.bggofurther.com/2015/01/create-an-interactive-command-line-menu-using-python/
# Encryption: https://www.sitepoint.com/encrypt-large-messages-asymmetric-keys-phpseclib/
