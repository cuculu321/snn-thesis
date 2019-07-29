########################################################## README ###########################################################

# This file implements STDP curve and weight update rule

##############################################################################################################################



import numpy as np
from matplotlib import pyplot as plt
from parameters import param as par

#STDP reinforcement learning curve
def rl(t):
	#back time
	if t > 0:
		return -par.kNegativeReinforcement_ * np.exp(-float(t) / par.kNegativeTau_)
	#fore time
	if t <= 0:
		return par.kPositiveReinforcement_ * np.exp(float(t) / par.kPositiveTau_)


#STDP weight update rule
def update(w, del_w):
	if del_w < 0:
		return w + par.kSigma_ * del_w * (w - abs(par.kMinWait_)) * par.kScale_
	elif del_w > 0:
		return w + par.kSigma_ * del_w * (par.kMaxWait_ - w) * par.kScale_

if __name__ == '__main__':
	
	print(rl(-20) * par.kSigma_)

	