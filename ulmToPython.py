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
import sys
from Classe2 import *
if len(sys.argv):
    p=Programme(sys.argv[1])
    print(p)
    p.save()
else:
    print("passer le nom du fichier à convertir en argument")
