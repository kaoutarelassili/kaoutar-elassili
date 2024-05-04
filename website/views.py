import datetime
import os
import uuid
from flask import Blueprint, Flask, flash, url_for, request, render_template, redirect,send_from_directory
from flask_login import login_required, current_user
from .models import Candidat
from .models import Recruteur, Offre, Postuler
from . import db
from datetime import date, datetime
from sqlalchemy.sql import func, or_
from .fonctions import envoie_email, genere_mdp, offre_tableau



views = Blueprint('views',__name__)

upload_image = os.path.join(views.root_path, 'static', 'images')
upload_cv = os.path.join(views.root_path, 'static', 'cv') 






@views.route('/upload-cv/<filename>')
def upload_cv_route(filename):
    return send_from_directory(upload_cv, filename)

upload_cv_route = views.root_path + '/static/cv'
upload_image_route = views.root_path + '/static/images'


@views.route('/upload-image/<filename>')
def get_uploaded_image(filename):
    return send_from_directory(upload_image_route, filename)

@views.route('/', methods=['GET', 'POST'])
def home():
      
    offre_emploi=Offre.query.filter_by(status='active').all()
    regions = Offre.query.with_entities(Offre.region.distinct()).all()


    if request.method == 'POST':
        keyword = request.form.get('keyword')
        location = request.form.get('location')

        ks = []
        ls = []

        if (keyword == '' or keyword is None) and location == '0':
            return  render_template("index.html", offre_emploi=offre_emploi, regions=regions)

        
        if keyword != '' and not None:
            ks1 = Offre.query.filter( Offre.titre.like('%'+keyword+'%')).all()

            ks2 = Offre.query.filter(Offre.description.like('%'+keyword+'%')).all()
            ks3 = Offre.query.filter(Offre.speciality.like('%'+keyword+'%')).all()
            ks4 = Offre.query.filter(Offre.type_de_contrat.like('%'+keyword+'%')).all()

            ks = ks1 + ks2 + ks3 + ks4 

        if location != '0':
            ls = Offre.query.filter(Offre.region.like('%'+location+'%')).all()

        rs = [ks, ls]
        bgs = max(rs, key=lambda array: len(array), default=[])
        offres = []

        for i in bgs:
            v = True 

            if keyword != '' and not None:
                if not offre_tableau(i, ks):
                    v = False 
            
            if location != '0':
                if not offre_tableau(i, ls):
                    v = False 
            
            if v:
                offres.append(i)

        return render_template('index.html', offre_emploi=offres, regions = regions)

    return render_template("index.html", offre_emploi=offre_emploi, regions=regions)


@views.route('/mdp-oublie', methods=['GET', 'POST'])
def mdp_oublie():
     

     return render_template('mdpoublie.html')

@views.route('/aboutus')
def aboutus():
      return render_template("aboutus.html")

@views.route('/home-Candidat', methods=['GET', 'POST'])
@login_required
def home_candidate():
    offre_emploi=Offre.query.all()
    
    offre_emploi=Offre.query.filter_by(status='active').all()
    regions = Offre.query.with_entities(Offre.region.distinct()).all()


    if request.method == 'POST':
        keyword = request.form.get('keyword')
        location = request.form.get('location')

        ks = []
        ls = []

        if (keyword == '' or keyword is None) and location == '0':
            return  render_template("home-Candidat.html", user=current_user, offre_emploi=offre_emploi, regions=regions)

        
        if keyword != '' and not None:
            ks1 = Offre.query.filter( Offre.titre.like('%'+keyword+'%')).all()

            ks2 = Offre.query.filter(Offre.description.like('%'+keyword+'%')).all()
            ks3 = Offre.query.filter(Offre.speciality.like('%'+keyword+'%')).all()
            ks4 = Offre.query.filter(Offre.type_de_contrat.like('%'+keyword+'%')).all()

            ks = ks1 + ks2 + ks3 + ks4 

        if location != '0':
            ls = Offre.query.filter(Offre.region.like('%'+location+'%')).all()

        rs = [ks, ls]
        bgs = max(rs, key=lambda array: len(array), default=[])
        offres = []

        for i in bgs:
            v = True 

            if keyword != '' and not None:
                if not offre_tableau(i, ks):
                    v = False 
            
            if location != '0':
                if not offre_tableau(i, ls):
                    v = False 
            
            if v:
                offres.append(i)

        return render_template('home-Candidat.html', user=current_user, offre_emploi=offres, regions = regions)

    return render_template("home-Candidat.html", user=current_user,offre_emploi=offre_emploi, regions=regions) 

@views.route('/home-Recruteur')
@login_required
def home_recruiter():
    offres = Offre.query.filter_by(id_recruteur=current_user.id).all()
    return render_template('tabcandidat.html', user=current_user, offres=offres)

