from toolbox import *
import math
import re

# Définition des constantes globales
LONG_FENETRE = 800
LARG_FENETRE = 800
CENTRE_X = LONG_FENETRE // 2
CENTRE_Y = LARG_FENETRE // 2
MAX = 5
DIV = MAX / 100

def trouverPoints(centre, R, num_points):
    points = []
    angle_increment = 2 * math.pi / num_points

    for i in range(num_points):
        angle = i * angle_increment
        x = centre.x + R * math.cos(angle)
        y = centre.y + R * math.sin(angle)
        P = Point(x, y)
        points.append(P)

    return points

def absolue(nombre):
    return abs(nombre)

def repere():
    P = Point(CENTRE_X, CENTRE_Y)
    segment(Point(0, P.y), Point(LONG_FENETRE, P.y), BLANC)
    segment(Point(P.x, 0), Point(P.x, LARG_FENETRE), BLANC)

def distance(p1, p2):
    return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5

def relier(liste):
    for i in range(len(liste)):
        if liste[i] != liste[-1]:
            segment(liste[i], liste[i+1], JAUNE)

###########################################################

def find_y(A, B, x):
    # Coefficients de l'équation quadratique en y
    a = 1
    b = 2 * B * x + 2
    c = A * x ** 2 + 2 * x

    # Calcul du discriminant
    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        return None, None  # Pas de solutions réelles

    sqrt_discriminant = discriminant ** 0.5

    # Solutions de l'équation quadratique
    y1 = (-b + sqrt_discriminant) / (2 * a)
    y2 = (-b - sqrt_discriminant) / (2 * a)

    return y1, y2

#################################################################

def valeurs_pose(A, B, r, zoom):
    y1_values = []
    y2_values = []

    x_increment = 1 / zoom  # Adjust the increment based on zoom

    x = 0
    while x < r:
        y1, y2 = find_y(A, B, x)
        if y1 is not None and y2 is not None:
            y1_values.append(int(y1 * zoom))
            y2_values.append(int(y2 * zoom))
        x += x_increment

    return [y1_values, y2_values]

def valeurs_neg(A, B, r, zoom):
    y1_values = []
    y2_values = []

    x_increment = 1 / zoom  # Adjust the increment based on zoom

    x = 0
    while x < r:
        y1, y2 = find_y(A, B, -x)
        if y1 is not None and y2 is not None:
            y1_values.append(int(y1 * zoom))
            y2_values.append(int(y2 * zoom))
        x += x_increment

    return [y1_values, y2_values]

#####################################################################

def tracer_pose(A, B, r, zoom):
    l = valeurs_pose(A, B, r, zoom)
    l1 = l[0]
    l2 = l[1]
    x_increment = 1 / zoom  # Adjust the increment based on zoom

    x = 0
    for i in range(1, len(l1)):
        if x * zoom + CENTRE_X < LONG_FENETRE and x * zoom + CENTRE_X > 0:
            y1 = l1[i]
            y2 = l2[i]
            y1_prev = l1[i - 1]
            y2_prev = l2[i - 1]
            x_prev = x - x_increment
            if y1 + CENTRE_Y < LARG_FENETRE:
                segment(Point(int(x_prev * zoom) + CENTRE_X, y1_prev + CENTRE_Y), Point(int(x * zoom) + CENTRE_X, y1 + CENTRE_Y), ROUGE)
            segment(Point(int(x_prev * zoom) + CENTRE_X, y2_prev + CENTRE_Y), Point(int(x * zoom) + CENTRE_X, y2 + CENTRE_Y), ROUGE)
            x += x_increment

def tracer_neg(A, B, r, zoom):
    l = valeurs_neg(A, B, r, zoom)
    l1 = l[0]
    l2 = l[1]
    x_increment = 1 / zoom  # Adjust the increment based on zoom

    x = 0
    for i in range(1, len(l1)):
        if CENTRE_X - x * zoom < LONG_FENETRE and CENTRE_X - x * zoom > 0:
            y1 = l1[i]
            y2 = l2[i]
            y1_prev = l1[i - 1]
            y2_prev = l2[i - 1]
            x_prev = x - x_increment
            if y1 + CENTRE_Y < LARG_FENETRE:
                segment(Point(CENTRE_X - int(x_prev * zoom), y1_prev + CENTRE_Y), Point(CENTRE_X - int(x * zoom), y1 + CENTRE_Y), ROUGE)
            segment(Point(CENTRE_X - int(x_prev * zoom), y2_prev + CENTRE_Y), Point(CENTRE_X - int(x * zoom), y2 + CENTRE_Y), ROUGE)
            x += x_increment

def tracer(A, B, r, zoom):
    tracer_pose(A, B, r, zoom)
    tracer_neg(A, B, r, zoom)
    afficher_tout()

#######################################################################

