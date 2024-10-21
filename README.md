# KNumber

## Investigate Kaprekar's Routine for Various bases and integer lengths

- Description: 
    - The number 6174 is known as Kaprekar's constant after the Indian mathematician D. R. Kaprekar.
    -  A process, known as Kaprekar's routine is:
        - 1. Take any four-digit number, using at least two different digits(leading zeros are allowed).
        - 2. Arrange the digits in descending and then in ascending order to get two four-digit numbers, adding leading zeros if necessary.
        - 3. Subtract the smaller number from the bigger number.
        - 4. Go back to step 2 and repeat.
    - Any four digit positive integer will converge on 6174 within 6 iterations,  unless it violates rule 1 (i.e. all digits are identical)

## General info

This program introduces general classes of KNumbers which can have a radix
from 2 to 16, length greated than 2. These are used to play around with
variant forms of numbers to see if there are other constants similar to
Kaprekar's are available in other bases or number lengths.

-------------------------------------------------------------------------------