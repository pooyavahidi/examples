# Vectors and Matrices

## Vector Operations
Operations on two vectors are performed **element-wise**. For example, addition of two vectors $\vec{\mathbf{a}}$ and $\vec{\mathbf{b}}$ is done by adding corresponding elements of the two vectors.

Give the two vectors:

$$\vec{\mathbf{a}} = \begin{bmatrix} a_1 \\ a_2 \\ \vdots \\ a_n \end{bmatrix} \text{ , } \vec{\mathbf{b}} = \begin{bmatrix} b_1 \\ b_2 \\ \vdots \\ b_n \end{bmatrix}$$

### Addition of vectors
The sume of two vectors results in a new vector with the same size.
$$c_i = a_i + b_i \text{ ,} \quad \vec{\mathbf{c}}=\vec{\mathbf{a}}+\vec{\mathbf{b}} = \begin{bmatrix} a_1+b_1 \\ a_2+b_2 \\ \vdots \\ a_n+b_n \end{bmatrix}$$

### Subtraction of vectors
The difference of two vectors results in a new vector with the same size.
$$c_i = a_i - b_i \text{ ,} \quad \vec{\mathbf{c}} = \vec{\mathbf{a}} - \vec{\mathbf{b}} = \begin{bmatrix} a_1 - b_1 \\ a_2 - b_2 \\ \vdots \\ a_n - b_n \end{bmatrix}$$

### Dot product of vectors
The dot product of two vectors is the sum of the products of their corresponding elements. So, the dot product of two vectors is a **scalar** value.

$$\vec{\mathbf{a}} \cdot \vec{\mathbf{b}} = a_1b_1 + a_2b_2 + \dots + a_nb_n = \vec{\mathbf{a}} \cdot \vec{\mathbf{b}} = \sum_{i=1}^{n} a_ib_i$$

### Multiplication of vectors by a scalar
Multiplying a vector by a scalar results in a new vector with the same size.

$$
\alpha \in \mathbb{R} \quad \Rightarrow \quad \alpha \vec{\mathbf{a}} = \begin{bmatrix} \alpha a_1 \\ \alpha a_2 \\ \vdots \\ \alpha a_n \end{bmatrix}
$$


## Matrix Operations
Operations on two matrices are performed **element-wise**. For example, addition of two matrices $\mathbf{A}$ and $\mathbf{B}$ is done by adding corresponding elements of the two matrices.

Given the two matrices:
$$A=\begin{bmatrix} a_{11} & a_{12} & \dots & a_{1n} \\ a_{21} & a_{22} & \dots & a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1} & a_{m2} & \dots & a_{mn} \end{bmatrix} \text{ , } B=\begin{bmatrix} b_{11} & b_{12} & \dots & b_{1n} \\ b_{21} & b_{22} & \dots & b_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ b_{m1} & b_{m2} & \dots & b_{mn} \end{bmatrix}$$

### Addition of matrices

$$C = A + B = \begin{bmatrix} a_{11}+b_{11} & a_{12}+b_{12} & \dots & a_{1n}+b_{1n} \\ a_{21}+b_{21} & a_{22}+b_{22} & \dots & a_{2n}+b_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1}+b_{m1} & a_{m2}+b_{m2} & \dots & a_{mn}+b_{mn} \end{bmatrix}$$


### Subtraction of matrices
$$C = A - B = \begin{bmatrix} a_{11}-b_{11} & a_{12}-b_{12} & \dots & a_{1n}-b_{1n} \\ a_{21}-b_{21} & a_{22}-b_{22} & \dots & a_{2n}-b_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ a_{m1}-b_{m1} & a_{m2}-b_{m2} & \dots & a_{mn}-b_{mn} \end{bmatrix}$$

### Multiplication by a scalar
$$\alpha \in \mathbb{R} \quad \Rightarrow \quad \alpha A = \begin{bmatrix} \alpha a_{11} & \alpha a_{12} & \dots & \alpha a_{1n} \\ \alpha a_{21} & \alpha a_{22} & \dots & \alpha a_{2n} \\ \vdots & \vdots & \ddots & \vdots \\ \alpha a_{m1} & \alpha a_{m2} & \dots & \alpha a_{mn} \end{bmatrix}$$

### Matrix Multiplication
Matrix multiplication is a bit more complex than element-wise operations. The product of two matrices $A$ and $B$ is defined only if the number of columns in $A$ is equal to the number of rows in $B$. If $A$ is of size $m \times n$ and $B$ is of size $n \times p$, then the product $C = A \cdot B$ is of size $m \times p$.

> $A$ of size $m \times n$ and $B$ of size $n \times p$ $\Rightarrow$ $C$ of size $m \times p$.
>
> Columns of $A$ must be equal to rows of $B$.

$$C = A \cdot B = \begin{bmatrix} c_{11} & c_{12} & \dots & c_{1p} \\ c_{21} & c_{22} & \dots & c_{2p} \\ \vdots & \vdots & \ddots & \vdots \\ c_{m1} & c_{m2} & \dots & c_{mp} \end{bmatrix}$$

$$c_{ij} = \sum_{k=1}^{n} a_{ik}b_{kj}$$

> Both notations of $A.B$ or $A \times B$ are used for matrix multiplication.

For example, given matrices $A$ (2x3) and $B$ (3x2):

$$A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix} \text{ , } B = \begin{bmatrix} 7 & 8 \\ 9 & 10 \\ 11 & 12 \end{bmatrix}$$

So for $C = A \cdot B$:

$$C=A \cdot B = \begin{bmatrix} 1 \cdot 7 + 2 \cdot 9 + 3 \cdot 11 & 1 \cdot 8 + 2 \cdot 10 + 3 \cdot 12 \\ 4 \cdot 7 + 5 \cdot 9 + 6 \cdot 11 & 4 \cdot 8 + 5 \cdot 10 + 6 \cdot 12 \end{bmatrix} = \begin{bmatrix} 58 & 64 \\ 139 & 154 \end{bmatrix}$$

We can think of matrix multiplication as a series of dot products between rows of the first matrix and columns of the second matrix.

$$C=\begin{bmatrix} \text{A row 1} \cdot \text{B column 1} & \text{A row 1} \cdot \text{B column 2} \\ \text{A row 2} \cdot \text{B column 1} & \text{A row 2} \cdot \text{B column 2} \end{bmatrix}$$

Or in a more general form:

$$C_{ij} = \sum_{k=1}^{n} A_{ik} \cdot B_{kj}$$

> **Note**: The above also is written without the dot notation as follows:
> $$C_{ij} = \sum_{k=1}^{n} A_{ik} B_{kj}$$

**Matrix Multiplication is not Commutative**
In general, matrix multiplication is not commutative, meaning that the order of matrices in a product matters. Swapping the order of matrices in a product usually yields a different result.

$$A \cdot B \neq B \cdot A$$

**Matrix-Vector Multiplication**
This is a special case of matrix multiplication where one of the matrices has only one column or row, i.e. a vector.

$$A = \begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \text{ , } \vec{\mathbf{b}} = \begin{bmatrix} 5 \\ 6 \end{bmatrix}$$

$$\vec{\mathbf{c}} = A \cdot \vec{\mathbf{b}} = \begin{bmatrix} 1 \cdot 5 + 2 \cdot 6 \\ 3 \cdot 5 + 4 \cdot 6 \end{bmatrix} = \begin{bmatrix} 17 \\ 39 \end{bmatrix}$$
$$
