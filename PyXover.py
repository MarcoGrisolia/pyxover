#!/usr/bin/env python3
# ----------------------------------
# PyXover
# ----------------------------------
# Author: Stefano Bertone
# Created: 16-Oct-2018
#
import warnings

from Amat import Amat
from xov_prc_iters import xov_prc_iters_run

warnings.filterwarnings("ignore", category=RuntimeWarning)
import os
import glob

import numpy as np
import pandas as pd
import itertools as itert
# from itertools import izip, count
import multiprocessing as mp
# from geopy.distance import vincenty

import spiceypy as spice

# from collections import defaultdict
# import mpl_toolkits.basemap as basemap

import time

# mylib
from prOpt import new_xov, vecopts, outdir, debug, monthly_sets, new_algo
# from mapcount import mapcount
from ground_track import gtrack
from xov_setup import xov


# from util import lflatten
########################################
# # test space
#
# tst = [np.array([ 89.72151033, 103.94256763]), np.array([139.94256763])]
# tst = lflatten(tst)
# print(tst)
# exit()
# vecopts = {'SCID':'-236'}
#
# tmp_ser = Amat(vecopts)
# for f in glob.glob('/home/sberton2/Works/NASA/Mercury_tides/out/xov_130101*_13.pkl'):
#     tmp_ser = tmp_ser.load(f)
#
#     print(tmp_ser.xovers)
#
# # tmp_par = Amat(vecopts)
# # tmp_par = tmp_par.load('out/small_par/Amat_small_dataset.pkl')
#
# # print(tmp_par.spA.to_dense().equals(tmp_ser.spA.to_dense()))
#
# # print(tmp_par.spA)
# # print(tmp_ser.spA)
#
# exit()

