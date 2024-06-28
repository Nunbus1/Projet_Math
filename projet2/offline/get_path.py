#!/usr/bin/python3

from platform import system


def getPath(script_dir, file_dir):
    #Détection du système d'exploitation
    plat = system()
    #remplace tous les / par des \ dans les chemins script_dir et file_dir.
    if plat == "Windows":
        script_dir = script_dir.replace("/", "\\")
        file_dir = file_dir.replace("/", "\\")
    else:
        script_dir = script_dir.replace("\\", "/")
        file_dir = file_dir.replace("\\", "/")
    return script_dir, file_dir