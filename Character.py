from flask import Flask
import random



class Humain:
    
    def life(self, life: int):
        life 
    def your_name(self):
        """
        Demande à l'utilisateur son prénom et l'affiche.
        Si le prénom est 'null', affiche un message spécifique.
        """
        prenom = input("Quel est ton prénom : ").strip()
        
        if prenom.lower() == "null":
            print("Bah t'as pas de prénom, boloss !")
        elif prenom:
            print(f"Je m'appelle {prenom}")
        else:
            print("Tu n'as rien saisi.")
    


    def legume_pref(self):
        """
        Demande à l'utilisateur ses légumes préférés et les affiche.
        """
        legume = input("Quels sont tes légumes préférés ? ")
        print(f"Mes légumes préférés sont : {legume}")


    def Lol_Valo(self):
        valo_ou_lol = ["valo", "lol"]
        jeu = random.choice(valo_ou_lol)
        print(f"Je vais jouer à {jeu}")
        

if __name__ == "__main__":
    humain = Humain()
    humain.your_name()
    humain.legume_pref()
    humain.Lol_Valo()