def launch_xov(
        args):  # pool.map functions have to stay on top level (not inside other functions) to avoid the "cannot be pickled" error
    track_id = args[0]
    # print(track_id)
    comb = args[1]
    misycmb = args[2]
    par = args[3]
    outdir = args[4]

    if new_xov:  # and track_id=='1301232350':
        # print( "check", track_id, misycmb[par])
        if not os.path.isfile(outdir + 'xov/xov_' + track_id + '_' + misycmb[par][1] + '.pkl') or new_xov == 2:

            # print("Processing " + track_id + " ...")

            # try:
            #    trackA = track_id
            #    trackA = tracklist[str(track_id)]
            trackA = gtrack(vecopts)

            if monthly_sets:
                trackA = trackA.load(outdir + 'gtrack_' + misycmb[par][0][:2] + '/gtrack_' + track_id + '.pkl')
            else:
                trackA = trackA.load(outdir + 'gtrack_' + misycmb[par][0] + '/gtrack_' + track_id + '.pkl')


            if not trackA == None and len(trackA.ladata_df) > 0:

                xov_tmp = track_id
                xov_tmp = xov(vecopts)

                # print(comb)

                # loop over all combinations containing track_id
                for gtrackA, gtrackB in [s for s in comb if track_id in s[0]]:

                    # if debug:
                    #    print("Processing " + gtrackA + " vs " + gtrackB)

                    if gtrackB > gtrackA:
                        # try:
                        #        trackB = track_id
                        #        trackB = tracklist[str(gtrackB)]
                        trackB = gtrack(vecopts)

                        if monthly_sets:
                           trackB = trackB.load(outdir + 'gtrack_' + misycmb[par][1][:2] + '/gtrack_' + gtrackB + '.pkl')
                        else:
                           trackB = trackB.load(outdir + 'gtrack_' + misycmb[par][1] + '/gtrack_' + gtrackB + '.pkl')

                        if not trackB == None and len(trackB.ladata_df) > 0:

                            # # TODO remove when recomputing
                            # trackA.ladata_df[['X_NPstgprj', 'Y_NPstgprj']] = trackA.ladata_df[['X_stgprj', 'Y_stgprj']]
                            # trackB.ladata_df[['X_NPstgprj', 'Y_NPstgprj']] = trackB.ladata_df[['X_stgprj', 'Y_stgprj']]
                            # trackA.ladata_df[] = trackA.ladata_df.rename(index=str, columns={"X_stgprj": "X_NPstgprj", "Y_stgprj": "Y_NPstgprj"})
                            # trackB.ladata_df = trackB.ladata_df.rename(index=str, columns={"X_stgprj": "X_NPstgprj", "Y_stgprj": "Y_NPstgprj"})

                            # looping over all track combinations and updating the general df xov_tmp.xovers
                            xov_tmp.setup([trackA,trackB])

                    # except:
                    #     print(
                    #         'failed to load trackB ' + outdir + 'gtrack_' + gtrackB + '.pkl' + ' to process ' + outdir + 'gtrack_' + track_id + '.pkl')

                # exit()

                # for each gtrackA, write
                # print([s for s in comb if track_id in s[0]])
                if [s for s in comb if track_id in s[0]] and len(xov_tmp.xovers) > 0:
                    # get xover LAT and LON
                    xov_tmp.get_xov_latlon(trackA)

                    if new_algo:
                        # Save to temporary folder
                        if not os.path.exists(outdir + 'xov/tmp/'):
                            os.mkdir(outdir + 'xov/tmp/')
                        xov_tmp.save(outdir + 'xov/tmp/xov_' + gtrackA + '_' + misycmb[par][1] + '.pkl')
                        # just pass rough_xovs to next step
                        return xov_tmp.xovers
                    else:
                        # Save to file
                        if not os.path.exists(outdir + 'xov/'):
                            os.mkdir(outdir + 'xov/')
                        xov_tmp.save(outdir + 'xov/xov_' + gtrackA + '_' + misycmb[par][1] + '.pkl')
                        print(
                            'Xov for ' + track_id + ' processed and written to ' + outdir + 'xov/xov_' + gtrackA + '_' +
                            misycmb[par][1] + '.pkl @' + time.strftime("%H:%M:%S", time.gmtime()))
                        return gtrackA

        # except:
        #     print(
        #         'failed to load trackA ' + outdir + 'gtrack_' + track_id + '.pkl' + ' to process xov from ' + outdir + 'gtrack_' + track_id + '.pkl')

        else:

            #      track = track.load('out/xov_'+gtrackA+'.pkl')
            print('Xov for ' + track_id + ' already exists in ' + outdir + 'xov_' + track_id + '_' +
                          misycmb[par][1] + '.pkl @' + time.strftime("%H:%M:%S", time.gmtime()))

    ########################################
