# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:00:55 2020

@author: manil

Alexy Rousseau 21910036
Manil Kesouri 21914480
Simon Cardoso 21605269

"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import scipy.stats


############################# Question 1 ####################################

def generateurCongruentiel(germe, a, b, m):
   courant = germe
   while 1:
      yield courant
      courant = (a*courant+b)%m
     
def generateurB(germe):
    return generateurCongruentiel(germe,22695477,1,2**32)

germe = 19061998 

########################### Question 2 ####################################

gen = generateurB(germe)

d = 10 + next(gen)%16

print("notre d :",d)

alpha = d//4+next(gen)%(d//4)
beta = d//2+next(gen)%(d//4)

print("alpha :", alpha, "beta :", beta)

def appartientIntervalle(alpha,beta,valeur):
    return valeur>=alpha and valeur<=beta

def probaIntervalle(d,alpha,beta):
    return (beta - alpha + 1)/d

print("Probalibilité d'appartenir à l'intervalle :", probaIntervalle(d, alpha, beta))

########################### Question 3 ####################################


#on regroupe tous les individus de taille >= t, pour limiter le nombre de groupes
t = 5+next(gen)%5

print("la valeur t:", t)
           
def constructionIndividu(generateur, d,alpha,beta,t):
    chaine = ""
    while(True):
       valeur = next(generateur)%d
       if(appartientIntervalle(alpha, beta, valeur)):
           if len(chaine) > t :
               return t
           else:
               return len(chaine)   
       else:
           chaine += str(valeur)
           
############################## Question 4 ################################
    

#On définit le nombre de la population selon d, on s'assure que l'effectif soit d'au moins 5

#Cette méthode retourne une liste de populations, chaque population est un ensemble
#d'individus générés par un set de valeurs différents
def constructionPopulation(gen,d,alpha,beta,t,m):
    populations = []
    intermediaire = []
    for test_sets in range(250):
        for individu in range(m):
            intermediaire.append(constructionIndividu(gen, d, alpha, beta, t))
        populations.append(intermediaire.copy())
        intermediaire.clear()
    return populations
        


def constructionObserves(population):
    return np.array(np.unique(population, return_counts=True))

############################## Question 5 ####################################    
    
def calculAttendus(m,p,t):
    dico = {}
    for groupe in range(t+1):
        if(groupe == t):
            dico[groupe] = round(m*(1-p)**t,2)
        else:
            dico[groupe] = round(m*p*(1-p)**groupe,2)
        
    listeClefs = sorted(list(dico.keys()))
    listeValeurs = [dico[clef] for clef in listeClefs]
    return np.array([listeClefs,listeValeurs])

############################## Question 6 ####################################

    
def testChiDeux(observes,attendus):
    return sc.stats.chisquare(observes[1],f_exp=attendus[1])

def appartienIntervalleConfiance(alpha,pvalue):
    return pvalue >= alpha and pvalue < 1-alpha
    
def afficheIntervalles(pvalue):
    listeAlpha = [0.01,0.05,0.1]
    for alpha in listeAlpha:
        if appartienIntervalleConfiance(alpha,pvalue):
            print("La pvalue appartient à l'intervalle [",alpha,",",1-alpha,"[")


m = 1000

populations = constructionPopulation(gen, d, alpha, beta, t, m)


#Affichage des pvalues et intervalles pour chaque test
for i in range(10):
    print("test numéro :", i+1)
    observes = constructionObserves(populations[i])
    attendues = calculAttendus(m,  probaIntervalle(d, alpha, beta), t)
    print("\n observes :\n", observes, "\n\n attendus :\n", attendues, "\n")
    nombreGroupes = len(observes[0])
    pvalue = testChiDeux(attendues, observes)[1]
    print("Pvalue = ", pvalue)
    afficheIntervalles(pvalue)
    print("\n#########################################################################")


################################## Série de tests #####################################


  
def scoreTest(pvalue):
    if pvalue <= 0.01 or pvalue >= 0.99:
        return ["red", 3]
    if (pvalue >= 0.01 and pvalue <= 0.05) or (pvalue >= 0.95 and pvalue <= 0.99):
        return ["orange", 2]
    if (pvalue >= 0.05 and pvalue <= 0.1) or (pvalue >= 0.9 and pvalue <= 0.95):
        return ["blue", 1]
    return ["green", 0]

print("\n")


#Plusieurs fois cinq séries de trois tests
def cinqSeries(gen,d,alpha,beta,t,m):
    series = []
    populations = []
    i = 0
    populations = constructionPopulation(gen, d, alpha, beta, t, m)
    for essai in range(3):
            print("\nessaie numéro :", essai+1, "\n")
            for serie in range(5):
                print("série numéro :", serie+1)
                scoreSerie = 0
                for test in range(3):
                    print("\t test numéro :", test+1)
                    observes = constructionObserves(populations[i])
                    attendues = calculAttendus(m,  probaIntervalle(d, alpha, beta), t)
                    pvalue = testChiDeux(attendues, observes)[1]
                    scoreT = scoreTest(pvalue)
                    print("\t\t score du test :", scoreT[1])
                    scoreSerie += scoreT[1]
                    i+=1
                    series.append(scoreSerie)
    return series
            

series = cinqSeries(gen, d, alpha, beta, t, m)   

#On rejette une série avec un score supérieur ou égal à 4
#On rejette l'hypothèse lorsqu'au moins deux séries sont rejetées
def succesCinqSeries(series):
    counter = 0
    for serie in series:
        if serie >= 4:
            counter += 1
    return counter<2

print("\n")

if succesCinqSeries(series):
    print("L'hypothèse : acceptée")
else:
    print("L'hypothèse : rejetée")




    