# Gradient Descent
Gradient Descent is an optimization algorithm used to minimize any function that can be expressed as a sum of differentiable functions.

> Gradient Descent is the most common algorithm used for minimizing the cost function of many machine learning models, from linear regression to the most complex neural networks. It can minimize cost functions with any number of parameters $J(w_1, w_2, ..., w_n, b)$.

The Gradient Descent algorithm start with an initial guess for the parameters, then iteratively adjust these parameters to move towards a minimum of the function.




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
2. **Compute the Cost Function:** Calculate the cost function $J(w,b)$ with the new values of $w$ and $b$. Also called the **forward pass**.
3. **Compute the Gradient:** Calculate the derivative of the cost function $J(w,b)$ at the current point with respect to the parameters $w$ and $b$. Also called the **backward pass** or **backpropagation**.
4. **Update the Parameters:** Update the parameters $w$ and $b$ in the opposite direction of the gradient (to descent down the hill) by a small step size $\alpha$.
5. **Repeat until Convergence:** Repeat from step 2, until we reach a point where parameters $w$ and $b$ don't change much with each iteration, and the cost function doesn't decrease significantly. This is called **convergence**.


Steps 1 and 2 are self-explanatory and have been discussed previously. So, we will focus on steps 3 onwards.

### 3. Compute the Gradient

At each step of the gradient descent algorithm, we calculate the derivative of the cost function with respect to each parameter. In other words, we calculate the rate of change of the cost function with respect to each parameter. This tells us how much the cost function will change if we change the parameters slightly in a particular direction.

The following is the **derivative** of the cost function $J(w,b)$ with respect to the parameters $w$ and $b$:

$$\frac{\partial J(w,b)}{\partial w}$$
$$\frac{\partial J(w,b)}{\partial b}$$

Intuitively, this derivative tells us in which direction we should move to descent down the hill (minimize the cost function).


