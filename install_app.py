# ------------------------------
# Imports
# ------------------------------

import os
from guizero import App, Box, Picture, PushButton, Text,CheckBox
from zipfile import ZipFile #Pour dezipper les logiciels telecharges
import requests

# ------------------------------
# Variables
# ------------------------------

# Header pour se faire passer pour un navigateur
headers = { 'DNT': '1',
            'sec-ch-ua': '"Opera";v="81", " Not;A Brand";v="99", "Chromium";v="95"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 OPR/81.0.4196.60'
            }

# Definit le dossier contenant les icones des matieres
logos_dir = "matieres"
logos = [os.path.join(logos_dir, f) for f in os.listdir(logos_dir)]

# Definit le dossier contenant les logiciels
logiciels_dir="logiciels"
# On le cree s'il n'existe pas
if not os.path.exists('logiciels'):
    os.makedirs('logiciels')
#Creer le dossier vide pour chaque categorie de logiciels
for f in os.listdir(logos_dir):
    f=f.replace('.png','')
    chemin=os.path.join(logiciels_dir, f)
    if not os.path.exists(chemin):
        os.makedirs(chemin)

# ------------------------------
# Fonctions
# ------------------------------

def recharger(matiere='init'):
    print(matiere)
    #Le fichier devra etre stocke en ligne plus tard pour
    #toujours etre a jour
    fichier=open('detail.csv','r')
    contenu=fichier.readlines()
    fichier.close()
    #On supprime toutes les boxes existantes
    for b in boxes:
        try:
            b.destroy()
        except:
            pass
        #boxes.remove(b)
    for c in checkboxes:
        try:
            c.destroy()
        except:
            pass
    if matiere=='init':
        i,x,y=0,0,0
        
        while len(logos)>i:
            box = Box(buttons_box, grid=[x,y])
            boxes.append(box)
            logo=logos[i]
            i+=1
            matiere=logo.split('\\')[1].replace('.png','')

            button = PushButton(box)
            button.image = logo
            button.update_command(recharger, args=[matiere])
            buttons.append(button)
            text = Text(box, text=matiere)
            matieres.append(text)
            if x<5:
                x+=1
            else:
                x=0
                y+=1
    #On met de nouveaux boutons avec les sous-categories     
    else:
        x=0
        y=0
        sous_cat=[]
        for ligne in contenu[1:]:
            try:
                if matiere in ligne:
                    c=ligne.replace(f"{matiere};",'').split(';')[0]
                    #Si la longueur est supérieure 3 c'est qu'il y a une sous categorie
                    if len(ligne.replace(f"{matiere};",'').split(';'))>2:
                        if c not in sous_cat:
                            sous_cat.append(c)
                            box = Box(buttons_box, grid=[x,y])
                            boxes.append(box)
                            
                            button = PushButton(box, text=c)
                            buttons.append(button)
                            button.update_command(recharger, args=[f"{matiere};{c}"])
                            print(f"{matiere};{c}")
                            if x<5:
                                x+=1
                            else:
                                x=0
                                y+=1
                    #Sinon on direct un logiciel, on met les checkbox avec les logiciels
                    else:
                        box = Box(buttons_box, grid=[x,y])
                        boxes.append(box)
                        nom_logiciel=ligne.split(';')[-2]
                        checkbox = CheckBox(box, text=nom_logiciel)
                        #On verifie si le logiciel est installé
                        d=os.path.join(logiciels_dir, ligne.split(';')[0])
                        dossiers=[os.path.join(d, f) for f in os.listdir(d)]
                        for l in dossiers:
                            if nom_logiciel in l:
                                checkbox.value=1
                        checkboxes.append(checkbox)
                        if x<5:
                            x+=1
                        else:
                            x=0
                            y+=1
                            
            except:
                pass
        x=0
        y+=1
        box = Box(buttons_box, grid=[x,y])
        boxes.append(box)
        text = Text(box, text="")
        y+=1
        box = Box(buttons_box, grid=[x,y])
        boxes.append(box)
        button = PushButton(box, text="Retour")
        buttons.append(button)
        if ';' in matiere:
            retour=matiere.replace(';'+matiere.split(';')[-1],'')
        else:
            retour='init'
        button.update_command(recharger, args=[f"{retour}"])
        x+=1
        box = Box(buttons_box, grid=[x,y])
        boxes.append(box)
        button = PushButton(box, text="Appliquer")
        buttons.append(button)
        button.update_command(installer, args=[checkboxes,matiere])
                
def installer(logiciels,matiere):
    print(matiere)
    for l in logiciels:
        nom=str(l).split("text '")[-1].replace("'",'')
        installed=0
        dossier=os.path.join('logiciels',matiere.replace(';','\\'))
        dossier=os.path.join(dossier, nom)
        if os.path.exists(dossier):
            installed=1
        #On cherche a désinstaller s'il existe
        if l.value==0 and installed==1:
            print(f'On desinstalle {nom}')
            #On supprime le dossier
            os.system(f"rmdir /s /q {dossier}")
            
        #On cherche à installer s'il n'existe pas
        elif l.value==1 and installed==0:
            print(f'On installe {nom}')
            #On recupere le lien vers le logiciel
            fichier=open('detail.csv','r')
            contenu=fichier.readlines()
            fichier.close()
            #print(f"{matiere};{nom}")
            for ligne in contenu:
                #print(ligne)
                if f"{matiere};{nom}" in ligne:
                    lien=ligne.split(';')[-1]
            print(lien)
            #On telecharge le zip
            print('Telechargement lance')
            response = requests.get(lien,
                                    headers=headers)
            d=os.path.join('logiciels',matiere.replace(';','\\'))
            fichier=os.path.join(d,nom)
            print(fichier)
            #https://drive.google.com/uc?export=download&confirm=${CODE}&id=<FILE_ID>
            open(f"{fichier}.zip", "wb").write(response.content)
            
            print('Telechargement OK')
            
            #On cree le dossier
            #os.makedirs(dossier)
            #On dezippe le fichier
            with ZipFile(f"{fichier}.zip", 'r') as zipObj:
                zipObj.extractall(d)
            #On supprime le zip
            os.remove(f"{fichier}.zip")
    

# ------------------------------
# App
# ------------------------------

#On cree la fenetre
app = App("MCNL_v2022",height=600, width=800)

buttons_box = Box(app, layout="grid")

matieres = []
buttons = []
boxes=[]
checkboxes=[]
## On telechargera le fichier csv avec les infos

## On initialise la fenetre avec les matieres 
recharger('init')


app.display()
