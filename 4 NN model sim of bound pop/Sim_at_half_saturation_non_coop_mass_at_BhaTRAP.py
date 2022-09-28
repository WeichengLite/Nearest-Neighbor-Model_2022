#!/usr/bin/env python
# Python script reads table of populations and simulates mass spectra
# 2018-07-27

#import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
import datetime

parser = argparse.ArgumentParser(description='Read a table of populations and simulate mass spectra given the masses and charges of the species; saves simulated spectra to a file')
parser.add_argument('fname', help='file name with populations of states as columns', type=open)
parser.add_argument("-M", help="Molecular Weight of Macromol in Da", type=float, default=111448.56)
# apo Bha TRAP is 9287.38*12, RNA+TRAP is 108855.96 Da.
parser.add_argument("-LM", help="Molecular Weight of Ligand in Da", type=float, default=204.2)
parser.add_argument("-LW", help="specify linewidth of signals, in m/z", type=float, default=12)
parser.add_argument("-Points", help="number of points to simulate in spectrum", type=int, default=1500)
parser.add_argument("-Noise", help="optional noise to be added to spectrum", type=float, default=0)
args = parser.parse_args()
print (args)

H = 1.00794	# mass of a proton

data_file = args.fname
M = args.M
LM = args.LM
LW = args.LW
Points = args.Points
Noise = args.Noise

# Gaussian Shape: A*exp(-0.5*((x-B)/C)**2)

def gaussian(x, A, m, lw):
	# x is a vector (list) of m/z points
	return A*np.exp(-0.5*((x-m)/lw)**2)

def sim_spectrum(DataSet):
	"""
	DataSet : defined by a titration series, w/ mass, populations
	CS : the desired charge state to be simulated
	[not used]
	"""
#	for i in self.States:
#		self.Response += Populations[i]*exp(-0.5*((x-(M+i*LM)/CS)/LW)**2)
	Pops = DataSet.Pops
	LW = [1]*len(Pops)
#	Response(x) =  Pop[0]*np.exp(-0.5*((x-mz)/LW)**2)
	x = np.linspace(FirstP, LastP, Points)
	y = Response(x)

def response(x, Pops, M, LM, LW):
	y = [0.0]*x
	for i in range(len(Pops)):
		m = (M + i*LM)
		y = y + gaussian(x, Pops[i], m, LW)
	return y

def add_noise(signal, noise):
	"""Signal is a vector
	noise : random noise (normalized to 1) """
	# randn is random noise from a normal distribution w/ a sigma of 1
#	print signal
#	print noise*np.random.randn(len(signal))*10
	return signal+noise*np.random.randn(len(signal))

df = pd.read_table(data_file, comment = "#")	# read data
nconc, nstates = df.iloc[:,2:].shape	# determine dimensions
FirstP = 111000 ###(M-LM-LW)	# first point is before first signal
LastP = 114400 ###(M+(nstates+1)*LM)	# last point after last signal

x = np.linspace(FirstP, LastP, Points)	# define x values
ds = pd.DataFrame(x, columns = ['m'])	# create a dataframe for the spectra
LigC = df.iloc[:,1]	# used for names of spetra (columns in table)
Pops = df.iloc[:,2:]	# make a new dataframe w/ just populations
#y = [0.0]*Points	# empty vector
#y = response(x, Pops.iloc[8], M, LM, CS, LW)
#y = list()	# make y a list
y = [[] for col in range(nconc)]	# list of lists

#fig, axarr = plt.subplots(nconc, sharex=True)	# multi-plot
#fig.suptitle(data_file.name)

for c in range(nconc):
	y[c] = response(x, Pops.iloc[c], M, LM, LW)
	ds[LigC[c]] = y[c]
	if Noise > 0:
		y[c] = add_noise(y[c],Noise)
#	plt.plot(x,y[c])
#	ax.plot(x,y[c])
#	axarr[c].plot(x,y[c])
#	fig.subplots_adjust(hspace=0)
#	for ax in axarr:
#        	ax.yaxis.set_visible(False)
#        	ax.grid(linestyle='-')
#        	ax.set_xlim(4750,4925)
#        	ax.grid(axis='x')
#        	ax.set_xlabel('$State$')
#        	ax.set_xlabel('$m/z$')
#        	ax.label_outer()

#plt.plot(x,y)
#plt.plot(x,y[8])
#plt.show()

# using pandas to plot is so easy, if less flexible:
ds.plot(x = 'm', subplots=True, figsize=(6,1*nconc),legend=False, sharex=True, sharey=False)
#ds.plot(x = 'mz', subplots=True)
#ds.plot(x = 'mz', subplots=True,sharex=True, sharey=True)



plt.tight_layout()
plt.savefig('plot.pdf')
plt.show()

f = open('sim_spectra_halfs.txt', 'w')
f.write('# Simulated spectrum generated from populations in: '+ data_file.name+'\n')
f.write('# '+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")+'\n')
f.write('# '+ str(args)+ '\n')
f.write('# First column is m/z, others are intensities at different conditions\n')
f = open('sim_spectra_halfs.txt', 'a')
ds.to_csv(f, sep='\t', index=False)
f.close()
print ("Saved spectra to:", data_file.name)
#print ds.info()
