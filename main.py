import smtplib, ssl, argparse, random
from getpass import getpass
from message import GetMessage, GetWishlist
import re

class Participant:
    def __init__(self, name, email, wishList=None):
        self.Name = name
        self.Email = email
        self.WishList = wishList
    
    def __str__(self):
        return "Participant Name={}\nEmail={}\n{}".format(self.Name, self.Email, GetWishlist(self))

    Name = ""
    Email = ""
    WishList = []

participantsDefinition = [
    Participant("Stefan Annell",
            "steann@kth.se",
            [
                "Klättertränings redskap, https://www.addnature.com/max-climbing-maxgrip-hybrid-M889083.html#cgid=236483",
                "Quickdraws, https://www.addnature.com/black-diamond-hotforge-quickpack-12cm-M841006.html?vgid=G1182940#cgid=236464",
                "Kettlebel ~24-28 kg (obs! Beställ hem till oss istället för upp till Norrland så slipper ta på flyg!) https://gymkompaniet.se/kettlebells-neopren-8-48kg-recoil?___store=default",
                "1x Låskarbin, https://www.addnature.com/edelrid-hms-strike-slider-fg-ii-M1152029.html?vgid=G1703525#cgid=236466",
                "2x Standard yoga block, gärna kork vilket märke som helst funkar.",
        ]),
    Participant("Anna-Karin Ek",
            "annakarin.ek@gmail.com",
            [
                "Halsband från Bluebillie, STOR SOL GULD: https://bluebillie.com/sv/shop/favourite-combinations-sv/big-sun-gold-on-plain-chain-gold/. De saker Anna har listat är dyrare än gränsen på 1000 kr, Anna kommer givetvis betala mellanskillnaden till den som köper till henne.",
                "Fleecetröja från Astrid Wild, färg SVART, storlek SMALL: https://www.astridwild.com/sv/collections/fleeces-tops/products/minna-wool-fleece-jacket?variant=42485110571232 (OBS spara retursedeln + paketet om du köper tröjan utifall jag behöver byta storlek. OBS på deras hemsida kan du lägga till månadens gåva med köpet av fleecetröjan, gör gärna det i samband med köpet!). De saker Anna har listat är dyrare än gränsen på 1000 kr, Anna kommer givetvis betala mellanskillnaden till den som köper till henne.",
        ]),

    Participant("Boel Ek",
            "boel.ek@live.se",
            [
            "Obs special! Mats köpte ett par tofflor från Naturkompaniet till Boel, swisha honom 1000kr - årspremunation på Allers eller Året runt.",
        ]),

    Participant("Mats Ek",
            "mats.ek@hotmail.se",
            [
            "https://www.jackjones.com/sv-se/product/12190170_6/mock-neck-stickad-troeja stl Large",
            "https://www.intersport.se/klader/underklader/understall/mckinley-dylan-ux-understallsbyxor-herr/black-night stl Large",
        ]),

    Participant("Gustav Ek",
            "gustav.ek86@gmail.com",
            [
                "Iitala Essence dricksglas 35 cl",
                "Le creuset Ugnsform med lock. Gärna orange färg.",
                "Skeppshult Gjutjärnspanna med trähandtag .",
                "Prydnader/inredning kanske vasmed tillhörande kvistar/grenar eller dylikt, snygg väggklocka"
        ]),

    Participant("Jacob Ek",
            "jacobek98@gmail.com",
            [
                "https://beaumont-pictures.com/products/shoulder-zip-sweater - storlek M", 
                "https://beaumont-pictures.com/products/tracksweat-2000 - storlek M", 
                "https://beaumont-pictures.com/products/tact-sweater?variant=39616622395531 - storlek M"
        ]),
]

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
        # Remember to fix smtplib.py, gets encoding error if its ascii! 875: msg = _fix_eols(msg).encode('utf-8')
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

def ValidateTargets(participants):
    """ Circular dependency check"""
    def findParticipant(participants, participantGiver):
        for participant in participants:
            if participant.Giver == participantGiver:
                return participant
        return None

    for participant in participants:
        targetParticipant = findParticipant(participants, participant.Target)
        if participant.Giver == targetParticipant.Target:
            if targetParticipant.Giver == participant.Target:
                #print("---")
                #print("Circular dependency!")
                #print(targetParticipant.Giver.Name, "<->", targetParticipant.Target.Name)
                #print("---")
                return False
                
    """ Self check, cannot give yourself a present """
    for participant in participants:
        if participant.Giver == participant.Target:
            #print("---")
            #print("Self check failed!")
            #print(participant.Giver.Name, "<->", participant.Target.Name)
            #print("---")
            return False
    
    return True 

def GeneratePresentTargets(participants):
    presentTargets = []
    participantsTargets = participants.copy()
    random.shuffle(participantsTargets)
    
    while participants:
        giver = participants.pop()
        target = participantsTargets.pop()
        presentTargets.append(PresentTarget(giver, target))

    return presentTargets

def GetPresentTargetsList():
    random.shuffle(participantsDefinition)
    presentTargets = None
    n = 0
    while not presentTargets:
        n += 1
        print("Generation nr: {}".format(n))
        presentTargets = GeneratePresentTargets(participantsDefinition.copy())
        if not ValidateTargets(presentTargets):
            presentTargets = None

        if n >= 100:
            print("Generation failed!")
            return None
    return presentTargets

 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
def check(email):
    result = re.fullmatch(regex, email)
    if(result):
        print("Valid Email")
    else:
        print("Invalid Email")
    return result

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
    if not check(sender_email):
        return
    if not password:
        password = getpass()

    emailServer = FindEmailServer(sender_email)
    if emailServer:
        for presentTarget in presentTargets:
            SendEmail(emailServer, sender_email, password, presentTarget.Giver.Email, GetMessage(presentTarget.Giver, presentTarget.Target))
    else:
        print("Email server not defined in EmailServers, cannot send away email.")

"""
import customtkinter
def gui(email="Email", password=""):
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()  # create CTk window like you do with the Tk window
    app.geometry("1024x900")
    app.title("Christmas Present Game")


    entry_1 = customtkinter.CTkEntry(master=app, placeholder_text=email)
    entry_1.pack(pady = 12, padx = 10)

    entry_2 = customtkinter.CTkEntry(master=app, placeholder_text=password, show="*")
    entry_2.pack(pady = 12, padx = 10)


    def send():
        main(entry_1.get(), entry_2.get(), True)
    button = customtkinter.CTkButton(master=app, text="Send", command=send)
    button.pack(pady = 12, padx = 10)

    def test():
        main(entry_1.get(), entry_2.get(), True)
    button2 = customtkinter.CTkButton(master=app, text="Test", command=test)
    button2.pack(pady = 12, padx = 10)

    participantsButtons = []
    for participant in participantsDefinition:
        outputText = str(participant)
        text = customtkinter.CTkLabel(master=app, text=outputText, anchor="w", width=250)
        text.pack(pady = 5, padx = 5)

    app.mainloop()
"""    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--gui", help="Open a GUI of the software.", action="store_true")
    parser.add_argument("-e", "--email", help="The address that will send off the email's.")
    parser.add_argument("-p", "--password", help="Password for the sender email (can be provided as hidden input as well).")
    parser.add_argument("-t", "--test", help="Test of generatior mode.", action="store_true")
    args = parser.parse_args()
    if args.gui:
        gui(args.email, args.password)
    else:
        main(args.email, args.password, args.test)
