# Derivatives

The derivative of a function $f(x)$ provides a measure of how the value of the function changes with respect to changes in the independent variable $x$. It is defined by the limit of the difference quotient as the increment $\Delta x$ approaches zero. In the limit, the derivative represents the instantaneous rate of change of the function at a specific point, $x$.

$$f'(x) = \frac{df(x)}{dx} = \lim_{\Delta x \to 0} \frac{f(x+\Delta x)-f(x)}{\Delta x}$$

We can also write it this way:

$$\frac{df(x)}{dx}=\lim_{\epsilon\to 0} \frac{f(x+\epsilon)-f(x)}{\epsilon}=\frac{\text{Changes of }f(x)}{\text{In respect to changes of }x}$$

In simple terms, derivative of $f(x)$ is what would be value of function $f(x)$ if $x$ has a very small change $\epsilon$.


Let's compute the derivative of $f(x)=x^2$ step by step using this definition:

First, plug $f(x) = x^2$ into the limit definition:

$$\frac{df(x)}{dx}=\lim_{\epsilon\to 0} \frac{(x+\epsilon)^2-x^2}{\epsilon}$$

Then expand the numerator:

$$\frac{df(x)}{dx}=\lim_{\epsilon\to 0} \frac{x^2+2x\epsilon+\epsilon^2-x^2}{\epsilon}$$

Simplify by cancelling $x^2$ in the numerator:

$$\frac{df(x)}{dx}=\lim_{\epsilon\to 0} \frac{2x\epsilon+\epsilon^2}{\epsilon}$$

Factor out $\epsilon$ from the numerator:

$$\frac{df(x)}{dx}=\lim_{\epsilon\to 0} \epsilon (2x+\epsilon)$$

Cancel out $\epsilon$:

$$\frac{df(x)}{dx}=\lim_{\epsilon\to 0} (2x+\epsilon)$$

Finally, as $\epsilon$ approaches zero, the second term in the parenthesis disappears, and we are left with:

$$\frac{df(x)}{dx}=2x$$

So the derivative of $f(x) = x^2$ is $f'(x) = 2x$, as expected.


For example, let's take the function $J(w) = w^2$. Suppose that $w = 3$. Then $J(w)$ will be equal to $3^2 = 9$. If we increase $w$ by a tiny amount, denoted as $\varepsilon$ (let's say $\varepsilon = 0.001$), we get $w = 3.001$ and $J(w) = (3.001)^2 \approx 9.006001$. This demonstrates that if $w$ increases by $\varepsilon$, $J(w)$ increases by approximately $2w \times \varepsilon = 2 \times 3 \times 0.001 = 0.006$. This isn't exactly accurate due to the fact that $\varepsilon$ is small, but not infinitesimally small. As $\varepsilon$ becomes smaller and approaches zero, this approximation becomes more accurate.

In calculus, we would express this by saying that the derivative of $J(w)$ with respect to $w$ is equal to $2w$. Symbolically, we write this as:

$$\frac{dJ(w)}{dw} = 2w$$

In our specific case, since $w=3$, the derivative at this point would be:

$$\frac{dJ(w)}{dw} = 2 \times 3 = 6$$

This means that, at $w=3$, if $w$ increases by a very small amount, $J(w)$ will increase approximately six times as much. This concept holds true regardless of the specific value of $\varepsilon$, as long as $\varepsilon$ is small.

The informal definition of the derivative is that it gives us the ratio by which the function value changes ($J(w)$) for a small change in the input ($w$). In our case, this ratio is 6:1 when $w=3$. Thus, the derivative $\frac{dJ(w)}{dw}$ equals 6 at $w=3$. This numerical value is commonly known as the slope of the tangent line to the function at that specific point.


## Slope and Tangent Line
The **slope** of a line is a measure of how much the line rises or falls vertically for each unit of horizontal movement. It is typically represented by the letter $m$ in the formula of a line, $y=mx+b$, where $b$ is the y-intercept. The slope is calculated by the formula:

$$m = \frac{{\text{{change in }} y}}{{\text{{change in }} x}} = \frac{{\Delta y}}{{\Delta x}}$$

This is also known as the "rise over run" formula.

A **tangent line** to a function at a specific point is a straight line that just touches the curve of the function at that point. It is the best linear approximation to the function near that point.

The **derivative** of a function at a particular point gives the slope of the tangent line at that point. This is because the derivative represents the instantaneous rate of change of the function at that point, which is exactly the concept of slope.

