#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Utilisateur
#
# Created:     14/12/2019
# Copyright:   (c) Utilisateur 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import string
class Transcode:
    transcodage=[["EUk0","ABCDEFGHIJKLMNO","EIMQUYcgkosw048"],["FVl1","PQRSTUVWXYZ","AEIMQUYcgko"],
    ["GWm2","abcdefghijklmno","EIMQUYcgkosw048"],["HXn3","pqrstuvwxyz","AEIMQUYcgko"],
    ["DTjz","0123456789:;<=>?","AEIMQUYcgkosw048"],["CSiy"," !\"#$%&'()*+,-./","AEIMQUYcgkosw048"],
    ["q"," ¡¢£¤¥¦§¨©ª«¬­®¯","AEIMQUYcgkosw048"],["r","°±²³´µ¶·¸¹º»¼½¾¿","AEIMQUYcgkosw048"],
    ["4","ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏ","AEIMQUYcgkosw048"],["5","ÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞß","AEIMQUYcgkosw048"],
    ["6","àáâãäåæçèéêëìíîï","AEIMQUYcgkosw048"],["7","ðñòóôõö÷øùúûüýþÿ","AEIMQUYcgkosw048"],
    ["upper","ABCDEFGHIJKLMNOPQRSTUVWXYZ","BCDEFGHIJKLMNOPQRSTUVWXYZa"],["lower","abcdefghijklmnopqrstuvwxyz","hijklmnopqrstuvwxyz0123456"],
    ["num","0123456789","wxyz012345"],["asc"," !\"#$%&'()*+,-./","ghijklmnopqrstuv"]]

    def encode(car,fin=False):
        if fin==False:
            debut=0
        else:
            debut=12
        for i in range(debut,len(Transcode.transcodage)):
            trans=Transcode.transcodage[i]
            pos=trans[1].find(car)
            if pos>=0:
                return trans[0],trans[2][pos]
        return None

    def decode(c1,c2,fin=False):
        if fin==False:
            debut=0
        else:
            debut=12
        for i in range(debut,len(Transcode.transcodage)):
            trans=Transcode.transcodage[i]
            if c1=="" :
                pos=trans[2].find(c2)
                if pos>=0:
                    return trans[0],trans[1][pos]
            elif c1 in trans[0]:
                pos=trans[0].find(c1)
                pos1=trans[2].find(c2)
                return pos,trans[1][pos1]


class Decode:
    b="IJKLMNOPQRSTUVWXYZabcdef"
    c="AQgw"
    f="GWm2"
    g="HXn3"
    h="EUk0"
    k="FVl1"
    asc="Mcs8"
    num="DTjz"
    sup="CSiy"
    d=""
    d=d.join(list(string.ascii_uppercase)+list(string.ascii_lowercase)+[str(i) for i in range(10)]+["!"," "])
    transAsciiEtendu=["AEIMQUYcgkosw048",d[0:-2]+"+/"]
    dico={}
    for i in range(32,128):
        dico[b[(i-32)//4]+c[i%4]]=chr(i)
    for i in range(4,8):
        for j,ca in enumerate(transAsciiEtendu[0]):
            dico["w"+str(i)+ca]=chr((i+8)*16+j)

    def encode1(s):
        if len(s)>1 or (127<=ord(s)<=161):
            raise ValueError
        if ord(s)<127:
            return Decode.b[(ord(s)-32)//4]+Decode.c[ord(s)%4]+"=="
        else:
            encodage=Transcode.encode(s)
            return "w{}{}=".format(encodage[0],encodage[1])

    def encode2(sprecedente,car):
        if sprecedente[-1]!="=":
            raise ValueError
        if sprecedente[0] in Decode.b:
            pos="AQgw".find(sprecedente[1])
            encodage=Transcode.encode(car)
            return sprecedente[0]+chr(ord(encodage[0][pos]))+encodage[1]+"="
        elif sprecedente[0]=="w":
            encodage=Transcode.encode(car,True)
            pos=1
            if encodage[0]=="num" or encodage[0]=="asc":
                pos=0
            return sprecedente[:2]+Decode.d[Decode.d.find(sprecedente[2])+pos]+encodage[1]
        raise ValueError

    def encode3(sprecedente,car):
        if sprecedente[-1]=="=":
            encodage=Transcode.encode(car,True)
            pos=1
            if encodage[0]=="num" or encodage[0]=="asc":
                pos=0
            return sprecedente[:2]+Decode.d[Decode.d.find(sprecedente[2])+pos]+encodage[1]

    def decode1(s):
        if len(s)!=4 or s[2:]!="==":
            raise ValueError
        pos=Decode.b.find(s[0])
        if pos>=0:
            pos1="AQgw".find(s[1])
            if pos1>=0:
                return chr(32+pos*4+pos1)
            else:
                raise ValueError
        return Decode.dico[s[:2]]

    def decode2(s):
        if len(s)!=4 or s[2]=="=" or s[3]!="=":
            raise ValueError
        if s[0]=="w":
            return "",Transcode.decode(s[1],s[2])[1]
        else:
            decode=Transcode.decode(s[1],s[2])
            return s[0]+"AQgw"[decode[0]]+"==",decode[1]

    def decode3(s):
        decode=Transcode.decode("",s[3],True)
        pos=1
        if decode[0]=="num" or decode[0]=="asc":
            pos=0
        return s[:2]+Decode.d[Decode.d.find(s[2])-pos]+"=",decode[1]

    def decode(s):
        """decode une chaine (de 1 à 3 caractères) encodée"""
        p=s.find("=")
        if p==2:
            return Decode.decode1(s)
        elif p==3:
            decodage=Decode.decode2(s)
            if decodage[0]=="":
                return decodage[1]
            else:
                return Decode.decode1(decodage[0])+decodage[1]
        else:
            decodage=Decode.decode3(s)
            return Decode.decode(decodage[0])+decodage[1]

    def encode(s):
        """encode une chaine de 1 à 3 caractère"""
        for c in range(len(s)):
            if c==0:
                r=Decode.encode1(s[c])
            elif c==1:
                r=Decode.encode2(r,s[c])
            elif c==2:
                r=Decode.encode3(r,s[c])
        return r



    def encodeChaine(chaine):
        """Encode une chaine de caractère"""
        t=[]
        for i in range(0,len(chaine),3):
            if i+3<=len(chaine):
                t.append(chaine[i:i+3])
            else:
                t.append(chaine[i:])
        s=""
        for bloc in t:
            s+=Decode.encode(bloc)
        return s

    def decodeChaine(chaine):
        """Décode une chaine de caractère"""
        t=[]
        for i in range(0,len(chaine),4):
            if i+4<=len(chaine):
                t.append(chaine[i:i+4])
            else:
                t.append(chaine[i:])
        s=""
        for bloc in t:
            s+=Decode.decode(bloc)
        return s

def main():
##    for i in range(32,128):
##        print(chr(i),Decode.code(chr(i)))
##
##    chaine=["e0","ezt","22","g 2","e0t","mý","555","tp"]
##
##    for s in chaine:
##        s1=Decode.encode(s)
##        s2=Decode.decode(s1)
##        print(s,s1,s2)
##    print(Decode.decode(Decode.encode("kff")))
    print(Decode.decodeChaine("Y29sbGVjdGlvbiBkJ0VsZXZlcw=="))
    print(Decode.encodeChaine("Collection d'Elèves"))
    print(Decode.d)
    print(Decode.decodeChaine("biFk"))
if __name__ == '__main__':
    main()
