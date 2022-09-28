# Nearest-neighbor-model_2022

## Introduction

This is the collections of data fitting scripts in the paper of [Li, Weicheng, Norris, Andrew N, *et al*, *Protein science* (2022)](https://onlinelibrary.wiley.com/doi/full/10.1002/pro.4424). 

It includes the scripts of:

1. Hyperbolic curve fitting for CD and ITC data (Fig 3)
2. Quadratic curve fitting for concentration correction (Fig S6)
3. NN model simulations of bound population distributions via *itcsimlib* (Fig 2b)
4. NN model simulations of bound fractional saturations via *itcsimlib* (Fig 2c)
5. NN model data fitting of native Mass Spectra (nMS) titration via *itcsimlib* (Fig 4b)
6. NN model predictions of cellular protein saturations via *itcsimlib* (Fig 5d)

Note: *[itcsimlib](https://github.com/elihuihms/itcsimlib)* is the python module that helps to fit the thermodynamic binding data via statistical mechanics model. The statistical thermodynamic model can be easily self-designed and automatically computed and displayed in itcsimlib.


More scripts will be updated in the future. Feel free to comment or contact.


## Requirements

* *numpy*
* *scipy*
* *matplotlib*
* *sympy*
* *pyx*
* *[itcsimlib](https://github.com/elihuihms/itcsimlib)*


## Acknowledgment

I hope this work could potentially inspire or accelerate your research. If it does, please consider cite the following paper:

1. Li, Weicheng, Norris, Andrew N. et al. "Thermodynamic coupling between neighboring binding sites in homo-oligomeric ligand sensing proteins from mass resolved ligand-dependent population distributions." Protein Science (2022) [https://doi.org/10.1002/pro.4424](https://doi.org/10.1002/pro.4424)

If you are using *itcsimlib*, please also consider cite the following paper:

2. Ihms, Elihu C. et al. "Mechanistic models fit to variable temperature calorimetric data provide insights into cooperativity.” Biophysical Journal (2017) [https://doi.org/10.1016/j.bpj.2017.02.031](https://doi.org/10.1016/j.bpj.2017.02.031)



