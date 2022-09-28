import sys, os
sys.path.append(os.path.abspath("..")) # add parent directory for import

from itcsimlib.model_ising import HalfAdditive
from itcsimlib.mass_spec import MSModel

itc_model = HalfAdditive(
    nsites=12, circular=1, units="J",
    lattice_name="BhaTRAPWT", ligand_name="Trp",
)

#dGb: additional free energy change upon binding to a site flanked by an occupied site
itc_model.set_params(dG0=-20000, dGb=-10000)

ms_model = MSModel(itc_model)
print(ms_model)

from itcsimlib import ITCSim

sim = ITCSim(verbose=True, threads=1, units="J")


from itcsimlib import ITCFit
from itcsimlib.mass_spec import MSExperiment

empirical_exp = MSExperiment("Your_experimental_data.txt")
print(empirical_exp)

sim.remove_all_experiments()
sim.add_experiment( empirical_exp )

sim.set_model( ms_model )

opt = ITCFit(sim).optimize(params=('dG0','dGb'), update_fits=True)

sim.run()
from itcsimlib.utilities import write_params_to_file
write_params_to_file( "output_of_fitted_parameter.txt", params=sim.get_model_params() )

sim.experiments[0].make_plot()

sim.experiments[0].make_population_plot(dataset="experimental")
sim.experiments[0].make_population_plot(dataset="fit")
sim.experiments[0].make_population_plot(dataset="residuals")
print(opt)
