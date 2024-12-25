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

### Day 13
This was really a good day for me. While I was reading the text, I noticed something misleading was in, when the text was saying "the minimum amount of moves" or "with the minimum amount of tokens".
Luckily, it was a very simple system with two equation and two unknowns. Once solved, there was only one possible solution, and that could be either a natural number or not.
So, this was time moving from quiz1 to quiz2 was really really a matter of three minutes.

Edit: I noticed many people online fought against approximation, while I didn't. This is because instead of inverting the matrix, I computed the formula and kept simplifying it until I got a clean numerator vs denominator, which does not carry approximation issues.

### Day 14
Quiz 1 was quick, quiz 2 was hard, but luckily I got the right intuition (dear standard deviation, you've rarely failed me).

### Day 15
Day 15 was solved Dec 20. December is a wonderful month, but there are too many deadlines and it was hard to find the energy to code after dinner, or the time to do it during lunch break.

### Day 18 (done at Dec 25th)
Found out recursive way was somehow too big, so I used a better map.
Quiz 2 was quick thanks to a nice binary search

### Day 19 (done after Day22)
First quiz took me short enough after I realized I could get rid of the redundant patterns (those that could be made by means of other patterns). Now I have the opposite problem: I need to describe EVERY possible combination of patterns. This is basically breaking my solution so I'm calling it a day.
After some suggestions from the internet, I found a good solution and solved it.

### Day 20
I skipped too many days, so now I'll try to keep up with new quizzes and then solve old ones.

### Day 21
Took me long, but happy to see that what I learned from Day11 helped me today.

### Day22
Well, this was exhausting and at the end I basically brute-forced it. 

### Day23
Solved both. Second quiz seemed harder, but I think I found an elegant and rather unexpensive solution.

### Day24
Quiz1 was easy, quiz2 was struggling


## Who am I
My name is Michele Buccoli, I am not a developer. My job is not coding, but it involves coding. Actually, as a senior scientist at BdSound, my job involves reviewing other people's code (poteto potato tometo tomato).
You can learn other info on myself and contact me through my website mbuccoli.github.io .