#@profile
def main(args):
    from prOpt import parallel, outdir, auxdir, local, vecopts

    print(args)

    # read input args
    print('Number of arguments:', len(args), 'arguments.')
    print('Argument List:', str(args))

    cmb_y_in = args[0]
    indir_in = args[1]
    outdir_in = args[2]
    iter_in = args[-1]

    # locate data
    if local == 0:
        data_pth = '/att/nobackup/sberton2/MLA/data/'  # /home/sberton2/Works/NASA/Mercury_tides/data/'
        dataset = indir_in  # 'test/' #'small_test/' #'1301/' #
        data_pth += dataset

        # load kernels
        spice.furnsh('/att/nobackup/emazaric/MESSENGER/data/furnsh/furnsh.MESSENGER.def')  # 'aux/mymeta')
    else:
        data_pth = '/home/sberton2/Works/NASA/Mercury_tides/data/'
        # data_pth = '/home/sberton2/Works/NASA/Mercury_tides/data/'  # /home/sberton2/Works/NASA/Mercury_tides/data/'
        dataset = indir_in  # 'SIM_1301/mlatimes/0res_35amp_tst/' #'1301' #SIM_1301/sphere/' #35-1024-1-8-5/'  #35-1024-32-4-5/' #  'small_dataset/' #''# "test1/"  #''  #
        data_pth += dataset
        # outdir += outdir_in #'sim_mlatimes/0res_35amp/'

        # load kernels
        spice.furnsh(auxdir + 'mymeta')  # 'aux/mymeta')

    # set ncores
    ncores = mp.cpu_count() - 1  # 8

    if parallel:
        print('Process launched on ' + str(ncores) + ' CPUs')

    ##############################################

    # Setup some useful options
    # vecopts = {'SCID': '-236',
    #            'SCNAME': 'MESSENGER',
    #            'SCFRAME': -236000,
    #            'INSTID': (-236500, -236501),
    #            'INSTNAME': ('MSGR_MLA', 'MSGR_MLA_RECEIVER'),
    #            'PLANETID': '199',
    #            'PLANETNAME': 'MERCURY',
    #            'PLANETRADIUS': 2440.,
    #            'PLANETFRAME': 'IAU_MERCURY',
    #            'OUTPUTTYPE': 1,
    #            'ALTIM_BORESIGHT': '',
    #            'INERTIALFRAME': 'J2000',
    #            'INERTIALCENTER': 'SSB',
    #            'PARTDER': ''}

    # out = spice.getfov(vecopts['INSTID'][0], 1)
    # updated w.r.t. SPICE from Mike's scicdr2mat.m
    vecopts['ALTIM_BORESIGHT'] = [0.0022105, 0.0029215, 0.9999932892]  # out[2]
    ###########################

    # print(vecopts['ALTIM_BORESIGHT'])

    # apply pointing corrections
    # vecin = {'ZPT':vecopts['ALTIM_BORESIGHT']}

    # setup all combinations between years
    par = int(cmb_y_in)

    if monthly_sets:
      misy = ['11', '12', '13', '14', '15']
      months = np.arange(1,13,1)
      misy = [x+f'{y:02}' for x in misy for y in months]
      misy = ['0801','0810']+misy[2:-8]
    else:
      misy = ['08','11', '12', '13', '14', '15']

    misycmb = [x for x in itert.combinations_with_replacement(misy, 2)]
    # print(misycmb)
    if debug:
        print("Choose grid element among:",dict(map(reversed, enumerate(misycmb))))
    print(par, misycmb[par]," has been selected!")

    # exit()

    if args[-1] == 0:

        # -------------------------------
        # File reading and ground-tracks computation
        # -------------------------------

        startInit = time.time()

        # read all MLA datafiles (*.TAB in data_pth) corresponding to the given years
        # for orbitA and orbitB.
        # Geoloc, if active, will process all files in A+B. Xov will only process combinations
        # of orbits from A and B
        # allFilesA = glob.glob(os.path.join(data_pth, 'MLAS??RDR' + misycmb[par][0] + '*.TAB'))
        # allFilesB = glob.glob(os.path.join(data_pth, 'MLAS??RDR' + misycmb[par][1] + '*.TAB'))

        # print(os.path.join(outdir, indir_in + misycmb[par][0][:2] + '/gtrack_'+misycmb[par][0]+'*'))
        # print(glob.glob(os.path.join(outdir, indir_in + misycmb[par][0][:2] + '/gtrack_'+misycmb[par][0]+'*')))

        if monthly_sets:
          allFilesA = glob.glob(os.path.join(outdir, indir_in + misycmb[par][0][:2] + '/gtrack_'+misycmb[par][0]+'*'))
          allFilesB = glob.glob(os.path.join(outdir, indir_in + misycmb[par][1][:2] + '/gtrack_'+misycmb[par][1]+'*'))
        else:
          allFilesA = glob.glob(os.path.join(outdir, indir_in + misycmb[par][0] + '/*'))
          allFilesB = glob.glob(os.path.join(outdir, indir_in + misycmb[par][1] + '/*'))


        if misycmb[par][0] == misycmb[par][1]:
            allFiles = allFilesA
        else:
            allFiles = allFilesA + allFilesB

        # print(allFiles)

        endInit = time.time()
        print(
            '----- Runtime Init= ' + str(endInit - startInit) + ' sec -----' + str(
                (endInit - startInit) / 60.) + ' min -----')

        # -------------------------------
        # Xovers setup
        # -------------------------------

        startXov2 = time.time()

        xovnames = ['xov_' + fil.split('.')[0][-10:] for fil in allFiles]
        # trackxov_list = []

        # Compute all combinations among available orbits, where first orbit is in allFilesA and second orbit in allFilesB (exclude same tracks cmb)
        # comb=np.array(list(itert.combinations([fil.split('.')[0][-10:] for fil in allFiles], 2))) # this computes comb btw ALL files
        comb = list(
            itert.product([fil.split('.')[0][-10:] for fil in allFilesA], [fil.split('.')[0][-10:] for fil in allFilesB]))
        comb = np.array([c for c in comb if c[0] != c[1]])

        # if iter>0, don't test all combinations, only those resulting in xovers at previous iter
        # TODO, check wether one could safely save time by only considering xovers with a given weight
        iter = int(outdir_in.split('/')[1].split('_')[-1])
        if iter>0:
            comb = select_useful_comb(comb, iter, outdir_in)

        # print(comb)

        # load all tracks
        # tmp = [gtrack(vecopts) for i in range(len(allFiles))]

        # if False:
        #     tracklist = {}
        #     for idx, fil in enumerate(allFiles):
        #         try:
        #             print(outdir)
        #             _ = tmp[idx].load(outdir + '/gtrack_' + fil.split('.')[0][-10:] + '.pkl')
        #             tracklist[str(_.name)] = _
        #         except:
        #             print('Failed to load' + outdir + '/gtrack_' + fil.split('.')[0][-10:] + '.pkl')

        args = ((fil.split('.')[0][-10:], comb, misycmb, par, outdir + outdir_in) for fil in allFilesA)

        # loop over all gtracks
        # parallel = 1
        if parallel:
            # filnams_loop = [fil.split('.')[0][-10:] for fil in allFiles]
            # print(filnams_loop)
            # print((mp.cpu_count() - 1))
            pool = mp.Pool(processes=ncores)  # mp.cpu_count())
            # store list of tracks with xovs
            result = pool.map(launch_xov, args)  # parallel
            pool.close()
            pool.join()

        else:
            result = [launch_xov(arg) for arg in args]  # seq
            print(result)

        if len(result)>0:
            if new_algo:
                rough_xov = pd.concat(result).reset_index()
            else:
                acttracks = np.unique(np.array([x for x in result if x is not None]).flatten())
        else:
            print("### PyXover: no xovers between these tracks")
            exit()

        endXov2 = time.time()
        print(
            '----- Runtime Xov2 = ' + str(endXov2 - startXov2) + ' sec -----' + str(
                (endXov2 - startXov2) / 60.) + ' min -----')

    else: # xovs will be taken from old iter
        rough_xov = pd.DataFrame()

    if new_algo:
        print("Calling another awesome routine")
        xov_prc_iters_run(outdir_in, iter_in, misycmb[par],rough_xov)
        exit()


