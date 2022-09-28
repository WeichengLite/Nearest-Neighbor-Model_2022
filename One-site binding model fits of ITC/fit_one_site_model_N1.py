import sys, os
sys.path.append(os.path.abspath(".."))

from itcsimlib import *
from itcsimlib.model_independent import OneMode

sim = ITCSim(T0=298.15,units="kcal",verbose=True)

sim.add_experiment_file('Bst_WT_25.txt', skip=[0])
sim.set_model( OneMode() )
sim.set_model_params(n=11, dG=-10, dH=-10)

fit = ITCFit( sim, verbose=True )
optimized_params,chisq = fit.optimize( params=['n','dG','dH'], update_fits=True)
sim.run()
print(optimized_params,chisq)
sim.make_plots()

from itcsimlib.utilities import write_params_to_file
write_params_to_file( "Bst_WT_25_fit.txt", params=sim.get_model_params(),format="%.5E" )

sim.done()
