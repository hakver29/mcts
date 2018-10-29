"""
Generell input for spillet.

G: Antall spill som skal spilles
P: Spiller som starter
K: Maksimalt antall steiner det er mulig å velge hver runde
N: Antallet steiner man starter med
M: Antall simulasjoner
verbose: True
"""

import yaml
from definitions import ROOT_DIR

class GameSetting:
    def __init__(self):
        configfile = yaml.load(open(ROOT_DIR+"WhichSetting.yaml"))
        config = yaml.load(open(ROOT_DIR+configfile["filename"]))
        self.G = config["G"]
        self.P = config["P"]
        self.M = config["M"]
        self.N = config["N"]
        self.K = config["K"]
        self.verbose = config["verbose"]