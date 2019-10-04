#!/usr/bin/env python3
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
from random import shuffle


from Creation_texture import la_texture


def metric(paterne,paterne_cible,dispersion):
    """ABSOLUMENT URGENT DE VERIFIER CECI"""
    valeur = 0
    for couleur1,couleur2 in zip(paterne,paterne_cible):
        r1,g1,b1 = couleur1
        r2,g2,b2 = couleur2
        r = 1 + ((r1-r2)/dispersion)**2
        g = 1 + ((g1-g2)/dispersion)**2
        b = 1 + ((b1-b2)/dispersion)**2
        valeur += np.log(r*g*b)
    return(valeur)


def choix(N_plus_proches,N_candidats,position,texture,nouveau,dispersion):
    """
    choisis le meilleur candidat parmi N_candidats (positions dans texture je le rappelle)
    par rapport à la distribution de Cauchy et aux valeurs rgb de nouveau[N_plus_proches]

    On va donc d'abord chercher le meme paterne que celui former par les N_plus_proches pour position pour chaque candidat et ensuite chercher celui qui minimise la metric
    """
    x,y = position
    a,b,c = texture.shape
    vecteur_paternes = []
    decalages = list((a-x,b-y) for a,b in N_plus_proches)
    for candidat in N_candidats:
        c1,c2 = candidat
        vecteur_paternes.append(list(texture[(c1+d1)%a,(c2+d2)%b] for d1,d2 in decalages))
    paterne_cible = list(nouveau[pos] for pos in N_plus_proches)

    indice_meilleur = 0
    score = metric(vecteur_paternes[0],paterne_cible,dispersion)
    for i,paterne in enumerate(vecteur_paternes):
        valeur = metric(paterne,paterne_cible,dispersion)
        if valeur < score:
            indice_meilleur = i
            score = valeur
    return(N_candidats[indice_meilleur])

def localisation(position,nouveau,texture,origine_pixel,rempli_ou_non,N):
    """
    renvoie un couple avec:
        les N plus proches tq nouveau[N_plus_proches] = rgb les plus proches de position
        les N candidats (position dans texture) issues du principe de continuité décrit par Harrison et tirées de texture celle là
    """
    x,y = position
    N_positions_proches  = []#positons dans nouveau hein
    a,b = rempli_ou_non.shape
    a,b = a//2,b//2#pour remettre cohérent par rapport à synthèse

    cran = 1 #cran désigne le décalage par rapport à position dans lequel on va regarder
    while len(N_positions_proches)<N:
        """les bandes..."""
        for i in range(-cran+1,cran):
            if y-cran>=0 and x+i>=0 and x+i<2*a and rempli_ou_non[x+i,y-cran]:
                N_positions_proches.append((x+i,y-cran))
            if y+cran<2*b and x+i>=0 and x+i<2*a and rempli_ou_non[x+i,y+cran]:
                N_positions_proches.append((x+i,y+cran))
        for j in range(-cran+1,cran):
            if x-cran>=0 and y+j>=0 and y+j<2*b and rempli_ou_non[x-cran,y+j]:
                N_positions_proches.append((x-cran,y+j))
            if x+cran<2*a and y+j>=0 and y+j<2*b and rempli_ou_non[x+cran,y+j]:
                N_positions_proches.append((x+cran,y+j))
        """et les coins"""
        if x-cran>=0 and y-cran>=0 and rempli_ou_non[x-cran,y-cran]:
            N_positions_proches.append((x-cran,y-cran))
        if x-cran>=0 and y+cran<2*b and rempli_ou_non[x-cran,y+cran]:
            N_positions_proches.append((x-cran,y+cran))
        if x+cran<2*a and y+cran<2*b and rempli_ou_non[x+cran,y+cran]:
            N_positions_proches.append((x+cran,y+cran))
        if x+cran<2*a and y-cran>=0 and rempli_ou_non[x+cran,y-cran]:
            N_positions_proches.append((x+cran,y-cran))
        """QUEL ENFER CES IF"""
        cran +=1
    N_positions_proches = N_positions_proches[:N]


    #N_plus_proches = list(nouveau[position] for position in N_positions_proches)
    N_plus_proches = N_positions_proches

    N_origines = list(origine_pixel[position] for position in N_positions_proches)
    """Gros doutes sur le dessous là"""
    N_candidats = list(((i + (x-q))%a,(j + (y-s))%b) for (q,s),(i,j) in zip(N_positions_proches,N_origines))

    return(N_plus_proches,N_candidats) #essayer de penser à un test qui permettrait de vérifier ... je sais pas trop


