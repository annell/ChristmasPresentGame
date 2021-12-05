# Christmas Present Game
Small tool for hosting the Christmas Present Game

# Requirements
- Python 3+

# How to use script
1. Modify the participantsDefinition and fill out their details.
2. Modify the message in message.py.
3. Start the program with python 3 main.py (--help for some helpers).
4. Emails is sent out to all participants with instructions.

# Usage  of main.py
usage: main.py [-h] [-e EMAIL] [-p PASSWORD] [-t]

optional arguments:
  -h, --help            show this help message and exit
  -e EMAIL, --email EMAIL
                        The address that will send off the email's.
  -p PASSWORD, --password PASSWORD
                        Password for the sender email (can be provided as
                        hidden input as well).
  -t, --test            Test of generatior mode.