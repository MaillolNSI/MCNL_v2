# ------------------------------
# Imports
# ------------------------------

import os
from guizero import App, Box, Picture, PushButton, Text,CheckBox
from zipfile import ZipFile #Pour dezipper les logiciels telecharges

# ------------------------------
# Variables
# ------------------------------

# Definit le dossier contenant les icones des matieres
logos_dir = "matieres"
logos = [os.path.join(logos_dir, f) for f in os.listdir(logos_dir)]

# Definit le dossier contenant les logiciels
logiciels_dir="logiciels"


# ------------------------------
# Fonctions
# ------------------------------

def recharger(matiere='init'):
    print(matiere)
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
        button.update_command(installer, args=[checkboxes])
                
def installer(logiciels):
    for l in logiciels:
        nom=str(l).split("text '")[-1].replace("'",'')
        print(nom)
        print(l.value)
        if l.value==0:
            #On cherche a désinstaller s'il existe
            pass
        elif l.value==1:
            #On cherche à installer s'il n'existe pas
            pass
            
    

# ------------------------------
# App
# ------------------------------

#On cree la fenetre
app = App("MCNL_v2",height=600, width=800)

buttons_box = Box(app, layout="grid")

matieres = []
buttons = []
boxes=[]
checkboxes=[]
recharger('init')


app.display()
