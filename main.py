import sys
import time
import os

# coding : utf-8

COLORS = {
    "black": "\u001b[30;1m",
    "red": "\u001b[31;1m",
    "green": "\u001b[32m",
    "lightgreen": "\u001b[38;5;82m",
    "lightyellow": "\u001b[38;5;226m",
    "yellow": "\u001b[33;1m",
    "blue": "\u001b[34;1m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "yellow-background": "\u001b[43m",
    "black-background": "\u001b[40m",
    "cyan-background": "\u001b[46;1m",
}

asciidraw = "\n[[lightyellow]] _ _ _     _      _____         _         _   \n| | | |___| |_   |  _  |___ ___| |_ _ ___| |_ \n| | | | -_| . |  |     |   | .'| | | |_ -|  _|\n|_____|___|___|  |__|__|_|_|__,|_|_  |___|_|  \n                                 |___|        \nAuthor : @Coroxx on github\n\n"


def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text


def lang():
    global lang
    global asciidraw
    os.system("clear")
    response = input(
        colorText("[[yellow]]Language :\n\n[1] FR\n[2] ANG \n\nChoice : "))
    if response == "1":
        lang = "fr"
        asciidraw += "[1] Analyser une page web\n\n[2] Quitter"
    elif response == "2":
        lang = "ang"
    else:
        print(colorText("[[red]]\n[!] Incorrect choice, try again"))
        time.sleep(2)
        lang()


lang()

try:
    import requests
    from bs4 import BeautifulSoup
    import urllib
    from urllib.request import urlopen
except:
    os.system("clear")
    if lang == "fr":
        print(
            colorText(
                "[[red]]Tu n'a pas correctement réalisé l'installation, laisse moi le faire pour toi.."
            )
        )
        time.sleep(2)
    elif lang == "ang":
        print(
            colorText(
                "[[red]]You didn't do the installation correctly, let me do it for you..."
            )
        )
        time.sleep(2)
    try:
        os.system("pip install -r requirements.txt")
        os.system("clear")
        print(colorText("[[green]]Succes !"))
        time.sleep(2)
    except:
        os.system("clear")
        time.sleep(1)
        print(
            colorText(
                "[[red]]Uh, an error has occurred, please report the problem on github."
            )
        )


def parameters_FR():
    pass


def parameters_US():
    pass


def parser(url):
    pass


def main_ANG():
    pass


def main_FR():
    global asciidraw
    os.system("clear")
    print(colorText(asciidraw))
    choice = input("\nChoix : ")
    try:
        choice = int(choice)
    except ValueError:
        print(colorText('[[red]]\n[!] Choix incorrect !\n'))
        time.sleep(2)
        os.system('clear')
        main_FR()
    if (choice == 1):
        parameters_FR()
    elif(choice == 2):
        print(colorText('[[red]]\n[!] Retour au terminal...'))
        sys.exit()
    else:
        print(colorText('[[red]]\n[!] Choix incorrect !\n'))
        time.sleep(2)
        main_FR()


main_FR()
