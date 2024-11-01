# Glossary

## Scalar, Vector, Matrix, Tensor
### Scalar Value **$x$**
- **Represents:** A single **feature value** or element of a vector.
- **Example:** $x_j$ is the $j^{th}$ feature of a data point.
- **Usage example:** A single input feature in linear regression or neural networks.
$$f_{w,b}(x) = w_{1}x_{1} + w_{2}x_{2} + \dots + w_{n}x_{n} + b$$


### Vector **$\mathbf{x}$**
- **Represents:** A **data point** or **feature vector** consisting of multiple feature values.
- **Example:** $\mathbf{x}^{(i)}$ is the feature vector for the $i^{th}$ data point.
- **Usage example:** In regression or classification tasks, each input data point is a vector of n features:
$$\mathbf{x}^{(i)} = [x_1^{(i)}, x_2^{(i)}, \dots, x_n^{(i)}]$$


### Matrix (Dataset) $X$
- **Represents:** A **matrix** containing the entire dataset (or batch) with multiple feature vectors (data points). Each row corresponds to a data point, and each column corresponds to a feature.
- **Example:** $X \in \mathbb{R}^{m \times n}$, where $m$ is the number of data points, and $n$ is the number of features.
- **Usage example:** In linear regression, $X$ is the **matrix**:
 $$
    X =
    \begin{bmatrix}
    \mathbf{x}^{(1)} \\
    \mathbf{x}^{(2)} \\
    \vdots \\
    \mathbf{x}^{(m)}
    \end{bmatrix}
 $$
Used in batch operations, multiplication of input matrix $X$ with weight matrix $\mathbf{W}$, etc.
$$\hat{\mathbf{Y}} = X \cdot \mathbf{W} + \mathbf{b}$$


|Symbol|Meaning|Example|Usage|
|-|-|-|-|
| $x$ | Scalar feature value | $x_j$ = value of feature $j$ | Single feature in a model |
| $\mathbf{x}$ | Feature vector (data point) | $\mathbf{x}^{(i)} = [x_1, x_2, \dots, x_n]$ | Input vector for one data point |
| $X$ | Dataset matrix | $X \in \mathbb{R}^{m \times n}$ | Matrix containing all data points |


### Vector and Matrix Operations

The following is the Linear Regression Model in Vector Form:

$$f_{w,b}(x^{(i)}) = w_1 x_1^{(i)} + w_2 x_2^{(i)} + \dots + w_n x_n^{(i)} + b$$

This sums the contributions of the input features $x_1, x_2, \dots, x_n$ with corresponding weights $w_1, w_2, \dots, w_n$. However, we can write this more compactly using **vectors** and **matrix multiplication** as follows:


$$f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}) = \vec{\mathbf{w}}^T \vec{\mathbf{x}}^{(i)} + b$$

- **$\vec{\mathbf{w}}$**: Column vector of weights.

$$\vec{\mathbf{w}} = \begin{bmatrix} w_1 \\ w_2 \\ \vdots \\ w_n \end{bmatrix} \quad \in \mathbb{R}^n$$

- **$\vec{\mathbf{x}}^{(i)}$**: Column vector of input features for the $i^{th}$ data point.

$$\vec{\mathbf{x}}^{(i)} = \begin{bmatrix} x_1^{(i)} \\ x_2^{(i)} \\ \vdots \\ x_n^{(i)} \end{bmatrix} \quad \in \mathbb{R}^n$$

**Row vs Column Vectors**

**Column Vector**: is a vector with $n$ rows and 1 column (i.e., $n \times 1$).

**Row Vector**: is a vector with 1 row and $n$ columns (i.e., $1 \times n$).

**Transpose**: transpose is an operation that flips a matrix over its diagonal, i.e., the rows become columns and vice-versa. So, for transpose of a column vector (size $n \times 1$), we get a row vector (size $1 \times n$).

In the context of machine learning, we often use **column vectors** for input features and weights. So, we assume vectors like $\vec{\mathbf{w}}$ and $\vec{\mathbf{x}}^{(i)}$ are **column vectors** with $n$ rows and 1 column (i.e., $n \times 1$). which $n$ is the number of features.

However to compute dot product of two vectors, one of them should be converted to a row vector. So, we take the transpose of the weight vector $\vec{\mathbf{w}}$ to get a row vector $\vec{\mathbf{w}}^T$. Then the dot product of $\vec{\mathbf{w}}^T$ and $\vec{\mathbf{x}}^{(i)}$ gives a scalar value.

$\vec{\mathbf{w}}^T$: Transpose of the weight vector $\vec{\mathbf{w}}$. $\vec{\mathbf{w}}$ is a column vector (size $n \times 1$) which means $n$ rows and $1$ column, its **transpose** becomes a **row vector** (size $1 \times n$).

