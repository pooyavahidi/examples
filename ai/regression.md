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

The output (target) value of the first training example is $400,000
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

$$f_{w,b}(x^{(i)}) = wx^{(i)} + b$$

where:
- $w$: weight (slope) of the line
- $b$: bias (y-intercept) of the line
- $x^{(i)}$: input feature of the $i^{th}$ training example

For simplicity, we can write the above function as:
$$f(x) = wx + b$$

The above function is a linear function which represent a straight line with slope $w$ and y-intercept $b$. Different values of $w$ and $b$ will give different lines.

As described, the model output $\hat{y}$ is the predicted value of the target variable $y$. So, for the $i^{th}$ training example, the predicted value $\hat{y}^{(i)}$ would be:

$$f_{w,b}(x^{(i)})= \hat{y}^{(i)}$$
