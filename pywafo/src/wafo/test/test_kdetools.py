'''
Created on 20. nov. 2010

@author: pab
'''

import numpy as np
from numpy import array
import wafo.kdetools as wk
#import pylab as plb

def test0_KDE1D():
    '''
    >>> data = array([ 0.75355792,  0.72779194,  0.94149169,  0.07841119,  2.32291887,
    ...        1.10419995,  0.77055114,  0.60288273,  1.36883635,  1.74754326,
    ...        1.09547561,  1.01671133,  0.73211143,  0.61891719,  0.75903487,
    ...        1.8919469 ,  0.72433808,  1.92973094,  0.44749838,  1.36508452])

    >>> x = np.linspace(0, max(data.ravel()) + 1, 10) 
    >>> import wafo.kdetools as wk 
    >>> kde = wk.KDE(data, hs=0.5, alpha=0.5)
   
    >>> kde0 = wk.KDE(data, hs=0.5, alpha=0.0, inc=16)
    
    >>> kde0.eval_grid(x)
    array([ 0.2039735 ,  0.40252503,  0.54595078,  0.52219649,  0.3906213 ,
            0.26381501,  0.16407362,  0.08270612,  0.02991145,  0.00720821])
    >>> kde0.eval_grid_fast(x)
    array([ 0.20729484,  0.39865044,  0.53716945,  0.5169322 ,  0.39060223,
            0.26441126,  0.16388801,  0.08388527,  0.03227164,  0.00883579])
            
    >>> f = kde0.eval_grid_fast(); f
    array([ 0.01149411,  0.03485467,  0.08799292,  0.18568718,  0.32473136,
            0.46543163,  0.54532016,  0.53005828,  0.44447651,  0.34119612,
            0.25103852,  0.1754952 ,  0.11072989,  0.05992731,  0.02687784,
            0.00974983])
    >>> np.trapz(f,kde0.args)
    array([ 0.99500101])
    '''
def test1_TKDE1D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(N,))
    >>> data = array([ 0.75355792,  0.72779194,  0.94149169,  0.07841119,  2.32291887,
    ...        1.10419995,  0.77055114,  0.60288273,  1.36883635,  1.74754326,
    ...        1.09547561,  1.01671133,  0.73211143,  0.61891719,  0.75903487,
    ...        1.8919469 ,  0.72433808,  1.92973094,  0.44749838,  1.36508452])
    
    >>> x = np.linspace(0.01, max(data.ravel()) + 1, 10)  
    >>> kde = wk.TKDE(data, hs=0.5, L2=0.5)
    >>> f = kde(x)
    >>> f
    array([ 1.03982714,  0.45839018,  0.39514782,  0.32860602,  0.26433318,
            0.20717946,  0.15907684,  0.1201074 ,  0.08941027,  0.06574882])
               
    >>> np.trapz(f, x)
    0.94787730659349068
    
    h1 = plb.plot(x, f) #  1D probability density plot
    '''
def test1_KDE1D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(N,))
    >>> data = array([ 0.75355792,  0.72779194,  0.94149169,  0.07841119,  2.32291887,
    ...        1.10419995,  0.77055114,  0.60288273,  1.36883635,  1.74754326,
    ...        1.09547561,  1.01671133,  0.73211143,  0.61891719,  0.75903487,
    ...        1.8919469 ,  0.72433808,  1.92973094,  0.44749838,  1.36508452])
    
    >>> x = np.linspace(0, max(data.ravel()) + 1, 10)  
    >>> kde = wk.KDE(data, hs=0.5)
    >>> f = kde(x)
    >>> f
    array([ 0.2039735 ,  0.40252503,  0.54595078,  0.52219649,  0.3906213 ,
            0.26381501,  0.16407362,  0.08270612,  0.02991145,  0.00720821])
               
    >>> np.trapz(f, x)
    0.92576174424281876
    
    h1 = plb.plot(x, f) #  1D probability density plot
    '''
