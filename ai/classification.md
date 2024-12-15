# Classification

Classification is a type of supervised learning where the target variable is group of categories or classes.

> The terms **Class** and **Category** are used interchangeably in classification.

The example of classification problems are:

| Question | Target Variable |
| --- | --- |
| Is this email spam or not? | Yes or No |
| Is this tumor malignant? | Yes or No |
| Is this transaction fraudulent? | Yes or No |

**Binary Classification**<br>
This is a type of classification where the target variable has only two classes.
- Yes or No
- True or False
- Positive or Negative
- 1 or 0


**Multi-class Classification**<br>
This is a type of classification where the target variable has more than two classes.

| Question | Target Variable |
| --- | --- |
| What type of tumor is this? | Malignant, Benign, Normal |
| What type of animal is this? | Cat, Dog, Bird |
| What type of vehicle is this? | Car, Truck, Bus, Motorcycle, Bicycle |

**Can Linear Regression algorithm be used for Classification?**<br>
As it turns out, linear regression is not a suitable algorithm for classification problems.

- **Continuous Output**: Linear regression predicts continuous values, often outside [0, 1], making it unsuitable for classification probability outputs.

- **Unreliable Decision Boundary**: Minimizing squared error doesn't ensure effective class separation, leading to poor performance in classifying overlapping or imbalanced data.

- **Inapplicability to Multi-class**: Linear regression cannot naturally handle multiple discrete classes, making it infeasible for multi-class classification problems.


## Logistic Regression

Logistic regression is one of the most popular algorithms for binary classification. It predicts the probability of an input belonging to a class, and classifies it based on a threshold value.

> Unlike the linear regression Logistic regression uses the sigmoid function, which maps continuous inputs to probabilities between 0 and 1. This makes it suitable for binary classification. While the sigmoid function is continuous, its output emphasizes values near 0 and 1, and its derivative is computationally simple, aiding optimization during training.
>
> The term _regression_ in logistic regression is a misnomer and is because of historicl reasons. Logistic regression is a classification algorithm not a regression algorithm.


### Sigmoid Function
Sigmoid function (also called logistic function) is a mathematical function which maps any real value to a value between 0 and 1. It is defined as:

$$
\sigma(x) = \frac{1}{1 + e^{-x}}
$$

where:
- $e$ (Euler's number) is the base of the natural logarithm, which is approximately equal to 2.71828.
- $x$ is the input to the function.

![Sigmoid Function](images/sigmoid_function.png)

The above S-shape of sigmoid function also called the **sigmoid curve**.

> [Good video on Euler's number $e$](https://www.youtube.com/watch?v=m2MIpDrF7Es)

Output of Sigmoid function is always between 0 and 1.

$$ 0 < \sigma(x) < 1 $$

As we can see, the result of large positive values of $x$ approaches 1, and the result of large negative values of $x$ approaches 0.

For example:

$$\sigma(100) = \frac{1}{1 + e^{-100}}= \frac{1}{1 + e^{\frac{1}{100}}} = \frac{1}{1 + \text{very small number}}  \approx 1$$

Similarly:

$$\sigma(-100) = \frac{1}{1 + e^{100}}= \frac{1}= \frac{1}{1 + \text{very large number}}  \approx 0$$

In specific case of $x=0$, the sigmoid function returns 0.5.

$$\sigma(0) = \frac{1}{1 + e^{0}} = \frac{1}{1 + 1} = 0.5$$

### Logistic Regression Model
Now let's bring this back to the context of classification.

Recall that the linear regression model defined as:
$$f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}) = \vec{\mathbf{w}} \cdot \vec{\mathbf{x}} + b$$

Let's assume $z=\vec{\mathbf{w}} \cdot \vec{\mathbf{x}} + b$, and we call the sigmoid function $g$ (instead of $\sigma$) in this context.

$$g(z) = \frac{1}{1 + e^{-z}}$$
$$z = \vec{\mathbf{w}} \cdot \vec{\mathbf{x}} + b$$

So the logistic regression model can be defined as:
$$g(z) = g(\vec{\mathbf{w}} \cdot \vec{\mathbf{x}} + b) = \frac{1}{1 + e^{-(\vec{\mathbf{w}} \cdot \vec{\mathbf{x}} + b)}}$$

#### Interpretation of Logistic Regression Output
The output of logistic regression model is a **probability** value between 0 and 1. In other words, the output shows the probability that class is $1$ or $0$.

In the math terms, the output of logistic regression model is:
$$f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}) = P(y=1|\vec{\mathbf{x}}) $$

Where:
- $P(y=1|\vec{\mathbf{x}})$ is the probability that the target variable $y$ is $1$ given the input $\vec{\mathbf{x}}$.

> $P(a | b)$ is the conditional probability of $a$ given $b$.

In some texts, this probability also denoted as:

$$f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}) = g(\vec{\mathbf{w}} \cdot \vec{\mathbf{x}} + b) = P(y=1|\vec{\mathbf{x}};\vec{\mathbf{w}},b)
$$

Where:
- $\vec{\mathbf{x}};\vec{\mathbf{w}},b$ denotes that the probability is conditioned on $\vec{\mathbf{x}}$ based on the given parameters $\vec{\mathbf{w}}$ and $b$.


For example:<br>
If $x$ is the "email" and $y$ is the "spam" or "not spam" class.

- $x$ is the input email.
- $y=0$ means "not spam".
- $y=1$ means "spam".

And for an email the logistic regression model output is $0.7$.

$$f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}) = P(y=1|\vec{\mathbf{x}}) = 0.7$$

This means that the probability of the email being spam is $0.7$ or in simple terms the email has $70\%$ chance of being spam.

We know that the sum of probabilities of all possible outcomes is $1$.

$$P(y=0) + P(y=1) = 1$$

So, the probability of the email being not spam is $0.3$ or $30\%$.

$$P(y=0|\vec{\mathbf{x}}) = 1 - P(y=1|\vec{\mathbf{x}}) = 1 - 0.7 = 0.3$$
