#!/usr/bin/env python

# script to simulate ms populations from a lattice model
# 2019-06-30
# TODO: implement pandas data structure

import numpy
import argparse

from itcsimlib import *
from itcsimlib.model_ising import NonAdditive
from itcsimlib.mass_spec import MSExperimentSynthetic, MSModel

parser = argparse.ArgumentParser(description='simulate populations of free and bound species from a lattice model; saves populations to a text file')
parser.add_argument("-T", help="Temperature /K", type=float, default=298)
parser.add_argument("-nsites", help="specify number of sites", type=int, default=12)
parser.add_argument("-kdx", help="first dissociation constant in M", type=float, default=3.17806E-06)
parser.add_argument("-kdy", help="second dissociation constant in M", type=float, default=3.17806E-06)
parser.add_argument("-kdz", help="third dissociation constant in M", type=float, default=3.17806E-06)
parser.add_argument("-lattice", help="concentration of lattice w/ nsites in M", type=float, default=5E-06)
parser.add_argument("-maxlig",
	help="maximum titrated ligand concentration in M", type=float,
	default=90e-6)
parser.add_argument("-npoints", help="number of ligand titration points", type=int, default=6)
parser.add_argument("-noise", help="decimal fraction of noice in the data", type=float, default=0)
parser.add_argument("-shape", help="shape of lattice: circular, or linear",
	type=str, default='circular', choices=['circular', 'linear'])
args = parser.parse_args()
#print args
print(vars(args))
#for arg in vars(args):
#	print arg, getattr(args,arg)

# set parameters from input, or defaults --
# This seems like a kludge -- how to set the golbal parameters from the args namespace?
T = args.T
kdx = args.kdx
kdy = args.kdy
kdz = args.kdz
nsites = args.nsites
npoints = args.npoints
lattice_conc = args.lattice
maxlig = args.maxlig
noise = args.noise
if args.shape == 'linear':
	circular = 0
else:
	circular = 1

# set dG values from Kds
dGX = thermo.dG_from_Kd(kdx, T)
dGY = thermo.dG_from_Kd(kdy, T)
dGZ = thermo.dG_from_Kd(kdz, T)

ms_model = MSModel(NonAdditive(nsites=nsites, circular=circular, units="J"))
ms_model.set_params(dGX=dGX,dGY=dGY,dGZ=dGZ)
print (ms_model)

sim = ITCSim(verbose=True, threads=1, units="J")

sim.set_model(ms_model)

#
# simulated experimental params
#
#lattice_conc = 1E-6	# defined above
#ligand_conc_start = 0	# assume 0
#ligand_conc_end = maxlig
#ligand_conc_step = maxlig/npoints	# npoints defined above
#ligand_conc_step = (maxlig - ligand_conc_start)/npoints	# npoints defined above

# issue warning if max-lig < site concentration
if maxlig < lattice_conc * nsites:
	print ("*** Warning: final ligand concentration is less than the site concentation...")
	print ("... saturation cannot be achieved under these conditions ***")

# generate the concentrations to simulate
#ligand_concs = numpy.arange(ligand_conc_start,ligand_conc_end,ligand_conc_step) # arange is non-inclusive
ligand_concs = [0, (90e-6)*(0.370106762)]
lattice_concs = [lattice_conc]*2	# make the list of lattice concentrations match ligand

# initialize the synthetic experiment
exp = MSExperimentSynthetic(
	lattice_concs=lattice_concs,
	ligand_concs=ligand_concs,
	noise=noise,
	T=T,
	title="simulated-halfs-ms-" + str(nsites)
	)
print (exp) # this will produce a warning because no data simulated yet!

sim.add_experiment( exp )

sim.run()

print (exp) # now that it has been simulated, there's information here (not much though...)

# the experiment contains the perfect simulated data as the "fit"
# the noisy data obtained by adding gaussian noise to the simulated data is the "experimental" data
sim.make_plots(hardcopy=True,hardcopytype='png')

# Now export the intensities

path= ("simulated-halfs-" + str(nsites) + "-ms.txt")
from datetime import datetime

fh = open(path, 'w')
#print exp
#print dir(exp)
fh.write("# %s\n"%exp.title)
fh.write("# Populations simulated for a %s lattice with %i sites and NN Kds of %.2e, %.2e, %.2e M\n"%(args.shape,nsites,kdx,kdy,kdz) )
fh.write("# itcsim export of %s\n#\n"%(exp.title))
fh.write("# Date        %s\n"%(datetime.ctime(datetime.today())))
fh.write("Lattice/M \tLigand/M \t%s\n" % (
      	"\t".join(["State-%i"%s for s in range(exp.npops)])))
for i in range(exp.npoints//exp.npops):
       	fh.write("%0.3E\t%0.3E\t%s\n" % (
               	exp.Concentrations[i]['Lattice'],
               	exp.Concentrations[i]['Ligand'],
               	"\t".join(["%f"%f for f in exp.PopIntens[i]])))

fh.close()


sim.done()