def test2_KDE1D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(N,))
    >>> data = array([ 0.75355792,  0.72779194,  0.94149169,  0.07841119,  2.32291887,
    ...        1.10419995,  0.77055114,  0.60288273,  1.36883635,  1.74754326,
    ...        1.09547561,  1.01671133,  0.73211143,  0.61891719,  0.75903487,
    ...        1.8919469 ,  0.72433808,  1.92973094,  0.44749838,  1.36508452])
    
    >>> data = np.asarray([1,2])
    >>> x = np.linspace(0, max(data.ravel()) + 1, 10)  
    >>> kde = wk.KDE(data, hs=0.5)
    >>> f = kde(x)
    >>> f
    array([ 0.0541248 ,  0.16555235,  0.33084399,  0.45293325,  0.48345808,
            0.48345808,  0.45293325,  0.33084399,  0.16555235,  0.0541248 ])
             
    >>> np.trapz(f, x)
    0.97323338046725172
     
    h1 = plb.plot(x, f) #  1D probability density plot
    
    '''

def test1a_KDE1D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(N,))
    >>> data = array([ 0.75355792,  0.72779194,  0.94149169,  0.07841119,  2.32291887,
    ...        1.10419995,  0.77055114,  0.60288273,  1.36883635,  1.74754326,
    ...        1.09547561,  1.01671133,  0.73211143,  0.61891719,  0.75903487,
    ...        1.8919469 ,  0.72433808,  1.92973094,  0.44749838,  1.36508452])
    
    >>> x = np.linspace(0, max(data.ravel()) + 1, 10)  
    >>> kde = wk.KDE(data, hs=0.5, alpha=0.5)
    >>> f = kde(x)
    >>> f
    array([ 0.17252055,  0.41014271,  0.61349072,  0.57023834,  0.37198073,
            0.21409279,  0.12738463,  0.07460326,  0.03956191,  0.01887164])
            
    >>> np.trapz(f, x)
    0.92938023659047952
     
    h1 = plb.plot(x, f) #  1D probability density plot
   
    '''
def test2a_KDE1D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(N,))
    >>> data = array([ 0.75355792,  0.72779194,  0.94149169,  0.07841119,  2.32291887,
    ...        1.10419995,  0.77055114,  0.60288273,  1.36883635,  1.74754326,
    ...        1.09547561,  1.01671133,  0.73211143,  0.61891719,  0.75903487,
    ...        1.8919469 ,  0.72433808,  1.92973094,  0.44749838,  1.36508452])
    
    >>> data = np.asarray([1,2])
    >>> x = np.linspace(0, max(data.ravel()) + 1, 10)  
    >>> kde = wk.KDE(data, hs=0.5, alpha=0.5)
    >>> f = kde(x)
    >>> f
    array([ 0.0541248 ,  0.16555235,  0.33084399,  0.45293325,  0.48345808,
            0.48345808,  0.45293325,  0.33084399,  0.16555235,  0.0541248 ])
       
    >>> np.trapz(f, x)
    0.97323338046725172
           
    h1 = plb.plot(x, f) #  1D probability density plot
    '''

def test_KDE2D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(2, N))
    >>> data = array([[ 0.38103275,  0.35083136,  0.90024207,  1.88230239,  0.96815399,
    ...         0.57392873,  1.63367908,  1.20944125,  2.03887811,  0.81789145,
    ...         0.69302049,  1.40856592,  0.92156032,  2.14791432,  2.04373821,
    ...         0.69800708,  0.58428735,  1.59128776,  2.05771405,  0.87021964],
    ...       [ 1.44080694,  0.39973751,  1.331243  ,  2.48895822,  1.18894158,
    ...         1.40526085,  1.01967897,  0.81196474,  1.37978932,  2.03334689,
    ...         0.870329  ,  1.25106862,  0.5346619 ,  0.47541236,  1.51930093,
    ...         0.58861519,  1.19780448,  0.81548296,  1.56859488,  1.60653533]])
             
    >>> x = np.linspace(0, max(data.ravel()) + 1, 3)
    
    >>> kde = wk.KDE(data, hs=0.5, alpha=0.5)
   
    >>> kde0 = wk.KDE(data, hs=0.5, alpha=0.0, inc=16)
    
    >>> kde0.eval_grid(x, x)
    array([[  3.27260963e-02,   4.21654678e-02,   5.85338634e-04],
           [  6.78845466e-02,   1.42195839e-01,   1.41676003e-03],
           [  1.39466746e-04,   4.26983850e-03,   2.52736185e-05]])
    >>> kde0.eval_grid_fast(x, x)  
    array([[ 0.04435061,  0.06433531,  0.00413538],
           [ 0.07218297,  0.12358196,  0.00928889],
           [ 0.00161333,  0.00794858,  0.00058748]])

    '''
    