def synthese(texture,N,M,dispersion,etapes):
    """
    on va créer une image deux fois plus grande que texture : nouveau
    origine_pixel va nous permettre de tracer l'origine des pixels synthétisés càd que le pixel synthétisé à la position x,y est tiré dans texture de la position origine_pixel[x,y]
    rempli_ou_non nous indique si une position a déja reçu une valeur de texture ou non

    positions enumere les 2*a * 2*b positions que nous allons avoir à remplir pour remplir notre nouvelle image nouveau
    """
    a,b,c = texture.shape
    nouveau = np.zeros((2*a,2*b,c))
    origine_pixel = np.zeros((2*a,2*b,2),dtype = np.uint8) #de par le type uint8 taille maximale de texture c'est 256*256
    rempli_ou_non = np.zeros((2*a,2*b),dtype = bool) #initialisation à False, rien n'a encore été rempli

    positions = list((x,y) for y in range(2*b) for x in range(2*a))

    avancement = set()

    p = 0.5 #hyperparametre présenté p.44 de dissertation.pdf en lien avec etapes et le processus de raffinage

    for etape in range(etapes,0,-1):
        shuffle(positions) #on mélange positions histoire d'avoir un ordre de complétion aléatoire, non prévisible
        for position,_ in zip(positions,range(int(2*a*2*b * p**etape))):
            if len(avancement)<N:
                i,j = np.random.randint(0,a),np.random.randint(0,b)
                nouveau[position] = texture[i,j]
                origine_pixel[position] = (i,j)
                rempli_ou_non[position] = True
                avancement.add(position)
            else:
                """on est assuré d'avoir déja N positions synthétisés et on peut donc utiliser la méthode décrite par Harrison"""
                N_plus_proches,N_candidats = localisation(position,nouveau,texture,origine_pixel,rempli_ou_non,N)
                """faire les M_candidats aussi"""

                meilleur_candidat = choix(N_plus_proches,N_candidats,position,texture,nouveau,dispersion)

                nouveau[position] = texture[meilleur_candidat]
                origine_pixel[position] = meilleur_candidat
                rempli_ou_non[position] = True
                avancement.add(position)

    """on finit enfin en (re)passant sur TOUTES les positions de nouveau"""
    shuffle(positions)
    for position in positions:
        if len(avancement)<N:
            i,j = np.random.randint(0,a),np.random.randint(0,b)
            nouveau[position] = texture[i,j]
            origine_pixel[position] = (i,j)
            rempli_ou_non[position] = True
            avancement.add(position)
        else:
            """on est assuré d'avoir déja N positions synthétisés et on peut donc utiliser la méthode décrite par Harrison"""
            N_plus_proches,N_candidats = localisation(position,nouveau,texture,origine_pixel,rempli_ou_non,N)
            """faire les M_candidats aussi"""

            meilleur_candidat = choix(N_plus_proches,N_candidats,position,texture,nouveau,dispersion)

            nouveau[position] = texture[meilleur_candidat]
            origine_pixel[position] = meilleur_candidat
            rempli_ou_non[position] = True
            avancement.add(position)

    return(nouveau)





texturepil = Image.open("texture4.jpg")
texture = np.asarray(texturepil)

texture=texture

image = synthese(texture,4,1,30,3)

texture = np.uint8(texture)
image=np.uint8(image)
texturepil = Image.fromarray(texture)
texturepil.save("input.jpg")


nouvelle_imgpil = Image.fromarray(image)
nouvelle_imgpil.save("output.jpg")
