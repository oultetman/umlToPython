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
    """
    converti une chaine nom1:type1,nom2:type2 en nom1,nom2
    :param chaine:
    :return:
    """
    pos=chaine.find(":")
    while pos>=0:
        pos1 = chaine.find(",",pos)
        if pos1==-1: pos1=len(chaine)
        chaine = chaine[:pos]+chaine[pos1:]
        pos = chaine.find(":")
    return chaine

def search_getter(chaine:str)->str:
    """
    retourne titre en minuscule si chaine = gettitre, settitre, gettertitre, settertitre,
     get_titre, set_titre, getter_titre, setter_titre,
     getTitre, setTitre, getterTitre, setterTitre,
     get_Titre, set_Titre, getter_Titre, setter_Titre,
    :param chaine:
    :return: str
    """
    pos = max(chaine.find("getter"),chaine.find("setter"))
    if pos==-1:
        pos= max(chaine.find("get"),chaine.find("set"))
        if pos==-1 or pos > 0: return ""
        if chaine[3]=="_" : return chaine[4:].lower()
        return chaine[3:].lower()
    if pos>0 : return ""
    if chaine[6] == "_": return chaine[7:].lower()
    return chaine[6:].lower()


def interchange_element_naming_convention(element_name: str) -> str:
    converted_element_name = ""

    if element_name.find("_")!=-1:  # snake_case
        index = 0
        while index < len(element_name):
            character = element_name[index]
            if character == "_" and (index != 0 or index == len(element_name) - 1):
                converted_element_name += element_name[index + 1].upper()
                index += 1
            else:
                converted_element_name += character
            index += 1
    else:  # camelCase
        for index in range(len(element_name)):
            if element_name[index].isupper():
                if index != 0: converted_element_name += "_"
                converted_element_name += element_name[index].lower()
            else:
                converted_element_name += element_name[index]

    return converted_element_name


def lower_underscore_camel_case(chaine:str)->str:
    """
    Converti une chaine prefix_suffixe en prefixSuffixe
    :param chaine:
    :return: str
    """
    return chaine[0]+"".join([s.capitalize() for s in chaine.split("_")])[1:]

def camel_case_to_lower_underscore(chaine:str)->str:
    """
    Converti une chaine prefixeSuffixe en prefixe_suffixe
    :param chaine:
    :return: str
    """
    return "".join([chaine[i] if chaine[i]==chaine.lower()[i] else "_"+chaine[i] for i in range(len(chaine))])

def main():
    print(remplacer("bon jour"," ","_"))
    print(enleve_anotation("date:date,essai:int"))
    print(camel_case_to_lower_underscore("getTitre"))
    print(lower_underscore_camel_case("get_Titre_Eleve_De_Neige"))
    print(search_getter("set_titre"))
    print(camel_case_to_lower_underscore("getTitreEleveDeNeige"))
if __name__ == '__main__':
    main()