def test_smooth_params():
    '''
    >>> data = np.array([[ 0.932896  ,  0.89522635,  0.80636346,  1.32283371,  0.27125435,
    ...         1.91666304,  2.30736635,  1.13662384,  1.73071287,  1.06061127,
    ...         0.99598512,  2.16396591,  1.23458213,  1.12406686,  1.16930431,
    ...         0.73700592,  1.21135139,  0.46671506,  1.3530304 ,  0.91419104],
    ...       [ 0.62759088,  0.23988169,  2.04909823,  0.93766571,  1.19343762,
    ...         1.94954931,  0.84687514,  0.49284897,  1.05066204,  1.89088505,
    ...         0.840738  ,  1.02901457,  1.0758625 ,  1.76357967,  0.45792897,
    ...         1.54488066,  0.17644313,  1.6798871 ,  0.72583514,  2.22087245],
    ...       [ 1.69496432,  0.81791905,  0.82534709,  0.71642389,  0.89294732,
    ...         1.66888649,  0.69036947,  0.99961448,  0.30657267,  0.98798713,
    ...         0.83298728,  1.83334948,  1.90144186,  1.25781913,  0.07122458,
    ...         2.42340852,  2.41342037,  0.87233305,  1.17537114,  1.69505988]])
                
    >>> gauss = wk.Kernel('gaussian')
    >>> gauss.hns(data)
    array([ 0.18154437,  0.36207987,  0.37396219])
    >>> gauss.hos(data)
    array([ 0.195209  ,  0.3893332 ,  0.40210988])
    >>> gauss.hmns(data)
    array([[  3.25196193e-01,  -2.68892467e-02,   3.18932448e-04],
           [ -2.68892467e-02,   3.91283306e-01,   2.38654678e-02],
           [  3.18932448e-04,   2.38654678e-02,   4.05123874e-01]])
    >>> gauss.hscv(data)
    array([ 0.16858959,  0.32739383,  0.3046287 ])
    
    >>> gauss.hstt(data)
    array([ 0.18099075,  0.50409881,  0.11018912])
    
    >>> gauss.hste(data)
    array([ 0.16750009,  0.29059113,  0.17994255])
    
    >>> gauss.hldpi(data)
    array([ 0.1732289 ,  0.33159097,  0.3107633 ])
    
    
    >>> gauss.hisj(data)
    array([ 0.24222479,  0.74277133,  0.15492661])
    
    >>> data = np.array([0.753557920000000, 0.727791940000000,   0.941491690000000,
    ...   0.078411190000000,   2.322918870000000,   1.104199950000000,   0.770551140000000,
    ...   0.602882730000000,       1.368836350000000,       1.747543260000000,       1.095475610000000,
    ...   1.016711330000000,       0.732111430000000,       0.618917190000000,       0.759034870000000,
    ...   1.891946900000000,   0.724338080000000,   1.929730940000000,   0.447498380000000,   1.365084520000000])
   
    '''