The equation for a tangent line to a function at a particular point is derived from the point-slope form of a linear equation, which is given as:

$$y - y_1 = m(x - x_1)$$

where $(x_1, y_1)$ is a point on the line, and $m$ is the slope of the line. When the line is tangent to a function $f(x)$ at $x_1$, then $y_1 = f(x_1)$ and $m = f'(x_1)$, where $f'(x_1)$ is the derivative of the function at $x_1$.

So:

$$m = f'(x)=\frac{{\Delta y}}{{\Delta x}}$$

So, the equation of the tangent line to $f(x)$ at $x_1$ is:

$$f'(x_1) = \frac{y - f(x_1)}{x - x_1}$$

So:

$$y - f(x_1) = f'(x_1)(x - x_1)$$

For example, if we have a funciton $f(x) = x^2$ and calculate the tangent line at $x_1=3$. The derivative of the function is $f'(x) = 2x$, so the slope of the tangent line at $x_1=3$ is $f'(3) = 2 \times 3 = 6$.

$$y - f(3) = f'(3)(x - 3)$$
$$y - 9 = 6(x - 3)$$
$$y = 6x - 18 + 9 = 6x - 9$$

So the equation of the tangent line to the function $f(x) = x^2$ at the point $(3,9)$ is $y = 6x - 9$, and the slope of this line (which is 6) is the value of the derivative of the function at $x = 3$.

> This relationship holds in general: the derivative of a function at a particular point gives the slope of the tangent line to the function at that point.


This can be visually confirmed using matplotlib and numpy in Python:



```python
import numpy as np
import matplotlib.pyplot as plt

w = np.linspace(-5, 5, 100)
J = w**2

fig, ax = plt.subplots()  # create a figure and an axes object

# the function
ax.plot(w, J, label="J(w) = w^2")

# the tangent line at w=3
w_tangent = 3
J_tangent = w_tangent**2
slope_tangent = 2 * w_tangent  # which is the derivative at w=3
tangent_line = slope_tangent * (w - w_tangent) + J_tangent
ax.plot(w, tangent_line, label=f"Tangent at w={w_tangent}")

ax.set_ylim([0, 20])  # limit the y-axis to 10
ax.grid(True, which="both")  # add a grid
ax.legend()  # add a legend

plt.show()
```



![](images/derivatives_tangent_line.png)




The plot will show the function $J(w) = w^2$ and the tangent line at $w=3$. The slope of this tangent line is indeed 6, which confirms our mathematical derivation.

## Partial and Total Derivatives

There are two types of derivatives that are commonly used in calculus: the **total derivative** and the **partial derivative**:

1. **Total Derivative (or simply Derivative) ($\frac{d}{dw}$):** When the function depends on a single variable, we often use $\frac{d}{dw}$ to denote the derivative. For example, if $J(w)$ is a function of $w$, the derivative of $J(w)$ with respect to $w$ is written as:

$$\frac{dJ(w)}{dw}$$

2. **Partial Derivative ($\frac{\partial}{\partial w_i}$):** When the function depends on more than one variable, we use the partial derivative notation. For instance, if $J$ is a function of multiple variables, say $w_1, w_2, \ldots, w_n$, and we want to find out how $J$ changes with respect to $w_i$ while keeping other variables constant, we use the notation:

$$\frac{\partial}{\partial w_i} J(w_1, w_2, \ldots, w_n)$$

The symbol $\partial$ (called "del" or "partial") is used to denote partial derivatives, as opposed to the $d$ for ordinary derivatives. This distinction is necessary to indicate that only one variable is considered for the change, while others are held constant.

**Example:**


Let's define a function $J(w_1, w_2) = w_1^2w_2 + w_2^3$.

1. The partial derivative of $J$ with respect to $w_1$ (keeping $w_2$ constant) is obtained by differentiating $J$ with respect to $w_1$ and treating $w_2$ as a constant:

$$\frac{\partial J}{\partial w_1} = \frac{\partial}{\partial w_1}(w_1^2w_2) + \frac{\partial}{\partial w_1}(w_2^3) = 2w_1w_2 + 0 = 2w_1w_2$$

2. The partial derivative of $J$ with respect to $w_2$ (keeping $w_1$ constant) is obtained by differentiating $J$ with respect to $w_2$ and treating $w_1$ as a constant:

