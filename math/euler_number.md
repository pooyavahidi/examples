# Euler Number

The Euler number shown as $e$ is a fundamental mathematical constant that is the base of the natural logarithm. It is approximately equal to $2.71828$. The Euler number is named after the Swiss mathematician Leonhard Euler.

## Where does Euler's number come from?
Let's start with the compound interest formula:

$$A = P \left(1 + \frac{r}{n}\right)^{n \cdot t}$$

where:
- $A$ = the final amount
- $P$ = the initial principal amount
- $r$ = the growth rate as a decimal in a unit of time (e.g. annual)
- $n$ = the number of compounding periods per unit of time (e.g. year)
- $t$ = the total number of time units

For example, if let's assume the _unit of time_ is a year:
- $P$ = Initial amount is $1000
- $r$ = 0.05 (5% growth rate) per _unit of time_ which is a year
- $n$ = Number of times we apply the compounding in _unit of time_. Our unit of time is a year, and let's say we compound quarterly, so $n = 4$.
- $t$ = For how many _unit of time_ we want to calculate the final amount. Let's say we want to calculate for 2 _unit of time_ which is 2 years.

So, the formula becomes:

$$A = 1000 \left(1 + \frac{0.05}{4}\right)^{4 \times 2} \approx 1104.94$$

**Discrete Compounding:**<br>
The above formula is for discrete compounding where the compounding happens at discrete intervals during the time period. For example if our _unit of time_ is a year, and we compound quarterly, then the compounding happens discretely at the end of each quarter in total of 4 times during that period.


**Incerase the number of compounding events:**<br>
Let's use a simpler example:
- $P = 1$ which is Initial amount
- $r = 1$ means 100% growth rate
- $n = 1$ means we compound once in a year
- $t = 1$ means we want to calculate for 1 year

Without using the formula, intuitively we can guess if we grow $1 by 100% in a year, the final amount should be $2 at the end of the year. Let's calculate this using the formula:

$$A = 1 \left(1 + \frac{1}{1}\right)^{1 \times 1} = 2$$

Now, let's increase the number of compounding events to 4 times in a year (quarterly), we should get more than $2 at the end of the year as we are compounding the compounded amount 4 times in a year. Let's calculate this:

$$(1 + \frac{1}{4}) \cdot (1 + \frac{1}{4}) \cdot (1 + \frac{1}{4}) \cdot (1 + \frac{1}{4}) = 2.4414$$

This means for a 100% growth rate, if we compound the amount 4 times in a year, each time we grow by 25%, the final amount should be $2.4414 at the end of the year:

$$(1 + 0.25) \cdot (1 + 0.25) \cdot (1 + 0.25) \cdot (1 + 0.25) = 2.4414$$

And using the compounding formula:

$$A = 1 \left(1 + \frac{1}{4}\right)^{4 \times 1} = 2.4414$$

Now, if we keep increasing the number of compounding events, we should get more than $2.4414 at the end of the year. Again, because we are compounding the compounded amount more frequently. Let's calculate this for 12 times in a year (monthly):

$$(1 + \frac{1}{12}) \cdot (1 + \frac{1}{12}) \cdot \ldots \cdot (1 + \frac{1}{12}) = 2.6130$$

$$(1 + \frac{1}{12})^{12} = 2.6130$$

Let's calculate the _Daily_ compounding:

$$(1 + \frac{1}{365})^{365} = 2.7146$$


**What if we increase the number of compounding events to a very large number?**<br>
Now, the question arises, if there is any limit to this growth? If we keep increasing the number of compounding events, will this growth goes to infinity or there is ceiling to this growth?

$$\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^{n}$$

Let's calculate this limit for a large number of compounding events:

$$\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^{n} = \left(1 + \frac{1}{1000000}\right)^{1000000} \approx 2.71828$$

If plug in any large number for $n$ it turned out that this limit approaches a constant, and that constant is called the Euler number $e$ which is approximately equal to $2.71828$.

$$e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^{n}$$



**Continuous Compounding:**<br>
The above limit shows the continuous compounding where the compounding happens at every possible moment during the time period.

