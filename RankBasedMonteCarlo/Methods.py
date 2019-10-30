import numpy
import pandas
import sys
import multiprocessing

class _RankBasedMonteCarlo:
	
	def _RandomRank(self, ns):
		objects = numpy.concatenate([numpy.repeat((i+1), n) for i, n in enumerate(ns)],axis=None)
		numpy.random.shuffle(objects)
		return pandas.DataFrame({'Group':objects.tolist(),}).assign(Rank = range(1,objects.size+1))

	def _RandomStatistic(self, sampleSizes):
		sample = self._RandomRank(sampleSizes)
		return self.CalculateStatistic(sample)

	def _PoolMonteCarlo(self, ns, reps):
		p = multiprocessing.Pool()
		r = []
		for i, result in enumerate(p.imap_unordered(self._RandomStatistic, (ns,)*reps)):
			r.append(result)
			sys.stderr.write('\r{: .2f}% done'.format(100*i/reps))
		p.close()
		p.join()
		return numpy.array(r)

	def CalculateStatistic(self, sample):
		return sample['Rank'].median()

	def PrintCriticalValueTable(self, ns, reps = 10000, observedValue = None, PrintToScreen = True, cvs = [0.01, 0.025, 0.05, 0.1], reverseDist = False):
		r = self._PoolMonteCarlo(ns, reps)

		cvresults = []
		for i in cvs:
			qvalue = numpy.quantile(r, i)
			cvresults.append(qvalue)
		
		if PrintToScreen: print("\n" + pandas.DataFrame(zip(cvs, cvresults), columns=["Quantile", "Critical Value"]).to_string(index=False)) 
		
		try:
			observedValue = float(observedValue)
			pvalue = len(r[(r > observedValue)])/reps if reverseDist else len(r[(r < observedValue)])/reps
			if PrintToScreen: print("Percent of distribution " + ("above" if reverseDist else "below") + " the observed value:" + "{: .4f}".format(pvalue))
			return (dict(zip(cvs, cvresults)), pvalue)
		
		except:
			return (dict(zip(cvs, cvresults)), None)


class MonteCarloKolmogorovSmirnov(_RankBasedMonteCarlo):

	def CalculateStatistic(self, sample):
		n1len = len(sample[sample['Group'] == 1].index)
		n2len = len(sample[sample['Group'] == 2].index)
		return numpy.array([numpy.abs(len(sample[((sample['Group'] == 1) & (sample['Rank'] <= x))].index)/n1len -
                    len(sample[((sample['Group'] == 2) & (sample['Rank'] <= x))].index)/n2len) for x in sample['Rank']]).max()
	
	def PrintCriticalValueTable(self, ns, reps = 10000, observedValue = None, PrintToScreen = True, cvs = [0.9, 0.95, 0.975, 0.99], reverseDist = True):
		return super().PrintCriticalValueTable(ns, reps, observedValue, PrintToScreen, cvs, reverseDist)


class MonteCarloKuiper(_RankBasedMonteCarlo):
	
	def CalculateStatistic(self, sample):
		n1len = len(sample[sample['Group'] == 1].index)
		n2len = len(sample[sample['Group'] == 2].index)
		dPos = numpy.array([len(sample[((sample['Group'] == 1) & (sample['Rank'] <= x))].index)/n1len -
                   len(sample[((sample['Group'] == 2) & (sample['Rank'] <= x))].index)/n2len for x in sample['Rank']]).max()
		dNeg = numpy.array([len(sample[((sample['Group'] == 2) & (sample['Rank'] <= x))].index)/n2len -
                   len(sample[((sample['Group'] == 1) & (sample['Rank'] <= x))].index)/n1len for x in sample['Rank']]).max()
		return dPos + dNeg
	
	def PrintCriticalValueTable(self, ns, reps = 10000, observedValue = None, PrintToScreen = True, cvs = [0.9, 0.95, 0.975, 0.99], reverseDist = True):
		return super().PrintCriticalValueTable(ns, reps, observedValue, PrintToScreen, cvs, reverseDist)

class MonteCarloMannWhitney(_RankBasedMonteCarlo):
	
	def CalculateStatistic(self, sample):
		n1len = len(sample[sample['Group'] == 1].index)
		U1 = sample[sample['Group'] == 1]['Rank'].sum() - (n1len*(n1len+1))/2
		return U1

class MonteCarloKruskalWallis(_RankBasedMonteCarlo):

	def CalculateStatistic(self, sample):
		n = len(sample.index)
		rbar = 0.5*(n+1)
		divisor = 0
		numerator = 0
		
		for group in pandas.unique(sample['Group']):
			grouplen = len(sample[sample['Group'] == group].index)
			groupmean = sample[sample['Group'] == group]['Rank'].mean()
			divisor += numpy.array([numpy.power((x-rbar),2) for x in sample[sample['Group'] == group]['Rank']]).sum()
			numerator += grouplen*numpy.power((groupmean-rbar),2)
		
		return ((n-1)*numerator)/divisor

	def PrintCriticalValueTable(self, ns, reps = 10000, observedValue = None, PrintToScreen = True, cvs = [0.9, 0.95, 0.975, 0.99], reverseDist = True):
		return super().PrintCriticalValueTable(ns, reps, observedValue, PrintToScreen, cvs, reverseDist)