$$\frac{\partial J}{\partial w_2} = \frac{\partial}{\partial w_2}(w_1^2w_2) + \frac{\partial}{\partial w_2}(w_2^3) = w_1^2 + 3w_2^2$$

As you can see, the partial derivatives of the function $J(w_1, w_2)$ with respect to $w_1$ and $w_2$ are different in this example.


## Chain Rule
The chain rule is a fundamental tool in calculus for computing the derivative of a function composition. It allows us to break down complex functions into simpler ones when differentiating.

Formally, suppose we have a function $f$ of $x$, which is a composition of function $g$ of $x$:

$$f(x) = f(g(x))$$

The chain rule states that the derivative of $f$ with respect to $x$ can be computed by multiplying the derivative of $f$ with respect to $g$ by the derivative of $g$ with respect to $x:

$$\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}$$


For simplicity, we usually use variables like $u$, $v$, and $w$, ... to represent intermediate functions. For example, when function $f$ of $x$ is a composition of function $g$ of $x$, we can write it as:
$$u = g(x)$$
$$f(x) = f(g(x)) = f(u)$$

Then the chain rule can be written as:
$$\frac{df}{dx} = \frac{df}{du} \cdot \frac{du}{dx}$$


**Prime Notation:**

The chain rule can also be written in a different notation that uses prime notation, $f'(x)$, for derivatives. Here, $f'(x)$ represents the derivative of function $f$ at the point $x$.

Given that $i(x) = f(g(x))$, the chain rule can be written as:

$$i'(x) = f'(g(x)) \cdot g'(x)$$

For the case where we have three functions composed together, if $i(x)=p(g(h(x)))$, using the prime notation, the chain rule can be written as:

$$i'(x) = p'(g(h(x))) \cdot g'(h(x)) \cdot h'(x)$$

This tells us that the derivative of the composed function at $x$ is the product of the derivative of $p$ at $g(h(x))$, the derivative of $g$ at $h(x)$, and the derivative of $h$ at $x$.

This is the chain rule in prime notation. It is equivalent to the one using $\frac{df}{dx}$ notation, and the choice between them is usually a matter of personal preference or context.


**Number of Compositions:**

The chain rule can be extended to any number of compositions. For instance, if we have 4 functions composed together, $f(g(h(i(x))))$, the derivative would be:

$$\frac{d}{dx}[f(g(h(i(x))))] = \frac{df}{dg}\frac{dg}{dh}\frac{dh}{di}\frac{di}{dx}$$

The chain rule is crucial in many areas of calculus, including the computation of complex derivatives and integrals, and forms the basis of backpropagation in machine learning.

