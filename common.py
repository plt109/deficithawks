from concurrent.futures import ProcessPoolExecutor, as_completed
import warnings

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import hypney.all as hp

# Colorblind-friendly color set
ibm = dict(
    blue='#648FFF',
    purple='#785EF0',
    red='#DC267F',
    orange='#FE6100',
    gold='#FFB000',
)


def t0(mu, n):
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore')
        return np.where(
            n == 0,
            -np.sqrt(2 * mu),
            np.sign(n - mu) * 2**0.5 * np.sqrt(mu - n + n * np.log(n/mu)))


def draw_limits(ul, source, n_limits=1, tolerant=True):
    """Simulate n_limits toy MC limits with 
        ul: hypney.UpperLimit
        source: hypney.Model to simulate events from
        
    tolerant: on exception, print and set limit to NaN
        instead of raising
    """
    results = np.zeros(n_limits)
    for i in range(n_limits):
        try:
            x = ul(source.simulate())
        except hp.FullIntervalError:
            x = float('inf')
        except hp.EmptyIntervalError:
            x = 0
        except Exception as e:
            if tolerant:
                print("Error while setting limits: ", e)
                x = float('nan')
            else:
                raise
        results[i] = x
    return results


##
# Example distributions on [0,1]
##
signal = hp.uniform().fix_except('rate')

def powerlaw(mu=1, alpha=0.5, loc=0):
    if alpha < 0:
        # Flip side
        return powerlaw(-alpha, mu, loc=-1).scale(-1)
    elif alpha == 0:
        return hp.DiracDelta(rate=mu, loc=1)
    return hp.powerlaw(a=1/alpha, rate=mu, loc=loc)

def block_bg(mu=1, alpha=0.5):
    """A uniform distribution on [0, alpha]"""
    return hp.uniform(scale=alpha, rate=mu).fix_except('rate')

def triangle_bg(mu=1):
    return hp.triang(rate=mu).fix_except('rate')

def _split_rates(q):
    return {'m0_rate': q['rate'] / 2, 'm1_rate': q['rate'] / 2}

def staircase_bg(mu=1, alpha=0.5):
    """A U[0,5] mixed with a U[0,1] signal"""
    return (
        hp.uniform(scale=0.5).fix_except('rate') + 
        hp.uniform().fix_except('rate')
    ).reparametrize(
        _split_rates,
        param_specs=[hp.DEFAULT_RATE_PARAM])

def beta_halfpipe(mu=1, alpha=0.5):
    """A 'halfpipe' formed by a beta distribution"""
    return hp.beta(a=alpha, b=alpha, rate=mu)


def halfpipe_bg(mu=1, halfpipe_width=0.2):
    """A 'halfpipe' formed by two truncated Gaussians"""
    # ~50% of each component is in [0, 1], but we have two components
    # so we can just share the rate
    return hp.mixture(
        hp.norm(loc=0, scale=halfpipe_width).fix_except('rate'), 
        hp.norm(loc=1, scale=halfpipe_width).fix_except('rate'),
        share='rate')(rate=mu).cut(0, 1)

def halfpipe_narrow(mu=1, halfpipe_width=0.1):
    return halfpipe_bg(mu=mu, halfpipe_width=halfpipe_width)

def _split_rates_asym(q):
    asym = 5  # to 1
    return {
        'm0_rate': q['rate'] * 2 * asym/(1 + asym), 
        'm1_rate': q['rate'] * 2 * 1/(1 + asym)}

def halfpipe_asym(mu=1, halfpipe_width=0.2):
    """Asymmetric halfpipe background"""
    return (
        (hp.norm(loc=0, scale=halfpipe_width).cut(0, 1).fix_except('rate') +
         hp.norm(loc=1, scale=halfpipe_width).cut(0, 1).fix_except('rate')) 
        .reparametrize(
            _split_rates_asym,
            param_specs=[hp.DEFAULT_RATE_PARAM]))



##
# Plotting helpers
##

def sketch_dist(dist, fudge=1e-7, xlabel='Unknown PDF', annotation=None, color='k'):
    ax = plt.gca()
    x = np.linspace(fudge, 1 - fudge, 1000)

    plt.fill_between(x, 0.0, dist.diff_rate(x), color=color, alpha=0.5, linewidth=0)
    
    #plt.plot(x, 1 + 0 * x, c='r', linestyle='--')
    
    plt.ylim(0, 2.1)
    plt.xlim(0, 1 + fudge)

    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    plt.yticks([0, .5, 1, 1.5, 2])
    plt.xticks([0, .25, .5, .75, 1])
    
    if xlabel:
        plt.xlabel(xlabel, fontsize=8)
    
    # Hide tick marks on axes        
    ax.tick_params(axis='both', which='both',length=0)
    
    # Hide all except bottom spine
    for q in 'top right left'.split():
        ax.spines[q].set_visible(False)

    plt.grid(c='k', alpha=0.1, linewidth=0.5)

    if annotation:
        plt.text(
            0.025, 0.9, annotation,
            alpha=0.5,
            transform=plt.gca().transAxes,
            va='top',
            ha='left', fontsize=3)


def logticks(tmin, tmax=None, tick_at=None):
    if tick_at is None:
        tick_at = (1, 2, 5, 10)
    a, b = np.log10([tmin, tmax])
    a = np.floor(a)
    b = np.ceil(b)
    ticks = np.sort(np.unique(np.outer(
        np.array(tick_at), 
        10.**np.arange(a, b)).ravel()))
    ticks = ticks[(tmin <= ticks) & (ticks <= tmax)]
    return ticks

def log_x(a=None, b=None, scalar_ticks=True, tick_at=None):
    plt.xscale('log')
    if a is not None:
        if b is None:
            a, b = a[0], a[-1]
        plt.xlim(a, b)
        ax = plt.gca()
        if scalar_ticks:
            ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
            ax.set_xticks(logticks(a, b, tick_at))
            ax.xaxis.set_minor_locator(matplotlib.ticker.NullLocator())


def log_y(a=None, b=None, scalar_ticks=True, tick_at=None):
    plt.yscale('log')
    if a is not None:
        if b is None:
            a, b = a[0], a[-1]
        ax = plt.gca()
        plt.ylim(a, b)
        if scalar_ticks:
            ax.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter('%g'))
            ax.set_yticks(logticks(a, b, tick_at))
            ax.yaxis.set_minor_locator(matplotlib.ticker.NullLocator())
    
