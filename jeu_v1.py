import pyxel, random, math

# taille de la fenetre 248x180 pixels, chargement des ressources(perso, ennemis, sons), chargement du décor
pyxel.init(248, 180, title="Cours Sonic !")
pyxel.load("assets/ressources.pyxres")
pyxel.image(2).load(0, 0, "assets/BG.jpg") 

# position initiale du personnage
# (origine des positions : coin haut gauche)
personnage_x = 92
personnage_y = 120

vélocité_personnage = 7
masse_personnage = 1
sauter = False
F = None

vies = 1000
score = 0

# initialisation des ennemis
ennemis_liste = []

def personnage_deplacement(x, y):
    global masse_personnage, vélocité_personnage, F, sauter
    """Saut du personnage"""
    if sauter == False:
   
        #si la touche espace est pressée
        if pyxel.btn(pyxel.KEY_SPACE):
                  
            #Le saut est activé
            sauter = True
               
    if sauter :
        # Calcul de la force (F). F = 1 / 2 * masse * vélocité ^ 2.
        F =(1 / 2)*masse_personnage*(vélocité_personnage**2)
           
        # change in the y co-ordinate
        y-= F
           
        # La vélocité diminue en montant, la vélocité devient négatif en descendant
        vélocité_personnage = vélocité_personnage-1
           
        #l'objet a atteint sa hauteur max
        if vélocité_personnage<0:
               
            #un signe négatif est ajouté pour contrer la vélocité négative
            masse_personnage =-1
   
        #l'object a atteint son état d’origine
        if vélocité_personnage == -8:
   
            #donc le saut n'est plus activé
            sauter = False
  
     
            #on redéfinit les valeurs d'origine de la vélocité et la masse
            vélocité_personnage = 7
            masse_personnage = 1

    return x, y


def ennemis_creation(ennemis_liste):
    """création aléatoire des ennemis"""

    # un ennemi toute les 2 secondes en y = 140 de x = 400 à 0
    if (pyxel.frame_count % 60 == 0):
        ennemis_liste.append([random.randint(140, 140), 400])
        
    #un ennemi toute les 1.3 secondes en y = 110 de x = 400 à 0
    if (pyxel.frame_count % 40 == 0):
        ennemis_liste.append([random.randint(110, 110), 400])
        
    if score > 500:
        #un ennemi toute les 2.6 secondes en y = 125 de x = 400 à 0
        if (pyxel.frame_count % 80 == 0):
            ennemis_liste.append([random.randint(125, 125), 400])
        
        
    return ennemis_liste


def ennemis_deplacement(ennemis_liste):
    """déplacement des ennemis de droite à gauche et suppression s'ils sortent du cadre"""
    
    #les obstacles se déplacent de la droite vers la gauche avec une vitesse de 4.5, cette vitesse augmente en fonction du score
    for ennemi in ennemis_liste:
        ennemi[1] -= 4.5
        if  ennemi[1]>400:
            ennemis_liste.remove(ennemi)
        
        if score > 500 and score < 1200:
            ennemi[1] -= 2
            
        if score > 1200:
            ennemi[1] -= 4.5
            
            
    return ennemis_liste

def personnage_suppression(vies):
    """disparition du personnage et d'un ennemi si contact"""

    for ennemi in ennemis_liste:
        #on définit les hitbox pour les contacts 32x32 pour le perso et 8x8 pour les ennemis
        if ennemi[1] <= personnage_x+32 and ennemi[0] <= personnage_y+32 and ennemi[1]+8 >= personnage_x and ennemi[0]+8 >= personnage_y:
            ennemis_liste.remove(ennemi)
            vies -= 1
    return vies


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global personnage_x, personnage_y, ennemis_liste, vies, saute, score
    
    #si le perso meurt, on stoppe la musique principale et la musique game over est jouée en boucle
    if vies == 0:
            pyxel.stop()
            pyxel.play(2, 2, loop=True)

    # mise à jour de la position du personnage
    personnage_x, personnage_y = personnage_deplacement(personnage_x, personnage_y)

    # creation des ennemis
    ennemis_liste = ennemis_creation(ennemis_liste)

    # mise a jour des positions des ennemis
    ennemis_liste = ennemis_deplacement(ennemis_liste)

    # suppression du personnage et ennemi si contact
    vies = personnage_suppression(vies)


# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""
    global score
    if vies > 0:   
        
        #le décor change lorsque le score atteint 1200
        if score > 1200:
            pyxel.image(2).load(0, 0, "assets/BG2.png") 
        
        #on charge l'image 2 en plein écran
        pyxel.blt(0, 0, 2, 0, 0, 248, 180)
        score+= 1
        pyxel.text(5,5, 'VIES:'+ str(vies), 7)    
        pyxel.text(5,20, 'SCORE:'+ str(score), 7)

        # personnage  32x32
        
        #animation du personnage
        idx = (pyxel.frame_count // 5) % 4
        u = 32 * idx
        pyxel.blt(personnage_x, personnage_y, 0, u, 0, 32, 32, 10)

        #ennemis 16x16
        for ennemi in ennemis_liste:
            pyxel.blt(ennemi[1], ennemi[0], 1, 16, 0, 16, 16, 3)
            if score > 1200:
                pyxel.blt(ennemi[1], ennemi[0], 1, 0, 0, 16, 16, 3)

    # sinon: GAME OVER
    else:
        pyxel.image(2).load(0, 0, "assets/BG3.png")
        pyxel.blt(0, 0, 2, 0, 0, 248, 180)
        pyxel.text(98,24, 'GAME OVER', 7)
        pyxel.text(98,34, 'SCORE :'+ str(score), 7)


#lecture de la musique principale en boucle
pyxel.playm(0, loop=True)

pyxel.run(update, draw)