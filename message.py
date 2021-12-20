def GetRules():
    return """    - Det är absolut förbjudet att avslöja vem du ska ge present till.
    - Priset på presenten ska vara ca 1000 kr.
    - Du måste respektera önskelistan (förutom om du har en annan jätte bra idé!).
    - Du måste göra ett bra rim till presenten!
    
Straffet för att misslyckas med att följa reglerna är att du måste gå ut i skogen tillsammans med Mats och brottas med björnen.
"""

def GetWishlist(target):
    wishlist = ""
    for wish in target.WishList:
        wishlist += "- " + wish + "\n"
    return wishlist

def safe_str(obj):
    return str(obj)

def GetMessage(giver, target):
    SUBJECT = "Julklappsspelet 2021"
    TEXT = "Hej {}!\n\nDu ska ge din present till {} vars önskelista är: \n{}\nReglerna för årets julklapsspel är: \n{}\nMvh,\nJulklappsspelsfixaren".format(giver.Name, target.Name, GetWishlist(target), GetRules())
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    return safe_str(message)