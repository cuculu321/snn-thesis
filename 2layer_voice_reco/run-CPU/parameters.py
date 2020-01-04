################################################ README #########################################################

# This file contains all the parameters of the network.

#################################################################################################################

class param:
	kScale_ = 1
	kTime_ = 200
	kTimeBack_ = -20
	kTimeFore_ = 20

	kPixelX_ = 28
	kPrest_ = 0
	kFirstLayerNuerons_ = 22 #Number of neurons in first layer
	kSecondLayerNuerons_ =  100  #Number of neurons in second layer
	kMinPotential_ = -500 * kScale_
	# Pth = 5
	# D = 0.7
	kMaxWait_ = 1.5 * kScale_
	kMinWait_ = -1.2 * kScale_
	kSigma_ = 0.1 #0.02
	kNegativeReinforcement_ = 0.8  # time difference is positive i.e negative reinforcement
	kPositiveReinforcement_ = 0.3 # 0.01 # time difference is negative i.e positive reinforcement 
	kNegativeTau_ = 8 #tau is 'τ:時定数'
	kPositiveTau_ = 5
	
	kEpoch_ = 12
	
	kMelChannelCount_ = 22  # メルフィルタバンクのチャネル数

#-- No use constant
	#fr_bits = 12
	#int_bits = 12