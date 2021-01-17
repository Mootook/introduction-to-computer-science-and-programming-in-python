# Intro to Computer Science and Programming in Python Notes

## Lecture 1 - What is Computation?

Formerly two types of computers

1. Fixed program computer (calculator), single tasked
2. Stored program computers (personal computer), machines that store sequence of instructions

## Lecture 10 - Understanding Program Efficiency, Part 1

Big O notation, order of growth, captures worst case behavior of a function.
It ignores multiplicative and additive constants (derived from number of steps in a function), focuses on dominant terms.

n^2 + 2n + 2 = O(n^2)
n^2 + 100000n + 3^1000 = O(n^2)
log(n) + n + 4 = O(n)\
0.0001 * n * log(n) + 300n = O(n log n)
2n^30 + 3^n = O(3^n)
