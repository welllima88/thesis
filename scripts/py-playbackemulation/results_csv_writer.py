# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 09:18:44 2011

@author: fm
"""

import sys
import os
import os.path

import csv

import subprocess
import string

from numpy import *

import matplotlib.pyplot as plt

import pylab

import ytresults_commandline as yt

def calcstalls(stalls):
	stcnt = 0
	stlen = 0
	plcnt = 0
	pllen = 0

	num = None
	for i in range(len(stalls)):
		if(stalls[i].type == "Stall"):
			stcnt = stcnt + 1
			num = stcnt
			stlen = stlen + (stalls[i].end-stalls[i].start)
		else:
			plcnt = plcnt + 1
			num = plcnt
			pllen = pllen + (stalls[i].end-stalls[i].start)

			print(str(i) + ": " + stalls[i].type + "=" + str(i) + "; start=" + str(stalls[i].start) + "; end:" + str(stalls[i].end) + "; duration="+str(stalls[i].end-stalls[i].start))

			print("")
			print("num_stalls="+str(stcnt))
			print("time_stall_total="+str(stlen)) 
			print("num_playruns="+str(plcnt))
			print("time_play_total="+str(pllen)) 

			return(stcnt,stlen,plcnt,pllen)


if __name__ == "__main__":

	algs = ["ytfa","ffh5","nnbs","stbs"]

	rootdir = sys.argv[1]
	#subvideoid = sys.argv[2]

		
	# dirs = os.listdir(os.path.abspath(rootfolder))
	vals = []

	for current_dir, subfolders, files in os.walk(rootdir):
		if not subfolders: # only leaf dirs are interesting

			for alg in algs:
				for subvideoid in range(10):
					print "Calculating values for " + current_dir

					try:
						dirname = string.split(current_dir, "/")[-1]
						dirsplit = string.split(dirname,"_")
						videoid = dirsplit[0]
						qostype = dirsplit[1]
						qosparam = dirsplit[2]

					
						myG = yt.Graphs(current_dir, subvideoid)
						(bufferlevels, frame_timestamps, total_offset, stalls) = myG.stallingalgorithm(alg)
						video_width = myG.video_width
						video_height = myG.video_height
						video_bitrate = myG.overall_bitrate

						(num_stalls, time_stalls, num_playruns, time_play) = calcstalls(stalls)
						vals.append((videoid, alg, video_width, video_height, video_bitrate, qostype, float(qosparam), time_play, time_stalls, num_stalls))

					except Exception, e:
						print e



	vals = sorted(vals, key=lambda x: x[1]) # sort by first item in tuple: qosparam

	with open('playbackemulation.csv', 'wb') as f:
	    writer = csv.writer(f)
	    writer.writerow(["video_id", "strat", "video_width", "video_height", "video_bitrate", "qostype", "qosvalue", "duration", "stall_duration", "stall_count"])
	    writer.writerows(vals)





