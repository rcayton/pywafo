''' 
Contains FitDistribution and Profile class, which are

important classes for fitting to various Continous and Discrete Probability Distributions

Author:  Per A. Brodtkorb 2008
'''

from __future__ import division

from wafo.plotbackend import plotbackend
from wafo.misc import ecross, findcross
#from scipy.misc.ppimport import ppimport

import numdifftools 
from scipy import special
from scipy.linalg import pinv2
from scipy import optimize

import numpy
import numpy as np
from numpy import alltrue, arange, ravel, ones, sum, zeros, log, sqrt, exp
from numpy import (atleast_1d, any, asarray, nan, pi, reshape, repeat, 
                   product, ndarray, isfinite)
from numpy import flatnonzero as nonzero


__all__ = [
           'Profile', 'FitDistribution'
          ]

floatinfo = np.finfo(float)
#arr = atleast_1d
arr = asarray
all = alltrue

def chi2isf(p, df):
    return special.chdtri(df, p)

def chi2sf(x, df):
    return special.chdtrc(df, x)

def norm_ppf(q):
    return special.ndtri(q)

def valarray(shape, value=nan, typecode=None):
    """Return an array of all value.
    """
    out = reshape(repeat([value], product(shape, axis=0), axis=0), shape)
    if typecode is not None:
        out = out.astype(typecode)
    if not isinstance(out, ndarray):
        out = arr(out)
    return out 

# Frozen RV class
class rv_frozen(object):
    ''' Frozen continous or discrete 1D Random Variable object (RV)

    RV.rvs(size=1)
        - random variates

    RV.pdf(x)
        - probability density function (continous case)

    RV.pmf(x)
        - probability mass function (discrete case)

    RV.cdf(x)
        - cumulative density function

    RV.sf(x)
        - survival function (1-cdf --- sometimes more accurate)

    RV.ppf(q)
        - percent point function (inverse of cdf --- percentiles)

    RV.isf(q)
        - inverse survival function (inverse of sf)

    RV.stats(moments='mv')
        - mean('m',axis=0), variance('v'), skew('s'), and/or kurtosis('k')

    RV.entropy()
        - (differential) entropy of the RV.
    '''
    def __init__(self, dist, *args, **kwds):
        self.dist = dist
        loc0, scale0 = map(kwds.get, ['loc', 'scale'])
        if hasattr(dist, 'fix_loc_scale'): #isinstance(dist, rv_continuous):
            args, loc0, scale0 = dist.fix_loc_scale(args, loc0, scale0)
            self.par = args + (loc0, scale0)
        else: # rv_discrete
            args, loc0 = dist.fix_loc(args, loc0)
            self.par = args + (loc0,)

    def pdf(self, x):
        ''' Probability density function at x of the given RV.'''
        return self.dist.pdf(x, *self.par)
    def cdf(self, x):
        '''Cumulative distribution function at x of the given RV.'''
        return self.dist.cdf(x, *self.par)
    def ppf(self, q):
        '''Percent point function (inverse of cdf) at q of the given RV.'''
        return self.dist.ppf(q, *self.par)
    def isf(self, q):
        '''Inverse survival function at q of the given RV.'''
        return self.dist.isf(q, *self.par)
    def rvs(self, size=None):
        '''Random variates of given type.'''
        kwds = dict(size=size)
        return self.dist.rvs(*self.par, **kwds)
    def sf(self, x):
        '''Survival function (1-cdf) at x of the given RV.'''
        return self.dist.sf(x, *self.par)
    def stats(self, moments='mv'):
        ''' Some statistics of the given RV'''
        kwds = dict(moments=moments)
        return self.dist.stats(*self.par, **kwds)
    def median(self):
        return self.dist.median(*self.par)
    def mean(self):
        return self.dist.mean(*self.par)
    def var(self):
        return self.dist.var(*self.par)
    def std(self):
        return self.dist.std(*self.par)
    def moment(self, n):
        par1 = self.par[:self.dist.numargs]
        return self.dist.moment(n, *par1)
    def entropy(self):
        return self.dist.entropy(*self.par)
    def pmf(self, k):
        '''Probability mass function at k of the given RV'''
        return self.dist.pmf(k, *self.par)
    def interval(self,alpha):
        return self.dist.interval(alpha, *self.par)


