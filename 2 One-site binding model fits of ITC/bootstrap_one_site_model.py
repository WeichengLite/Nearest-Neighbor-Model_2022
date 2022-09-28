import sys, os
sys.path.append(os.path.abspath(".."))

from itcsimlib import *
from itcsimlib.model_independent import OneMode

sim = ITCSim(T0=298.15, units="kcal", verbose=False)
sim.set_model( OneMode())

sim.add_experiment_file('Bst_WT_25_measuredconc.txt', skip=[0])


fit = ITCFit( sim, verbose=True )

from itcsimlib.utilities import read_params_from_file

tmp = read_params_from_file( "Bst_WT_25_fit.txt", row=1 )
sim.set_model_params( **tmp )

f = open('workfile.txt', 'w')
#'w' for only writing (an existing file with the same name will be erased), and 'a' opens the file for appending


params = fit.estimate( params=['dG'], bootstraps=200 )
print("dG Mean: %.3f kcal +/- %.3f kcal"%params['dG'], file = f)

params = fit.estimate( params=['dH'], bootstraps=200 )
print("dH Mean: %.3f kcal +/- %.3f kcal"%params['dH'], file = f)

params = fit.estimate( params=['n'], bootstraps=200 )
print("n Mean: %.3f kcal +/- %.3f kcal"%params['n'], file = f)

f.close()


sim.done()
