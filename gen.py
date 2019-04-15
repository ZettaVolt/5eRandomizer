#!/usr/bin/python3

#@author: Jon Sawin
import sys
import os
import time
import argparse
import subprocess
import random
import math
import json

random.seed()
# curiosity
randobj = random.getstate()
classes_json = {}
with open("classes.json", 'r') as fh:
    classes_json = json.load(fh)

def roll(die):
    try:
        val = random.randint(1, die)
    except Exception as ex:
        print("cannot generate random value btwn 1 and %s - %s" %die, ex)
        sys.exit(1)
    return val

def dieStrToInt(dN):
    try:
        retval = dN[1:]
        return int(retval)
    except Exception as ex:
        print("failed to convert str %s to int (trim leading d) - %s" %(dN, ex))

# def selectFromDict()
# might be useful

def rollStats(output=True):
    stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    finals = []
    for stat in stats:
        scores = []
        for i in range(4):
            scores.append(roll(6))
        # if output: print("rolled %s" %scores)
        scores.remove(min(scores))
        final = sum(scores)
        finals.append(final)
        if output: print("%s: %d" %(stat, final))
    avg = sum(finals) / 6
    if output: print("average = %s" %avg)
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
    print("final avg = %s" %finalavg)
    print("best scores = %s" %mymax)
    print("worst scores = %s" %mymin)

def pickClass(output=True):
    class_list = classes_json["classes"]
    # support artifacer/homebrew
    size = len(class_list)
    index = roll(size) - 1
    class_json = class_list[index]
    if output: print("class json - %s" %class_json)
    return class_json

class character(object):
    
    def __init__(self, scores=None, myclass=None, level=1):
        self.level = level
        self.scores = scores
        self.name = "Grigif"
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

    def printInfo(self):
        print("Character - %s" %self.name)
        print("class - %s" %self.classname)
        print("hit points = %s" %self.basehp)
        print('xp = %d' %self.xp)
        if self.scores:
            for key in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]:
                print("%s: %d" %(key, self.scores[key]))


def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--roll', '-r', action="store_true", dest="roll", help="roll new char stats", default=False)
    parser.add_argument('--class', '-c', action="store_true", dest="aclass", help="select character class", default=False)
    parser.add_argument('--newchar', '-n', action="store_true", dest="new", help="generate a new character", default=False)
    parser.add_argument('--multiroll', '-m', action="store", dest="multiroll", help="number of times to gen stats", type=int)

    opts = parser.parse_args()

    if opts.new:
        lightchar = character()
        lightchar.printInfo()
        newstats, avg = rollStats(output=False)
        newclass = pickClass(output=False)
        newchar = character(newstats, newclass, 1)
        newchar.printInfo()
        sys.exit(0)

    # for stats generating purposes/curiosity 
    if opts.roll and opts.multiroll:
        multiRoll(opts.multiroll)

    elif opts.roll:
        rollStats()

    if opts.aclass:
        pickClass()


    print("finished known operations")

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])


