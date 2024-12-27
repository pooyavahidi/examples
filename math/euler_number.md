# Euler Number

The Euler number shown as $e$ is a fundamental mathematical constant that is the base of the natural logarithm. It is approximately equal to $2.71828$. The Euler number is named after the Swiss mathematician Leonhard Euler.

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