- This [tutorial](https://www.khanacademy.org/math/ap-calculus-ab/ab-differentiation-2-new/ab-3-1a/v/chain-rule-introduction) is a good tutorial on the chain rule.
- This [video](https://youtu.be/YG15m2VwSjA) is also another great intro to the chain rule.



### Examples
**Example:**Suppose you have a function:

$$f(x) = \left(3x + 1\right)^2$$

This is a **composite function** because it consists of two parts:
- The **inner function** is $g(x) = 3x + 1$.
- The **outer function** is $f(u) = u^2$, where $u = g(x) = 3x + 1$.

$$f(x) = f(g(x))$$

Using the chain rule:
$$\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dx}$$

Rewriting the above using the new variable $u = g(x)$:
$$\frac{df}{dx} = \frac{df}{du} \cdot \frac{du}{dx}$$


1. Differentiate the outer function $f(u) = u^2$:
   $$\frac{d}{du}(u^2) = 2u$$

2. Differentiate the inner function $g(x) = 3x + 1$:
   $$\frac{d}{dx}(3x + 1) = 3$$

3. Apply the chain rule by multiplying:
   $$\frac{df}{dx} = 2u \cdot 3$$

To get the final derivative of $f$ with respect to $x$, we need to substitute back $u = 3x + 1$:
$$\frac{df}{dx} = 2(3x + 1) \cdot 3 = 6(3x + 1)$$


**Example:**

Now let's go through another example with a bit more complex function composition. We are given function $f$ of $x$ as follows:

$$f(x) = ((x + 1)^3)^2$$

The goal is to break this into smaller functions, so we can apply the chain rule effectively. We start with the **innermost operation** and work our way out:
   $$h(x) = x + 1$$
   $$g(w) = w^3 \quad \text{where} \quad w = h(x) = x + 1$$
   $$f(v) = v^2 \quad \text{where} \quad v = g(w) = (x + 1)^3$$

Now, to find the derivative of the original function, let’s rewrite the composition:

$$f(x) = \left((x + 1)^3\right)^2 = f(g(h(x)))$$

The derivative of this composition using the chain rule would be:

$$\frac{df}{dx} = \frac{d}{dx}[f(g(h(x)))]$$

Which we can rewrite as:

$$\frac{df}{dx} = \frac{df}{dg} \cdot \frac{dg}{dh} \cdot \frac{dh}{dx}$$

Or using $w$ and $v$ as intermediate variables, we can write this as:

$$\frac{df}{dx} = \frac{df}{dv} \cdot \frac{dv}{dw} \cdot \frac{dw}{dx}$$

Step-by-step differentiation:

1. Differentiate $f(v) = v^2$ with respect to $v$:
   $$\frac{df}{dv} = 2v$$

2. Differentiate $g(w) = w^3$ with respect to $w$:
   $$\frac{dv}{dw} = 3w^2$$

3. Differentiate $h(x) = x + 1$ with respect to $x$:
   $$\frac{dw}{dx} = 1$$

So:

$$\frac{d}{dx}[f(g(h(x)))] = 2v \cdot 3w^2 \cdot 1$$

Finally, to get the derivative of $f(x)$ with respect to $x$, we need to substitute back the intermediate variables $v$ and $w$:
If we substitute everything back, $v = (x + 1)^3$ and $w = x + 1$, we get:

$$\frac{df}{dx} = 2(x + 1)^3 \cdot 3(x + 1)^2 = 6(x + 1)^5$$


**Example - Sigmoid function:**

We start with the sigmoid function, defined as:

$$\sigma(x) = \frac{1}{1+e^{-x}}$$

Let's first rewrite the function slightly to make differentiation easier:

$$\sigma(x) = (1+e^{-x})^{-1}$$

Now, let's use the chain rule to differentiate. The chain rule states that the derivative of a composite function is the derivative of the outer function times the derivative of the inner function.

If we consider $f(u) = u^{-1}$ and $u(x) = 1 + e^{-x}$ as our outer and inner functions respectively, then the derivative of $\sigma(x)$ is:

$$
\sigma'(x) = f'(u) \cdot u'(x)
$$

1. Differentiating the outer function $f(u)$ gives $f'(u) = -u^{-2}$.
2. Differentiating the inner function $u(x)$ gives $u'(x) = -e^{-x}$.

So,

$$
\sigma'(x) = -u^{-2} \cdot -e^{-x} = \frac{e^{-x}}{(1+e^{-x})^2} = \frac{1}{1+e^{-x}} \cdot \frac{e^{-x}}{1+e^{-x}}
$$

Then, note that $e^{-x}$ in the numerator can be written as $(1+e^{-x}) - 1$. Substituting this and simplifying, we get:

$$
\sigma'(x) = \frac{1}{1+e^{-x}} \cdot \left(1 - \frac{1}{1+e^{-x}}\right) = \sigma(x)(1-\sigma(x))
$$

So, the derivative of the sigmoid function is:

$$
\sigma'(x) = \sigma(x)(1-\sigma(x))
$$



**Example - Mean Squared Error (MSE) Cost Function:**

MSE defined as:
$$J(w) = \frac{1}{2m} \sum_{i=1}^{m} (f_{w}(x^{(i)}) - y^{(i)})^2$$


Where:
- $f_{w}(x) = wx + b$ is a linear regression model.
- $x^{(i)}$ is the input feature for the $i^{th}$ example.
- $y^{(i)}$ is the actual target value for the $i^{th}$ example.
- $m$ is the total number of training examples.

So, we can write it as:
$$J(w) = \frac{1}{2m} \sum_{i=1}^{m} (wx^{(i)} + b - y^{(i)})^2$$

Let's define the inner function:
$$u = g(w) = wx^{(i)} + b - y^{(i)}$$

Then, the cost function $J(w)$ can be written as a composition of functions:

$$J(w) = J(g(w)) = J(u) = \frac{1}{2m} \sum_{i=1}^{m} u^2$$

Now, we can apply the chain rule to find the derivative of $J(w)$ with respect to $w$:

$$\frac{dJ(w)}{dw} = \frac{dJ(u)}{du} \cdot \frac{du}{dw}$$

$$\frac{dJ(w)}{dw} = \frac{1}{m} \sum_{i=1}^{m} u \cdot x$$

Substitute back $u = wx^{(i)} + b - y^{(i)}$:

$$\frac{dJ(w)}{dw} = \frac{1}{m} \sum_{i=1}^{m} (wx^{(i)} + b - y^{(i)}) \cdot x^{(i)}$$



### Rate of Change

When we're taking the derivative of a function, we're trying to understand how fast the function is changing at a particular point. If we have a complex function formed by composing several simpler functions, we're interested in how fast that whole composition is changing.

Let's consider a composed function $h(x) = f(g(x))$. If we want to find out how fast $h$ changes with respect to $x$, we can break down this change into two parts:

1. How fast does $f$ change with respect to $g$ (i.e., $\frac{df}{dg}$)? This part tells us how a small change in $g$ would affect $f$.

2. How fast does $g$ change with respect to $x$ (i.e., $\frac{dg}{dx}$)? This part tells us how a small change in $x$ would affect $g$.

The chain rule combines these two rates of change to find out how fast $h$ changes with respect to $x$. If we change $x$ a little bit, this change propagates through $g$, then $f$, causing $h$ to change. The chain rule basically says that the total change in $h$ is the product of these two rates of change.

Now, if we add more functions to the chain, the same logic applies. For $h(x) = f(g(i(x)))$, we would compute $\frac{df}{dg}$, $\frac{dg}{di}$, and $\frac{di}{dx}$, and multiply these together to get $\frac{dh}{dx}$. The rate of change of each function with respect to the next function in the chain gets multiplied together to get the total rate of change of $h$ with respect to $x$.

In essence, the chain rule is taking advantage of the fact that a small change in the input of a function results in a small change in the output, and these small changes can be approximated by the derivatives of the functions involved. By multiplying the derivatives together, we are effectively "canceling out" the intermediate variables, leaving only the rate of change of the output with respect to the input.

**Example**:

Given $J(w)=(3w+2)^2$, we can express it as a composition of two functions: $a(w) = 3w+2$ and $J(a) = a^2$.

- A small change in $w$, (denoted as $\epsilon$), causes $a$ to change by $3 \times \epsilon$.
- A small change in $a$, causes $J$ to change by $2a \times \epsilon$.

Now if we substitute the change in $a$ due to a change in $w$ into the second step:

- A small change in $w$ of size $\epsilon$ will cause $J$ to change by $3 \times 2a \times \epsilon$.


let's give our example a concrete value, let's say $w=3$, then $a=11$ and $J(w)=121$. Now, a small change of $\epsilon$ in $w$ will cause $J$ to change by $3 \times 2\times 11 \times \epsilon=66\epsilon$. For example, if $\epsilon=0.001$ then $w=3.001$, and:

$$J(3.001)=J(3)+J(0.001)=121+66\epsilon=121+0.066=121.066$$

We can confirm this by calculating the $J(3.001)=(3\times 3.001 + 2)^2 = 121.066009$. This two number are not _exactly_ the same, but if we take our $\epsilon$ small enough i.e. $\epsilon \to 0$, this two number will become the same.

So, as the chain rule defined:

$$\frac{\partial J}{\partial w} = \frac{\partial a}{\partial w} \frac{\partial J}{\partial a} $$

This expression says that the rate of change of $J$ with respect to $w$ is equal to the product of the rate of change of $a$ with respect to $w$ and the rate of change of $J$ with respect to $a$. In another words, a small change in $w$ is multiplied by $\frac{\partial a}{\partial w}$ resulting in a change that is 3 times as large. This larger change is then multiplied by $\frac{\partial J}{\partial a}$ resulting in a change that is now $3 \times 22 = 66$ times larger.




## Other Resources
These are great additional resources for understanding of derivatives in a more visualized way:
- [The paradox of the derivative](https://www.youtube.com/watch?v=9vKqVkMQHKk&list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&index=2)
- [Derivative formulas through geometry](https://www.youtube.com/watch?v=S0_qX4VJhMQ&list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&index=3)
- [Visualizing the chain rule and product rule](https://www.youtube.com/watch?v=YG15m2VwSjA&list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&index=4)
- [What's so special about Euler's number e?](https://www.youtube.com/watch?v=m2MIpDrF7Es&list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr&index=5)
