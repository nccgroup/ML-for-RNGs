import numpy as np
from mersenne_twister import MersenneTwister

def main():
    n = 6000000
    mt = MersenneTwister()
    vxorshifter = np.vectorize(mt.xorshifter)
    states = np.array([mt.extract_state() for i in range(n)])
    mt_randoms = vxorshifter(states)
    
    with open('mersenne_twist_states.txt', 'w') as f:
        for item in states:
            f.write("%s\n" % item)

    with open('mersenne_twist_xorshifter.txt', 'w') as f:
        for i in range(n):
            f.write("%s, %s\n" % (mt_randoms[i], states[i]))

if __name__ == '__main__':
    main()