# -------------------------------------------------------------------------------
# Nom:        module1
# Description:
#
# Auteur:      Utilisateur
#
# Created:     05/05/2019
# Copyright:   (c) Utilisateur 2019
# Licence:     <your licence>
# -------------------------------------------------------------------------------
from decode import *
from strTools import remplacer, enleve_anotation
import sys
from typing import List

version = float(sys.version[:3])


class Import:

    def __init__(self):
        self.interface = False
        self.abstract = False
        self.importation = []

    def __str__(self):
        s = ""
        if self.abstract or self.interface:
            s += "from abc import ABC,abstractmethod\n"
        if self.interface:
            s += "from interface.interface import interface\n"
        s += listToStr(self.importation, "\n")
        return s + "\n\n"

    def add_import(self, importation: str):
        self.importation.append(importation)


class Variable:
    def __init__(self, nom, typeVar="", defaut=""):
        self.nom = remplacer(nom.strip(), " ", "_")
        self.typeAtt = typeVar
        self.defaut = defaut

    def __str__(self):
        if self.defaut == "":
            if self.typeAtt == "" or version < 3.6:
                return self.nom
            else:
                return "{}:{}".format(self.nom, self.typeAtt)
        else:
            if self.typeAtt == "" or version < 3.6:
                return "{}={}".format(self.nom, self.defaut)
            else:
                return "{}:{}={}".format(self.nom, self.typeAtt, self.defaut)

    def str_nom(self):
        return self.nom

    def str_init(self):
        if self.valInit is not None and self.valInit != "":
            init = self.valInit
        else:
            init = self.nom
        if self.typeAtt == "" or version < 3.6:
            return "self.{}={}".format(self.nom, init)
        else:
            return "self.{}:{}={}".format(self.nom, self.typeAtt, init)


class Attribut(Variable):
    def __init__(self, nom, valInit, typeAtt=''):
        super().__init__(nom, typeAtt)
        self.valInit = valInit

    def __str__(self):
        return super().__str__() + "=" + str(self.valInit)


class Methode:
    def __init__(self, nom, *variables):
        self.nom = remplacer(nom.strip(), " ", "_")
        self.variables: List[Variable] = []
        self.instance = True
        if self.nom.find("<abstract>") >= 0:
            self.nom = self.nom[10:].strip()
            self.abstract = True
        else:
            self.abstract = False
        for v in variables:
            self.variables.append(v)
        self.retour = ""

    def addVariable(self, nom, typeVar="", defaut=""):
        self.variables.append(Variable(nom, typeVar, defaut))

    def variablesToStr(self):
        """
        :return: liste des variables d'une méthode sous la forme str
        nom:type=valeur,...
        """
        s = ""
        for v in self.variables:
            s += v.__str__() + ','
        return s[:-1]

    def str_noms(self):
        """
        :return: liste des variables d'une méthode sous la forme str
        nom1, nom2,...
        """
        s = ""
        for v in self.variables:
            s += v.str_nom() + ','
        return s[:-1]

    def init_variable_str(self, str_tab="", nbTab=0):
        """
        :return: liste des variables d'une méthode sous la forme str
        self.nom1=nom1
        self.nom2=nom2
        """
        s = ""
        for v in self.variables:
            s += str_tab * nbTab + v.srt_init() + '\n'
        return s[:-1]

    def __str__(self):
        s = ""
        if self.abstract:
            s = "@abstractmethod\n    "
        if self.instance:
            s += "def " + self.nom + "(self,"
        else:
            s += "def " + self.nom + "(cls,"
        if len(self.variables) > 0:
            s += self.variablesToStr()
        else:
            s = s[:-1]
        s += ")"
        if self.retour != "":
            s += "->" + self.retour
        if self.nom == "":
            s = ""
        return s


class Commentaire:
    def __init__(self, nom, texte):
        self.nom = nom
        self.commentaire = texte

    def __str__(self):
        return self.commentaire