@views.route('/recherche-cv')
@login_required
def recherche_cv():
    return render_template('recherche-cv.html', user=current_user)

@views.route('/candidatures')
@login_required
def candidatures_recruteur():
    offres = Offre.query.filter_by(id_recruteur=current_user.id).all()

    return render_template('candidatures.html', user=current_user, offres=offres)

@views.route('/offres-emplois')
@login_required
def offres_emplois():
    return render_template('offres-emplois.html', user=current_user)





@views.route('/mescandidatures')
@login_required
def mesCandidatures():

    candidatures = Postuler.query.filter_by(id_candidat=current_user.id).all()


    return render_template('mes-Candidatures.html', user=current_user, candidatures=candidatures)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def modif_Candidat():
    upload_image_dir = views.root_path + '/static/images' 
    if request.method == 'POST':
        
        candidat = Candidat.query.filter_by(id=current_user.id).first()
        if candidat is not None:
        

            nom = request.form.get('nom')
            candidat.nom = nom
    


            prenom = request.form.get('prenom')
            candidat.prenom = prenom
        
            email = request.form.get('email')
       
            candidat.email = email

            # mdp= request.form.get('mdp')
       
            # Candidat.mdp = mdp

            domaine= request.form.get('domaine')
       
            candidat.domaine = domaine

            # date_naissance = request.form.get('date_naissance')
       
            # Candidat.date_naissance = date_naissance

            telephone = request.form.get('telephone')
      
            candidat.telephone = telephone

            ville = request.form.get('ville')
        
            candidat.ville = ville

            # bio = request.form.get('bio')
     
            # Candidat.bio = bio

            genre= request.form.get('genre')
    
            candidat.genre = genre

        image= request.files['image']
        
        if image:
            imagename = str(uuid.uuid4()) + os.path.splitext(image.filename)[1]
            image.save(os.path.join(upload_image, imagename))
            candidat.image = imagename
 
            
        cv = request.files['cv']


        if cv:
            cvname = str(uuid.uuid4()) + os.path.splitext(cv.filename)[1]
            cv.save(os.path.join(upload_cv, cvname))
            candidat.cv = cvname
             

     
        db.session.commit()
        flash('Votre modification a ete effectuer avec success', category='success')
        return redirect('/profile')

    return render_template("profile.html",user=current_user)




@views.route('/informationpersonnel', methods=['GET', 'POST'])
@login_required
def modif_recruteur():
    if request.method == 'POST':
        
        recruteur = Recruteur.query.filter_by(id=current_user.id).first()
        if recruteur is not None:
          
            
            nom = request.form.get('nom')
            recruteur.nom = nom
    


            prenom = request.form.get('prenom')
            recruteur.prenom = prenom
        
            email = request.form.get('email')
       
            recruteur.email = email
            
            nom_societe = request.form.get('nom_societe')
      
            recruteur.nom_societe = nom_societe
            
            adresse = request.form.get('adresse')
        
            recruteur.adresse = adresse
             
            domaine= request.form.get('domaine')
       
            recruteur.domaine = domaine
          
             
        db.session.commit()

        flash('Votre modification a été effectuée avec succès.', category='success')
        return redirect('/informationpersonnel')

    return render_template("informationpersonnel.html",user=current_user)



@views.route('/supprimerCandidat')
@login_required
def supprimerCandidat():
        candidat = Candidat.query.filter_by(id=current_user.id).first()
        if candidat:
            postulations = Postuler.query.filter_by(id_candidat=current_user.id).all()
            for postulation in postulations:
                db.session.delete(postulation)
            db.session.delete(candidat)
            db.session.commit()
            flash('Votre compte a été supprimé avec succès.', category='success')

        return redirect('/')
            
@views.route('/supprimerRecruteur')
@login_required
def supprimerRecruteur():
        recruteur = Recruteur.query.filter_by(id=current_user.id).first()
        if recruteur:
            offers = Offre.query.filter_by(id_recruteur=current_user.id).all()
            for offre in offers:
                postulations = Postuler.query.filter_by(id_offre=offre.id).all()
                for postulation in postulations:
                    db.session.delete(postulation)
                db.session.delete(offre)

            db.session.delete(recruteur)
            db.session.commit()
            flash('Votre compte a été supprimé avec succès.', category='success')

        return redirect('/')



@views.route('/display-cv/<cvname>')
@login_required
def display_cv(cvname):
    return send_from_directory('static/cv', cvname, as_attachment=True)

