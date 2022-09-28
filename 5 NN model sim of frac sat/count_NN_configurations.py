#!/usr/bin/env python

#
# This script provides the number of sites that are empty, or have 0, 1, or 2 neighbors in a circular lattice.
#

from itcsimlib import ITCSim
from itcsimlib.thermo import *
from itcsimlib.model_ising import NonAdditive

class NonAdditiveRecorder(NonAdditive):
	def __init__(self,log=None,nsites=3,circular=1,**kwargs):
		NonAdditive.__init__(self,nsites,circular,**kwargs)

		self.log = log
		self.log_counter = 1
		self.neighbors = None

	def get_neighbors(self):
		neighbors = [ [0,0,0,0] for i in range(self.nconfigs) ]

		for i in range(self.nconfigs):
			for j in range(self.nsites):

				if self.get_site_occupancy(i,j): # is site occupied?
					if self.get_site_occupancy(i,j+1): # is the next neighboring site occupied?
						if self.get_site_occupancy(i,j-1): # is previous neighboring site occupied?
							neighbors[i][3]+=1
						else:
							neighbors[i][2]+=1

					elif self.get_site_occupancy(i,j-1):
						neighbors[i][2]+=1
					else:
						neighbors[i][1]+=1
				else:
					neighbors[i][0]+=1

			# normalize
			for j in range(4):
				neighbors[i][j] *= self.weights[i]

		return neighbors

	def set_probabilities(self,totalP,totalL,T):

		# set the weights of each configuration
		NonAdditive.set_probabilities(self,totalP,totalL,T)
		if self.log == None:
			return

		# get the configuration-weighted number of sites either unoccupied, with no neighbors, one, or two neighboring sites occupied
		# must be called after set_probabilities()
		neighbors = self.get_neighbors()

		probabilities = [0.0,0.0,0.0,0.0]
		for i in range(self.nconfigs):
			for j in range(4):
				probabilities[j] += (neighbors[i][j] / self.nsites)

		# write probability information to logfile
		handle = open(self.log,'a+')
		if self.log_counter == 1:
			handle.write("#inj	ratio	empty	loaded0	loaded1	loaded2\n")
		handle.write( "%i\t"%(self.log_counter) )
		handle.write( "%f\t"%(totalL / totalP) )
		handle.write( "%f\t"%(probabilities[0]) )
		handle.write( "%f\t"%(probabilities[1]) )
		handle.write( "%f\t"%(probabilities[2]) )
		handle.write( "%f\t"%(probabilities[3]) )
		handle.write( "\n" )
		handle.close()

		self.log_counter+=1
"""
from itcsimlib.mass_spec import MSModel
itc_model = NonAdditive(
    nsites=12, circular=1, units="J",
    lattice_name="BhaTRAP", ligand_name="Trp",
)
itc_model.set_params(dGX=-20000, dGY=-25160.8 ,dGZ=-30989.1)
ms_model = MSModel(itc_model)
"""
from itcsimlib.mass_spec import MSModel
from itcsimlib.mass_spec import MSExperiment
for name in ['simulated-12-ms_cnn']:
	sim = ITCSim(T0=273.15+25, units='J', verbose=True, threads=1) # threads=1, as if multiple experiments are being simulated simultaneously, results from both will be written to the files out of order
	sim.set_model( MSModel(NonAdditiveRecorder(log="log_%s.txt"%(name), nsites=12, circular=1, lattice_name="BhaTRAPWT", ligand_name="Trp") ))
	sim.set_model_params(dGX=-7.5*4184, dGY=-7.5*4184 ,dGZ=-7.5*4184)
	sim.add_experiment( MSExperiment("./data/%s.txt"%(name)))
	sim.run()
	sim.make_plots(hardcopy=True)
	sim.done()
