# Regression

Regression is a type of supervised learning algorithm that predicts a number (continuous value) based on input data. Regression models are trained on labeled data, pair of $Input(X) \rightarrow Output(Y)$ to make predictions on new, unseen data.

The model learns to predict a continuous value by comparing its predictions with the correct output during the training process.

## Notations
**Training set:** A data set which consists of list of training examples (pairs of input and output data).

$X$: **input** variable (features)

$Y$: **output** or **target** variable

$m$: Total number of training examples in the training set.

$n$: total number of features. e.g. in house price prediction, $n$ could be the number of features like size, location, number of bedrooms, etc.
> If $n=1$, it's called **univariate regression** or regression with one variable. If $n>1$, it's called **multivariate regression**.

$(x, y)$: Single training example

We use superscript to denote the index of the training example. For example, $x^{(i)}$ denotes the input features of the $i^{th}$ training example.

$(x^{(i)}, y^{(i)})$: $i^{th}$ training example

For example, for house price prediction _training set_ with $m = 4$ training examples with $n = 2$ features (size and number of bedrooms) and the target value (price) for each example:

Item | Size (m²) | Number of bedrooms | Price in $1000's|
| ---| --- | --- | --- |
| 1 | 210 | 3 | 400 |
| 2 | 150 | 2 | 300 |
| 3 | 120 | 2 | 250 |
| 4 | 300 | 4 | 500 |


Looking at the $1^{st}$ training example:

210 m², 3 bedrooms are the features of the first training example.
$$x^{(1)} = [210, 3]$$

The output (target) value of the first training example is $400K.

$$y^{(1)} = 400$$

Then the complete notation of $1^{st}$ training example would be:

$(x^{(1)}, y^{(1)}) = ([210, 3], 400)$

## How Regression Works

The traning set (including both features and target values) will be given to the supervised learning algorithm. Then algorithm produce a model (function $f$) that maps the input features to the target value.

![Regression](images/regression1.png)

> The model is just a function (also called hypothesis) that maps the input features to the (estimated) target value $\hat{y}$. The model is trained to minimize the difference between the predicted (or estimated) value $\hat{y}$ and the actual target value $y$.


$y$: Actual target value

$\hat{y}$: Predicted target value (output of the model).

$f$: The model

$$f: x \rightarrow \hat{y}$$


For example, in the house price prediction example, the model $f$ would be a function that maps the size and number of bedrooms to the price of the house.

$$f: [size, bedrooms] \rightarrow price$$


## Linear Regression - Univariate Regression
Linear Regression with **one** variable (univariate regression) is a simplest form of regression model that assumes a linear relationship between the input feature and the target value.

This is the most basic form of regression where the model tries to fit a straight line that best represents the relationship between the input feature and the target value.


### Model function
The model function $f$ for linear regression is a linear function of the input feature $x$ (which is a function that maps from $x$ to $\hat{y}$).

The model:

$$f_{w,b}(x) = wx + b$$

$w$ and $b$ are called the **parameters** of the model. Also called **weights** and **bias**.

We can also write the model with the following notation:

$$f_{w,b}(x^{(i)}) = wx^{(i)} + b$$

where:
- $w$: weight (slope) of the line
- $b$: bias (y-intercept) of the line
- $x^{(i)}$: input feature of the $i^{th}$ training example



> In simple notation, the model function $f$ can be written as $f(x) = wx + b$


The above function is a linear function which represent a straight line with slope $w$ and y-intercept $b$. Different values of $w$ and $b$ will give different lines.

As described, the model output $\hat{y}$ is the predicted value of the target variable $y$. So, for the $i^{th}$ training example, the predicted value $\hat{y}^{(i)}$ would be:

$$f_{w,b}(x^{(i)})= \hat{y}^{(i)}$$


## Cost Function
So we have our model $f_{w,b}(x)$ defined. But, how do we know which values of $w$ and $b$ are the best? We need a way to measure how well the model is performing. In other words, how far or close the predicted value $\hat{y}$ is to the actual target value $y$(labels).


The goal is to find $w$ and $b$ which $\hat{y}$ is as close as possible to the actual target value $y$ for all training examples.


![cost_function](images/cost_function1.png)

**Error**: is the difference between the predicted value (by the model), and the actual target value.

$$Error =y_{pred} - y_{actual}$$

In a more formal way, Error is the difference between predicted value of the model for the $i^{th}$ training example (denoted as ${\hat{y}}^{(i)}$) and the actual target value $y^{(i)}$.

$$Error(\hat{y}^{(i)}, y^{(i)}) = \hat{y}^{(i)} - y^{(i)}$$



**Loss function**: A function that measures how well the model's prediction $\hat{y}$ for a single training example is compared to the actual target value $y$.

