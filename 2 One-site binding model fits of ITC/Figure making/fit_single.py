import sys, os
sys.path.append(os.path.abspath(".."))

from itcsimlib import *
from itcsimlib.model_independent import NModes

sim = ITCSim(T0=298.15,units="kcal",verbose=True)

sim.add_experiment_file('Bha_WT_noHis_25.txt', skip=[0])
sim.set_model( NModes(modes=2) )
sim.set_model_params(n1=0.5, n2=11.5, dG1=-11, dG2=-10, dH1=-15, dH2=+10)

fit = ITCFit( sim, verbose=True )
optimized_params,chisq = fit.optimize(  params=['n1','dG1','dH1','n2','dG2','dH2'], update_fits=True)
sim.run()
print(optimized_params,chisq)
sim.make_plots()

from itcsimlib.utilities import write_params_to_file
write_params_to_file( "Bha_WT_noHis_25_fit.txt", params=sim.get_model_params(),format="%.5E" )

sim.done()
