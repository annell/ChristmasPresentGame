def GetRules():
    return """    - It is absolutly forbidden to reveal who you will give your present to.
    - The price of the present should be around 1000 kr.
    - You should respect the wishing list (except if you have a really good idea of course!).
    - There needs to be a good rhyme when giving out the present!
    
Punishment for breaking with any of the rules will result in that you need to go and wrestle with the bears.
"""

def GetWishlist(target):
    wishlist = ""
    for wish in target.WishList:
        wishlist += "- " + wish + "\n"
    return wishlist

def GetMessage(giver, target):
    SUBJECT = "Christmas Game 2021"
    TEXT = "Hello {}!\n\nYou should give your christmas present to {} and their christmas present wish list is: \n{}\nThe rules for this years Christmas Game are: \n{}\nBest regards,\nJulklappsspelsfixaren".format(giver.Name, target.Name, GetWishlist(target), GetRules())
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    return message