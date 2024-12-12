# adventofcode2024

## Intro
Just another random guy trying to solve advent of code for 24 days straight.

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

### Day6
For the second quiz I probably chose a bruter force solution than needed, which takes a lot. I'm very curious to know what could be a better way to solve it.

### Day7
Oops I did it again, jump on the solution before better reading the instructions. This is a common mistake: who has the time for reading the instructions?
Turned out if I had taken the time, I would not have spent a lot of time trying a wrong and very elaborate solution.

### Day 8
This was easier to solve than to understand. 

### Day 9
Quiz 1 was solved quick&dirt, Quiz 2 took more effort and runs greatly faster.
Fun fact: I was commenting the quiz with a colleague and we joked about the first quiz was about "fragmenting" the disk. 

### Day 10
Nice solution, quiz 2 took me more than I want to admit: the logic was easy, but I left a nasty bug.

### Day 11
Solved the first quiz in 8 minutes, took several hours before surrending and check the solution on Reddit.
However, I am quite satisfied to see that the hint of the solution was enough, and I am also happy that now solving this kind of problem is in my toolbox (or at least I hope so).

### Day 12
Quiz 2 took me forever, it's getting interesting.


## Who am I
My name is Michele Buccoli, I am not a developer. My job is not coding, but it involves coding. Actually, as a senior scientist at BdSound, my job involves reviewing other people's code (poteto potato tometo tomato).
You can learn other info on myself and contact me through my website mbuccoli.github.io .
