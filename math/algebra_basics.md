# Algebra Basics
Here are some fundamental algebraic rules and properties related to arithmetic operations:


## Properties of Operations
**Commutative Property**
- Addition: $a + b = b + a$
- Multiplication: $ab = ba$

**Associative Property**
- Addition: $(a + b) + c = a + (b + c)$
- Multiplication: $(ab)c = a (bc)$

**Distributive Property**
- Left distributive property: $a  (b + c) = a  b + a  c$
- Right distributive property: $(a + b)  c = a  c + b  c$

## Special Elements
**Identity Elements**
- Addition: $a + 0 = a$
- Multiplication: $a \cdot 1 = a$

**Inverse Elements**
- Addition: $a + (-a) = 0$
- Multiplication: $a  \frac{1}{a} = 1$ for $a \neq 0$

## Exponents
**Basic Rules**
- Product Rule: $a^{m}  a^{n} = a^{m+n}$
- Power of a Power: $(a^{m})^{n} = a^{mn}$
- Power of a Product: $a^{n}  b^{n} = (ab)^{n}$
- Quotient Rule: $\frac{a^{m}}{a^{n}} = a^{m-n} \quad \text{for } a \neq 0$

**Special Rules**
- Zero Exponent Rule: $a^{0} = 1 \quad \text{for } a \neq 0$
- Negative Exponent Rule: $a^{-n} = \frac{1}{a^n} \quad \text{for } a \neq 0$

## Logarithms
**Basic Rules**
- Definition:$\log_{b}(a) = c \iff b^{c} = a$
- Product Rule: $\log_{b}(ac) = \log_{b}(a) + \log_{b}(c)$
- Quotient Rule: $\log_{b}\left(\frac{a}{c}\right) = \log_{b}(a) - \log_{b}(c)$
- Power Rule: $\log_{b}(a^{c}) = c \log_{b}(a)$
- Change of Base Rule: $\log_{b}(a) = \frac{\log_{c}(a)}{\log_{c}(b)}$
- Inverse Rule: $b^{\log_{b}(a)} = a$

Inverse Rule is a direct consequence of the definition of logarithm:
$$\log_{b}(a) = c \iff b^{c} = a$$
We know $c = \log_{b}(a)$, so, replacing $c$ in the above equation, we get:
$$b^{\log_{b}(a)} = a$$


### Natural Logarithm
The natural logarithm is a logarithm to the base $e$, where $e$ is the [Euler number](euler_number.md). The natural logarithm is denoted by $\ln(x)$ which $\ln(x) = \log_{e}(x)$. We can apply all the logarithmic rules to the natural logarithm.

- Definition: $\ln(a) = c \iff e^{c} = a$
- Product Rule: $\ln(ac) = \ln(a) + \ln(c)$
- Quotient Rule: $\ln\left(\frac{a}{c}\right) = \ln(a) - \ln(c)$
- Power Rule: $\ln(a^{c}) = c \ln(a)$
- Change of Base Rule: $\ln(a) = \frac{\log_{b}(a)}{\log_{b}(e)} = \frac{\log_{b}(a)}{\frac{1}{\ln(b)}} = \ln(b) \log_{b}(a)$
- Inverse Rule: $e^{\ln(a)} = a$
- Inverse Rule (Exponential Form): $\ln(e^{a}) = a$
- Inverse Rule (both side to power of $c$): $e^{c \ln(a)} = a^{c}$

**Exponential of $a^{x}$**<br>
In calculus, we often encounter the exponential of $a^{x}$ where $a$ is a constant. However, we usually write the exponential of $a^{x}$ as $e^{x \ln(a)}$.

This is signifies that the exponential of $a^{x}$ is equivalent to the exponential of $e$ to some **constant** times the $x$.

$$ a^{x} = e^{x \ln(a)} = e^{x \times \text{constant}}$$
This way of writing is not only limited to base of $e$, we can write the exponential of $a^{x}$ as $b^{x \log_{b}(a)}$ where $b$ is any base. For example:

$$a^{x} = b^{x \log_{b}(a)} = e^{x \ln(a)} = \pi^{x \log_{\pi}(a)} = 42^{x \log_{42}(a)} = \ldots$$
