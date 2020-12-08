## Survey Template v1.03
#### November 2020
#### Description: 
Python3 command line interface program to give users an interactive survey experience and allow them to create encrypted json objects after completion and ensure confidentiality and integrity between user and receiver.
#### Usage:
Owner
```bash
# Set up RSA keys
python3 rsa_gen.py
# After user completion, read encrypted file
python3 read_data.py responses/file-to-read.bin
```
User 
```bash
python3 survey.py
```
#### Current Dependencies: 
	termcolor - pip3 install termcolor
	progress.bar - pip3 install progress
	crypto - pip3 install pycryptodome
#### Instructions: 
To create a survey first provide a questions text file with a list of questions where each question has the following format:

> ***question-type*** ~ ***question-prompt*** ~ ***question-choices***
> 
> There are four types of questions:
> 1. text i.e. "text ~ What is your favorite color? ~ "
> 2. number i.e. "number ~ How old are you? ~ "
> 3. choice i.e. "choice ~ Which comic universe? ~ DC * Marvel * Other"
> 4. list i.e. "list ~ List your favorite foods: ~ "
> Only choice requires the third argument, others still require the '~' but no argument to follow it. After creating a text file, edit the two variables at the top of the program called 'survey_source' and 'survey_description'.

Next, you'll have to update the survey.py script by changing the following values:
- survey_source = 'data/questions.txt'
- survey_title = 'Simple Superhero Survey'
- survey_author = 'V3JpdHRlbiBieSBUaG9tYXMgRmlubg=='
- survey_description = "Sample Description"

After make sure to generate your own RSA key pair, keep the private key (rsa) safe and sound, give the public key (rsa.pub) to the participants of the survey. After receiving the data back, you can read the file by running the `read_data.py` script.