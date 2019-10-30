from RankBasedMonteCarlo import MonteCarloMannWhitney, MonteCarloKruskalWallis, MonteCarloKolmogorovSmirnov, MonteCarloKuiper

if __name__ == '__main__':

    mw = MonteCarloMannWhitney()
    mw.PrintCriticalValueTable((20, 20), 10000, 130)

    kw = MonteCarloKruskalWallis()
    kw.PrintCriticalValueTable((25, 25, 25))
    
    ks = MonteCarloKolmogorovSmirnov()
    ks.PrintCriticalValueTable((12, 12))

    k = MonteCarloKuiper()
    k.PrintCriticalValueTable((12, 12))
