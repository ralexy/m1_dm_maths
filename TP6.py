# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:00:55 2020

@author: manil

"""

import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import scipy.stats
import random
import sys

################# Question 1 ####################################

#Fonction générique pour définir un générateur congruentiel linéaire
def generateurCongruentiel(germe, a, b, m):
   courant = germe
   while 1:
      yield courant
      courant = (a*courant+b)%m
     
def generateurB(germe):
    return generateurCongruentiel(germe,22695477,1,2**32)

germe = 19061998 #mettez votre date de naissance

################# Question 2 ####################################

gen = generateurB(germe)

d = 10 + next(gen)%16
    
valeur = next(gen)%d

print(d, "et notre valeur :", valeur)

alpha = d//4+next(gen)%(d//4)
beta = d//2+next(gen)%(d//4)

print("alpha :", alpha, "beta :", beta)

def appartientIntervalle(alpha,beta,valeur):
    return valeur>=alpha and valeur<=beta

print(appartientIntervalle(alpha, beta, valeur))

def probaIntervalle(d,alpha,beta):
    return (beta - alpha + 1)/d

print(probaIntervalle(d, alpha, beta))


#on regroupe tous les individus de taille >= t, pour limiter le nombre de groupes
t = 5+next(gen)%5

print("la valeur t:", t)

def constructionIndividu(generateur, d,alpha,beta,t):
    chaine = ""
    while(True):
       valeur = next(generateur)%d 
       if(appartientIntervalle(alpha, beta, valeur)):
           return len(chaine)   
       else:
           chaine += str(valeur)
    

print(constructionIndividu(gen, d, alpha, beta, t))

#On définit le nombre de la population selon d, on s'assure que l'effectif soit d'au moins 5
m = d * 10


def constructionPopulation(gen,d,alpha,beta,t,m):
    population = []
    observes = []
    for n in range(m):
        population.append(constructionIndividu(gen, d, alpha, beta, t))
    observes = np.unique(population, return_counts=True)
    for i in range(t+1, len(observes[0])):
        observes[1][t] += observes[1][i]
    groupes = np.delete(observes[0], np.s_[t+1::])
    frequences = np.delete(observes[1], np.s_[t+1::])
    return np.array([groupes, frequences])

observes = constructionPopulation(gen, d, alpha, beta, t, m)

print("\n\n", observes, "\n\n")

def calculAttendus(m,p,t):
    dico = {}
    for groupe in range(t+1):
        dico[groupe] = round(m*p*(1-p)**groupe,2)
    listeClefs = sorted(list(dico.keys()))
    listeValeurs = [dico[clef] for clef in listeClefs]
    return np.array([listeClefs,listeValeurs])



p = probaIntervalle(d, alpha, beta)

attendues = calculAttendus(m, p, t)

print(attendues)
    