# internal class to profile parameters of a given distribution
class Profile(object):
    ''' Profile Log- likelihood or Product Spacing-function.
            which can be used for constructing confidence interval for
            either phat(i), probability or quantile.
    Call
    -----
      Lp = Profile(fit_dist,**kwds)

    Parameters
    ----------
    fit_dist : FitDistribution object with ML or MPS estimated distribution parameters.

    **kwds : named arguments with keys
          i          - Integer defining which distribution parameter to
                         profile, i.e. which parameter to keep fixed
                         (default index to first non-fixed parameter)
          pmin, pmax - Interval for either the parameter, phat(i), prb, or x,
                        used in the optimization of the profile function (default
                        is based on the 100*(1-alpha)% confidence interval
                        computed using the delta method.)
          N          - Max number of points used in Lp (default 100)
          x          - Quantile (return value)
          logSF      - log survival probability,i.e., SF = Prob(X>x;phat)
          link       - function connecting the quantile (x) and the
                         survival probability (SF) with the fixed distribution
                         parameter, i.e.: self.par[i] = link(x,logSF,self.par,i),
                         where logSF = log(Prob(X>x;phat)).
                         This means that if:
                          1) x is not None then x is profiled
                          2) logSF is not None then logSF is profiled
                          3) x and logSF both are None then self.par[i] is profiled (default)
          alpha       - confidence coefficent (default 0.05)
    Returns
    -------
    Lp : Profile log-likelihood function with parameters phat given
               the data, phat(i), probability (prb) and quantile (x) (if given), i.e.,
                 Lp = max(log(f(phat|data,phat(i)))),
               or
                 Lp = max(log(f(phat|data,phat(i),x,prb)))
    Member methods
      plot()
      get_CI()

    Member variables
      fit_dist - fitted data object.
      data - profile function values
      args - profile function arguments
      alpha - confidence coefficient
      Lmax - Maximum value of profile function
      alpha_cross_level -

    PROFILE is a utility function for making inferences either on a particular
    component of the vector phat or the quantile, x, or the probability, SF.
    This is usually more accurate than using the delta method assuming
    asymptotic normality of the ML estimator or the MPS estimator.


    Examples
    --------
    #MLE and better CI for phat.par[0]
    >>> import numpy as np
    >>> R = weibull_min.rvs(1,size=100);
    >>> phat = weibull_min.fit(R,1,1,par_fix=[np.nan,0.,np.nan])
    >>> Lp = Profile(phat,i=0)
    >>> Lp.plot()
    >>> Lp.get_CI(alpha=0.1)
    >>> SF = 1./990
    >>> x = phat.isf(SF)

    # CI for x
    >>> Lx = phat.profile(i=1,x=x,link=phat.dist.link)
    >>> Lx.plot()
    >>> Lx.get_CI(alpha=0.2)

    # CI for logSF=log(SF)
    >>> Lpr = phat.profile(i=1,logSF=log(SF),link = phat.dist.link)


    '''
    def __init__(self, fit_dist, **kwds):
        self.fit_dist = fit_dist
        self.data = None
        self.args = None
        self.title = 'Profile log'
        self.xlabel = ''
        self.ylabel = ''
        self.i_fixed, self.N, self.alpha, self.pmin, self.pmax, self.x, self.logSF, self.link = map(kwds.get,
                            ['i', 'N', 'alpha', 'pmin', 'pmax', 'x', 'logSF', 'link'],
                            [0, 100, 0.05, None, None, None, None, None])

        self.ylabel = '%g%s CI' % (100 * (1.0 - self.alpha), '%')
        if fit_dist.method.startswith('ml'):
            self.title = self.title + 'likelihood'
            Lmax = fit_dist.LLmax
        elif fit_dist.method.startswith('mps'):
            self.title = self.title + ' product spacing'
            Lmax = fit_dist.LPSmax
        else:
            raise ValueError("PROFILE is only valid for ML- or MPS- estimators")
        if fit_dist.par_fix == None:
            isnotfixed = valarray(fit_dist.par.shape, True)
        else:
            isnotfixed = 1 - numpy.isfinite(fit_dist.par_fix)

        self.i_notfixed = nonzero(isnotfixed)

        self.i_fixed = atleast_1d(self.i_fixed)

        if 1 - isnotfixed[self.i_fixed]:
            raise ValueError("Index i must be equal to an index to one of the free parameters.")

        isfree = isnotfixed
        isfree[self.i_fixed] = False
        self.i_free = nonzero(isfree)

        self.Lmax = Lmax
        self.alpha_Lrange = 0.5 * chi2isf(self.alpha, 1) 
        self.alpha_cross_level = Lmax - self.alpha_Lrange
        #lowLevel = self.alpha_cross_level - self.alpha_Lrange / 7.0

        ## Check that par are actually at the optimum
        phatv = fit_dist.par.copy()
        self._par = phatv.copy()
        phatfree = phatv[self.i_free].copy()


        ## Set up variable to profile and _local_link function

        self.profile_x = not self.x == None
        self.profile_logSF = not (self.logSF == None or self.profile_x)
        self.profile_par = not (self.profile_x or self.profile_logSF)

        if self.link == None:
            self.link = self.fit_dist.dist.link
        if self.profile_par:
            self._local_link = lambda fix_par, par : fix_par
            self.xlabel = 'phat(%d)' % self.i_fixed
            p_opt = self._par[self.i_fixed]
        elif self.profile_x:
            self.logSF = log(fit_dist.sf(self.x))
            self._local_link = lambda fix_par, par : self.link(fix_par, self.logSF, par, self.i_fixed)
            self.xlabel = 'x'
            p_opt = self.x
        elif self.profile_logSF:
            p_opt = self.logSF
            self.x = fit_dist.isf(exp(p_opt))
            self._local_link = lambda fix_par, par : self.link(self.x, fix_par, par, self.i_fixed)
            self.xlabel = 'log(R)'
        else:
            raise ValueError("You must supply a non-empty quantile (x) or probability (logSF) in order to profile it!")

        self.xlabel = self.xlabel + ' (' + fit_dist.dist.name + ')'

        pvec = self._get_pvec(p_opt)


        mylogfun = self._nlogfun
        self.data = numpy.empty_like(pvec)
        self.data[:] = nan
        k1 = (pvec >= p_opt).argmax()
        for ix in xrange(k1, -1, -1):
            phatfree = optimize.fmin(mylogfun, phatfree, args=(pvec[ix],) , disp=0)
            self.data[ix] = -mylogfun(phatfree, pvec[ix])
            if self.data[ix] < self.alpha_cross_level:
                pvec[:ix] = nan
                break

        phatfree = phatv[self.i_free].copy()
        for ix in xrange(k1 + 1, pvec.size):
            phatfree = optimize.fmin(mylogfun, phatfree, args=(pvec[ix],) , disp=0)
            self.data[ix] = -mylogfun(phatfree, pvec[ix])
            if self.data[ix] < self.alpha_cross_level:
                pvec[ix + 1:] = nan
                break

        # prettify result
        ix = nonzero(numpy.isfinite(pvec))
        self.data = self.data[ix]
        self.args = pvec[ix]
        cond = self.data == -numpy.inf
        if any(cond):
            ind, = cond.nonzero()
            self.data.put(ind, floatinfo.min / 2.0)
            ind1 = numpy.where(ind == 0, ind, ind - 1)
            cl = self.alpha_cross_level - self.alpha_Lrange / 2.0
            t0 = ecross(self.args, self.data, ind1, cl)

            self.data.put(ind, cl)
            self.args.put(ind, t0)


    def _get_pvec(self, p_opt):
        ''' return proper interval for the variable to profile
        '''

        linspace = numpy.linspace
        if self.pmin == None or self.pmax == None:

            if self.profile_par:
                pvar = self.fit_dist.par_cov[self.i_fixed, :][:, self.i_fixed]
            else:
                i_notfixed = self.i_notfixed
                phatv = self._par

                if self.profile_x:
                    gradfun = numdifftools.Gradient(self._myinvfun)
                else:
                    gradfun = numdifftools.Gradient(self._myprbfun)
                drl = gradfun(phatv[self.i_notfixed])

                pcov = self.fit_dist.par_cov[i_notfixed, :][:, i_notfixed]
                pvar = sum(numpy.dot(drl, pcov) * drl)

            #p_crit = _WAFODIST.norm.isf(self.alpha / 2.0) * sqrt(numpy.ravel(pvar)) * 1.5
            p_crit = -norm_ppf(self.alpha / 2.0) * sqrt(numpy.ravel(pvar)) * 1.5
            if self.pmin == None:
                self.pmin = p_opt - 5.0 * p_crit
            if self.pmax == None:
                self.pmax = p_opt + 5.0 * p_crit

            N4 = numpy.floor(self.N / 4.0)

            pvec1 = linspace(self.pmin, p_opt - p_crit, N4 + 1)
            pvec2 = linspace(p_opt - p_crit, p_opt + p_crit, self.N - 2 * N4)
            pvec3 = linspace(p_opt + p_crit, self.pmax, N4 + 1)
            pvec = numpy.unique(numpy.hstack((pvec1, p_opt, pvec2, pvec3)))

        else:
            pvec = linspace(self.pmin, self.pmax, self.N)
        return pvec
    def  _myinvfun(self, phatnotfixed):
        mphat = self._par.copy()
        mphat[self.i_notfixed] = phatnotfixed;
        prb = exp(self.logSF)
        return self.fit_dist.dist.isf(prb, *mphat);

    def _myprbfun(self, phatnotfixed):
        mphat = self._par.copy()
        mphat[self.i_notfixed] = phatnotfixed;
        return self.fit_dist.dist.sf(self.x, *mphat)


    def _nlogfun(self, free_par, fix_par):
        ''' Return negative of loglike or logps function

           free_par - vector of free parameters
           fix_par  - fixed parameter, i.e., either quantile (return level),
                      probability (return period) or distribution parameter

        '''
        par = self._par
        par[self.i_free] = free_par
        # _local_link: connects fixed quantile or probability with fixed distribution parameter
        par[self.i_fixed] = self._local_link(fix_par, par)
        return self.fit_dist.fitfun(par)

    def get_CI(self, alpha=0.05):
        '''Return confidence interval
        '''
        if alpha < self.alpha:
            raise ValueError('Unable to return CI with alpha less than %g' % self.alpha)

        cross_level = self.Lmax - 0.5 * chi2isf(alpha, 1) #_WAFODIST.chi2.isf(alpha, 1)
        ind = findcross(self.data, cross_level)
        N = len(ind)
        if N == 0:
            #Warning('upper bound for XXX is larger'
            #Warning('lower bound for XXX is smaller'
            CI = (self.pmin, self.pmax)
        elif N == 1:
            x0 = ecross(self.args, self.data, ind, cross_level)
            isUpcrossing = self.data[ind] > self.data[ind + 1]
            if isUpcrossing:
                CI = (x0, self.pmax)
                #Warning('upper bound for XXX is larger'
            else:
                CI = (self.pmin, x0)
                #Warning('lower bound for XXX is smaller'

        elif N == 2:
            CI = ecross(self.args, self.data, ind, cross_level)
        else:
            # Warning('Number of crossings too large!')
            CI = ecross(self.args, self.data, ind[[0, -1]], cross_level)
        return CI

    def plot(self):
        ''' Plot profile function with 100(1-alpha)% CI
        '''
        plotbackend.plot(self.args, self.data,
            self.args[[0, -1]], [self.Lmax, ]*2, 'r',
            self.args[[0, -1]], [self.alpha_cross_level, ]*2, 'r')
        plotbackend.title(self.title)
        plotbackend.ylabel(self.ylabel)
        plotbackend.xlabel(self.xlabel)

