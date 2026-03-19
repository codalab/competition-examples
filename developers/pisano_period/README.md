Pisano Period
=============

This competition is from [Jimmy Keith's weekly code challenges](https://github.com/jimmykodes/code_challenges/tree/master/02_25_pisano_period) at our company
[CKC](http://ckcollab.com)

## What is a Pisano Period?

A Pisano period is the length at which a sequence of the remainders of a given number divided by each number in
the fibonacci sequence repeats.<sup>[1]</sup>

```
| Fibonacci          | 0 | 1 | 1 | 2 | 3 | 5 | | 8 | 13 | 21 | 34 | 55 | 89 |
|--------------------|---|---|---|---|---|---| |---|----|----|----|----|----|
| Pisano period of 4 | 0 | 1 | 1 | 2 | 3 | 1 | | 0 | 1  | 1  | 2  | 3  | 1  |
```
This table shows the Fibonacci sequence and the Pisano period of the number 4. You can see
by the break in the table where the pattern of the remainders repeats. For the entirety of the 
Fibonacci sequence (i.e. infinity) this pattern will _always_ remain the same for the given divisor.
The length of this pattern is that number's Pisano period, so the Pisano period of `4` would be `6`.

Write a function `pisano_period` that takes in a positive integer and returns the length
of its Pisano period. 

___
<sub>[1] The fibonacci sequence starts with `0, 1` and is calculated by adding the last 2 numbers of the sequence
to get the next number. `0, 1, 1, 2, 3, 5, 8, 13, etc.` since `1 + 1 = 2, 1 + 2 = 3, 3 + 2 = 5, and so on` </sub>


## Task

Create a function solving the pisano period for some given divisor, using the least code, memory, and CPU as possible!

```python
assert pisano_period(1) == 0
assert pisano_period(8) == 12
assert pisano_period(5) == 20
assert pisano_period(11) == 10
assert pisano_period(4) == 6
assert pisano_period(6) == 24
assert pisano_period(7) == 16
```

## Solution

To make a solution, submit a zip with `solution.py` containing this function:

```python
def pisano_period(divisor):
   ...
   return the_pisano_period_of_the_divisor
```



## Adjustments from original for Codalab

Added some metrics for CPU, memory, and amount of characters in the code of the applicant.

## Todo

Better leaderboard metrics? Use computational somehow?
