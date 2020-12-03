import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import scipy.stats
import random
import sys
sys.setrecursionlimit(100000)

#exercice de Knuth
#expérience aléatoire : lancer de deux dés
#variable aléatoire : somme des deux dés

################################################################################"
#Partie 1 -- génération des valeurs avec la fonction random.randint

def generateurRandom():
    yield random.randint(1,36)
    for nombre in generateurRandom():
        yield nombre

gen1 = generateurRandom()

def jetDeuxDes(gen):
    nombre = next(gen)
    return nombre%6+1, (nombre//6)%6+1

def variableAleatoire(i,j):
     return i+j

def constructionAttendus(N):
    dico = {}
    for i in range(1,7):
        for j in range(1,7):
            somme = i+j
            if somme in dico:
                dico[somme] += 1
            else:
                dico[somme] = 1
    listeClefs = sorted(list(dico.keys()))
    listeValeurs = [(dico[clef]*N)/36 for clef in listeClefs]
    return np.array([listeClefs,listeValeurs])

def constructionPopulation(gen,N):
    liste = []
    for n in range(N):
        i, j = jetDeuxDes(gen)
        liste.append(variableAleatoire(i,j))
    return liste

def constructionObserves(population):
    return  np.unique(population, return_counts=True)

def histogrammeValeurs(population,nombreGroupes):
    plt.hist(population,bins=nombreGroupes)
    plt.show()

def testChiDeux(observes,attendus):
    return sc.stats.chisquare(observes[1],f_exp=attendus[1])

def appartienIntervalle(alpha,pvalue):
    return pvalue >= alpha and pvalue < 1-alpha

def afficheIntervalles(pvalue):
    listeAlpha = [0.01,0.05,0.1]
    for alpha in listeAlpha:
        if appartienIntervalle(alpha,pvalue):
            print("La pvalue appartient à l'intervalle [",alpha,",",1-alpha,"[")

print("################################################################")
print("Test du générateur mersenne")
N = 144
population1 = constructionPopulation(gen1,N)
attendus = constructionAttendus(N)
observes1 = constructionObserves(population1)
nombreGroupes1 = len(observes1[0])
print(nombreGroupes1)
print(observes1)

#histogramme des différents groupes
histogrammeValeurs(population1,nombreGroupes1)
pvalue = testChiDeux(attendus, observes1)[1]
print("Pvalue = ", pvalue)
afficheIntervalles(pvalue)
#pvalue = 0.24380680001101077
#La pvalue appartient à l'intervalle [ 0.01 , 0.99 [
#La pvalue appartient à l'intervalle [ 0.05 , 0.95 [
#La pvalue appartient à l'intervalle [ 0.1 , 0.9 [


###########################################################################"
# Partie 2 -- génération des nombre avec un générateur congruentiel linéaire

#Fonction générique pour définir un générateur congruentiel linéaire
def generateurCongruentiel(germe, a, b, m):
   courant = germe
   while 1:
      yield courant
      courant = (a*courant+b)%m

#Définition des générateurs Randu, Standard et Borlan C++

def generateurRandu(germe):
    return generateurCongruentiel(germe,65539,0,2**31)

def generateurStandard(germe):
    return generateurCongruentiel(germe,16807,0,2**31-1)

def generateurBorland(germe):
    return generateurCongruentiel(germe,22695477,1,2**32)

germe = 12111998 #mettez votre date de naissance

###############################################################
#Etude de Randu

print("################################################################")
print("Test du générateur Randu")
genRandu = generateurRandu(germe)
population2 = constructionPopulation(genRandu,144)
observes2 = constructionObserves(population2)
nombreGroupes2 = len(observes2[0])
print(nombreGroupes2)#8 il manque trois groupe
print(observes2)#il manque les groupes 2, 10 et 12
#on ne peut donc pas faire le test du chi-deux

#test en retirant le 8 derniers bits

def jetDeuxDes2(gen):
    nombre = (next(gen)//256)%36
    return nombre%6+1, nombre//6+1

def constructionPopulation2(gen,N):
    liste = []
    for i in range(N):
        i, j = jetDeuxDes2(gen)
        liste.append(variableAleatoire(i,j))
    return liste

print("################################################################")
print("Test du générateur Randu en retirant le 8 derniers bits")

population2bis = constructionPopulation2(genRandu,144)
observes2bis = constructionObserves(population2bis)
nombreGroupes2bis = len(observes2[0])
print(nombreGroupes2bis) #11 il ne manque pas de groupe
print(observes2bis) #on peut donc le test du chi-deux
histogrammeValeurs(population2bis,nombreGroupes2bis)
pvalue = testChiDeux(attendus, observes2bis)[1]
print("pvalue = ", pvalue)
afficheIntervalles(pvalue)
#Pvalue = 0.7896469944732578
#La pvalue appartient à l'intervalle [ 0.01 , 0.99 [
#La pvalue appartient à l'intervalle [ 0.05 , 0.95 [
#La pvalue appartient à l'intervalle [ 0.1 , 0.9 [

###############################################################
#Etude de Standard minimal

print("################################################################")
print("Test du générateur Standard minimal")
genStandard = generateurStandard(germe)
population3 = constructionPopulation(genStandard,144)
observes3 = constructionObserves(population3)
nombreGroupes3 = len(observes3[0])
print(nombreGroupes3)#10 il manque un groupe
print(observes3)#il manque le groupe 2
#on ne peut donc pas faire le test du chi-deux


###############################################################
#Etude de Borland C++

print("################################################################")
print("Test du générateur Borland C++")
genBorland = generateurBorland(germe)
population4 = constructionPopulation(genBorland,144)
observes4 = constructionObserves(population4)
nombreGroupes4 = len(observes4[0])
print(nombreGroupes4)#11 il ne manque pas de groupe
print(observes4)#on peut donc le test du chi-deux

histogrammeValeurs(population4,nombreGroupes1)
pvalue = testChiDeux(attendus, observes4)[1]
print("pvalue = ", pvalue)
afficheIntervalles(pvalue)
#Pvalue = 0.011876992952189813
#La pvalue appartient à l'intervalle [ 0.01 , 0.99 [

########################################################"
#jet de trois dés

def jetTroisDes(gen):
    nombre = next(gen)
    return nombre%6+1,(nombre//6)%6+1,(nombre//36)%6+1

def variableAleatoire3des(i,j,k):
     return i+j+k

def constructionPopulation3des(gen,N):
    liste = []
    for n in range(N):
        i, j,k = jetTroisDes(gen)
        liste.append(variableAleatoire3des(i,j,k))
    return liste

def constructionAttendus3des(N):
    dico = {}
    for i in range(1,7):
        for j in range(1,7):
            for k in range(1,7):
                somme = i+j+k
                if somme in dico:
                    dico[somme] += 1
                else:
                    dico[somme] = 1
    listeClefs = sorted(list(dico.keys()))
    listeValeurs = [(dico[clef]*N)/6**3 for clef in listeClefs]
    return np.array([listeClefs,listeValeurs])

########################################################"
print("Test du générateur Borland C++ avec trois dés")
N= 1200
attendus4bis = constructionAttendus3des(N)
print("attendus", attendus4bis)
#avec N = 12 tous les groupes ont une cardinalité attendue supérieure à 5
population4bis = constructionPopulation3des(genBorland,N)
observes4bis = constructionObserves(population4bis)
nombreGroupes4bis = len(observes4bis[0])
print(nombreGroupes4bis)#16 il ne manque pas de groupe
print(observes4bis)#on peut donc le test du chi-deux
histogrammeValeurs(population4,nombreGroupes1)
pvalue = testChiDeux(attendus, observes4)[1]
print("pvalue = ", pvalue)
afficheIntervalles(pvalue)
#pvalue = 0.011876992952189813
#La pvalue appartient à l'intervalle [ 0.01 , 0.99 [
