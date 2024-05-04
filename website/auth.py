import os
import uuid
from flask import render_template, Blueprint, request, redirect, flash, url_for
from .models import Candidat, Recruteur
from . import db 
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.sql import func 
from werkzeug.security import generate_password_hash, check_password_hash
from .fonctions import genere_mdp, envoie_email



auth = Blueprint('auth', __name__ )

upload_image = os.path.join(auth.root_path, 'static', 'images')
upload_cv = os.path.join(auth.root_path, 'static', 'cv') 



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        mdp = request.form.get('mdp')

        candidat = Candidat.query.filter_by(email=email).first()
        recruteur = Recruteur.query.filter_by(email=email).first()

        if candidat:
            if candidat.mdp == mdp:
                nom_complet = f'{candidat.prenom} {candidat.nom}'
                flash(f'Bienvenue dans votre profil {nom_complet}', category='success')
                login_user(candidat, remember=True)
                return redirect(url_for('views.home_candidate'))
            else:
                flash('Mot de passe incorrect', category='error')
        elif recruteur:
            if recruteur.mdp == mdp:
                nom_complet = f'{recruteur.prenom} {recruteur.nom}'
                flash(f'Bienvenue dans votre profil {nom_complet}', category='success')
                login_user(recruteur, remember=True)
                return redirect(url_for('views.home_recruiter'))
            else:
                flash('Mot de passe incorrect', category='error')
        else:
            flash('Utilisateur n\'existe pas')

    return render_template('login.html')
    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@auth.route('/register/<user_type>')
def register(user_type):
    if user_type == 'candidat':
        return redirect('/inscription-candidat')
    elif user_type == 'recruteur':
        return redirect('/inscription-recruteur')


@auth.route('/inscription-recruteur', methods=['GET', 'POST'])
def inscription_recruteur():

    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        nom_societe = request.form.get('societe')
        adresse = request.form.get('adresse')
        mdp = request.form.get('mdp')
        mdp2 = request.form.get('mdp2')
        domaine = request.form.get('domaine')
        image = 'defaut.png'

        if mdp != mdp2:
            flash('Veuillez saisir deux mots de passes identiques ! ', category='error')
            return redirect('/inscription-recruteur')

        recruteur = Recruteur(nom=nom, email=email, prenom=prenom, nom_societe=nom_societe, adresse=adresse, mdp=mdp, domaine=domaine, image=image)
        db.session.add(recruteur)
        db.session.commit()

        flash('Vous pouvez vous connectez maintenant.', category='success')
        login_user(recruteur, remember=True)
        return redirect('/login')
        

    return render_template('inscrirerecruteur.html')


@auth.route('/inscription-candidat', methods=['GET', 'POST'])
def inscription_candidat():

    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        ville = request.form.get('region')
        mdp = request.form.get('mdp')
        mdp2 = request.form.get('mdp2')
        domaine = request.form.get('domaine')
        cv= request.files['cv']
        image = request.files['image']
        
        imagename='defaut.png'
        cvname = '2c94503a-614d-48df-83bc-1fff181b2282.pdf'
        
        
        if mdp != mdp2:
            flash('Veuillez saisir deux mots de passes identiques !', category='error')
            return redirect('/inscription-candidat')
        
        
        if image:
            imagename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
            image.save(os.path.join(upload_image, imagename))


        if cv:
            cvname = str(uuid.uuid4()) + os.path.splitext(cv.filename)[1]
            cv.save(os.path.join(upload_cv, cvname))
        
        candidat = Candidat(nom=nom, prenom=prenom, email= email, telephone= telephone, mdp=mdp, domaine=domaine ,date_naissance=func.date(), ville=ville, bio='tset', genre='tests', image=imagename, cv=cvname)
        db.session.add(candidat)
        db.session.commit()

        flash('Vous pouvez vous connectez maintenant.', category='success')
        login_user(candidat, remember=True)
        return redirect('/login')

    return render_template('inscrirecandidat.html')



@auth.route('/forgotpassword', methods=['GET', 'POST'])
def forgot_password():

    if request.method == 'POST':
        email = request.form.get('email')

        candidat = Candidat.query.filter_by(email = email).first()
        recruteur = Recruteur.query.filter_by(email = email).first()
        mdp = genere_mdp(8)

        if candidat:
            candidat.mdp = mdp 
            envoie_email(candidat.email, 'Voila votre mot de passe', 'Voici votre nouveau mot de passe : ' + mdp )
            flash('Votre nouveau mot de passe a ete envoyer par mail', category='success')
            db.session.commit()
            return redirect('/login')
        
        elif recruteur:
            recruteur.mdp = mdp 
            envoie_email(recruteur.email, 'Voila votre mot de passe', 'Voici votre nouveau mot de passe : ' + mdp)
            flash('Votre nouveau mot de passe a ete envoyer par mail', category='error')
            db.session.commit()
            return redirect('/login')

        else:
            flash('Email n\'existe pas. Creer un nouveau compte', category='error')


    return render_template("mdpoublie.html")

