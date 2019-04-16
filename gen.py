#!/usr/bin/python3

#@author: Jon Sawin
# diff test
import sys
import os
import time
import argparse
import subprocess
import random
import math
import json
import logging, logging.handlers

random.seed()
# curiosity
randobj = random.getstate()
classes_json = {}
with open("classes.json", 'r') as fh:
    classes_json = json.load(fh)

# logging init
log = logging.getLogger(__name__)
log.setLevel("DEBUG")
filehandler = logging.handlers.WatchedFileHandler('gen.log')
formatter = logging.Formatter("%(asctime)s - 5e generator - %(levelname)s - %(message)s")
filehandler.setFormatter(formatter)
log.addHandler(filehandler)
stdouthandler = logging.StreamHandler(sys.stdout)
stdouthandler.setLevel("INFO")
log.addHandler(stdouthandler)

def roll(die):
    try:
        val = random.randint(1, die)
    except Exception as ex:
        log.error("cannot generate random value btwn 1 and %s - %s" %die, ex)
        sys.exit(1)
    return val

def dieStrToInt(dN):
    try:
        retval = dN[1:]
        return int(retval)
    except Exception as ex:
        log.error("failed to convert str %s to int (trim leading d) - %s" %(dN, ex))

# def selectFromDict()
# might be useful

def rollStats(output=True):
    stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    finals = []
    for stat in stats:
        scores = []
        for i in range(4):
            scores.append(roll(6))
        log.debug("rolled %s" %scores)
        scores.remove(min(scores))
        final = sum(scores)
        finals.append(final)
        if output: 
            log.info("%s: %d" %(stat, final))
        else:
            log.debug("%s: %d" %(stat, final))
    avg = sum(finals) / 6
    if output:
        log.info("average = %s" %avg)
    else:
        log.debug("average = %s" %avg)
    finals_dict = {}
    for i in range(6):
        finals_dict[stats.pop()] = finals.pop()
    return finals_dict, avg

def multiRoll(count):
    avgs = []
    mymax = []
    mymin = []
    maxavg = 0
    minavg = 18
    for i in range(count):
        stats, r = rollStats(output=False)
        avgs.append(r)
        if r >= maxavg:
            mymax = stats
            maxavg = r
        if r <= minavg:
            mymin = stats
            minavg = r
    finalavg = sum(avgs) / len(avgs)
    log.info("final avg = %s" %finalavg)
    log.info("best scores = %s" %mymax)
    log.info("worst scores = %s" %mymin)

def pickClass(output=True):
    class_list = classes_json["classes"]
    # support artifacer/homebrew
    size = len(class_list)
    index = roll(size) - 1
    class_json = class_list[index]
    if output: log.info("class json - %s" %class_json)
    return class_json

class character(object):
    
    def __init__(self, scores=None, myclass=None, level=1, name="Grigif"):
        self.json = {}
        self.level = level
        self.scores = scores
        self.name = name
        self.classjson = myclass
        self.xp = 0
        self.modifiers = {}
        if self.scores:
            for key in self.scores:
                    self.modifiers[key] = math.floor((self.scores[key] - 10) / 2 )
        if self.classjson:
            self.classname = myclass["name"]
            if self.modifiers:
                self.basehp = dieStrToInt(myclass["hit_dice"]) + self.modifiers["CON"]
            else:
                self.basehp = "unk"
            if self.level == 1:
                self.hp = self.basehp
            else:
                self.hp ="unk"
        else:
            self.classname = "Not set"
            self.basehp = "unk"
            self.hp = "unk"
        self.genJson()

    def printInfo(self):
        log.info("==================================================================")
        log.info("Character - %s" %self.name)
        log.info("class - %s" %self.classname)
        log.info("hit points = %s" %self.basehp)
        log.info('xp = %d' %self.xp)
        if self.scores:
            for key in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
                log.info("%s: %d" %(key, self.scores[key]))
        log.info("==================================================================")

    def genJson(self):
        with open("character.json", 'r') as fh:
            self.json = json.load(fh)["character"]
        self.json["name"] = self.name
        self.json["level"] = self.level
        self.json["scores"] = self.scores
        self.json["modifiers"] = self.modifiers
        self.json["xp"] = self.xp
        self.json["basehp"] = self.basehp
        self.json["hp"] = self.hp
        self.json["classname"] = self.classname
        self.json["classjson"] = self.classjson

    def printJson(self):
        log.info("character json = %s" %self.json)

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--roll', '-r', action="store_true", dest="roll", help="roll new char stats", default=False)
    parser.add_argument('--class', '-c', action="store_true", dest="aclass", help="select character class", default=False)
    parser.add_argument('--newchar', '-n', action="store_true", dest="new", help="generate a new character", default=False)
    parser.add_argument('--name', action="store", dest="char_name", help="name", type=str, default="Grigif")
    parser.add_argument('--multiroll', '-m', action="store", dest="multiroll", help="number of times to gen stats", type=int)

    opts = parser.parse_args()

    if opts.new:
        # unit test ish thing
        lightchar = character(name="lightweight")
        # lightchar.printInfo()
        # lightchar.printJson()
        newstats, avg = rollStats(output=False)
        newclass = pickClass(output=False)
        newchar = character(newstats, newclass, 1, name=opts.char_name)
        newchar.printInfo()
        newchar.printJson()
        sys.exit(0)

    # for stats generating purposes/curiosity 
    if opts.roll and opts.multiroll:
        multiRoll(opts.multiroll)

    elif opts.roll:
        rollStats()

    if opts.aclass:
        pickClass()


    log.info("finished known operations")

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])


