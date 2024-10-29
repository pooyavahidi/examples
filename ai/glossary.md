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
