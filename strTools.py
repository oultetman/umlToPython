#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     01/03/2020
# Copyright:   (c) Utilisateur 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def remplacer(chaine:str,cherche:str,remplace:str):
    """retourne une copie de chaine dans laquelle cherche est remplacer
    par remplace si possible. Lève une exeption Typeerror si les paramètres
    ne sont pas du type str"""
    if type(chaine)==type(cherche)==type(remplace)==str:
        pos=chaine.find(cherche)
        if pos==-1:
            return chaine
        else:
            return chaine[0:pos]+remplace+chaine[pos+1:]
    else:
        raise TypeError

def enleve_anotation(chaine:str):
    pos=chaine.find(":")
    while pos>=0:
        pos1 = chaine.find(",",pos)
        if pos1==-1: pos1=len(chaine)
        chaine = chaine[:pos]+chaine[pos1:]
        pos = chaine.find(":")
    return chaine
def main():
    print(remplacer("bon jour"," ","_"))
    print(enleve_anotation("date:date,essai:int"))
if __name__ == '__main__':
    main()
