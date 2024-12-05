# adventofcode2024

## Intro
Just another repo of a white straight guy trying to solve  advent of code for 24 days straight.

## Journal
### Day 1
Easy peasy, but I had to redefine numpy's "fromstring" as the documentation looked unclear and it was easier to redo than debug.

On a second thought, implementing everything as a class would have been easier to keep the intermediate outputs, but the solution is clean enough to me.
TBH I'm not sure I'll keep such nice docstring also for future solutions, today is a Sunday, tomorrow I'll do that during lunch break.

### Day 2
This was easy, again had to redefine the parsing. 
I made two mistakes here:
1) I assumed each report was supposed to have the same number of levels and wrote a first version of parsing under that assumption
2) I did not even notice I was assuming that, until the function broke. Little reminder: always take a moment to look at the data.

As expected, docstrings are gone but function names are readable enough

### Day3
Dear future me, please don't judge my parse function.

### Day4
Finished during night, as I had a short lunch break. Curiously, second quiz looked easier than the first one.
For the first quiz I'm not sure I took the easiest path: instead of looking for "XMAS" strings directly, I first looked for all the possible substrings.

### Day5
I was almost going to create a topological sorting algorithm, but luckily I remembered "topological sorting" is a thing and found out Python has a library to solve it. Code is architecturally wrong but I have dinner out tonight so little time to refine it.

TODO for me, study again sets (I too often use dictionaries instead) and graphs.


## Who am I
My name is Michele Buccoli, I am not a developer. My job is not coding, but it involves coding. Actually, as a senior scientist at BdSound, my job involves reviewing other people's code (poteto potato tometo tomato).
You can learn other info on myself and contact me through my website mbuccoli.github.io .
