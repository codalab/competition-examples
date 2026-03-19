"""Submission by Jimmy Keith ~March 1st, 2019"""


def pisano_period(divisor):
    if divisor == 1:
        return 0
    sequence = [0, 1, 1]
    while sequence[-2:] != [0, 1]:
        sequence.append(sum(sequence[-2:]) % divisor)
    return len(sequence) - 2