class Classe:
    dico_return = {"bool": "True", "int": "1", "float": "3.14", "str": '"str"'}

    def __init__(self, nom=""):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        if nom != "":
            self.nom = remplacer((nom[0].upper() + nom[1:]).strip(), " ", "_")
        else:
            self.nom = ""
        self.heritage = []
        self.enfants = []
        self.methodeInstance: List[Methode] = []
        self.methodeClass = []
        self.AttributClass = []
        self.AttributInstance = []
        self.commentaire = None
        self.interface = False
        self.abstract = False
        self.composition = []
        self.ordre = -1

    def init(self, dic):
        self.x = dic['x']
        self.y = dic['y']
        self.width = dic['width']
        self.height = dic['height']
        self.nom = dic['id'].strip().split("(")[0]
        pos = self.nom.find("<interface>")
        if pos >= 0:
            self.nom = self.nom[:pos]
            self.interface = True
            imp.interface = True
        pos = self.nom.find("<abstract>")
        if pos >= 0:
            self.nom = self.nom[:pos]
            self.abstract = True
            imp.abstract = True
        at = dic['attrs'].split("|")
        for a in at:
            t = ""
            if a != "":
                attrib = a.split("<class>")
                if len(attrib) == 2:
                    a = attrib[1].strip()
                pos1 = a.find(":")
                pos2 = a.find("=")
                if pos1 != -1:
                    v = a[:pos1]
                    if pos2 != -1:
                        t = a[pos1 + 1:pos2]
                        val = a[pos2 + 1:]
                    else:
                        t = a[pos1 + 1:]
                        val = None
                else:
                    if pos2 != -1:
                        v = a[:pos2]
                        val = a[pos2 + 1:]
                    else:
                        v = a
                        val = None
                        t = ""
                if len(attrib) == 2:
                    self.addAttribut(Attribut(v, val, t), "C")
                else:
                    self.addAttribut(Attribut(v, val, t), "I")
        met = dic['meths'].split("|")
        for m in met:
            meth = m.split("<class>")
            var1 = ""
            var2 = ""
            if len(meth) == 2:
                m = meth[1].strip()
            pos = m.find("(")
            pos1 = m.find(")")
            pos2 = m.find("->")
            if pos == -1:
                nom = m
                var = ""
            else:
                nom = m[0:pos]
                var1 = m[pos + 1:pos1]
                if pos2 > 0:
                    var2 = m[pos2 + 2:]
                else:
                    var2 = ""
            if len(var1) > 0:
                var1 = tuple(var1.split(","))
                if var1[0].lower() == "self":
                    var1 = var1[1:]
                me = Methode(nom)
                if len(meth) == 2:
                    me.instance = False
                for v in var1:
                    v = v.split("=")
                    if len(v) == 1:
                        v = v[0].split(":")
                        if len(v) == 1:
                            me.addVariable(v[0])
                        else:
                            me.addVariable(v[0], v[1], "")
                    else:
                        v[0] = v[0].split(":")
                        if len(v[0][0]) == 1:
                            me.addVariable(v[0][0], "", "")
                        else:
                            me.addVariable(v[0][0], v[0][1], v[1])
            else:
                me = Methode(nom)
            if me.nom != "":
                if len(meth) == 2:
                    me.instance = False
                    self.addMethode(me, "C")
                else:
                    self.addMethode(me, "I")
                me.retour = var2
        for m in self.methodeInstance:
            if m.nom == "__init__":
                for a in self.AttributInstance:
                    for v in m.variables:
                        if a.nom == v.nom and a.valInit == None:
                            a.valInit = v.nom
                            break
                break

    def __str__(self):
        tab = 0
        s = ""
        abst = ""
        if self.abstract:
            abst = "    # abstractClass <{}>\n".format(self.nom)
        if self.interface:
            s += "@interface\nclass {}({}):\n".format(self.nom, "ABC")
            s += "    # interface <{}>\n".format(self.nom)
        else:
            if self.herite() == "" and self.abstract:
                s += "class {}(ABC):\n{}".format(self.nom, abst)
            else:
                s += "class {}({}):\n{}".format(self.nom, self.herite(), abst)
            impl = False
            for c in self.heritage:
                if c.interface:
                    s += "    # <{}> implements <{}>\n".format(self.nom, c.nom)
                    impl = True
                    break
            if not impl and self.herite() != "":
                s += "    # <{}> extends <{}>\n".format(self.nom, self.herite())
        tab += 1
        if self.commentaire != None:
            s += "    " * tab + '"""{}"""'.format(self.commentaire) + "\n"
        if len(self.AttributClass) > 0:
            for a in self.AttributClass:
                s += "    " * tab + a.__str__() + "\n"
            s += "\n"
        if len(self.methodeClass) > 0:
            for m in self.methodeClass:
                s += "    " * tab + m.__str__() + ":\n" + ("    " * (tab + 1)) + "pass\n\n"

        if len(self.methodeInstance) > 0:
            for m in self.methodeInstance:
                s += "    " * tab + m.__str__() + ":\n"
                if m.nom == "__init__" and not m.abstract:
                    if len(self.heritage) > 0:
                        param = ""
                        for c in self.heritage:
                            for m in c.methodeInstance:
                                if m.nom == "__init__":
                                    param = m.str_noms()
                                    break
                            if param != "":
                                break
                        s += ("    " * (tab + 1)) + "super().__init__({})\n".format(param)
                    if len(self.AttributInstance) > 0:
                        tab += 1
                        for a in self.AttributInstance:
                            s += "    " * tab + a.str_init() + "\n"
                        tab -= 1
                    s += "\n"
                elif m.abstract or self.interface:
                    s = s[:-1] + "pass\n"
                elif m.nom == "__str__":
                    tab += 1
                    s += "    " * tab + 's="' + self.nom + '"\n'
                    s += "    " * tab + "return s\n\n"
                    tab -= 1
                elif m.retour != "":
                    s += ("    " * (tab + 1)) + f"return {Classe.dico_return.get(m.retour,1)}\n\n"
                else:
                    s += ("    " * (tab + 1)) + "pass\n\n"
            if m.abstract or self.interface:
                s += "\n"
        else:
            s += "    " * tab + "pass\n\n"
        return s

    def addMethode(self, methode, typeMethode="I"):
        if typeMethode.upper() == "I":
            self.methodeInstance.append(methode)
        elif typeMethode.upper() == "C":
            self.methodeClass.append(methode)
        else:
            assert TypeError

    def addAttribut(self, attribut, typeAttibut="I"):
        if typeAttibut.upper() == "I":
            self.AttributInstance.append(attribut)
        elif typeAttibut.upper() == "C":
            self.AttributClass.append(attribut)
        else:
            assert TypeError

    def addParent(self, parent):
        self.heritage.append(parent)

    def addEnfant(self, enfant):
        self.enfants.append(enfant)

    def addComposition(self, composition):
        self.composition.append(composition)

    def herite(self):
        return listToStr([n.nom for n in self.heritage])

    def affiche_ordre(self):
        return f"{self.nom} {self.ordre}"