@views.route('/ajouter-offre', methods=['GET', 'POST'])
@login_required
def add_offer():
    if request.method == 'POST':
        titre = request.form.get('titre')
        description = request.form.get('description')
        region = request.form.get('region')
        salaire = float(request.form.get('salaire'))
        speciality = request.form.get('speciality')
        dateLimite = datetime.strptime(request.form.get('dateLimite'), "%Y-%m-%d").date()
        type_de_contrat=request.form.get('type_de_contrat')
        


        offre = Offre( id_recruteur = current_user.id, titre=titre, description=description, region=region, salaire=salaire, status='active', dateCreation=func.date(), dateLimite = dateLimite, speciality=speciality, type_de_contrat= type_de_contrat)
        
        db.session.add(offre)
        db.session.commit()

        flash('Loffre a été bien ajoutée.', category='success')
        return redirect(url_for('views.home_recruiter'))  # Redirect to the offers page or any desired page

    return render_template("ajouter-offre.html", user=current_user)

@views.route('/offre-profile/<string:offre_id>')
def offre(offre_id):
    offre = Offre.query.filter_by(id=offre_id).first()

    offre_id = offre.id if offre else None
    offre = Offre.query.get_or_404(offre_id )

    if offre:
        print("\n\n\n"+str(offre)+"\n\n\n")

    return render_template("afficherrec.html", user=current_user,title=offre.titre,offre=offre ) 
############################

@views.route('/offre-c/<string:offre_id>')
def offrec(offre_id):
    offre = Offre.query.filter_by(id=offre_id).first()

    if offre:
        print("\n\n\n"+str(offre)+"\n\n\n")

    return render_template("offre.html", user=current_user,title=offre.titre,offre=offre ) 


@views.route('/offre-visiteur/<string:offre_id>', methods=['GET','POST'])
def offre_visiteur(offre_id):

    if request.method == 'POST':
        flash('Vous devez vous connecter premièrement. ', category='error')
        return redirect('/login')
    
    offre = Offre.query.filter_by(id=offre_id).first()


    if offre:
        print("\n\n\n"+str(offre)+"\n\n\n")

    return render_template("offrev.html", user=current_user,title=offre.titre,offre=offre ) 

# wa khaltek li tu m'ecoute -- oui oui 



@views.route("/offres-emploisrec", methods=["GET", "POST"])
@login_required
def user_offre():
   
    offres = Offre.query.filter_by(id_recruteur= current_user.id).all()
    
    return render_template("offres-emploisrec.html", title="Mes offres", user=current_user, offres=offres)



@views.route("/offres/modifier/<string:offre_id>", methods=["GET", "POST"])
@login_required  
def modifier_offre(offre_id):
    offre = Offre.query.get_or_404(offre_id)


    if request.method == "POST":
        offre.titre = request.form.get("titre")
        offre.description = request.form.get("description")
        offre.region = request.form.get("region")
        offre.speciality = request.form.get("speciality")
        offre.categories = request.form.get("categories")
        offre.status = request.form.get("status")
        offre.type_de_contrat = request.form.get("type_de_contrat")
        offre.salaire = (request.form.get("salaire"))

        db.session.commit()
        flash("L'offre a été modifiée avec succès", "success")
        return redirect('/offre-profile/'+offre.id)

    return render_template("modifier_offre.html", user=current_user, offre=offre)
###########################

@views.route('/postuler/<string:offre_id>')
@login_required
def postuler(offre_id):
    offre = Offre.query.filter_by(id=offre_id).first()
    postulations = Postuler.query.filter_by(id_offre=offre_id).all()
    for postulation in postulations:
        if postulation.id_candidat == current_user.id:
           
            flash('Vous avez déjà postulé à cette offre.', category = 'error')
            return redirect('/home-Candidat')
    postulation = Postuler(id_candidat= current_user.id, id_offre= offre.id, status = 'En Attente',dateApply=func.date())
    db.session.add(postulation)    
    db.session.commit()
    flash("Votre candidature a été soumise avec succès", "success")

    return redirect('/home-Candidat')

@views.route('/offres/annuler/<offre_id>')
def offres_annuler(offre_id):
    offre = Offre.query.filter_by(id=offre_id).first()
    postulations = Postuler.query.filter_by(id_offre=offre.id).all()
    

    for p in postulations:
        db.session.delete(p)
    
    db.session.delete(offre)

    #offre.status = 'Annuler'

    db.session.commit()
    flash('Cette offre a été supprimée. ',category='success')
    return redirect('/candidatures')

@views.route('/offre-candidats-profile/<offre_id>')
def offre_candidats_profile(offre_id):

    offre = Offre.query.filter_by(id = offre_id).first()
    cs = Postuler.query.filter_by(id_offre=offre_id).all()
    candidats = []
    for c in cs:
        candidat = Candidat.query.filter_by(id=c.id_candidat).first()
        candidats.append(candidat)

    return render_template('tab1candidat.html', user=current_user, offre=offre, candidats=candidats)

@views.route('/candidat-profile/<candidat_id>')
def candidat_profile(candidat_id):
    candidat = Candidat.query.filter_by(id=candidat_id).first()
    
    return render_template('infoscandidat.html', user=current_user, candidat=candidat )