def test_gridcount_1D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(N,))
    >>> data = array([ 0.75355792,  0.72779194,  0.94149169,  0.07841119,  2.32291887,
    ...        1.10419995,  0.77055114,  0.60288273,  1.36883635,  1.74754326,
    ...        1.09547561,  1.01671133,  0.73211143,  0.61891719,  0.75903487,
    ...        1.8919469 ,  0.72433808,  1.92973094,  0.44749838,  1.36508452])
    
    >>> x = np.linspace(0, max(data.ravel()) + 1, 10)  
    >>> dx = x[1] - x[0]  
    >>> c = wk.gridcount(data, x)
    >>> c 
    array([ 0.78762626,  1.77520717,  7.99190087,  4.04054449,  1.67156643,
            2.38228499,  1.05933195,  0.29153785,  0.        ,  0.        ])
            
    h = plb.plot(x, c, '.')   # 1D histogram
   
    h1 = plb.plot(x, c / dx / N) #  1D probability density plot
    t = np.trapz(c / dx / N, x)   
    print(t)
    '''

def test_gridcount_2D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(2, N))
    >>> data = array([[ 0.38103275,  0.35083136,  0.90024207,  1.88230239,  0.96815399,
    ...         0.57392873,  1.63367908,  1.20944125,  2.03887811,  0.81789145,
    ...         0.69302049,  1.40856592,  0.92156032,  2.14791432,  2.04373821,
    ...         0.69800708,  0.58428735,  1.59128776,  2.05771405,  0.87021964],
    ...       [ 1.44080694,  0.39973751,  1.331243  ,  2.48895822,  1.18894158,
    ...         1.40526085,  1.01967897,  0.81196474,  1.37978932,  2.03334689,
    ...         0.870329  ,  1.25106862,  0.5346619 ,  0.47541236,  1.51930093,
    ...         0.58861519,  1.19780448,  0.81548296,  1.56859488,  1.60653533]])
             
    >>> x = np.linspace(0, max(data.ravel()) + 1, 5)  
    >>> dx = x[1] - x[0]
    >>> X = np.vstack((x, x))   
    >>> c = wk.gridcount(data, X)
    >>> c 
    array([[ 0.38922806,  0.8987982 ,  0.34676493,  0.21042807,  0.        ],
           [ 1.15012203,  5.16513541,  3.19250588,  0.55420752,  0.        ],
           [ 0.74293418,  3.42517219,  1.97923195,  0.76076621,  0.        ],
           [ 0.02063536,  0.31054405,  0.71865964,  0.13486633,  0.        ],
           [ 0.        ,  0.        ,  0.        ,  0.        ,  0.        ]])
    
    h = plb.plot(x, c, '.')   # 1D histogram
   
    h1 = plb.plot(x, c / dx / N) #  1D probability density plot
    t = np.trapz(c / dx / N, x)   
    print(t)
    '''
