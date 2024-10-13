# Gradient Descent
Gradient Descent is an optimization algorithm used to minimize any function that can be expressed as a sum of differentiable functions.


> Gradient Descent is not only for cost functions, but it can be used to minimize any function. However, in this context, we commonly apply it to minimize the cost function $J(w,b)$.

The idea is to start with an initial guess for the parameters $w$ and $b$, then change the parameters $w$ and $b$ iteratively to move towards a minimum of the function.



Steps:
1. Start with an initial guess for the parameters $w$ and $b$.
2. Compute the cost function $J(w,b)$ with the current values of $w$ and $b$. Also called **forward pass**.
3. Compute the gradient of the cost function $J(w,b)$ at the current point with respect to the parameters $w$ and $b$. Also called **backward pass** or **backpropagation**.
4. Update the parameters $w$ and $b$ in the opposite direction of the gradient (to descent down the hill) by a small step size $r$.
5. Repeat steps 2 to 4, until we settle at or near the global minimum (convergence).


> A cost function could have a complex surface (other than squared error) with more than one minimum. These are called **local minima**. The lowest point in the entire function is called the **global minimum**.

![complex_loss_surface](images/gd_complex_loss_surface.png)

As you can see, the cost function $J(w,b)$ has a complex surface with multiple local minimas with one global minimum. The intuitive idea is to see this as a terrain in a hilly area where you want to reach the lowest valley (global minimum) by descending down the hill using the shortest path (steepest descent) possible.

**loss surface** is a graphical representation of a model's loss function in relation to its parameters (e.g., weights and biases). It shows how the loss changes as parameters vary, helping visualize the optimization process. The surface often features local minima, saddle points, and a global minimum, which optimization algorithms aim to find.

[**Convex**](https://developers.google.com/machine-learning/glossary#convex-function) surfaces such as _square error loss_ has a single global minimum, making optimization easier. **Non-convex** surfaces have multiple local minima, making optimization more challenging.