# internal class to fit given distribution to data
class FitDistribution(rv_frozen):
    def __init__(self, dist, data, *args, **kwds):
        extradoc = '''

        RV.plotfitsumry() - Plot various diagnostic plots to asses quality of fit.
        RV.plotecdf()     - Plot Empirical and fitted Cumulative Distribution Function
        RV.plotesf()      - Plot Empirical and fitted Survival Function
        RV.plotepdf()     - Plot Empirical and fitted Probability Distribution Function
        RV.plotresq()     - Displays a residual quantile plot.
        RV.plotresprb()   - Displays a residual probability plot.
    
        RV.profile()      - Return Profile Log- likelihood or Product Spacing-function.
    
        Member variables
        ----------------
        data - data used in fitting
        alpha - confidence coefficient
        method - method used
        LLmax  - loglikelihood function evaluated using par
        LPSmax - log product spacing function evaluated using par
        pvalue - p-value for the fit
        search - True if search for distribution parameters (default)
        copydata - True if copy input data (default)

        par     - parameters (fixed and fitted)
        par_cov - covariance of parameters
        par_fix - fixed parameters
        par_lower - lower (1-alpha)% confidence bound for the parameters
        par_upper - upper (1-alpha)% confidence bound for the parameters

        '''
        self.__doc__ = rv_frozen.__doc__ + extradoc
        self.dist = dist
        numargs = dist.numargs
        
        self.method=self.alpha=self.par_fix=self.search=self.copydata=None
        m_variables = ['method', 'alpha', 'par_fix', 'search', 'copydata']
        m_defaults = ['ml', 0.05, None, True, True]
        for (name, val) in zip(m_variables,m_defaults):
            setattr(self, name, kwds.get(name,val))
            
        #self.method, self.alpha, self.par_fix, self.search, self.copydata = map(kwds.get, m_variables, m_defaults)
        if self.method.lower()[:].startswith('mps'):
            self._fitfun = dist.nlogps
        else:
            self._fitfun = dist.nnlf
        
        self.data = ravel(data)
        if self.copydata:
            self.data = self.data.copy()
        self.data.sort()
        
        par, fixedn = self._fit(*args, **kwds)
        self.par = arr(par)
        somefixed = len(fixedn)>0 
        if somefixed:
            self.par_fix = [nan,]*len(self.par)
            for i in fixedn:
                self.par_fix[i] = self.par[i]
        
            self.i_notfixed = nonzero(1 - isfinite(self.par_fix))
            self.i_fixed = nonzero(isfinite(self.par_fix))

        numpar = numargs + 2
        self.par_cov = zeros((numpar, numpar))
        self._compute_cov()
        
        # Set confidence interval for parameters
        pvar = numpy.diag(self.par_cov)
        zcrit = -norm_ppf(self.alpha / 2.0)
        self.par_lower = self.par - zcrit * sqrt(pvar)
        self.par_upper = self.par + zcrit * sqrt(pvar)
        
        self.LLmax = -dist.nnlf(self.par, self.data)
        self.LPSmax = -dist.nlogps(self.par, self.data)
        self.pvalue = self._pvalue(self.par, self.data, unknown_numpar=numpar)
    
    def _reduce_func(self, args, kwds):
        args = list(args)
        Nargs = len(args) - 2
        fixedn = []
        index = range(Nargs) + [-2, -1]
        names = ['f%d' % n for n in range(Nargs)] + ['floc', 'fscale']
        x0 = args[:]
        for n, key in zip(index, names):
            if kwds.has_key(key):
                fixedn.append(n)
                args[n] = kwds[key]
                del x0[n]
                
        fitfun = self._fitfun
            
        if len(fixedn) == 0:
            func = fitfun
            restore = None
        else:
            if len(fixedn) == len(index):
                raise ValueError, "All parameters fixed. There is nothing to optimize."
            def restore(args, theta):
                # Replace with theta for all numbers not in fixedn
                # This allows the non-fixed values to vary, but
                #  we still call self.nnlf with all parameters.
                i = 0
                for n in range(Nargs):
                    if n not in fixedn:
                        args[n] = theta[i]
                        i += 1
                return args

            def func(theta, x):
                newtheta = restore(args[:], theta)
                return fitfun(newtheta, x)

        return x0, func, restore, args, fixedn
    
    def _fit(self, *args, **kwds):
        
        dist = self.dist
        data = self.data
        
        Narg = len(args)
        if Narg > dist.numargs:
                raise ValueError, "Too many input arguments."
        start = [None]*2
        if (Narg < dist.numargs) or not (kwds.has_key('loc') and
                                         kwds.has_key('scale')):
            start = dist._fitstart(data)  # get distribution specific starting locations
            args += start[Narg:-2]
        loc = kwds.get('loc', start[-2])
        scale = kwds.get('scale', start[-1])
        args += (loc, scale)
        x0, func, restore, args, fixedn = self._reduce_func(args, kwds)
        if self.search:
            optimizer = kwds.get('optimizer', optimize.fmin)
            # convert string to function in scipy.optimize
            if not callable(optimizer) and isinstance(optimizer, (str, unicode)):
                if not optimizer.startswith('fmin_'):
                    optimizer = "fmin_"+optimizer
                if optimizer == 'fmin_': 
                    optimizer = 'fmin'
                try:
                    optimizer = getattr(optimize, optimizer)
                except AttributeError:
                    raise ValueError, "%s is not a valid optimizer" % optimizer
            vals = optimizer(func,x0,args=(ravel(data),),disp=0)
            vals = tuple(vals)
        else:
            vals = tuple(x0)
        if restore is not None:
            vals = restore(args, vals)
        return vals, fixedn
    
    def _compute_cov(self):
        '''Compute covariance
        '''
        somefixed = (self.par_fix != None) and any(isfinite(self.par_fix))
        H = numpy.asmatrix(self.dist.hessian_nnlf(self.par, self.data))
        self.H = H
        try:
            if somefixed:
                allfixed = all(isfinite(self.par_fix))
                if allfixed:
                    self.par_cov[:,:]=0
                else:
                    pcov = -pinv2(H[self.i_notfixed, :][..., self.i_notfixed])
                    for row, ix in enumerate(list(self.i_notfixed)):
                        self.par_cov[ix, self.i_notfixed] = pcov[row, :]
            else:
                self.par_cov = -pinv2(H)
        except:
            self.par_cov[:, :] = nan
            
    def fitfun(self, phat):
        return self._fitfun(phat, self.data)

    def _fxfitfun(self, phat10):
        self.par[self.i_notfixed] = phat10
        return self._fitfun(self.par, self.data)

    def profile(self, **kwds):
        ''' Profile Log- likelihood or Log Product Spacing- function,
            which can be used for constructing confidence interval for
            either phat(i), probability or quantile.

        CALL:  Lp = RV.profile(**kwds)


       RV = object with ML or MPS estimated distribution parameters.
       Parameters
       ----------
       **kwds : named arguments with keys:
          i          - Integer defining which distribution parameter to
                         profile, i.e. which parameter to keep fixed
                         (default index to first non-fixed parameter)
          pmin, pmax - Interval for either the parameter, phat(i), prb, or x,
                        used in the optimization of the profile function (default
                        is based on the 100*(1-alpha)% confidence interval
                        computed using the delta method.)
          N          - Max number of points used in Lp (default 100)
          x          - Quantile (return value)
          logSF       - log survival probability,i.e., R = Prob(X>x;phat)
          link       - function connecting the quantile (x) and the
                         survival probability (R) with the fixed distribution
                         parameter, i.e.: self.par[i] = link(x,logSF,self.par,i),
                         where logSF = log(Prob(X>x;phat)).
                         This means that if:
                          1) x is not None then x is profiled
                          2) logSF is not None then logSF is profiled
                          3) x and logSF both are None then self.par[i] is profiled (default)
          alpha       - confidence coefficent (default 0.05)
       Returns
       --------
         Lp = Profile log-likelihood function with parameters phat given
               the data, phat(i), probability (prb) and quantile (x) (if given), i.e.,
                 Lp = max(log(f(phat|data,phat(i)))),
               or
                 Lp = max(log(f(phat|data,phat(i),x,prb)))

          PROFILE is a utility function for making inferences either on a particular
          component of the vector phat or the quantile, x, or the probability, R.
          This is usually more accurate than using the delta method assuming
          asymptotic normality of the ML estimator or the MPS estimator.


          Examples
          --------
          # MLE and better CI for phat.par[0]
          >>> R = weibull_min.rvs(1,size=100);
          >>> phat = weibull_min.fit(R)
          >>> Lp = phat.profile(i=0)
          >>> Lp.plot()
          >>> Lp.get_CI(alpha=0.1)
          >>> R = 1./990
          >>> x = phat.isf(R)

          # CI for x
          >>> Lx = phat.profile(i=1,x=x,link=phat.dist.link)
          >>> Lx.plot()
          >>> Lx.get_CI(alpha=0.2)

          # CI for logSF=log(SF)
          >>> Lpr = phat.profile(i=1,logSF=log(R),link = phat.dist.link)

          See also
          --------
          Profile
        '''
        if not self.par_fix == None:
            i1 = kwds.setdefault('i', (1 - numpy.isfinite(self.par_fix)).argmax())

        return Profile(self, **kwds)

    def plotfitsumry(self):
        ''' Plot various diagnostic plots to asses the quality of the fit.

        PLOTFITSUMRY displays probability plot, density plot, residual quantile
        plot and residual probability plot.
        The purpose of these plots is to graphically assess whether the data
        could come from the fitted distribution. If so the empirical- CDF and PDF
        should follow the model and the residual plots will be linear. Other
        distribution types will introduce curvature in the residual plots.
        '''
        plotbackend.subplot(2, 2, 1)
        #self.plotecdf()
        self.plotesf()
        plotbackend.subplot(2, 2, 2)
        self.plotepdf()
        plotbackend.subplot(2, 2, 3)
        self.plotresprb()
        plotbackend.subplot(2, 2, 4)
        self.plotresq()
        fixstr = ''
        if not self.par_fix == None:
            numfix = len(self.i_fixed)
            if numfix > 0:
                format = '%d,'*numfix
                format = format[:-1]
                format1 = '%g,'*numfix
                format1 = format1[:-1]
                phatistr = format % tuple(self.i_fixed)
                phatvstr = format1 % tuple(self.par[self.i_fixed])
                fixstr = 'Fixed: phat[%s] = %s ' % (phatistr, phatvstr)


        infostr = 'Fit method: %s, Fit p-value: %2.2f %s' % (self.method, self.pvalue, fixstr)
        try:
            plotbackend.figtext(0.05, 0.01, infostr)
        except:
            pass

    def plotesf(self):
        '''  Plot Empirical and fitted Survival Function

        The purpose of the plot is to graphically assess whether
        the data could come from the fitted distribution.
        If so the empirical CDF should resemble the model CDF.
        Other distribution types will introduce deviations in the plot.
        '''
        n = len(self.data)
        SF = (arange(n, 0, -1)) / n
        plotbackend.semilogy(self.data, SF, 'b.', self.data, self.sf(self.data), 'r-')
        #plotbackend.plot(self.data,SF,'b.',self.data,self.sf(self.data),'r-')

        plotbackend.xlabel('x');
        plotbackend.ylabel('F(x) (%s)' % self.dist.name)
        plotbackend.title('Empirical SF plot')

    def plotecdf(self):
        '''  Plot Empirical and fitted Cumulative Distribution Function

        The purpose of the plot is to graphically assess whether
        the data could come from the fitted distribution.
        If so the empirical CDF should resemble the model CDF.
        Other distribution types will introduce deviations in the plot.
        '''
        n = len(self.data)
        F = (arange(1, n + 1)) / n
        plotbackend.plot(self.data, F, 'b.', self.data, self.cdf(self.data), 'r-')


        plotbackend.xlabel('x');
        plotbackend.ylabel('F(x) (%s)' % self.dist.name)
        plotbackend.title('Empirical CDF plot')

    def plotepdf(self):
        '''Plot Empirical and fitted Probability Density Function

        The purpose of the plot is to graphically assess whether
        the data could come from the fitted distribution.
        If so the histogram should resemble the model density.
        Other distribution types will introduce deviations in the plot.
        '''

        bin, limits = numpy.histogram(self.data, normed=True) #, new=True)
        limits.shape = (-1, 1)
        xx = limits.repeat(3, axis=1)
        xx.shape = (-1,)
        xx = xx[1:-1]
        bin.shape = (-1, 1)
        yy = bin.repeat(3, axis=1)
        #yy[0,0] = 0.0 # pdf
        yy[:, 0] = 0.0 # histogram
        yy.shape = (-1,)
        yy = numpy.hstack((yy, 0.0))

        #plotbackend.hist(self.data,normed=True,fill=False)
        plotbackend.plot(self.data, self.pdf(self.data), 'r-', xx, yy, 'b-')

        plotbackend.xlabel('x');
        plotbackend.ylabel('f(x) (%s)' % self.dist.name)
        plotbackend.title('Density plot')


    def plotresq(self):
        '''PLOTRESQ displays a residual quantile plot.

        The purpose of the plot is to graphically assess whether
        the data could come from the fitted distribution. If so the
        plot will be linear. Other distribution types will introduce
        curvature in the plot.
        '''
        n = len(self.data)
        eprob = (arange(1, n + 1) - 0.5) / n
        y = self.ppf(eprob)
        y1 = self.data[[0, -1]]
        plotbackend.plot(self.data, y, 'b.', y1, y1, 'r-')

        plotbackend.xlabel('Empirical')
        plotbackend.ylabel('Model (%s)' % self.dist.name)
        plotbackend.title('Residual Quantile Plot');
        plotbackend.axis('tight')
        plotbackend.axis('equal')


    def plotresprb(self):
        ''' PLOTRESPRB displays a residual probability plot.

        The purpose of the plot is to graphically assess whether
        the data could come from the fitted distribution. If so the
        plot will be linear. Other distribution types will introduce curvature in the plot.
        '''
        n = len(self.data);
        #ecdf = (0.5:n-0.5)/n;
        ecdf = arange(1, n + 1) / (n + 1)
        mcdf = self.cdf(self.data)
        p1 = [0, 1]
        plotbackend.plot(ecdf, mcdf, 'b.', p1, p1, 'r-')


        plotbackend.xlabel('Empirical')
        plotbackend.ylabel('Model (%s)' % self.dist.name)
        plotbackend.title('Residual Probability Plot');
        plotbackend.axis([0, 1, 0, 1])
        plotbackend.axis('equal')



    def _pvalue(self, theta, x, unknown_numpar=None):
        ''' Return the P-value for the fit using Moran's negative log Product Spacings statistic

            where theta are the parameters (including loc and scale)

            Note: the data in x must be sorted
        '''
        dx = numpy.diff(x, axis=0)
        tie = (dx == 0)
        if any(tie):
            print('P-value is on the conservative side (i.e. too large) due to ties in the data!')

        T = self.dist.nlogps(theta, x)

        n = len(x)
        np1 = n + 1
        if unknown_numpar == None:
            k = len(theta)
        else:
            k = unknown_numpar

        isParUnKnown = True
        m = (np1) * (log(np1) + 0.57722) - 0.5 - 1.0 / (12. * (np1))
        v = (np1) * (pi ** 2. / 6.0 - 1.0) - 0.5 - 1.0 / (6. * (np1))
        C1 = m - sqrt(0.5 * n * v)
        C2 = sqrt(v / (2.0 * n))
        Tn = (T + 0.5 * k * isParUnKnown - C1) / C2 # chi2 with n degrees of freedom
        pvalue = chi2sf(Tn, n) #_WAFODIST.chi2.sf(Tn, n)
        return pvalue


 

