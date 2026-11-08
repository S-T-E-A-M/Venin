import re
import tkinter as tk
import sys 

# ====================
# GESTION DE LA PILE
# ====================
class Pile():
    def __init__(self):
      self.contenue=[]
      self.sommet=None
    def estvide(self):
        return len(self.contenue)==0
    def empiler(self,element):
       self.contenue.append(element)
       self.sommet=element
    def depiler(self,element):
        if not self.estvide():
            self.contenue.pop()
            if not self.estvide():
                self.sommet=self.contenue[len(self.contenue)-1]
            else:
                self.sommet=None
        else:
           raise IndexError("error logique(erreur ines)")
     
# ====================
# ANALYSE LEXICALE
# ====================
def tokeniser(code):
    motif = r'[a-zA-Z_][a-zA-Z0-9_\-]*|\d+|[=+\-*/()]|"'
    tokens = re.findall(motif, code)
    return tokens

# ====================
# ANALYSE SYNTAXIQUE ET EXECUTION
# ====================
def croc(code):
    """Bon faudrait j arrete les blagues avec les serpents
    ce code gere basiquement la traduction de venin a pyton et laisse python faire le reste
    serpent est un langage tres tres haut niveau"""
    texte=code.strip().split("\n")
    codepython=[]
    error=False
    variables_type={}
    traquevariable={}
    valeur={}
    MotsValide=["affiche","creer","liste","traque","si","alors","sinon","tant","que","def","Boucle","ajoute"]
    i = 0
    for ligne in texte:
        codeligne=""
 
        guillemetspile=Pile()
        variabletraquer=False
        if error:
           break
        i+=1
        typedeligne=""
        tokens=tokeniser(ligne)
        for t  in range(len(tokens)):
            token=tokens[t]
            
            # Traitement des mots-clés valides
            if tokens[t] in MotsValide:
                
                if token=="affiche":
                    if t==0:
                        if typedeligne=="":
                            typedeligne="affichage"
                    else:
                        print(f"Erreur syntaxe:essaie d afficher au milieu d une ligne de code a la ligne {i}")
                        error=True
                        break
                 
                    codeligne += "print("
                elif token=="creer":
                    if t==0:
                         if not tokens[t+1]=="liste":
                            error=True
                            print(f"Erreur syntaxe: a oublier liste apres creer ligne{i}")
                            break
                         if typedeligne=="":
                            typedeligne="creation de liste"
                    else:
                        print(f"Erreur syntaxe:essaie de creer une liste au milieu d une autre ligne de code de code a la ligne {i}")
                        error=True
                        break
                   
                elif token=="ajoute":
                    typedeligne="ajout"
                    if len(tokens)!=1 and t==0:
                        if tokens[t+1] in variables_type.keys():
                            if variables_type[tokens[t+1]]=="liste":
                                if "(" not in tokens and ")" not in tokens:
                                    pass
                                else:
                                    print(f"erreur syntaxe:paranthese inutile ligne{i}")
                                    error=True
                                    break
                            else:
                                print(f"erreur syntaxe:essaie d ajouter a un {variables_type[tokens[t+1]]} et non une liste")
                                error=True
                                break
                        else:
                            print(f" erreur syntaxe: essaie de faire un ajout a une variable non assigné")
                            error=True
                            break
                    else:
                        print("erreur syntaxe: ajout placé au mauvais endroit")
                        error=True
                        break
            
            # Gestion de l'affectation
            elif token=="=" :
                if t!=0 and  typedeligne=="affectation":
                    codeligne += " " + token
                else:
                    error=True
                    print(f"Erreur syntaxe:= au mauvais endroit ligne {i}")
            
            # Gestion de l'addition
            elif token=="+":
                if (
t != 0 
    and t != len(tokens) - 1 
    and (tokens[t-1].isnumeric() or variables_type.get(tokens[t-1])=="chiffre") 
    and (tokens[t+1].isnumeric() or variables_type.get(tokens[t+1]) == "chiffre") 
    and (typedeligne != "affichage" or  not " \" " in codeligne
)):

                        codeligne += " " + token
                else:   
                    print(f"erreur syntaxe: addition mal faite a la ligne{i} ")
                    error=True
                    break 
            
            # Gestion des guillemets
            elif token=="\"":
                if typedeligne=="affichage":
                    if  guillemetspile.estvide():
                        guillemetspile.empiler(""" " """)
                    else:
                        guillemetspile.depiler(None)
                    codeligne += " " + token
                else:
                    print(f"erreur de syntaxe: \" dans une ligne de type {typedeligne} a la ligne {i}")
            
            # Traitement des variables et valeurs
            else:
                if t == 0:
                    if t + 1 < len(tokens) and tokens[t + 1] == "=" and typedeligne != "test":
                        typedeligne = "affectation"
                        variables_type[token] = "chiffre"
                        if token.isnumeric():
                            error = True
                            print(f" erreur syntaxe: variable commencant avec un chiffre ligne {i}")
                            break 
                        codeligne += token
               
                elif typedeligne == "creation de liste":
                    if not len(tokens) == 3:
                        print(f"erreur syntaxe:Nom de liste espace ligne {i}")
                        error = True
                        break
                    elif token.isnumeric():
                        print(f"erreur syntaxe: nom de variable commencant avec un chiffre ligne {i}")
                        error = True
                        break
                    codeligne += token + "=[]"
                    variables_type[token] = "liste" 
                
                elif typedeligne == "affichage":
                    codeligne += " " + token
                elif typedeligne == "ajout":
                    if token in variables_type or token.isnumeric():
                        if t == 1:
                            codeligne += f"{token}.extend(["
                        elif t == 2:
                            codeligne += token
                        else:
                            codeligne += "," + token

                elif typedeligne == "affectation" and token in variables_type:
                    codeligne += " " + token

                elif token.isnumeric():
                    if t != 0:
                        codeligne += " " + token 
                    else:
                        codeligne += token 
                
                elif token not in variables_type.keys():
                    print(f"Erreur Varibale(StanislasError): variable non defini a la ligne {i}")
                    error = True
                    break    

            if t==len(tokens)-1:
                if typedeligne=="affichage":
                    
                    codeligne += " ) "
                if not guillemetspile.estvide():
                    print(f"erreur syntaxe(AmineError): trop de guillemts a la ligne {i}")
                    error=True
                    break 
                if typedeligne=="ajout":
                    codeligne+="])"
                codepython.append(codeligne)
    if not error:
        versionpython="\n".join(codepython)
        exec(versionpython)
    else:
        return

# ====================
# POINT D'ENTREE
# ====================
if __name__ == "__main__":
    if len(sys.argv) > 1:
        croc(sys.argv[1])