$$\vec{\mathbf{w}}^T = \begin{bmatrix} w_1 & w_2 & \dots & w_n \end{bmatrix} \quad \in \mathbb{R}^{1 \times n}$$


**Vector Multiplication: Dot Product as Matrix Multiplication**: In linear algebra, the dot product of two vectors can be represented as a matrix multiplication of a row vector and a column vector:

$$\vec{\mathbf{w}}^T \vec{\mathbf{x}}^{(i)} =  \begin{bmatrix} w_1 & w_2 & \dots & w_n \end{bmatrix} \begin{bmatrix} x_1^{(i)} \\ x_2^{(i)} \\ \vdots \\ x_n^{(i)} \end{bmatrix}$$

$$= w_1 x_1^{(i)} + w_2 x_2^{(i)} + \dots + w_n x_n^{(i)} = \text{scalar value}$$

In Matrix multiplication, when multiplying a $1 \times n$ row vector by an $n \times 1$ column vector, the result is a **scalar**. So, the model, $\vec{\mathbf{w}}^T \vec{\mathbf{x}}^{(i)} + b$ returns a **scalar value**, which represents the linear combination of inputs with weights plus the bias term.

> Note: For similicity this formula sometimes written without the transpose and ${i}^{th}$ index notations as follows:
> $$f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}) = \vec{\mathbf{w}} \cdot \vec{\mathbf{x}} + b$$

### **Multiple Data Points**
Similarly, we can represent all of the above for the entire dataset (or batch) of $m$ data points using _matrix representation_.

So, if we have multiple data points $\vec{\mathbf{x}}^{(1)}, \vec{\mathbf{x}}^{(2)}, \dots, \vec{\mathbf{x}}^{(m)}$, we can represent them in a matrix $X$.

$$X \in \mathbb{R}^{m \times n}$$

where:
- $m$ is the number of examples.
- $n$ is the number of features.


We can represent the dataset with $m$ data points as a matrix $X$:

$$X = \begin{bmatrix} \vec{\mathbf{x}}^{(1)} \\ \vec{\mathbf{x}}^{(2)} \\ \vdots \\ \vec{\mathbf{x}}^{(m)} \end{bmatrix} = \begin{bmatrix} x_1^{(1)} & x_2^{(1)} & \dots & x_n^{(1)} \\ x_1^{(2)} & x_2^{(2)} & \dots & x_n^{(2)} \\ \vdots & \vdots & \ddots & \vdots \\ x_1^{(m)} & x_2^{(m)} & \dots & x_n^{(m)} \end{bmatrix}$$

where:
- Each row represents a data point.
- $m$ is the number of data points.
- $n$ is the number of features.

We can represent the weights $\vec{\mathbf{w}}$ as a column vector:
$$\vec{\mathbf{w}} = \begin{bmatrix} w_1 \\ w_2 \\ \vdots \\ w_n \end{bmatrix} \quad \in \mathbb{R}^n$$


So, the complete linear regression model for the entire dataset can be represented in matrix form as:

$$\hat{\mathbf{y}} = X \cdot \vec{\mathbf{w}} + b$$

where:
- $\hat{\mathbf{y}}$ is the vector of predicted target values for all data points.
- $X$ is the matrix of input features.
- $\vec{\mathbf{w}}$ is the weight vector.
- $b$ is a scalar value which is the bias term.


We can expand the above in this way:

$$\begin{bmatrix} \hat{y}^{(1)} \\ \hat{y}^{(2)} \\ \vdots \\ \hat{y}^{(m)} \end{bmatrix} = \begin{bmatrix} x_1^{(1)} & x_2^{(1)} & \dots & x_n^{(1)} \\ x_1^{(2)} & x_2^{(2)} & \dots & x_n^{(2)} \\ \vdots & \vdots & \ddots & \vdots \\ x_1^{(m)} & x_2^{(m)} & \dots & x_n^{(m)} \end{bmatrix} \begin{bmatrix} w_1 \\ w_2 \\ \vdots \\ w_n \end{bmatrix} + b$$

> When working with matrix $X$ (size $m \times n$) and weight vector $\vec{\mathbf{w}}$ (size $n \times 1$), we no longer need to transpose the weights vector $\vec{\mathbf{w}}$ because $X$ is already structured so that each **row** corresponds to a data point and each **column** corresponds to a feature.
>
> Multiplying $X$ by $\vec{\mathbf{w}}$ directly produces an $m \times 1$ vector, where each element $\hat{y}^{(i)}$ is the dot product between the $i$-th row of $X$ (representing the features for the $i$-th data point) and the weights vector $\vec{\mathbf{w}}$. So, no transposition is required here!