Now let's bring back our compound interest formula:

$$A = P \left(1 + \frac{r}{n}\right)^{n \cdot t}$$

If the compounding happens continuously (infinitely many intervals) during the time period:

$$A = \lim_{n \to \infty} P \left(1 + \frac{r}{n}\right)^{n \cdot t}$$



Factor out $r$ for Simplicity: Rewrite the base $1 + \frac{r}{n}$ as:
   $$ 1 + \frac{r}{n} = \left(1 + \frac{1}{n/r}\right)$$
This lets us think of the expression as a form of $1 + \frac{1}{k}$ where $k = n / r$.

Recall the Definition of $e$: By definition, the number $e$ is:
$$e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n$$

Substitute into the Limit: From previous step, notice that our expression can now be written as:
$$\left(1 + \frac{r}{n}\right)^n = \left[\left(1 + \frac{1}{k}\right)^k\right]^r$$
where $k = n / r$. As $n \to \infty$, $k \to \infty$ too.


Simplify Using the Limit of $e$: The inner term $\left(1 + \frac{1}{k}\right)^k$ approaches $e$ as $k \to \infty$:

$$ \lim_{k \to \infty} \left(1 + \frac{1}{k}\right)^k = e $$

So:
$$ \lim_{n \to \infty} \left(1 + \frac{r}{n}\right)^n = e^r $$

And multiply both sides by $P$ and increase them to the power of $t$:

$$ \lim_{n \to \infty} P \left(1 + \frac{r}{n}\right)^{n \cdot t} = P \cdot e^{r \cdot t} $$


So, the **Continuous Compounding** formula becomes:

$$A = P \cdot e^{r \cdot t}$$

where:
- $A$ = the final amount
- $P$ = the initial principal amount
- $r$ = the growth rate as a decimal in a unit of time (e.g. annual)
- $t$ = the total number of time units
- $e$ = Euler's number

### Key Difference:
- **Discrete Compounding** depends on the number of intervals $n$.
- **Continuous Compounding** assumes growth occurs at every possible moment, leading to the $e^{r \cdot t}$ formula.

Continueous compounding is a theoretical concept, but it is used in many applications like finance, physics, and other fields where the growth is continuous. For example, the growth of bacteria, radioactive decay, etc.