def test_gridcount_3D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(3, N))
    >>> data = np.array([[ 0.932896  ,  0.89522635,  0.80636346,  1.32283371,  0.27125435,
    ...         1.91666304,  2.30736635,  1.13662384,  1.73071287,  1.06061127,
    ...         0.99598512,  2.16396591,  1.23458213,  1.12406686,  1.16930431,
    ...         0.73700592,  1.21135139,  0.46671506,  1.3530304 ,  0.91419104],
    ...       [ 0.62759088,  0.23988169,  2.04909823,  0.93766571,  1.19343762,
    ...         1.94954931,  0.84687514,  0.49284897,  1.05066204,  1.89088505,
    ...         0.840738  ,  1.02901457,  1.0758625 ,  1.76357967,  0.45792897,
    ...         1.54488066,  0.17644313,  1.6798871 ,  0.72583514,  2.22087245],
    ...       [ 1.69496432,  0.81791905,  0.82534709,  0.71642389,  0.89294732,
    ...         1.66888649,  0.69036947,  0.99961448,  0.30657267,  0.98798713,
    ...         0.83298728,  1.83334948,  1.90144186,  1.25781913,  0.07122458,
    ...         2.42340852,  2.41342037,  0.87233305,  1.17537114,  1.69505988]])
             
    >>> x = np.linspace(0, max(data.ravel()) + 1, 3)  
    >>> dx = x[1] - x[0]
    >>> X = np.vstack((x, x, x))   
    >>> c = wk.gridcount(data, X)
    >>> c 
    array([[[  8.74229894e-01,   1.27910940e+00,   1.42033973e-01],
            [  1.94778915e+00,   2.59536282e+00,   3.28213680e-01],
            [  1.08429416e-01,   1.69571495e-01,   7.48896775e-03]],
    <BLANKLINE>
           [[  1.44969128e+00,   2.58396370e+00,   2.45459949e-01],
            [  2.28951650e+00,   4.49653348e+00,   2.73167915e-01],
            [  1.10905565e-01,   3.18733817e-01,   1.12880816e-02]],
    <BLANKLINE>
           [[  7.49265424e-02,   2.18142488e-01,   0.00000000e+00],
            [  8.53886762e-02,   3.73415131e-01,   0.00000000e+00],
            [  4.16196568e-04,   1.62218824e-02,   0.00000000e+00]]])
            
    '''
def test_gridcount_4D():
    '''
    N = 20
    data = np.random.rayleigh(1, size=(2, N))
    >>> data = array([[ 0.38103275,  0.35083136,  0.90024207,  1.88230239,  0.96815399,
    ...         0.57392873,  1.63367908,  1.20944125,  2.03887811,  0.81789145],
    ...       [ 0.69302049,  1.40856592,  0.92156032,  2.14791432,  2.04373821,
    ...         0.69800708,  0.58428735,  1.59128776,  2.05771405,  0.87021964],
    ...       [ 1.44080694,  0.39973751,  1.331243  ,  2.48895822,  1.18894158,
    ...         1.40526085,  1.01967897,  0.81196474,  1.37978932,  2.03334689],
    ...       [ 0.870329  ,  1.25106862,  0.5346619 ,  0.47541236,  1.51930093,
    ...         0.58861519,  1.19780448,  0.81548296,  1.56859488,  1.60653533]])
             
    >>> x = np.linspace(0, max(data.ravel()) + 1, 3)  
    >>> dx = x[1] - x[0]
    >>> X = np.vstack((x, x, x, x))   
    >>> c = wk.gridcount(data, X)
    >>> c 
    array([[[[  1.77163904e-01,   1.87720108e-01,   0.00000000e+00],
             [  5.72573585e-01,   6.09557834e-01,   0.00000000e+00],
             [  3.48549923e-03,   4.05931870e-02,   0.00000000e+00]],
    <BLANKLINE>
            [[  1.83770124e-01,   2.56357594e-01,   0.00000000e+00],
             [  4.35845892e-01,   6.14958970e-01,   0.00000000e+00],
             [  3.07662204e-03,   3.58312786e-02,   0.00000000e+00]],
    <BLANKLINE>
            [[  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
             [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00],
             [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00]]],
    <BLANKLINE>
    <BLANKLINE>
           [[[  3.41883175e-01,   5.97977973e-01,   0.00000000e+00],
             [  5.72071865e-01,   8.58566538e-01,   0.00000000e+00],
             [  3.46939323e-03,   4.04056116e-02,   0.00000000e+00]],
    <BLANKLINE>
            [[  3.58861043e-01,   6.28962785e-01,   0.00000000e+00],
             [  8.80697705e-01,   1.47373158e+00,   0.00000000e+00],
             [  2.22868504e-01,   1.18008528e-01,   0.00000000e+00]],
    <BLANKLINE>
            [[  2.91835067e-03,   2.60268355e-02,   0.00000000e+00],
             [  3.63686503e-02,   1.07959459e-01,   0.00000000e+00],
             [  1.88555613e-02,   7.06358976e-03,   0.00000000e+00]]],
    <BLANKLINE>
    <BLANKLINE>
           [[[  3.13810608e-03,   2.11731327e-02,   0.00000000e+00],
             [  6.71606255e-03,   4.53139824e-02,   0.00000000e+00],
             [  0.00000000e+00,   0.00000000e+00,   0.00000000e+00]],
    <BLANKLINE>
            [[  7.05946179e-03,   5.44614852e-02,   0.00000000e+00],
             [  1.09099593e-01,   1.95935584e-01,   0.00000000e+00],
             [  6.61257395e-02,   2.47717418e-02,   0.00000000e+00]],
    <BLANKLINE>
            [[  6.38695629e-04,   5.69610302e-03,   0.00000000e+00],
             [  1.00358265e-02,   2.44053065e-02,   0.00000000e+00],
             [  5.67244468e-03,   2.12498697e-03,   0.00000000e+00]]]])
    
    h = plb.plot(x, c, '.')   # 1D histogram
   
    h1 = plb.plot(x, c / dx / N) #  1D probability density plot
    t = np.trapz(x, c / dx / N)   
    print(t)
    '''
    
def test_docstrings():
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    test_docstrings()