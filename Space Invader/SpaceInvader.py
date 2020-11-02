#Programme : Space Invader Modifie
#Auteur : Lucie KECA, Antoine LORIN
#Date : 10/02/2019




import pygame
pygame.font.init()
#Constantes de couleur

rouge = (126, 14, 11)
bleu = (11, 33, 126)
vert = (11, 126, 16)
gris = (79, 86, 78)
noir = (0,0,0)
blanc = (255,255,255)
violet = (87, 31, 151)


LargeurDeLaFenetre = 500
LongueurDeLaFenetre = 500


NombreDeLignes=4
NombreDeColonnes=5



#Variable Des ennemis et du joueur
VitesseEnnemis = 0.005
VitesseJoueur = 0.25
ImageJoueur = pygame.image.load("Joueur.png")
ImageEnnemis1 = pygame.transform.scale(pygame.image.load('alien1.png'), (25, 25))
ImageEnnemis2 = pygame.transform.scale(pygame.image.load('alien2.png'), (25, 25))
ImageEnnemis3 = pygame.transform.scale(pygame.image.load('alien3.png'), (25, 25))
TempsDeMouvementDesEnnemis = 10




pygame.init()


EcranDeJeu = pygame.display.set_mode((LargeurDeLaFenetre,LongueurDeLaFenetre),pygame.RESIZABLE)
pygame.display.set_caption('Space Invader !')



Minuteur = pygame.time.get_ticks()


#Class de definition des ennemis
class Ennemis():

    def __init__(self,x,y,groupe):

        self.largeur = 25
        self.hauteur = 25
        self.x = 185+x
        self.y = 150+y
        self.groupe = groupe
        self.Minuteur = Minuteur
        self.rect = pygame.Rect((self.x,self.y),(self.largeur,self.hauteur))


    #Definition pour le mouvement des ennemis
    def MouvementEnnemis(self,Temps=0):


    	if (Temps - self.Minuteur) > TempsDeMouvementDesEnnemis:
            if self.groupe == 1:
                self.y += -VitesseEnnemis
                EcranDeJeu.blit(ImageEnnemis1,(self.x, self.y))
            if self.groupe == 2:
                self.x += VitesseEnnemis
                EcranDeJeu.blit(ImageEnnemis2,(self.x, self.y))
            if self.groupe == 3:
                self.x += -VitesseEnnemis
                EcranDeJeu.blit(ImageEnnemis3,(self.x, self.y))
            if self.groupe == 4:
                self.y += VitesseEnnemis
                EcranDeJeu.blit(ImageEnnemis1,(self.x, self.y))
            Minuteur = pygame.time.get_ticks()
            self.rect = pygame.Rect((self.x,self.y),(self.largeur,self.hauteur))



#Class de definition des tirs
class Tirs():
    def __init__(self,x):
        self.largeur = 8
        self.hauteur = 8
        self.x = x+5
        self.y = 450
        self.image = pygame.transform.scale(pygame.image.load("Joueur.png"), (self.largeur, self.hauteur))
        self.rect = pygame.Rect((self.x,self.y),(self.largeur,self.hauteur))


    #Fonction permettant de faire bouger les balles
    def MouvementTir(self):
        self.y += -0.5
        EcranDeJeu.blit(self.image,(self.x,self.y))
        self.rect = pygame.Rect((self.x,self.y),(self.largeur,self.hauteur))

Liste = []

#Fonction de creation des aliens
def CreationDesEnnemis():
    print("Creation Des Ennemis")


    for k in range (0,NombreDeLignes+1):
        for i in range(0,NombreDeColonnes+1):
            Ennemi = Ennemis((k*25),(i*25),i)
            Liste.append(Ennemi)

    return Liste

#Fonction permettant d afficher le joueur et ses mouvements
def EmplacementJoueur(x):

    EcranDeJeu.blit(ImageJoueur,(x,450))
    pygame.display.flip()



#Fonctions pour faire les mouvement de TOUT les ennemis
def DeplacementEnnemis(Nombredevilains,Temps):

    for Ennemis in Nombredevilains:
        Ennemis.MouvementEnnemis(Temps)

#Fonctions pour faire les mouvement de TOUTES les balles
def MouvementDesBalles(ListeBalle):
    for Tirs in ListeBalle:
        Tirs.MouvementTir()


#Fonction pour gerer les collisions
def Collisions(ListeBalle,ListeEnnemis):
    for Ennemis in ListeEnnemis:
        rectEnnemis = Ennemis.rect
        for Tirs in ListeBalle:
            rectTir = Tirs.rect

            if rectEnnemis.colliderect(rectTir):

                ListeBalle.remove(Tirs)
                ListeEnnemis.remove(Ennemis)



def AfficherMessageGagner ():
    EcranDeJeu.fill(gris)
    Ecrire = pygame.font.SysFont('orena',40)
    MessageDeFin ="Bien joué ! Vous avez gagné "
    Texte=Ecrire.render(MessageDeFin,False,bleu)
    rectangleTexte = Texte.get_rect()
    rectangleTexte .topleft = (70,190)
    EcranDeJeu.blit(Texte,rectangleTexte)



def BoucleDuJeu():

    pygame.display.flip()
    #Definition de la couleur du fond
    EcranDeJeu.fill(gris)
    #Creation des ennemis et attribution du nombre d ennemis a cette variable
    NombreEnnemis = CreationDesEnnemis()

    Temps = pygame.time.get_ticks()
    JeuEnCours = True
    x = 100

    Deplacement_X = 0
    #Initialisation de la liste contenant les balles
    ListeBalle =[]

    print("Debut du jeu")
    while JeuEnCours:

        Temps = pygame.time.get_ticks()
        DeplacementEnnemis(NombreEnnemis,Temps)


        for event in pygame.event.get():
            #arret du jeu si on clique sur la croix
            if event.type == pygame.QUIT:
                JeuEnCours = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    Deplacement_X = -VitesseJoueur


                if event.key == pygame.K_RIGHT:

                    Deplacement_X = VitesseJoueur
                if event.key == pygame.K_SPACE:
                    Balle = Tirs(x)
                    ListeBalle.append(Balle)


            if event.type == pygame.KEYUP:
                Deplacement_X = 0



        Collisions(ListeBalle,NombreEnnemis)

        MouvementDesBalles(ListeBalle)
        #Verification que le personnage ne sorte pas du rectangle
        if x<0:
            x=0
        elif x>480:
            x=480

        x += Deplacement_X

        EmplacementJoueur(x)

        EcranDeJeu.fill(gris)

        if len(Liste)==0:
            AfficherMessageGagner()



BoucleDuJeu()
print("Arret du jeu")
pygame.quit()