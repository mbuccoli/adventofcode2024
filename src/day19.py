# I will start with this day for an attempt to make my way to the leaderboard (a private one)
# So solving MOST recent problems is more likely to give me more points

# now the stripes.
# Patterns
# r, wr, b, g, bwu, rb, gb, br
# Designs
# brwrr
# bggr
# gbbr
# rrbgbr
# ubwu
# bwurrg
# brgr
# bbrgwb

# So, maybe first I can simplify my problem by using a list of symbols (patterns) that are unique.
# E.g., why keeping rb and gb and br if I can use b, r, and g to use them? 
# (this actually means to solve the same problem across substring, not easy!)
# a dummy way is to start with smaller symbols and then compose it to form complex and complex symbols and remove them from patterns
# b, r, g are 1 letter, so I check bb, rr, gg, br, rb, bg, gb, gr, rg, and remove what I find.
# Now I compose any two letter symbols with the 1 letter and see what happens.
# etc.


# Patterns
# r, wr, b, g, bwu, 
# now is much easier! I have 5 symbols! 
# Now, for each design, I'll only consider the patterns that are its substrings. 

# brwrr --> r, wr, b
# bggr --> b,g,r
# gbbr ->  b, g, r
# rrbgbr -> r, b, g
# ubwu -> bwu, 
# bwurrg -> bwu, r, g
# brgr -> b,r,g
# bbrgwb -> b,r, g

# First thing first: in the design, is there any letter that is not covered by a substring? well, yes, let's show it in capital letter
# brwrr --> r, wr, b
# bggr --> b,g,r
# gbbr ->  b, g, r
# rrbgbr -> r, b, g
# Ubwu -> bwu,  --> IMPOSSIBLE
# bwurrg -> bwu, r, g  
# brgr -> b,r,g
# bbrgWb -> b,r, g --> IMPOSSIBLE

# Now, this is how we can solve the example, but possibly not the entire exercize.
# Suppose we have patterns bw wu and design bwu.
# While bw and wu BOTH belong to the design, there is NO WAY I can have them.
# I can exploit, however, the length of the design and the length of the "possible" symbols
# if len(bwu) = 3, I need to find ONLY combinations of 3*1, or 1+2, or 2+1, or 3. I can't use 2+2
# how can I find it?
# well, I can say
# D (len of design)
# P (len of patterns) = [P1, P2, P3, ... P]<D
# to find combinations of D, I start by looking recursively or iteratively combinations of D-P1, D-P2, etc.
# where I can't find it, I remove the sequence all toghether 

# ok, now let's be also smarter, what this stuff looks like? It looks like CODING. 
# Can I code a design with symbols? 

# I can try to divide and conquer by counting for each letter of the design how many patterns apply.
# Let's start with those that appears the least, because THOSE will simplify my problem.
# ok D D D D D D D
#    4 5 3 1 2 4 3
# hey, there is a D that only appears once. let's split and now look for all possible combinations of the substrings.
# (does it look easy?, well, recursively it may work!)

# (what is the brute force? check ALL the possible combinations and remove the design that shows it, until just few nonpossible designs remain)