from neocitizen import NeocitiesApi
import shutil
import os
import urllib.request
from pathlib import Path
import pickle


def get_highscore():
    try:
        with open("highscore.zombie", "rb") as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {"score": []}

def set_highscore(highscore, score):
    highscore["score"].append(int(score))
    highscore["score"] = sorted(highscore["score"], reverse=True)[:100]

    with open("highscore.zombie", "wb") as f:
        pickle.dump(highscore, f)

def u():
    data = get_highscore()
    a = NeocitiesApi(api_key=data['a'])
    shutil.copy("highscore.zombie", "highscore.txt")

    try:
        a.upload_files({Path("highscore.txt"): "highscore.txt"})
    finally:
        if os.path.exists("highscore.txt"):
            os.remove("highscore.txt")

def d():
    urllib.request.urlretrieve("https://bushbientotmodo.neocities.org/highscore.txt", "highscore.zombie")