# Probability


## Weighted Probability Distribution
The basic idea is that if you have several outcomes, each outcome is assigned a weight that represents its likelihood relative to the other outcomes. This weight can be any non-negative number.

The probability of each outcome is then calculated as its weight divided by the total weight of all outcomes.

In the example provided:

- Element A with a weight of 5
- Element B with a weight of 10
- Element C with a weight of 15

The total weight is the sum of the individual weights:

$W = w_A + w_B + w_C = 5 + 10 + 15 = 30$

The probability \(P(i)\) of each element \(i\) is calculated as its weight divided by the total weight:

$P(A) = \frac{w_A}{W} = \frac{5}{30} = \frac{1}{6}$

$P(B) = \frac{w_B}{W} = \frac{10}{30} = \frac{1}{3}$

$P(C) = \frac{w_C}{W} = \frac{15}{30} = \frac{1}{2}$

These probabilities represent the likelihood of each element being chosen. Element C, with the highest weight, is the most likely to be chosen, while Element A, with the lowest weight, is the least likely.

This principle of weighted probabilities can be applied in any situation where you have a set of outcomes that do not all have the same likelihood. For example, it is used in statistical analysis, machine learning algorithms, decision making under uncertainty, and many other fields.