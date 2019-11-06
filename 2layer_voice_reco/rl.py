########################################################## README ###########################################################

# This file implements STDP curve and weight update rule

##############################################################################################################################



import cupy as cp
from matplotlib import pyplot as plt
from parameters import param as par

#STDP reinforcement learning curve
def rl(t):
    """
    スパイク間隔の時間

    Parameters
    ----------
    t : int
            発火していた時刻

    Returns
    ------
    : float
            一般的なSTDP機能で得られる値
    """
    #back time
    if t > 0:
        return -par.kNegativeReinforcement_ * cp.exp(-float(t) / par.kNegativeTau_)
    #fore time
    if t <= 0:
        return par.kPositiveReinforcement_ * cp.exp(float(t) / par.kPositiveTau_)


#STDP weight update rule
def update(w, del_w):
    """
    STDP則に基づく重みの更新

    Parameters
    ----------
    w : float
            更新が行われるシナプスの値
    del_w : float
            SDTPによって導き出された値

    Returns
    ------
    : 新しく更新される値
    """
    if del_w < 0:
        return w + par.kSigma_ * del_w * (w - abs(par.kMinWait_)) * par.kScale_
    elif del_w > 0:
        return w + par.kSigma_ * del_w * (par.kMaxWait_ - w) * par.kScale_

if __name__ == '__main__':

    print(rl(-20) * par.kSigma_)