class Programme:
    capitalizeClassName = True
    repuml = "./uml/"
    reppy = "./umlToPy/"

    @classmethod
    def cleanName(cls, nom):
        pos = nom.find("<")
        if pos > 0:
            return nom[:pos].strip()
        else:
            return nom.strip()

    def __init__(self, fichierPyns, version="3.7"):
        self.uml = []
        self.classes: List[Classe] = []
        self.commentaires = []
        self.chargePyns(Programme.repuml + fichierPyns)
        self.nom = fichierPyns.split(".")[0]
        self.graphe = []

    def trouveByName(self, nom):
        index = 0
        for c in self.classes:
            if c.nom.lower() == nom.lower():
                return index
            index += 1
        return -1

    def trouveCommentaireByName(self, nom):
        index = 0
        for c in self.commentaires:
            if c.nom.lower() == nom.lower():
                return index
            index += 1
        return -1

    def affiche_ordre(self):
        for c in self.classes:
            print(c.affiche_ordre())

    def classeExist(self, nom):
        for c in self.classes:
            if c.nom.lower() == nom.lower():
                return True
        return False

    def commentaireExist(self, nom):
        for c in self.commentaires:
            if c.nom == nom:
                return True
        return False

    def chargePyns(self, fichierPyns):
        try:
            with open(fichierPyns, 'r') as f:
                # Opérations sur le fichier
                t = f.read()
                self.uml = t.split("\n")
                self.uml = self.uml[1:-1]

            for u in self.uml:
                dic = eval(u)
                print(dic)
                if dic['type'] == "umlshape":
                    if dic['id'].strip().lower() == "<import>":
                        importation = dic["attrs"].split("|")
                        for i in importation:
                            imp.add_import(i)
                    else:
                        c = Classe()
                        c.init(dic)
                        if not (self.classeExist(c.nom)):
                            if Programme.capitalizeClassName:
                                c.nom = c.nom[0].upper() + c.nom[1:]
                            self.classes.append(c)
                elif dic['type'] == 'comment':
                    c = Commentaire(dic['id'], Decode.decodeChaine(dic['comment']))
                    if not (self.commentaireExist(c.nom)):
                        self.commentaires.append(c)
                elif dic['type'] == "edge" and dic['uml_edge_type'] == "generalisation":
                    index = self.trouveByName(Programme.cleanName(dic['source']))
                    nom = Programme.cleanName(dic['target'])
                    (self.classes[self.trouveByName(Programme.cleanName(dic['target']))]).addEnfant(
                        self.classes[self.trouveByName(Programme.cleanName(dic['source']))])
                    (self.classes[index]).addParent(self.classes[self.trouveByName(nom)])

                elif dic['type'] == "edge" and dic['uml_edge_type'] == "association":
                    if self.classeExist(dic['source']) and self.commentaireExist(dic['target']):
                        (self.classes[self.trouveByName(dic['source'])]).commentaire = self.commentaires[
                            self.trouveByName(dic['target'])]
                    elif self.classeExist(dic['target']) and self.commentaireExist(dic['source']):
                        (self.classes[self.trouveByName(dic['target'])]).commentaire = self.commentaires[
                            self.trouveByName(dic['source'])]
                elif dic['type'] == "edge" and dic['uml_edge_type'] == "composition":
                    index = self.trouveByName(Programme.cleanName(dic['source']))
                    nom = Programme.cleanName(dic['target'])
                    (self.classes[index]).addComposition(self.classes[self.trouveByName(nom)])
                    (self.classes[self.trouveByName(Programme.cleanName(dic['source']))]).addEnfant(
                        self.classes[self.trouveByName(Programme.cleanName(dic['target']))])
        except IOError:
            print("Erreur! Le fichier n'a pas pu être ouvert")

    def triClasse(self, classe):
        classe.ordre -= 1
        if len(classe.enfants) > 0:
            for c in classe.enfants:
                self.triClasse(c)
            return
        return

    def parcours_largeur(self, c: Classe):
        self.graphe.append(c)
        c.ordre = 0
        while len(self.graphe) > 0:
            pere = self.graphe.pop(0)
            for fils in pere.enfants:
                if fils.ordre == -1:
                    self.graphe.append(fils)
                    fils.ordre = pere.ordre + 1
                else:
                    pere.ordre = fils.ordre - 1

    def __str__(self):
        for cl in self.classes:
            cl.ordre = -1
        for c in self.classes:
            if len(c.enfants) > 0:
                self.parcours_largeur(c)
        self.classes.sort(key=lambda cls: cls.ordre)
        s = ""
        s += imp.__str__()
        for c in self.classes:
            s += c.__str__()
        return s

    def save(self):
        f = open(Programme.reppy + self.nom + ".py", 'w')
        f.write(self.__str__())
        f.close()


def listToStr(liste, separateur=',', avant='', apres=''):
    s = ''
    for i in liste:
        s += str(i) + separateur
    s = avant + s[:-1] + apres
    return s


imp = Import()


def main():
    p = Programme("mediatheque.pyns")
    print(p)
    p.save()


if __name__ == '__main__':
    main()