def film(A, B, r, zoom):
    delta_A = 0.1
    delta_B = math.tan(A)
    
    while True:
        # Limiter les valeurs de A et B
        if A >= MAX:
            delta_A = -0.1
        elif A <= -MAX:
            delta_A = 0.1
        
        '''if B >= MAX:
            delta_B = -0.1
        elif B <= -MAX:
            delta_B = 0.1'''
        
        # Effacer l'écran
        remplir(NOIR)
        
        # Tracer les courbes avec les nouvelles valeurs de A et B
        tracer(A, B, r, zoom)
        
        # Mettre à jour les valeurs de A et B
        A += delta_A
        '''B += delta_B'''
        
        # Pause pour éviter un taux de rafraîchissement trop élevé
        attendre(10)

###################################################################################

def suivre_affine(A, p, q, r, zoom): # B = p * A + q
    deb, fin = tracer_fonction_affine(A, p, q)
    while A < MAX:
        B = A * p + q       
        # Effacer l'écran
        remplir(NOIR)
        # Tracer les courbes avec les nouvelles valeurs de A et B
        segment(deb,fin,JAUNE)
        cercle_plein(Point(int(A * (CENTRE_X / MAX) + CENTRE_X), int(B * (CENTRE_Y / MAX)) + CENTRE_Y), 3, JAUNE)
        repere()
        tracer(A, B, r, zoom)
                 
        # Mettre à jour les valeurs de A et B
        A += DIV
        
        # Pause pour éviter un taux de rafraîchissement trop élevé
        attendre(10)

def tracer_fonction_affine(A, p, q):
    # Coefficients long , larg
    LONG = int(CENTRE_X / MAX)
    LARG = int(CENTRE_Y / MAX)
    
    # Calcul des points les plus à gauche et à droite
    x_left = -MAX
    y_left = p * x_left + q
    
    x_right = MAX
    y_right = p * x_right + q
    
    point_left = Point(int(x_left * LONG + CENTRE_X), int((p * x_left + q) * LARG) + CENTRE_Y)
    point_right = Point(int(x_right * LONG + CENTRE_X), int((p * x_right + q) * LARG) + CENTRE_Y)
    
    return point_left, point_right
####################################################################################

def suivre_sec(A, a, b, c, r, zoom): # B = p * A + q
    li = tracer_fonction_sec(A, a, b, c)
    while A < MAX:
        B = A*A*a + A*b + c      
        # Effacer l'écran
        remplir(NOIR)
        # Tracer les courbes avec les nouvelles valeurs de A et B
        cercle_plein(Point(int(A * (CENTRE_X / MAX) + CENTRE_X), int(B * (CENTRE_Y / MAX)) + CENTRE_Y), 3, JAUNE)
        repere()
        relier(li)
        tracer(A, B, r, zoom)
                 
        # Mettre à jour les valeurs de A et B
        A += DIV
        
        # Pause pour éviter un taux de rafraîchissement trop élevé
        attendre(10)
        
def tracer_fonction_sec(A, a, b, c):
    li = []
    # Coefficients long , larg
    LONG = int(CENTRE_X / MAX)
    LARG = int(CENTRE_Y / MAX)
    while A < MAX:
        y = A*A*a + A*b + c 
        li.append(Point(int(A * LONG + CENTRE_X), int(y * LARG) + CENTRE_Y))
        A += DIV
    return li
    
##############################################################################    
    
def suivre_fonc(A, fonc, r, zoom):
    li = tracer_fonction(A,fonc)
    while A < MAX:
        B = trad(A, fonc)
        # Effacer l'écran
        remplir(NOIR)
        # Tracer les courbes avec les nouvelles valeurs de A et B
        cercle_plein(Point(int(A * (CENTRE_X / MAX) + CENTRE_X), int(B * (CENTRE_Y / MAX)) + CENTRE_Y), 3, JAUNE)
        repere()
        relier(li)
        tracer(A, B, r, zoom)
                 
        # Mettre à jour les valeurs de A et B
        A += DIV
        
        # Pause pour éviter un taux de rafraîchissement trop élevé
        attendre(10)
        
def tracer_fonction(A, fonc):
    li = []
    # Coefficients long , larg
    LONG = int(CENTRE_X / MAX)
    LARG = int(CENTRE_Y / MAX)
    while A < MAX:
        y = trad(A, fonc)
        li.append(Point(int(A * LONG + CENTRE_X), int(y * LARG) + CENTRE_Y))
        A += DIV
    return li

###############################################################################

def trad(A, fonc):
    nb = 0
    for i in range(len(fonc)-1):
        nb += fonc[i]*A**(len(fonc)-1-i)
    nb += fonc[-1]
    return nb
    
###############################################################################

def main():
    fenetre(LONG_FENETRE, LARG_FENETRE, "Coniques")
    afficher_auto_off()
    
    A = -MAX
    B = 0.7
    zoom = 70
    range = 1000
    a = -1
    b = 3
    c = -3
    d = 1
    suivre_affine(-MAX, a, b, range, zoom)
    suivre_sec(-MAX, a, b, c, range, zoom)
    suivre_fonc(-MAX, [-1,3,-3,1], range, zoom)
    suivre_fonc(-MAX, [-1,3,-1,-1.8,2], range, zoom)
    suivre_fonc(-MAX, [-0.55 ,2.5,-1,-4.2,+1,-2.4],range,zoom)
    #film(A,B, range, zoom)
    
    attendre_echap()
    quitter()

main()
