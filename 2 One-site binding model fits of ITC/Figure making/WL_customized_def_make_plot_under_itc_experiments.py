def make_plot(self, residuals=True, hardcopy=True, hardcopydir='.', hardcopyprefix='', hardcopytype='png'):
		"""Generate a plot of the experimental data, and the fit if present.

		Arguments
		----------
		residuals: boolean
			Includes a plot of fit residuals if a fit is present.
		hardcopy : boolean
			Writes the plot to a file instead of displaying to screen.
		hardcopydir : string
			The directory to write the hardcopy to.
		hardcopyprefix : string
			A prefix to append to the experiment's title when generating the output plot filename.
		hardcopytype : string
			The output format for the plot (availability is dependent upon what backends matplotlib was compiled with).

		Returns
		-------
		None
		"""
		if not self.initialized:
			raise Exception("No data to plot. If experiment is synthetic, call sim.run() first.")

		try:
			matplotlib.get_backend()
		except:
			if MATPLOTLIB_BACKEND != None:
				import matplotlib
				matplotlib.use(MATPLOTLIB_BACKEND)

		import matplotlib.pyplot as pyplot

		if self.dQ_fit is not None and residuals:
			fig, (ax1, ax2) = pyplot.subplots(2,1, figsize=(18/2.54,15/2.54),gridspec_kw={"height_ratios": [4, 1]}, sharex=True)
			gs = fig.add_gridspec(nrows=2, ncols=1, hspace=0)
			#ax2.set_ylabel("Residual (%s)"%(self.units))
			#ax2.set_xlabel("%s / %s"%(self.syringeRef,self.cellRef))
			ax2.axhline(y=0.0, c='#000000', ls="--",lw=1)
			ax2.set_ylim([-2, 2])
			ax2.tick_params(axis='both',direction='in',left=1, bottom=1, top=0, right=0, labelleft=0,labelbottom=0, labeltop=0, labelright=0)
			fig.tight_layout()
		else:
			fig, ax1 = pyplot.subplots()
			fig.tight_layout()


		#ax1.set_ylabel("%s/mol of %s"%(self.units,self.syringeRef))
		ax1.set_ylim([-14, 2])
		ax1.locator_params(axis="y", nbins=4)
		ax1.locator_params(axis="x", nbins=4)
		ax1.tick_params(axis='both',direction='in',left=1, bottom=1, top=0, right=0, labelleft=0,labelbottom=0, labeltop=0, labelright=0)




		# For convention, normalize the heat evolved as per mol of injected reference ligand
		tmp_rat = [ self.Concentrations[i][self.syringeRef]/self.Concentrations[i][self.cellRef] for i in range(self.npoints) if i not in self.skip ]
		tmp_exp = [ convert_from_J(self.units,self.dQ_exp[i])/self.Syringe[self.syringeRef]/self.injections[i] for i in range(self.npoints) if i not in self.skip ]

		if self.dQ_err is not None:
			tmp_err = [ convert_from_J(self.units,self.dQ_err[i]) for i in range(self.npoints) if i not in self.skip ]
			ax1.errorbar(tmp_rat,tmp_exp,yerr=tmp_err,c='#1d3d59',fmt='s')


		if len(self.skip) > 0:
			tmp_xsk = [ self.Concentrations[i][self.syringeRef]/self.Concentrations[i][self.cellRef] for i in self.skip ]
			tmp_ysk = [ convert_from_J(self.units,self.dQ_exp[i])/self.Syringe[self.syringeRef]/self.injections[i] for i in self.skip ]
			ax1.errorbar(tmp_xsk,tmp_ysk,yerr=0.0,c='r',fmt='s')

		if self.Q_dil != 0:
			tmp_xdl = [ self.Concentrations[i][self.syringeRef]/self.Concentrations[i][self.cellRef] for i in range(self.npoints) if i not in self.skip ]
			tmp_ydl = [ convert_from_J(self.units,self.dQ_dil[i])/self.Syringe[self.syringeRef]/self.injections[i] for i in range(self.npoints) if i not in self.skip ]
			ax1.plot(tmp_xdl,tmp_ydl,c='b')

		if self.dQ_fit is not None:
			tmp_fit = [ convert_from_J(self.units,self.dQ_fit[i])/self.Syringe[self.syringeRef]/self.injections[i] for i in range(self.npoints) if i not in self.skip ]
			ax1.plot(tmp_rat,tmp_fit,c='#f8aa9e',lw=3)
			if residuals:
				ax2.errorbar(tmp_rat,[y1-y2 for y1,y2 in zip(tmp_exp,tmp_fit)],yerr=tmp_err,c='#f8aa9e',fmt='s')
			if residuals and len(self.skip) > 0:
				tmp_fit = [ convert_from_J(self.units,self.dQ_fit[i])/self.Syringe[self.syringeRef]/self.injections[i] for i in self.skip ]
				ax2.errorbar(tmp_xsk,[y1-y2 for y1,y2 in zip(tmp_ysk,tmp_fit)],yerr=0.0,c='r',fmt='s')


		if hardcopy:
			fig.savefig( os.path.join(hardcopydir,"%s%s.%s"%(hardcopyprefix,self.title,hardcopytype)), bbox_inches='tight', dpi=1200)
			pyplot.close(fig)
		else:
			pyplot.show()
