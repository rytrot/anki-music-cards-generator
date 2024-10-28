from bs4 import BeautifulSoup
import bs4
import requests

count = 0
verbCards = open("verbCards.txt","w")
verbs = ["etre","avoir","aimer","saimer","jouer","saluer","etudier","briller","gagner","creer","naviguer","placer","manger","ceder","regner","leguer","rapiecer","proteger","lever","peler","appeler","interpeller","acheter","jeter","payer","essuyer","employer","envoyer","finir","hair","aller","courir","mourir","dormir","servir","sentir","vetir","fuir","tenir","acquerir","bouillir","couvrir","cueillir","defaillir","faillir","ouir","gesir","recevoir","voir","prevoir","pourvoir","savoir","devoir","pouvoir","valoir","prevaloir","vouloir","emouvoir","asseoir","pleuvoir","falloir","seoir","surseoir","choir","echoir","dechoir","faire","extraire","taire","plaire","croire","boire","conduire","rire","dire","interdire","maudire","lire","ecrire","suffire","confire","rendre","prendre","repandre","peindre","craindre","joindre","coudre","moudre","resoudre","rompre","battre","mettre","vaincre","connaitre","naitre","repaitre","croitre","accroitre","conclure","suivre","vivre","clore","monter","arriver","entrer","retourner","tomber","rester","sendormir","sasseoir","se-lever","se-reveiller","sen-aller","senfuir"]
for verb in verbs:
    htmlText = requests.get("https://conjugaison.bescherelle.com/verbes/"+verb).text
    soup = BeautifulSoup(htmlText, "lxml")
    infinitif = soup.find("span",class_="field").text
    print(infinitif)

    voices = soup.find_all("div",class_="container-verbe")
    for v in range(len(voices)):
        if len(voices) > 1:
            if v == 0:
                voix = "Voix active"
            elif v == 1:
                voix = "Voix passive"
        else:
            voix = "Voix ?"

        tempss = voices[v].find_all("div",class_="tab-pane")
        for t in range(len(tempss)):
            if len(voices) > 1:
                if t == 0:
                    temps = "Temps simples"
                elif t == 1:
                    temps = "Temps composés"
            else:
                temps = "Temps ?"

            cardsTypes = tempss[t].find_all("div",class_="card-type")
            for cardType in cardsTypes:
                title = cardType.find("h4").text
                title = title[0]+title[1:].lower()
                cardVerbes = cardType.find_all("div",class_="card-verbe")
                for cardVerbe in cardVerbes:
                    title1 = cardVerbe.find("h5").text
                    ps = cardVerbe.find_all("p")
                    imperatifCount = 0
                    numVerbes = 0
                    for p in ps:
                        if not p.text == "":
                            numVerbes += 1
                    for p in ps:
                        prenom = ""
                        prenomMasculin = ""
                        prenomFeminin = ""
                        prenomMasculinSingulier = ""
                        prenomFemininSingulier = ""
                        prenomMasculinPluriel = ""
                        prenomFemininPluriel = ""
                        prenomReflexive = ""
                        auxiliaire = ""
                        auxiliaire1 = ""
                        verbeRaw = ""
                        auxiliairesOu = [""]

                        if not p.find_all("auxiliary") == None:
                            auxiliaires = p.find_all("auxiliary")
                            if len(auxiliaires) > 0:
                                auxiliaire = auxiliaires[0].text.strip()+" "
                            if len(auxiliaires) > 1:
                                auxiliaire1 = auxiliaires[1].text.strip()+" "

                        if not p.find("reflexive-pronoun") == None:
                            prenomReflexive = p.find("reflexive-pronoun").text.strip()
                            if prenomReflexive=="nous" or prenomReflexive=="vous" or prenomReflexive=="me" or prenomReflexive=="te" or prenomReflexive=="se":
                                prenomReflexive += " "

                        if not p.find("verb")==None:
                            verbeRaw = p.find("verb").text.strip()
                            if title=="Impératif":
                                imperatifCount += 1
                            if " ou " in verbeRaw:
                                auxiliairesOu = verbeRaw.split(" ou ")
                                auxiliairesOu[0] = auxiliairesOu[0].strip()+" "
                                split = auxiliairesOu[1].split()
                                auxiliairesOu[1] = split[0].strip()+" "
                                verbeRaw = split[1].strip()
                            if " / " in verbeRaw:
                                verbes = verbeRaw.split(" / ")
                            else:
                                verbes = [verbeRaw]

                            for v in range(len(verbes)):
                                verbe = verbes[v]
                                infinitif = soup.find("span",class_="field").text
                                if len(verbes) == 2:
                                    if v == 0:
                                        infinitif += (" (type 1)")
                                    if v == 1:
                                        infinitif += (" (type 2)")
                                for a in range(len(auxiliairesOu)):
                                    if not p.find("personal-pronoun") == None:
                                        prenom = p.find("personal-pronoun").text.strip()
                                    #print("\n",voix,temps,title,title1,prenom,prenomReflexive,auxiliaire,verbe)
                                    if title=="Impératif":
                                        if numVerbes == 3:
                                            if imperatifCount == 1:
                                                prenom = "(tu)"
                                            if imperatifCount == 2:
                                                prenom = "(nous)"
                                            if imperatifCount == 3:
                                                prenom = "(vous)"
                                        elif numVerbes == 2:
                                            if imperatifCount == 1:
                                                prenom = "(nous)"
                                            if imperatifCount == 2:
                                                prenom = "(vous)"

                                    if len(auxiliairesOu) == 2:
                                        auxiliaire = auxiliairesOu[a]
                                        if a == 0:
                                            if "(e)(s)" in verbe:
                                                terminaison = "(e)(s)"
                                                verbe = verbe.replace("(e)(s)","")
                                            elif "(e)s" in verbe:
                                                terminaison = "(e)s"
                                                verbe = verbe.replace("(e)s","")
                                            elif "(e)" in verbe:
                                                terminaison = "(e)"
                                                verbe = verbe.replace("(e)","")
                                        elif a == 1:
                                            verbe += terminaison

                                    if "qu’il (elle)" in prenom:
                                        prenom = "qu'il/qu'elle/qu'on"
                                    elif "qu’ils (elles)" in prenom:
                                        prenom = "qu'ils/qu'elles"
                                    elif "il (elle)" in prenom:
                                        prenom = "il/elle/on"
                                    elif "ils (elles)" in prenom:
                                        prenom = "ils/elles"

                                    if "(e)s" in verbe:
                                        verbeMasculin = verbe.replace("(e)s","s")
                                        verbeFeminin = verbe.replace("(e)s","es")
                                        if "nous" in prenom or "vous" in prenom:
                                            prenomMasculin = "(m) "+prenom
                                            prenomFeminin = "(f) "+prenom
                                        elif "ils/elles" in prenom:
                                            prenomMasculin = "ils"
                                            prenomFeminin = "elles"
                                        elif "qu'ils/qu'elles" in prenom:
                                            prenomMasculin = "qu'ils"
                                            prenomFeminin = "qu'elles"
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                    elif "(es)" in verbe:
                                        verbeMasculin = verbe.replace("(es)","")
                                        verbeFeminin = verbe.replace("(es)","es")
                                        if "ils" in prenom or "elles" in prenom:
                                            prenomMasculin = "ils"
                                            prenomFeminin = "elles"
                                        elif "qu'ils" in prenom or "qu'elles" in prenom:
                                            prenomMasculin = "qu'ils"
                                            prenomFeminin = "qu'elles"
                                        else:
                                            prenomMasculin = "(m) "+prenom
                                            prenomFeminin = "(f) "+prenom
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                    elif "(e)" in verbe and not "(s)" in verbe:
                                        verbeMasculin = verbe.replace("(e)","")
                                        verbeFeminin = verbe.replace("(e)","e")
                                        if "il/elle/on" in prenom:
                                            prenomMasculin = "il"
                                            prenomFeminin = "elle"
                                            prenomOnMasculin = "(m) on"
                                            prenomOnFeminin = "(f) on"
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                        elif "qu'il/qu'elle/qu'on" in prenom:
                                            prenomMasculin = "qu'il"
                                            prenomFeminin = "qu'elle"
                                            prenomOnMasculin = "(m) qu'on"
                                            prenomOnFeminin = "(f) qu'on"
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                        else:
                                            prenomMasculin = "(m) "+prenom
                                            prenomFeminin = "(f) "+prenom
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                    elif "(e)(s)" in verbe:
                                        prenomMasculinSingulier = " (ms)"
                                        prenomFemininSingulier = " (fs)"
                                        prenomMasculinPluriel = " (mp)"
                                        prenomFemininPluriel = " (fp)"
                                        verbeMasculinSingulier = verbe.replace("(e)(s)","")
                                        verbeFemininSingulier = verbe.replace("(e)(s)","e")
                                        verbeMasculinPluriel = verbe.replace("(e)(s)","s")
                                        verbeFemininPluriel = verbe.replace("(e)(s)","es")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculinSingulier+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculinSingulier+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculinSingulier+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFemininSingulier+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFemininSingulier+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFemininSingulier+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculinPluriel+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculinPluriel+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculinPluriel+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFemininPluriel+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFemininPluriel+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFemininPluriel+";conjugaison::"+infinitif+"\n")
                                    elif "(s, se, s, ses)" in verbe:
                                        prenomMasculinSingulier = " (ms)"
                                        prenomFemininSingulier = " (fs)"
                                        prenomMasculinPluriel = " (mp)"
                                        prenomFemininPluriel = " (fp)"
                                        verbeMasculinSingulier = verbe.replace(" (s, se, s, ses)","")
                                        verbeFemininSingulier = verbe.replace(" (s, se, s, ses)","e")
                                        verbeMasculinPluriel = verbe.replace(" (s, se, s, ses)","")
                                        verbeFemininPluriel = verbe.replace(" (s, se, s, ses)","es")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculinSingulier+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculinSingulier+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculinSingulier+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFemininSingulier+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFemininSingulier+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFemininSingulier+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculinPluriel+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculinPluriel+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculinPluriel+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFemininPluriel+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFemininPluriel+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFemininPluriel+";conjugaison::"+infinitif+"\n")
                                    elif "(û, ue)" in verbe:
                                        verbeMasculin = verbe.replace(" (û, ue)","")
                                        verbeFeminin = verbe.replace("û (û, ue)","ue")
                                        if "il/elle/on" in prenom:
                                            prenomMasculin = "il"
                                            prenomFeminin = "elle"
                                            prenomOnMasculin = "(m) on"
                                            prenomOnFeminin = "(f) on"
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                        elif "qu'il/qu'elle/qu'on" in prenom:
                                            prenomMasculin = "qu'il"
                                            prenomFeminin = "qu'elle"
                                            prenomOnMasculin = "(m) on"
                                            prenomOnFeminin = "(f) on"
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                            verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomOnFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomOnFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                        else:
                                            prenomMasculin = "(m) "+prenom
                                            prenomFeminin = "(f) "+prenom
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculin+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFeminin+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFeminin+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFeminin+";conjugaison::"+infinitif+"\n")
                                    elif "(û, ue, us, ues)" in verbe:
                                        prenomMasculinSingulier = "(ms) "+prenom
                                        prenomFemininSingulier = "(fs) "+prenom
                                        prenomMasculinPluriel = "(mp) "+prenom
                                        prenomFemininPluriel = "(fp) "+prenom
                                        verbeMasculinSingulier = verbe.replace("û (û, ue, us, ues)","û")
                                        verbeFemininSingulier = verbe.replace("û (û, ue, us, ues)","us")
                                        verbeMasculinPluriel = verbe.replace("û (û, ue, us, ues)","ue")
                                        verbeFemininPluriel = verbe.replace("û (û, ue, us, ues)","ues")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculinSingulier+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculinSingulier+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculinSingulier+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFemininSingulier+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFemininSingulier+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFemininSingulier+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomMasculinPluriel+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomMasculinPluriel+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeMasculinPluriel+";conjugaison::"+infinitif+"\n")
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenomFemininPluriel+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenomFemininPluriel+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbeFemininPluriel+";conjugaison::"+infinitif+"\n")
                                    else:
                                        verbCards.write(voix+"|"+title+"|"+title1+"|"+prenom+"|"+infinitif+";"+voix+";"+temps +";"+title+";"+title1+";"+prenom+";"+infinitif+";"+prenomReflexive+auxiliaire+auxiliaire1+verbe+";conjugaison::"+infinitif+"\n")
        
            
