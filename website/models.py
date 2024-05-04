import uuid 
from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 


class Recruteur(db.Model, UserMixin):
    __tablename__ = 'recruteur'
    id = db.Column(db.String(255), primary_key=True)
    nom = db.Column(db.String(150))
    prenom = db.Column(db.String(150))
    nom_societe = db.Column(db.String(150))
    adresse = db.Column(db.String(150))
    email = db.Column(db.String(150))
    mdp = db.Column(db.String(150))
    domaine = db.Column(db.String(150))
    image = db.Column(db.String(150))
    offers = db.relationship('Offre', backref='recruteur', lazy=True)

    def __init__(self, nom, prenom, nom_societe, adresse, email, mdp, domaine, image):
        self.id = str(uuid.uuid4())
        self.nom = nom
        self.prenom = prenom
        self.nom_societe = nom_societe
        self.adresse = adresse
        self.email = email
        self.mdp = mdp
        self.domaine = domaine 
        self.image = image 

class Candidat(db.Model, UserMixin):
    __tablename__ = 'candidat'
    id = db.Column(db.String(255), primary_key=True)
    nom = db.Column(db.String(150))
    prenom = db.Column(db.String(150))
    email = db.Column(db.String(150))
    mdp = db.Column(db.String(150))
    domaine = db.Column(db.String(150))
    date_naissance = db.Column(db.Date())
    telephone = db.Column(db.String(150))
    ville = db.Column(db.String(150))
    bio = db.Column(db.String(10000))
    genre = db.Column(db.String(150))
    image = db.Column(db.String(150))
    cv = db.Column(db.String(150))
    postulations = db.relationship('Postuler', backref='recruteur', lazy=True)
    

    def __init__(self, nom, prenom, email, mdp, domaine, date_naissance, telephone, ville, bio, genre, image, cv):
        self.id = str(uuid.uuid4())
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.domaine = domaine 
        self.date_naissance = date_naissance
        self.telephone = telephone
        self.ville = ville
        self.bio = bio 
        self.genre = genre 
        self.image = image 
        self.cv = cv 


class Offre(db.Model):
    _tablename_ = 'offre'
    id = db.Column(db.String(255), primary_key=True)
    id_recruteur = db.Column(db.String(255), db.ForeignKey('recruteur.id'))
    titre = db.Column(db.String(255))
    description = db.Column(db.String(10000))
    region = db.Column(db.String(255))
    salaire = db.Column(db.Float)
    status = db.Column(db.String(255))
    dateCreation = db.Column(db.Date)
    dateLimite = db.Column(db.Date)
    speciality = db.Column(db.String(255))
    type_de_contrat=db.Column(db.String(100), nullable=True)
    postulations = db.relationship('Postuler', backref='offre', lazy=True)

    

    def __init__(self, id_recruteur, titre, description, region, salaire, status, dateCreation, dateLimite, speciality, type_de_contrat):
        self.id = str(uuid.uuid4())
        self.id_recruteur = id_recruteur
        self.titre = titre
        self.description = description
        self.region = region
        self.salaire = salaire
        self.status = status
        self.dateCreation = dateCreation
        self.dateLimite = dateLimite 
        self.speciality = speciality
        self.type_de_contrat = type_de_contrat




class Postuler(db.Model):
    __tablename__ = 'postuler'
    id_candidat = db.Column(db.String(255), db.ForeignKey('candidat.id'), primary_key=True)
    id_offre = db.Column(db.String(255), db.ForeignKey('offre.id'), primary_key=True)
    status = db.Column(db.String(255))
    dateApply = db.Column(db.Date) 




