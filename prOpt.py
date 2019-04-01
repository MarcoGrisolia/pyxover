#!/usr/bin/env python3
# ----------------------------------

##############################################
# @profile
# local or PGDA
local = 0
# debug mode
debug = 0
# parallel processing?
parallel = 0

# compute partials?
partials = 0
# std perturbations for finite differences
parOrb = {'dA':10.}#, 'dC':100., 'dR':20., 'dRl':20e-6, 'dPt':20e-6}
parGlo = {'dRA':[0.001, 0.000, 0.000]} #, 'dDEC':[0.001, 0.000, 0.000], 'dPM':[0.0, 0.00001, 0.0], 'dL':0.01,'dh2': 1.}

# orbital representation
OrbRep = 'cnt' #'lin'
# interpolation/spice direct call (0:no, 1:yes, use, 2: yes, create)
SpInterp = 1
# interpolation/spice direct call (0:no, 1:yes, use, 2: yes, create)
new_gtrack = 0
# interpolation/spice direct call (0:no, 1:yes, use, 2: yes, create)
new_xov = 0

# PyAltSim stuff
# simulation mode
sim = 1
# recompute a priori
new_illumNG = 0


# out and aux
if (local == 0):
    outdir = '/att/nobackup/sberton2/MLA/out/'
    auxdir = '/att/nobackup/sberton2/MLA/aux/'
else:
#    outdir = '/home/sberton2/Works/NASA/Mercury_tides/out/'
    outdir = '/home/sberton2/Works/NASA/Mercury_tides/out/'
    auxdir = '/home/sberton2/Works/NASA/Mercury_tides/aux/'
