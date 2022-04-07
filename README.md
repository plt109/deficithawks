# deficithawks
This is the code used to produce the results in  "Deficit hawks: robust new physics searches with unknown backgrounds".

... or at least, it soon will be. The code is gradually being posted while it is being cleaned up. Surely you have not finished reading the preprint already?

## Installation

This code depends on the [hypney](https://github.com/JelleAalbers/hypney) inference package. Until this appears on pypi, you can install it via
```
pip install git+https://github.com/JelleAalbers/hypney
```

Afterwards, you should be able to run the notebooks in the repository folder.

## Caveats

If you want to play around with deficit hawks, this code might not be the best place to start. Although cylinder.ipynb could be helpful, the other notebooks will seem unnecessarily complicated and may take hours to execute -- since they test many different unknown backgrounds at high statistics.

Instead, you might prefer to use your favourite inference pipeline (whether that is [RooFit](https://root.cern/manual/roofit/), [zfit](https://github.com/zfit/zfit), [pyhf](https://github.com/scikit-hep/pyhf), etc.) to brew your own deficit hawk. All you need is the ability to:

  * Do likelihood tests, and
  * Estimate the distribution of a test statistic through toy Monte Carlo.

You need both of these things anyway to do likelihood ratio inference. Unless you're in one of the lucky situations where you can use an asymptotic result like Wilks' theorem without worry..