def main():
    pass
#    _WAFODIST = ppimport('wafo.stats.distributions')
#     #nbinom(10, 0.75).rvs(3)
#    import matplotlib
#    matplotlib.interactive(True)
#    t = _WAFODIST.bernoulli(0.75).rvs(3)
#    x = np.r_[5, 10]
#    npr = np.r_[9, 9]
#    t2 = _WAFODIST.bd0(x, npr)
#    #Examples   MLE and better CI for phat.par[0]
#    R = _WAFODIST.weibull_min.rvs(1, size=100);
#    phat = _WAFODIST.weibull_min.fit(R, 1, 1, par_fix=[nan, 0, nan])
#    Lp = phat.profile(i=0)
#    Lp.plot()
#    Lp.get_CI(alpha=0.1)
#    R = 1. / 990
#    x = phat.isf(R)
#
#    # CI for x
#    Lx = phat.profile(i=0, x=x)
#    Lx.plot()
#    Lx.get_CI(alpha=0.2)
#
#    # CI for logSF=log(SF)
#    Lpr = phat.profile(i=0, logSF=log(R), link=phat.dist.link)
#    Lpr.plot()
#    Lpr.get_CI(alpha=0.075)
#
#    _WAFODIST.dlaplace.stats(0.8, loc=0)
##    pass
#    t = _WAFODIST.planck(0.51000000000000001)
#    t.ppf(0.5)
#    t = _WAFODIST.zipf(2)
#    t.ppf(0.5)
#    import pylab as plb
#    _WAFODIST.rice.rvs(1)
#    x = plb.linspace(-5, 5)
#    y = _WAFODIST.genpareto.cdf(x, 0)
#    #plb.plot(x,y)
#    #plb.show()
#
#
#    on = ones((2, 3))
#    r = _WAFODIST.genpareto.rvs(0, size=100)
#    pht = _WAFODIST.genpareto.fit(r, 1, par_fix=[0, 0, nan])
#    lp = pht.profile()
                
if __name__ == '__main__':
   main()