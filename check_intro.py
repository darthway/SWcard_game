import os
import platform

current_folder = os.path.dirname(os.path.abspath(__file__))
#images_folder = current_folder+'/images/'
#sounds_folder = current_folder+'/sounds/'
images_folder = current_folder+'\images'+'\\'
sounds_folder = current_folder+'\sounds'+'\\'

ICON = "star_wars.ico"
INTRO_PHOTO = "entrada.gif"

def isUp(hostname):

    giveFeedback = False

    if platform.system() == "Windows":
        response = os.system("ping "+hostname+" -n 1")
    else:
        response = os.system("ping -c 1 " + hostname)

    isUpBool = False
    if response == 0:
        if giveFeedback:
            print hostname, 'is up!'
        isUpBool = True
    else:
        if giveFeedback:
            print hostname, 'is down!'
        isUpBool = False  

    return isUpBool