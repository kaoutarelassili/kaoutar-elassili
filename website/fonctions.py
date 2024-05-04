import shutil
import smtplib
from email.message import EmailMessage
import secrets
import string
#from .models import Candidat, Recruteur, Offre, Postuler

def offre_tableau(offre, offres):
    for i in offres:
        if i.id == offre.id:
            return True 
    return False

def envoie_email(receiver, subject, message):
    sender_email = "elassilik@gmail.com"
    password = "htdbjmzaboqrfarj"

    email = EmailMessage()
    email["From"] = sender_email
    email["To"] = receiver
    email["Subject"] = subject
    email.set_content(message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    print("Login success")
    server.send_message(email)
    print("Email has been sent to", receiver)
    server.quit()



def genere_mdp(length):
    characters = string.ascii_letters + string.digits + "@*^%$#!"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password