## Derivative of $e^{x}$ is itself
This [video by 3Blue1Brown](https://www.youtube.com/watch?v=m2MIpDrF7Es) is a good explaination of Euler's number. The following is the summary of that video.

Let's start by seeing how to calculate the derivative of $a^{x}$ where $a$ is a constant e.g. $2^{x}$, $3^{x}$, etc.

Based on the definition of derivative, we can write the derivative of $a^{x}$ as:

$$\frac{d}{dx} a^{x} = \lim_{\epsilon \to 0} \frac{a^{x+\epsilon} - a^{x}}{\epsilon}$$

Using [exponents product rule](algebra_basics.md#exponents), we can write:

$$a^{x+\epsilon} = a^{x} \cdot a^{\epsilon}$$

So, the above equation becomes:

$$\frac{d}{dx} a^{x} = \lim_{\epsilon \to 0} \frac{a^{x} \cdot a^{\epsilon} - a^{x}}{\epsilon}$$

Factor out $a^{x}$ from the numerator:

$$\frac{d}{dx} a^{x} = \lim_{\epsilon \to 0} a^{x} (\frac{a^{\epsilon} - 1}{\epsilon})$$

We can see $\frac{a^{\epsilon} - 1}{\epsilon}$ is the only part that $\epsilon$ exists, and it's some kind of constant (when $\epsilon$ is very small).

It shows that derivative of $a^{x}$ is **porportional** to $a^{x}$.

Let's calculate this constant:

for $a = 2$ and $\epsilon = 0.00001$:
$$\frac{2^{0.00001} - 1}{0.00001} \approx 0.6931$$

and for $\epsilon = 0.000001$:

$$\frac{2^{0.000001} - 1}{0.000001} \approx 0.6931$$

and for $\epsilon = 0.0000001$:
$$\frac{2^{0.0000001} - 1}{0.0000001} \approx 0.6931$$

We can keep going on and calculate this for smaller $\epsilon$ but we can see that this constant is approximately $0.6931$.

So, the derivative of $2^{x}$:

$$\frac{d}{dx} 2^{x} = 2^{x} \times 0.6931$$
Let's see this for $a = 3$:
$$\frac{3^{0.00001} - 1}{0.00001} \approx 1.0986$$

and for $a=8$:
$$\frac{8^{0.00001} - 1}{0.00001} \approx 2.0794$$


The derivative of $a^{x}$ is itself $a^{x}$ times some constant. In other words, the derivative of $a^{x}$ is proportional to itself with some constant.

$$\frac{d}{dx} a^{x} = a^{x} \times \text{some constant}$$

**Is there a base that where that constant is 1?**

Yes, there is a base where that constant is 1, and that base is called the Euler number $e$ which is approximately equal to $2.71828$.



Remember, this is not that number $e$ happend to show up here, this is the definition of $e$.

$$\frac{e^{0.00000001}-1}{0.00000001} \approx 1$$

As $\epsilon$ approaches to 0, the constant approaches to 1.

$$\frac{d}{dx} e^{x} = \lim_{\epsilon \to 0} e^{x}(\frac{e^{\epsilon} - 1}{\epsilon}) = e^{x} \lim_{\epsilon \to 0} \frac{e^{\epsilon} - 1}{\epsilon}$$

$$\lim_{\epsilon \to 0} \frac{e^{\epsilon} - 1}{\epsilon} = 1$$

So:

$$\frac{d}{dx} e^{x} = e^{x} \times 1$$

The Euler number $e$ is defined the same way we defined $\pi$ which is the ratio of the circumference of a circle to its diameter.

$\pi$ is length of the circle with diameter 1. This is how we defined $\pi$, which happened to be approximately 3.14159.

Similarly, $e$ is the base where the derivative of $e^{x}$ is $e^{x}$ times 1. This is how we defined $e$, which happened to be approximately 2.71828.

$$\lim_{\epsilon \to 0} \frac{e^{\epsilon} - 1}{\epsilon} = 1$$

## Derivative of Exponentials

Using [Algebraic logarithm rules](algebra_basics.md#natural-logarithm), we can write:

$$a = e^{\ln(a)}$$

And increase both sides to the power of $x$:

$$a^{x} = e^{x \ln(a)}$$

Using the [chain rule](derivatives.md#chain-rule), we can write the derivative:

$$\frac{d}{dx} a^{x} = \frac{d}{dx} e^{x \ln(a)} = \ln(a)e^{x \ln(a)} $$



So, we can write our funciton as:

$$f(x) = e^{x \ln(a)}$$

Using the chain rule:
- Inner function: $g(x) = x \ln(a)$
- Outer function: $f(u) = e^u$, where $u = g(x) = x \ln(a)$

So, the derivative of $f(x)$ with respect to $x$ is:

$$\frac{df}{dx} = \frac{df}{du} \cdot \frac{du}{dx}$$

Differentiate the outer function $f(u) = e^u$ (see [Derivative of Euler Number](euler_number.md)):

$$\frac{d}{du}(e^u) = e^u$$


Differentiate the inner function $g(x) = x \ln(a)$:

$$\frac{d}{dx}(x \ln(a)) = \ln(a)$$

Apply the chain rule by multiplying:

$$\frac{df}{dx} = \ln(a) \cdot e^{x \ln(a)}  = \ln(a) \cdot a^x$$

So, the derivative of $a^{x}$ is $\ln(a) \cdot a^x$. Which means the derivative of $a^{x}$ is proportional to $a^{x}$ with a constant $\ln(a)$.


Now, that **some constant** we were talking about earlier is just the natural logarithm of the base $a$.

In other word, the derivative of any exponential function $a^{x}$ is itself times by a constant $\ln(a)$.

The _rate_ of a change of an exponential function is proportional to the function itself. For example the rate of change of growth of financial investment is proportional to the amount of the investment itself.
