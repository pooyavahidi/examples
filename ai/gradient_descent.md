# Gradient Descent
Gradient Descent is an optimization algorithm used to minimize any function that can be expressed as a sum of differentiable functions.

> Gradient Descent is the most common algorithm used for minimizing the cost function of many machine learning models, from linear regression to the most complex neural networks. It can minimize cost functions with any number of parameters $J(w_1, w_2, ..., w_n, b)$.

The idea is to start with an initial guess for the parameters $w$ and $b$, then iteratively adjust these parameters to move towards a minimum of the cost function.



Steps:
1. Start with an initial guess for the parameters $w$ and $b$.
2. Compute the cost function $J(w,b)$ with the current values of $w$ and $b$. Also called **forward pass**.
3. Compute the gradient of the cost function $J(w,b)$ at the current point with respect to the parameters $w$ and $b$. Also called **backward pass** or **backpropagation**.
4. Update the parameters $w$ and $b$ in the opposite direction of the gradient (to descent down the hill) by a small step size $r$.
5. Repeat steps 2 to 4, until we settle at or near the global minimum (convergence).


In linear regression with squared error loss, the cost function $J(w,b)$ is a convex function, which means it has a single global minimum. However, a cost function could have a complex surface (usually in training neural networks) with more than one global minimum. These are called **local minima**. The lowest point in the entire function is called the **global minimum**.

![complex_loss_surface](images/gd_complex_loss_surface.png)

The cost function $J$ shown above, has a complex surface with multiple local minimas, and one global minimum.

**Intuitive Explanation of Gradient Descent:**
Imagine this surface as a terrain in a hilly area where you want to reach the lowest valley (the global minimum) as quickly as possible. You start at a random point (initial values of $w$ and $b$) and want to find the path to the lowest valley. The gradient descent algorithm helps you find the path to this lowest valley by finding the **steepest descent** at each point, and moving in that direction step by step (with a predefined **step size**).

**loss surface** is a graphical representation of a model's loss function in relation to its parameters (e.g., weights and biases). It shows how the loss changes as parameters vary, helping visualize the optimization process. The surface often features local minima, saddle points, and a global minimum, which optimization algorithms aim to find.

[**Convex**](https://developers.google.com/machine-learning/glossary#convex-function) surfaces such as _square error loss_ has a single global minimum, making optimization easier. **Non-convex** surfaces have multiple local minima, making optimization more challenging.

## Gradient Descent Algorithm
Gradient Descent steps with more details:

1. **Initialize Parameters:** Start with an initial guess for the parameters $w$ and $b$.
2. **Compute the Cost Function:** Calculate the cost function $J(w,b)$ with the new values of $w$ and $b$.
3. **Compute the Gradient:** Calculate the derivative of the cost function $J(w,b)$ with respect to the parameters $w$ and $b$.
4. **Update the Parameters:** We update the parameters $w$ and $b$ in the opposite direction of the gradient.
5. **Repeat until Convergence:** Repeat from step 2, until we reach a point where parameters $w$ and $b$ don't change much with each iteration, and the cost function doesn't decrease significantly. This is called convergence.


Steps 1 and 2 are self-explanatory and have been discussed previously.

**3. Compute the Gradient:**

At each step of the gradient descent algorithm, we calculate the derivative of the cost function with respect to each parameter. In other words, we calculate the rate of change of the cost function with respect to each parameter. This tells us how much the cost function will change if we change the parameters slightly in a particular direction.

The following is the **derivative** of the cost function $J(w,b)$ with respect to the parameters $w$ and $b$:

$$\frac{\partial J(w,b)}{\partial w}$$
$$\frac{\partial J(w,b)}{\partial b}$$

Intuitively, this derivative tells us in which direction we should move to descent down the hill (minimize the cost function).


**Derivative** is part of calculus that represents the rate of change of a function at a given point. To be mathematically precise, the above term is the [**partial derivative**](https://developers.google.com/machine-learning/glossary#partial-derivative) of the cost function $J(w,b)$ with respect to the parameters $w$ and $b$. The _partial_ derivative is calculating the derivative (rate of change) of the cost function with respect to a single parameter while keeping all other parameters constant.

So, for $J(w,b)$, as we have two parameters $w$ and $b$, we need to calculate two partial derivatives: $\frac{\partial J(w,b)}{\partial w}$ and $\frac{\partial J(w,b)}{\partial b}$, one for each parameter while keeping the other constant.


**4. Update the Parameters:**

Then we simultaneously (at the same time) update the parameters $w$ and $b$ in the opposite direction of the gradient (to descent down the hill) by a small step size $r$.

$$w_{\text{new}} = w_{\text{current}} - r \frac{\partial J(w,b)}{\partial w}$$
$$b_{\text{new}} = b_{\text{current}} - r \frac{\partial J(w,b)}{\partial b}$$

where:
- $w_{\text{new}}$ and $b_{\text{new}}$ are the updated values of the parameters.
- $w_{\text{current}}$ and $b_{\text{current}}$ are the current values of the parameters.
- $r$ is the learning rate, which controls the step size in the parameter space.

[**learning rate**](https://developers.google.com/machine-learning/glossary#learning-rate) and **step size** are used interchangeably in machine learning. It determines how much we move in the direction of the gradient at each iteration.


**5. Repeat until Convergence:**

We repeat from step 2 (compute the cost function) to step 4 (update the parameters) iteratively, until we reach a point (a local or global minimum) where the cost function doesn't decrease further. In other words, parameters $w$ and $b$ don't change much with each iteration, and the cost function doesn't decrease significantly. This is called [**convergence**](https://developers.google.com/machine-learning/glossary#convergence).
