#!/usr/bin/env python
# By Jacek Zienkiewicz and Andrew Davison, Imperial College London, 2014
# Based on original C code by Adrien Angeli, 2009

from __future__ import print_function # use python 3 syntax but make it compatible with python 2

import random
import os
import sys
from sensors import Sensors
import brickpi333 as brickpi3
from collections import Counter
BP = brickpi3.BrickPi333()
S = Sensors(BP)

# Location signature class: stores a signature characterizing one location
class LocationSignature:
    def __init__(self, no_bins = 36):
        self.sig = [0] * no_bins
        
    def print_signature(self):
        for i in range(len(self.sig)):
            print(self.sig[i])

# --------------------- File management class ---------------
class SignatureContainer():
    def __init__(self, size = 5):
        self.size      = size; # max number of signatures that can be stored
        self.filenames = [];
        
        # Fills the filenames variable with names like loc_%%.dat 
        # where %% are 2 digits (00, 01, 02...) indicating the location number. 
        for i in range(self.size):
            self.filenames.append('loc_{0:02d}.dat'.format(i))

    # Get the index of a filename for the new signature. If all filenames are 
    # used, it returns -1;
    def get_free_index(self):
        n = 0
        while n < self.size:
            if (os.path.isfile(self.filenames[n]) == False):
                break
            n += 1
            
        if (n >= self.size):
            return -1;
        else:    
            return n;
 
    # Delete all loc_%%.dat files
    def delete_loc_files(self):
        print("STATUS:  All signature files removed.")
        for n in range(self.size):
            if os.path.isfile(self.filenames[n]):
                os.remove(self.filenames[n])
            
    # Writes the signature to the file identified by index (e.g, if index is 1
    # it will be file loc_01.dat). If file already exists, it will be replaced.
    def save(self, signature, index):
        filename = self.filenames[index]
        if os.path.isfile(filename):
            os.remove(filename)
            
        f = open(filename, 'w')

        for i in range(len(signature.sig)):
            s = str(signature.sig[i]) + "\n"
            f.write(s)
        f.close();

    # Read signature file identified by index. If the file doesn't exist
    # it returns an empty signature.
    def read(self, index):
        ls = LocationSignature()
        filename = self.filenames[index]
        if os.path.isfile(filename):
            f = open(filename, 'r')
            for i in range(len(ls.sig)):
                s = f.readline()
                if (s != ''):
                    ls.sig[i] = int(s)
            f.close();
        else:
            print("WARNING: Signature does not exist.")
        
        return ls
        
# FILL IN: spin robot or sonar to capture a signature and store it in ls
def characterize_location(ls):
    rots = 360 / len(ls.sig)
    nextAngle = rots
    for i in range(len(ls.sig)):
        print("Sonar sensor at %d, characterising location" %(nextAngle - rots))
        ls.sig[i] = S.getSensorReading()
        S.rotateSonarSensor(nextAngle)
        nextAngle += rots
    S.resetSonarSensorPos()
    
# Compare two given signatures
def compare_signatures(ls1, ls2):
    dist = 0
    dCount1 = Counter(ls1.sig)
    dCount2 = Counter(ls2.sig)

    for i in dCount1.elements():
        dist += (dCount1[i] - dCount2[i])**2
    return dist

def findShift(ls1, ls2):
    optShift = -1
    bestDist = sys.maxsize
    sigSize = len(ls1.sig)
    for i in range(sigSize):
        dist = 0
        for j in range(sigSize):
            dist += (ls1.sig[j] - ls2.sig[(j+i)%len(ls1.sig)])**2
        if dist < bestDist :
            bestDist = dist
            optShift = i
    return optShift * 360 / sigSize       

# This function characterizes the current location, and stores the obtained 
# signature into the next available file.
def learn_location(signatures):
    ls = LocationSignature()
    characterize_location(ls)
    idx = signatures.get_free_index();
    if (idx == -1): # run out of signature files
        print("\nWARNING:")
        print("No signature file is available. NOTHING NEW will be learned and stored.")
        print("Please remove some loc_%%.dat files.\n")
        return
    
    signatures.save(ls,idx)
    print("STATUS:  Location " + str(idx) + " learned and saved.")

# This function tries to recognize the current location.
# 1.   Characterize current location
# 2.   For every learned locations
# 2.1. Read signature of learned location from file
# 2.2. Compare signature to signature coming from actual characterization
# 3.   Retain the learned location whose minimum distance with
#      actual characterization is the smallest.
# 4.   Display the index of the recognized location on the screen
def recognize_location(signatures):
    ls_obs = LocationSignature();
    characterize_location(ls_obs);

    # FILL IN: COMPARE ls_read with ls_obs and find the best match
    best_ls = None
    opt_idx = -1
    optDist = sys.maxsize
    threshold = 9000
    for idx in range(signatures.size):
        print("STATUS:  Comparing signature " + str(idx) + " with the observed signature.")
        ls_read = signatures.read(idx);
        dist    = compare_signatures(ls_obs, ls_read)
        if dist < threshold and dist < optDist:
            best_ls = ls_read
            opt_idx = idx
            optDist = dist
            
    if best_ls == None:
        print("No matching signatures found. Unknown location.")
    else:
        lsShift = findShift(ls_obs, best_ls)
        print("The location is detected to be %d, the robot is rotated %d degrees" %(opt_idx, lsShift))

# Prior to starting learning the locations, it should delete files from previous
# learning either manually or by calling signatures.delete_loc_files(). 
# Then, either learn a location, until all the locations are learned, or try to
# recognize one of them, if locations have already been learned.

signatures = SignatureContainer(5);
"""
signatures.delete_loc_files()
for i in range(signatures.size):
    learn_location(signatures);
    input("Press enter to take signature of the next location:")
"""
recognize_location(signatures);


