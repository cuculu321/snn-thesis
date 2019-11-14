########################################################## README ###########################################################

# This file implements STDP curve and weight update rule

##############################################################################################################################



import cupy as cp
from matplotlib import pyplot as plt
from parameters import param as par

#STDP reinforcement learning curve
def back_rl(t):
    """
    スパイク間隔の時間(時差)

    Parameters
    ----------
    t : int
            発火していた時刻

    Returns
    ------
    : float
            時差
    """
    #back time
    return par.kPositiveReinforcement_ * cp.exp(float(t) / par.kPositiveTau_)

def fore_rl(t):
    #fore time
    return -par.kNegativeReinforcement_ * cp.exp(-float(t) / par.kNegativeTau_)


#STDP weight update rule
def positive_update(w, del_w):
    """
    STDP則に基づく重みの更新

    Parameters
    ----------
    w : float
            更新が行われるシナプスの値
    del_w : float
            スパイクの時差

    Returns
    ------
    : 新しく更新される値
    """
    #時差が負、foretime
    return w + par.kSigma_ * del_w * (w - abs(par.kMinWait_)) * par.kScale_

def negative_update(w, del_w):
    #時差が正、backtime
    return w + par.kSigma_ * del_w * (par.kMaxWait_ - w) * par.kScale_


if __name__ == '__main__':

    print(back_rl(-20) * par.kSigma_)