def select_useful_comb(comb, iter, outdir_in):
    outdir_old = outdir_in.replace('_' + str(iter) + '/', '_' + str(iter - 1) + '/')
    print(outdir_old, outdir_in)
    tmp = Amat(vecopts)
    tmp = tmp.load(glob.glob(outdir + outdir_old + 'Abmat*.pkl')[0])

    old_xov_orb = (tmp.xov.xovers['orbA'].map(str) + tmp.xov.xovers['orbB']).values

    if len(comb)>0:
        comb_new = np.sum(comb.astype(object),axis=1)
        common_index = np.intersect1d(comb_new,old_xov_orb,return_indices=True)[1]
        comb_new = comb[common_index]
    else:
        comb_new = np.array([])

    # slow
    # old_xov_orb = tmp.xov.xovers[['orbA', 'orbB']].values
    # intersetingRows = [(old_xov_orb == irow).all(axis=1).any() for irow in comb]
    # comb = comb[intersetingRows]

    print("Based on previous xovs:", len(comb_new), "tracks combs selected out of", len(comb))

    return comb_new


##############################################
# locate data
if __name__ == '__main__':
    import sys

    ##############################################
    # launch program and clock
    # -----------------------------
    start = time.time()

    args = sys.argv[1:]
    print(args)
    main(args)

    # stop clock and print runtime
    # -----------------------------
    end = time.time()
    print('----- Runtime = ' + str(end - start) + ' sec -----' + str((end - start) / 60.) + ' min -----')
