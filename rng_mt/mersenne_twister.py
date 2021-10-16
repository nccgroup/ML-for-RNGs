
class MersenneTwister():
    # Create a length n array to store the state of the generator
    def __init__(self, bits=32):
        if bits==32:
            (self.w, self.n, self.m, self.r) = (32, 624, 397, 31)
            self.a = 0x9908B0DF
            (self.u, self.d) = (11, 0xFFFFFFFF)
            (self.s, self.b) = (7, 0x9D2C5680)
            (self.t, self.c) = (15, 0xEFC60000)
            self.l = 18
            self.f = 1812433253
        else:
            (self.w, self.n, self.m, self.r) = (64, 312, 156, 31)
            self.a = 0xB5026F5AA96619E9
            (self.u, self.d) = (29, 0x5555555555555555)
            (self.s, self.b) = (17, 0x71D67FFFEDA60000)
            (self.t, self.c) = (37, 0xFFF7EEE000000000)
            self.l = 43
            self.f = 6364136223846793005
        
        self.MT = self.n * [0]
        self.index = self.n + 1

        # That is, the binary number of r 1's
        self.mask = (1 << self.w) - 1
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = self.mask & ~self.lower_mask
    
    ## Initialize the generator from a seed
    def seed_mt(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n): ## loop over each element
            self.MT[i] = self.mask & (self.f * (self.MT[i-1] ^ (self.MT[i-1] >> (self.w-2))) + i)
    
    ## Extract a tempered value based on MT[index]
    ## calling twist() every n numbers
    def extract_number(self):
        if self.index >= self.n:
            if self.index > self.n:
#                 raise Exception("Generator was never seeded")
                self.seed_mt(5489)
                ## Alternatively, seed with constant value; 5489 is used in reference C code[53]
            self.twist()

        y = self.MT[self.index]
        y = self.xorshifter(y)
    
        self.index += 1
        return self.mask & y
    
    def xorshifter(self, y):
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        return y

    def extract_state(self):
        if self.index >= self.n:
            if self.index > self.n:
#                 raise Exception("Generator was never seeded")
                self.seed_mt(5489)
                ## Alternatively, seed with constant value; 5489 is used in reference C code[53]
            self.twist()

        y = self.MT[self.index]
        self.index += 1
        return self.mask & y

    
    
    
    ## Generate the next n values from the series x_i 
    def twist(self):
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i+1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x%2 != 0: ## lowest bit of x is 1
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0