The _squared error_  and _absolute error_ are common [loss functions](https://developers.google.com/machine-learning/crash-course/linear-regression/loss#types_of_loss) used in regression models. Here, we will use the squared error loss function.

Squared Error Loss function:

$$Loss(\hat{y}^{(i)}, y^{(i)}) = (\hat{y}^{(i)} - y^{(i)})^2$$

Knowing that $\hat{y}^{(i)} = f_{w,b}(x^{(i)})$, we can write the loss function as:

$$Loss(f_{w,b}(x^{(i)}),y^{(i)}) = (f_{w,b}(x^{(i)}) - y^{(i)})^2$$


**Cost function**: A function denoted by $J(w,b)$ that measures the average loss over all training examples. This function is also called **Mean Squared Error (MSE)**.

$$J(w,b) = \frac{1}{2m} \sum\limits_{i = 1}^{m} (f_{w,b}(x^{(i)}) - y^{(i)})^2$$

where:
- $m$: total number of training examples
- $f_{w,b}(x^{(i)})$: predicted value for the $i^{th}$ training example


> Note: The terms **Loss** and **Cost** are often used interchangeably in machine learning. So, in many cases, they refer to the same thing.

### Recap
In the linear regression model, we have:

**Model:**

$$f_{w,b}(x) = wx + b$$

**Model Parameters:**

$$w, b$$

**Cost Function:** (using squared error loss function)

$$J(w,b) = \frac{1}{2m} \sum\limits_{i = 1}^{m} (f_{w,b}(x^{(i)}) - y^{(i)})^2$$

**Goal:**

Find the values of $w$ and $b$ that minimize the cost function $J(w,b)$, we can write this as:
$$w, b = \arg\min J(w,b)$$

> The process of achieving this goal is called **Training** the model.

### Minimizing the Cost Function

Let's visualize the $f_{w,b}(x)$ and the cost function $J(w,b)$ side by side to understand how the cost function changes with different values of $w$ and $b$.

For simplicity, let's assume $b=0$:

$$f_{w,b}(x) = f_{w}(x) = wx$$
and
$$J(w) = \frac{1}{2m} \sum\limits_{i = 1}^{m} (f_{w}(x^{(i)}) - y^{(i)})^2$$

Recall, the notation of $f_{w}(x)$ means that for **fixed value of $w$**. e.g. when $w=2$, then $f_{2}(x) = 2x$, or simply $f(x) = 2x$ which is just a function of $x$.

![cost_function](images/cost_function2.png)
The left side shows the model $f_{w,b}(x)$ which is a plot of $x$ and $y$. However, the right side shows the cost function $J(w,b)$ which is a plot of $w$ and $J$, showing the changes of cost $J$ with different values of $w$.

We can visually inspect the cost function $J(w)$ is at its minimum when $w$ is $1$.

Previously, we assumed $b=0$ for simplicity, the plot of cost function $J(w)$ is a 2D plot of $w$ and $J$ where $b$ is fixed at $0$. However, in reality, we have two parameters $w$ and $b$ that we need to optimize. So, the cost function $J(w,b)$ is a 3D plot of $w$, $b$, and $J$.

![cost_function](images/cost_function_3d_convex.png)

This is very similar to the 2D plot of $J(w)$, but now we have both $w$ and $b$ as parameters which create a 3D plot of $w$, $b$, and $J$.

As we can see, the minimum of the cost function $J(w,b)$ is at the very bottom of the bowl (where the cost $J$ is the lowest). This is called the **global minimum** of the cost function which is indicated by dark blue color.

This bowl shape of the cost function $J(w,b)$ is called a **convex function**.

### How to Minimize the Error Efficiently?
Now we need an efficient way to find the best values of $w$ and $b$ that minimize the cost function $J$ in a systematic way. [Gradient Descent](gradient_descent.md) is one of the most important algorithms in machine learning for doing that. It is used not only in linear regression but also in larger and more complex models.

## Gradient Descent for Linear Regression
Gradient Descent is an optimization algorithm used to minimize the cost function $J(w,b)$ by iteratively moving towards the minimum of the cost function.  For more details see [Gradient Descent](gradient_descent.md).

Gradient Descent Algorithm:

$\text{repeat until convergence:\{} \\
\quad w = w - \alpha \frac{\partial J(w,b)}{\partial w} \\
\quad b = b - \alpha \frac{\partial J(w,b)}{\partial b} \\
\text{\}}$

Linear Regression Model:
$$f_{w,b}(x) = wx + b$$

MSE Cost Function:
$$J(w,b) = \frac{1}{2m} \sum\limits_{i = 1}^{m} (f_{w,b}(x^{(i)}) - y^{(i)})^2$$


Let's calculate the partial derivatives of the cost function $J(w,b)$ with respect to the parameters $w$ and $b$.

$w= w - \alpha \frac{\partial J(w,b)}{\partial w}$

$$\frac{\partial J(w,b)}{\partial w} = \frac{\partial}{\partial w} \left( \frac{1}{2m} \sum\limits_{i = 1}^{m} (f_{w,b}(x^{(i)}) - y^{(i)})^2 \right)$$

We know $f_{w,b}(x) = wx + b$, so we can substitute $f_{w,b}(x)$ in the above equation:

$$\frac{\partial J(w,b)}{\partial w} = \frac{\partial}{\partial w} \left( \frac{1}{2m} \sum\limits_{i = 1}^{m} (wx^{(i)} + b - y^{(i)})^2 \right)$$
