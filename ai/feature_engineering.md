# Feature Engineering

Feature engineering is the process of transforming and selecting data representations to best capture information relevant for model training and performance. It can include creating new features, transforming existing features, and selecting the most relevant features for the model.

It's a crucial step in the machine learning workflow, as it can significantly impact the performance of the model.


Features is simple terms are the input data that we provide to the model for training and prediction. In the house price prediction example, features could be the number of bedrooms, bathrooms, square footage, etc, and the target variable would be the price.

In math term we show the features as $x_1, x_2, \dots, x_n$ or as a vector $\vec{\mathbf{x}} = [x_1, x_2, \dots, x_n]$.

For example, in a dataset of house prices with 3 features, we have vector of features $\vec{\mathbf{x}}$
- $x_1$: size
- $x_2$: number of bedrooms
- $x_3$: number of bathrooms

Which we can represent as a vector:

$$\vec{\mathbf{x}} = [x_1, x_2, x_3]$$


We show the our training set (the dataset of $m$ data points), as matrix $X$ of size $m \times n$ where each row is a data point and each column is a feature.
$$X = \begin{bmatrix} x_1^{(1)} & x_2^{(1)} & x_3^{(1)} \\ x_1^{(2)} & x_2^{(2)} & x_3^{(2)} \\ \vdots & \vdots & \vdots \\ x_1^{(m)} & x_2^{(m)} & x_3^{(m)} \end{bmatrix}$$

Or using the vector notation:
$$X = \begin{bmatrix} \vec{\mathbf{x}}^{(1)} \\ \vec{\mathbf{x}}^{(2)} \\ \vdots \\ \vec{\mathbf{x}}^{(m)} \end{bmatrix}$$


## Types of Features


Features can be categorized into different types based on their characteristics:

- **Nominal Variables**: Categories with no intrinsic ordering (e.g., types of houses, car brands).

- **Ordinal Variables**: Categories with a clear ordering but unknown spacing between categories (e.g., socio-economic status like low, middle, and high).

- **Binary Variables**: A nominal variable with only two categories (e.g., gender male/female, yes/no decisions).

- **Continuous Variables**: Numeric variables that can take on an infinite number of values or any value within a range (e.g., temperature, price).

- **Discrete Variables**: Numeric variables that take on a countable number of values, often integers (e.g., number of bedrooms, count of items).

- **Interval Variables**: Numeric variables with meaningful, equal intervals between values but no true zero point (e.g., dates, IQ scores).

- **Ratio Variables**: Numeric variables with both equal intervals and a meaningful zero point, allowing for the calculation of ratios (e.g., height, weight, age, income).

- **Cyclical Variables**: Numeric or ordinal variables that repeat in a cycle (e.g., hours of the day, days of the week, months of the year).


## Feature Engineering Techniques
Common techniques for feature engineering include:
- Scaling
- Standardization
- Dimensionality Reduction
- Creating Polynomial Features
- One-Hot Encoding
- Date formatting
- Normalization


## Scaling
We use scaling to normalize the range of independent variables or features of data.

For example, in the house-price prediction example:

Training set:

| House | Size (sqm) | Bedrooms | Price ($1000s) |
|-------|------------|----------|----------------|
| 1     | 210        | 4        | 800            |
| 2     | 190        | 3        | 700            |
| 3     | 300        | 4        | 850            |
| 4     | 100        | 2        | 450            |
| 5     | 200        | 3        | 820            |
| 6     | 500        | 5        | 900            |

We can see that the range of values for each feature is different. Size is in hundreds, bedrooms are single digits, and price is in thousands. This difference in scale can affect the performance of some machine learning algorithms.

The linear regression model for house price prediction could be:

$\hat{y} = w_1 \cdot \text{Size} + w_2 \cdot \text{Bedrooms} + b$


A tiny change in the parameter $w_1$ for the size feature can have a much larger effect on the output of the model than the same change in the parameter $w_2$ for the number of bedrooms. This can lead to model bouncing back and forth during training, making it harder to converge.

Also, over sensitivty to the scale of the features can make the model less robust and more sensitive to noise in the data.

So, to avoid these issues, we scale the features to have a similar range of values.

**Scatter Plot of Features**

Scatter plots are a common and useful way to visualize the relationship between two variables (features). They can help identify patterns, trends, and relationships in the data.

![](images/scatter_plot_house_price1.png)

As you can see the scatter plot is a plot of one feature against another. It can show the relationship between the two features, the distribution of the data, and any patterns or trends that may exist between the two features.

In this example, it shows us the the _scale discrapency_ between the features. The size feature is in hundreds, while the number of bedrooms is in single digits. Larger-scaled features (like Size) tend to dominate, potentially leading to slow training, biased or suboptimal learning.

**Scaling Techniques**

Now, let's scale the size and bedrooms features to have a similar range of values. We can use multiple scaling techniques, which we go through some of the most common ones.

Let's first rewrite our training set in a matrix form.

$$X = \begin{bmatrix} 210 & 4 \\ 190 & 3 \\ 300 & 4 \\ 100 & 2 \\ 200 & 3 \\ 500 & 5 \end{bmatrix}$$

So, we have $m=6$ data points and $n=2$ features. We can represent the features as $x_1$ and $x_2$ or as a vector $\vec{\mathbf{x}} = [x_1, x_2]$.

For example, for the first data point, we have:

$$\vec{\mathbf{x}}^{(1)} = [210, 4]$$
$$x_1^{(1)} = 210 \quad \text{ and } \quad x_2^{(1)} = 4  \quad \text{ and } \quad y_1 = 800$$
$$
