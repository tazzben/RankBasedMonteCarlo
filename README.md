# Rank Based Monte Carlo

This package produces the null hypothesis distribution of four non-parametric tests: Mann-Whitney (MW), Kruskal-Wallis (KW), Kolmogorov-Smirnov (KS) and Kuiper (K). 

In all cases, the distribution is created by initializing the class (MonteCarloMannWhitney, MonteCarloKruskalWallis, MonteCarloKolmogorovSmirnov, MonteCarloKuiper) from the package and calling the method PrintCriticalValueTable.  For instance, the KW test statistics can be accomplished with the following code:

~~~

from RankBasedMonteCarlo import MonteCarloKruskalWallis

if __name__ == '__main__':
    kw = MonteCarloKruskalWallis()
    criticalValues, pvalue = kw.PrintCriticalValueTable((6, 45, 30), 10000, 9)

~~~


The class is imported from the package on the first line.  Within the if statement, an instance of the class is created (kw) and the critical values and pvalue is determined on the next line.  The PrintCriticalValueTable method accepts the same parameters regardless of the statistical test:


1. ns : tuple : A tuple listing the number of observations per group.  For instance (6,5)
2. reps : int : The number of repetitions the process completes before producing critical values.  Default is 10,000.
3. observedValue : float : Optional value used to determine p-value
4. PrintToScreen : bool : Specifies if the critical values are printed to the screen.  Defaults to True.
5. cvs : list : Specifies a list of critical values.

## Installation

This package can be installed using pip or conda (Anaconda):

### Using Pip

~~~

pip install RankBasedMonteCarlo

~~~		

### Using Conda

~~~

conda install -c tazzben rankbasedmontecarlo

~~~