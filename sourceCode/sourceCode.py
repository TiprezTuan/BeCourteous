"from pynput import keyboard 
import csv
import sys
from pystray import Menu, MenuItem, Icon
from PIL import Image


#Création du dictionnaire contenant tout les mots bannies et leur remplaçants
with open('safeWords.csv', newline='') as csvfile:
    bannedWords = {}
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        couple_mot = ",".join(row)
        couple_mot = couple_mot.split(',')
        bannedWords[couple_mot[0]] = couple_mot[1]
    print(bannedWords)
count = 0
writer = keyboard.Controller()

def clear():
    with open("logs.txt", "w") as clear:
        clear.write("")

def switchWord(newWord, lastWord):
    print("lastWord :", lastWord)
    print("newWord :", newWord)
    for i in range(len(lastWord)+1):
        writer.press(keyboard.Key.backspace)
        writer.release(keyboard.Key.backspace)
    writer.type(newWord)
    with writer.pressed(keyboard.Key.ctrl_l):
        writer.press(keyboard.Key.right)
        writer.release(keyboard.Key.right)
    clear()


def checkWord(lastWord):
    #Vérification du mot, si il est dans la liste des mots bannes alors il est remplacé
    if str(lastWord) in bannedWords.keys() :
        print(bannedWords[lastWord])
        switchWord(bannedWords[lastWord], lastWord)

    #SafeWord pour stop le programme
    if lastWord == "closelogs":
        clear()
        sys.exit("SafeWord")

    else :
        clear()


def keyPressed(key):

    lastWord = []
    global count

    with open("logs.txt", 'a') as K_Log:
        try:
            char = key.char
            count += 1
            K_Log.write(char)

        except AttributeError:
            #Si on tape un espace alors il récupère le dernier mot entré
            if str(key) == "Key.ctrl_r" or str(key) == "Key.backspace" or str(key) == "Key.enter":
                clear()

            if str(key) == "Key.space":
                K_Log.write(" ")
                with open("logs.txt", 'r') as K_Log:
                    lastWord = K_Log.read()[-count:]
                    checkWord( lastWord )
                    count = 0
                    

if __name__ == "__main__" :
    tray_icon = Icon('name', Image.open('Icone_BeCourteous.ico'))
    tray_icon.menu = Menu(MenuItem('Quit', lambda: tray_icon.stop()))
    clear()
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()
    tray_icon.run()
