import smtplib, ssl, argparse, random
from getpass import getpass
from message import GetMessage

def SendEmail(emailServer, sender_email, password, reciever_email, message):
    context = ssl.create_default_context()
    try:
        print("Starting secure connection to EmailServer.")
        server = smtplib.SMTP(emailServer.Smtp_server, emailServer.Port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted

        print("Logging in to {sender_email}.".format(sender_email=sender_email))
        server.login(sender_email, password)
        print("Logged in successfully.")

        print("Sending email from {sender_email} to {reciever_email}.".format(
            sender_email=sender_email, 
            reciever_email=reciever_email
            ))
        server.sendmail(sender_email, reciever_email, message)
        print("Email sent successfully.")
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

class EmailServer:
    def __init__(self, serverSignature, smtp_server, port):
        self.ServerSignature = serverSignature
        self.Smtp_server = smtp_server
        self.Port = port
    
    def __str__(self):
        return "EmailServer ServerSignature={}, Smtp_Server={}, Port={}".format(self.ServerSignature, self.Smtp_server, self.Port)

    ServerSignature = ""
    Smtp_server = ""
    Port = 0

emailServers = [
    EmailServer("@outlook.com", "smtp-mail.outlook.com", 587),
    EmailServer("@gmail.com", "smtp.gmail.com", 587),
]

class Participant:
    def __init__(self, name, email, wishList=None):
        self.Name = name
        self.Email = email
        self.WishList = wishList
    
    def __str__(self):
        return "Participant Name={}, Email={}, Wishlist={}".format(self.Name, self.Email, self.WishList)

    Name = ""
    Email = ""
    WishList = []

participantsDefinition = [
    Participant("Stefan Annell", "steann@kth.se", ["En sko", "En skooter", "Boulder kritpase"]),
    Participant("Anna-Karin Ek", "steann@kth.se", ["En sko", "En skooter", "Boulder kritpase"]),
    Participant("Boel Ek", "steann@kth.se", ["En sko", "En skooter", "Boulder kritpase"]),
    Participant("Mats Ek", "steann@kth.se", ["En sko", "En skooter", "Boulder kritpase"]),
    Participant("Jakob Ek", "steann@kth.se", ["En sko", "En skooter", "Boulder kritpase"]),
    Participant("Gustav Ek", "steann@kth.se", ["En sko", "En skooter", "Boulder kritpase"]),
]

class PresentTarget:
    def __init__(self, giver, target):
        self.Giver = giver 
        self.Target = target

    Giver = None
    Target = None

def FindEmailServer(sender_email):
    for emailServer in emailServers:
        if emailServer.ServerSignature in sender_email:
            return emailServer
    return None

def GeneratePresentTargets(participants):
    presentTargets = []
    presentTargets = participants.copy()
    random.shuffle(presentTargets)
    
    while participants:
        participant = participants.pop()
        foundTarget = False
        for presentTarget in presentTargets:
            if participant != presentTarget:
                foundTarget = True
                presentTargets.append(PresentTarget(participant, presentTarget))
                presentTargets.remove(presentTarget)
                break;

        if not foundTarget:
            return None
    return presentTargets

def GetPresentTargetsList():
    random.shuffle(participantsDefinition)
    presentTargets = None
    n = 0
    while not presentTargets:
        n += 1
        print("Generation nr: {}".format(n))
        presentTargets = GeneratePresentTargets(participantsDefinition)
        if n >= 10:
            print("Generation failed!")
            return None
    return presentTargets


def main(sender_email, password, test):
    presentTargets = GetPresentTargetsList()
    if not presentTargets:
        return
    if test:
        for presentTarget in presentTargets:
            print("{} -> {}".format(presentTarget.Giver.Name, presentTarget.Target.Name))
        return

    if not sender_email:
        sender_email = input("Type your email and press enter: ")
    if "@" not in sender_email:
        print("Not a valid email address")
    if not password:
        password = getpass()

    emailServer = FindEmailServer(sender_email)
    if emailServer:
        for presentTarget in presentTargets:
            SendEmail(emailServer, sender_email, password, presentTarget.Giver.Email, GetMessage(presentTarget.Giver, presentTarget.Target))
    else:
        print("Email server not defined in EmailServers, cannot send away email.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--email", help="The address that will send off the email's.")
    parser.add_argument("-p", "--password", help="Password for the sender email (can be provided as hidden input as well).")
    parser.add_argument("-t", "--test", help="Test of generatior mode.", action="store_true")
    args = parser.parse_args()
    main(args.email, args.password, args.test)