**Derivative** is part of calculus that represents the rate of change of a function at a given point. To be mathematically precise, the above term is the [**partial derivative**](https://developers.google.com/machine-learning/glossary#partial-derivative) of the cost function $J(w,b)$ with respect to the parameters $w$ and $b$. The _partial_ derivative is calculating the derivative (rate of change) of the cost function with respect to a single parameter while keeping all other parameters constant.

So, for $J(w,b)$, as we have two parameters $w$ and $b$, we need to calculate two partial derivatives: $\frac{\partial J(w,b)}{\partial w}$ and $\frac{\partial J(w,b)}{\partial b}$, one for each parameter while keeping the other constant.


#### multi-dimentional surface and partial derivatives

$J$ is a function of $w$ and $b$, so it's a 3D plot of $w$, $b$, and $J$. Also the number of parameters can be more than 2, so the cost function $J$ can be a function of $n$ parameters $w_1, w_2, ..., w_n$. In that case, the cost function $J$ is a plot of $w_1, w_2, ..., w_n$, and $J$, which is a multi-dimensional surface.

However, the partial derivatives are calculated for each parameter separately while keeping all other parameters constant. For example, the partial derivative of $J$ with respect to $w_1$ is calculated while keeping $w_2, w_3, ..., w_n,b$ costant. So, the partial derivative of $J$ with respect to $w_1$ is a 2-dimensional plot of $w_1$ and $J$ while keeping all other parameters constant.

For example, the partial derivative of the cost function $J(w,b)$ with respect to the parameter $w$ is when we calculate the derivate of $J$ with respect to $w$ while keeping $b$ constant.

$$\frac{\partial J(w)}{\partial w}$$

> Derivative of a function at a point gives the _slope_ of the _tangent line_ to the function at that point. In the context of gradient descent, the derivative of the cost function tells us the slope of the cost function at a particular point in the parameter space. This slope guides us in the direction of the steepest descent (down the hill) to minimize the cost function.

#### Slope and Tangent Line
**Slope** is the ratio of the vertical change to the horizontal change between two distinct points. In other words the _rise_ over the _run_:
$$\text{slope} = \frac{\text{rise}}{\text{run}}$$


For example in 2D plane of $x$ and $y$ coordinates, the slope of the tangent line passing through two points $(x_1, y_1)$ and $(x_2, y_2)$ is:

$$\text{slope} = \frac{y_2 - y_1}{x_2 - x_1}$$


**Partial Derivative (Instantaneous Slope)**

The **partial derivative**, gives the **instantaneous rate of change** at a single point. Instead of measuring the slope between two distinct points, the partial derivative looks at how the function changes as you make an infinitesimally small change in one variable (in your case, $w$) while holding all other variables constant.

![slope_tangent_line](images/gd_slope_derivative.png)

Slope between two points of $a$ and $b$:

$$\text{slope} = \frac{\text{rise}}{\text{run}} = \frac{\Delta J(w)}{\Delta w}=\frac{-3}{1} = -3$$

Slope of $-3$ is a _negative_ slope, which means the function is decreasing as $w$ increases.

Now, to find the **exact** slope at any point like $p$, we need to draw a _tangent line_ at that point to find the slope of the function at that point.

**Tangent Line** is a straight line that touches a curve at a single point. The slope of the tangent line at that point is the derivative of the function at that point. The derivative gives the rate of change of the function at that point.

In order to find the slope at point $p$, we need to make the change in $w$ extremely small (infinitesimally small) to capture the exact rate of change at that point. This is expressed as:

$$\frac{\partial J(w)}{\partial w} = \lim_{\Delta w \to 0} \frac{\Delta J(w)}{\Delta w}$$

This limit gives us the **exact slope** at a particular point, also known as the **instantaneous rate of change** of the function $J(w)$ with respect to $w$.

The partial derivative is essentially the limit of the slope as the two points get closer and closer together, until they are infinitesimally close.


>The derivative is a more precise, continuous version of the slope, calculated as $\Delta w$ approaches an extremely small value. It maximizes the resolution (or sensitivity) of how the function $J(w)$ changes as $w$ changes. To increase this resolution, we need to make the changes in $w$ extremely small to capture the smallest impact on the function. That’s why we express this as $\lim_{\Delta w \to 0}$, where the change in $w$ becomes vanishingly small to capture the exact rate of change (with the highest resolution) at any given point.

Thus:

$$\text{slope exactly at any given point} = \frac{\partial j(w)}{\partial w}$$
"slope at any given point" means the rate of change of the function $J(w) with respect to $w$ at that point.


### 4. Update the Parameters:

Then we simultaneously (at the same time) update the parameters $w$ and $b$ in the opposite direction of the gradient (to descent down the hill) by a small step size $r$.

$$w_{\text{new}} = w_{\text{current}} - \alpha \frac{\partial J(w,b)}{\partial w}$$
$$b_{\text{new}} = b_{\text{current}} - \alpha \frac{\partial J(w,b)}{\partial b}$$

where:
- $w_{\text{new}}$ and $b_{\text{new}}$ are the updated values of the parameters.
- $w_{\text{current}}$ and $b_{\text{current}}$ are the current values of the parameters.
- $\alpha$ is the learning rate, which controls the step size in the parameter space.

>In machine learning literature, another common notation for the above is:
>
>$$\theta_{t+1} = \theta_t - \eta \nabla_{\theta} J(\theta_t)$$
>
>Where:
>- $\theta_t$ represents the parameters (weights and biases) at step $t$.
>- $\eta$ is the learning rate.
>- $\nabla_{\theta} J(\theta)$ is the gradient of the cost function $J$ with respect to the parameters $\theta$.

#### Moving Towards the Minimum

![update_parameters](images/gd_update_parameters.png)

In the Positive Slope:

$\text{slope}= \frac{\partial J(w)}{\partial w} > 0$

$w_{\text{new}} = w_{\text{current}} - \alpha \times \text{postive number}$

$w_{\text{new}} < w_{\text{current}}$

So, when the slope is positive, the new value of $w$ is less than the current value of $w$. This means we move in the opposite direction of the slope (down the hill) to minimize the cost function.

In the Negative Slope:

$\text{slope}= \frac{\partial J(w)}{\partial w} < 0$

$w_{\text{new}} = w_{\text{current}} - \alpha \times \text{negative number}$

$w_{\text{new}} > w_{\text{current}}$

So, when the slope is negative, the new value of $w$ is greater than the current value of $w$.

In both cases, we want to find the direction which moves us towards the minimum of the cost function, which means we move in the **opposite** direction of the slope.

#### Learning Rate
[**learning rate**](https://developers.google.com/machine-learning/crash-course/linear-regression/hyperparameters#learning_rate) and **step size** are used interchangeably in machine learning. It determines how much we move in the direction of the gradient at each iteration.

The learning rate is one of the most important _hyperparameters_ in the gradient descent algorithm. It directly affects the size of movements (descents) towards the minimum of the cost function. So, choosing the right learning rate is crucial.

$$w = w - \textcolor{red}{\alpha} \frac{\partial J(w,b)}{\partial w}$$

> Learning rate is also represented by $\eta$ (pronounced "eta") in many machine learning literature.


**Size of Slop and Learning Rate**
the steps in gradient descent are identical because the movement size depends on both factor, the gradient's magnitude (slope of the cost function at that point), and the learning rate. Assuming the learning rate is fixed, the size of the step depends on the slope (derivative) of the cost function at that point.

At ever step, we reduce $\alpha\frac{\partial J(w,b)}{\partial w}$ from the current value of $w$ to move towards the minimum of the cost function. So, considering fix $\alpha$, the larger the slope is, the larger the step size is, and the smaller the slope is, the smaller the step size is.


![](images/gd_slope_size_learning_rate.png)

In the above image, we can see the larger the slope is, the larger the step size, and when we get close to the minimum, the step gets smaller as the slope gets smaller.


**Too Small or Too Large Learning Rate**

![](images/gd_learning_rate_small_large.png)

**When the learning rate is too small**: The gradient descent may work, but it will be too slow.

As we saw earlier, the slope is the key factor in the size of the step. So, these small steps get even smaller as we go down the hill (slope gets smaller).

**When the learning rate is too large**: The gradient descent may overshoot the minimum and never converge (diverge).

Again here as we can see from the image, the overshooting gets larger as we go up the hill (slope gets larger). So, instead of going down the hill towards the minimum, the gradient descent algorithm may overshoot and diverge (gets further away from the minimum).



### 5. Repeat until Convergence:

We repeat from step 2 (compute the cost function) to step 4 (update the parameters) iteratively, until we reach a point (a local or global minimum) where the cost function doesn't decrease further. In other words, parameters $w$ and $b$ don't change much with each iteration, and the cost function doesn't decrease significantly. This is called [**convergence**](https://developers.google.com/machine-learning/glossary#convergence).

> Note that it's mentioned "until we reach a local or global minimum". So, there is always a possibility that the algorithm may get stuck at a local minimum instead of the global minimum. There are ways to avoid this which we will discuss later.


### Gradient Descent In Summary:
We can simply summarize all the steps of the Gradient Descent algorithm as follows:

$\text{repeat until convergence:\{} \\
\quad w = w - \alpha \frac{\partial J(w,b)}{\partial w} \\
\quad b = b - \alpha \frac{\partial J(w,b)}{\partial b} \\
\text{\}}$



> This whole process of running the Gradient Descent algorithm, is also called **training** the model. The goal of training is to find the best values of the parameters (weights and biases) that minimize the cost function $J$.
