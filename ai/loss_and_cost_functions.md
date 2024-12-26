# Loss and Cost Functions

In machine learning, a **loss function** quantifies how well our model's predictions match the actual or true values from the data. Think of it as a measure of **error**:
- If the model's predictions are very good, the loss (error) is near zero.
- If the model's predictions deviate from the truth, the more it deviates, the higher the loss (error).

The main goal during the training of a machine learning model is to minimize this loss function to improve the accuracy of the model's predictions.

**Loss Function**:<br>
Formally, a loss function $L$ is a function that takes as input:

$$ L(\hat{y}, y) = \text{error }$$

where:
- $\hat{y}$: the predicted value output by the model for a single instance.
- $y$: the true value for that instance.
- $\text{error}$: A non-negative real number, interpreted as the **error** or **penalty** for the model's prediction.

> In some texts, the **loss function** is also denoted by a lowercase $\ell$ (the Greek letter “ell”):
>
>$$\ell\bigl(\hat{y}, y\bigr)$$

For the model $f_{\mathbf{W}, \vec{\mathbf{b}}}$, which outputs predictions $\hat{y} = f_{\mathbf{W}, \vec{\mathbf{b}}}(\mathbf{x})$, the loss for a single instance is  written as:
$$
L(\hat{y}, y) = L(f_{\mathbf{W}, \vec{\mathbf{b}}}(\mathbf{x}), y)
$$

where:
- **$f$**: The machine learning model that maps input features $\mathbf{x}$ to output predictions $\hat{y}$.
- **$\hat{y}$**: The predicted value output by the model.
- **$\mathbf{W}$**: The weights of the model, representing the learnable parameters associated with each input feature. $\mathbf{W}$ is a **matrix** whose shape depends on the type of model:
    - For **linear regression** or **logistic regression**, $\mathbf{W}$ is a vector of shape $(m, 1)$, where $m$ is the number of input features.
    - For **neural networks**, $\mathbf{W}$ is a matrix of shape $(h, m)$, where $h$ is the number of neurons in the current layer, and $m$ is the number of inputs (or neurons in the previous layer).
- **$\vec{\mathbf{b}}$**: The biases of the model, for each output:
  - $\vec{\mathbf{b}}$ is a **vector**, where its length corresponds to the number of neurons in the current layer.
  - For simpler models like linear regression, the bias is a **scalar** $b$.
  - Sometime for batch processing, we use $B$ as the bias matrix which is a matrix of shape $(h, m)$, where $h$ is the number of neurons in the current layer, and $m$ is the number of instances in the batch.

**Using $\theta$ (theta) notation**:<br>
For simplicity, it's common to use a single parameter set $\theta$ to represent all the learnable parameters of the model, including the weights $\mathbf{W}$ and biases $\vec{\mathbf{b}}$. In this case, the loss function is written as:

$$
L\bigl(\hat{y}, y\bigr) \;=\; L(f_\theta(\mathbf{x}),\, y)
$$

where:
- $\theta$ encapsulates $\mathbf{W}$ and $\vec{\mathbf{b}}$ (all the learnable parameters of the model).


## Loss vs Cost Functions

While the terms **loss** and **cost** are often used interchangeably, they have distinct meanings:

- **Loss Function**: Measures error for a **single instance**, denoted as $L(\hat{y}, y)$.
- **Cost Function**: Aggregates the loss over the entire dataset, giving an overall measure of model performance. Typically, the cost function is the **average loss** across $m$ instances:
$$
J(\mathbf{W}, \vec{\mathbf{b}}) = \frac{1}{m} \sum_{i=1}^{m} L(f_{\mathbf{W}, \vec{\mathbf{b}}}(\mathbf{x}^{(i)}), y^{(i)})
$$

**Using $\theta$ (theta) notation**:<br>
In here again, for simplicity, we use a single parameter set $\theta$ to represent all the learnable parameters of the model. The cost function is written as:

$$
J(\theta) = \frac{1}{m} \sum_{i=1}^{m} L(f_\theta(\mathbf{x}^{(i)}), y^{(i)})
$$


> Both Loss $L$ and Cost $J$ are scalar values (non-negative real numbers) that quantify the error between the model's predictions and the true values.

Loss functions vary across models and problems, chosen based on the use-case, data, and objectives. The cost function is simply the average of these losses over the training set (or batch).

**Cost Function for batches**<br>
In practice, during the process of training, this averaging of losses is typically performed over a **subset** of the total training examples, known as a batch (or mini-batch). This batch-based averaging approach forms the basis of the commonly used [**mini-batch Stochastic Gradient Descent (SGD)**](gradient_descent.md#mini-batch-sgd) and its variants, where the model's parameters are updated incrementally after computing the cost function for each batch.

For example, in training neural networks, each batch (regardless of the size) goes through the following steps:
- forward pass for the batch.
- Cost computation for the batch
- backpropagation for the batch
- Update all the network parameters based on the gradients computed for the batch.

So, even though we run forward/backward pass for a batch, we update the parameters for the entire dataset.

>In simple terms, **Loss** is the error between the prediction of the model and actual ground truth label $y$ for one example from the training dataset. While **Cost** is the average of loss across all examples (or the batch) in the training dataset.
>
>The goal of training a machine learning model is to find $\mathbf{W}$ and $\vec{\mathbf{b}}$ (weights and biases) that minimize the cost function $J(\mathbf{W}, \vec{\mathbf{b}})$ using optimization algorithms such as gradient descent.



## Loss and Cost Functions for Linear Regression

The Linear Regression model is defined as:

$$f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}) = \vec{\mathbf{w}} \cdot \vec{\mathbf{x}}^{(i)} + b$$

where:
- $\vec{\mathbf{x}}^{(i)}$ is the feature vector for the $i^{th}$ instance.
- $\vec{\mathbf{w}}$ is the weight vector.
- $b$ is the bias term.

But, how do we know which values of $\vec{\mathbf{w}}$ and $b$ are the best? We need a way to measure how well the model is performing. In other words, how far or close the predicted value $\hat{y}$ is to the actual target value $y$ (labels).


So, the goal here is to find the best values for $\vec{\mathbf{w}}$ and $b$ that minimize the difference between the predicted value $\hat{y}$ and the actual target value $y$ for all training examples.

For simplicity, we use a univariate linear regression model $f_{w,b}(x) = wx + b$ where we have only one feature $x$. We use this model to explain the concept of cost function and how to minimize it.


![cost_function](images/cost_function1.png)

**Error**: is the difference between the predicted value (by the model), and the actual target value.

$$Error =y_{pred} - y_{actual}$$

In a more formal way, Error is the difference between predicted value of the model for the $i^{th}$ training example (denoted as ${\hat{y}}^{(i)}$) and the actual target value $y^{(i)}$.

$$Error(\hat{y}^{(i)}, y^{(i)}) = \hat{y}^{(i)} - y^{(i)}$$



**Loss function**:<br>
A function that measures how well the model's prediction $\hat{y}$ for a single training example is compared to the actual target value $y$. We denote the loss function as:

$$L(\hat{y}^{(i)}, y^{(i)})$$

And we have $\hat{y}^{(i)} = f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$, so we can write the loss function as:
$$L(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}), y^{(i)})$$

For example, the _squared error_  and _absolute error_ are common [loss functions](https://developers.google.com/machine-learning/crash-course/linear-regression/loss#types_of_loss) used in regression models. Here, we will use the squared error loss function.

### Mean Squared Error (MSE)

The **Squared Error Loss** function is defined as:

$$L(\hat{y}^{(i)}, y^{(i)}) = (\hat{y}^{(i)} - y^{(i)})^2$$

This function measures the squared difference between the predicted value $\hat{y}^{(i)}$ and the actual target value $y^{(i)}$. By squaring the difference, we ensure that the loss is always a non-negative value, and heavily penalizes large errors by squaring them. This makes it pariticularly sensitive to larger errors.

Knowing that $\hat{y}^{(i)} = f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$, we can write the loss function as:


$$L(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}), y^{(i)}) = (f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}) - y^{(i)})^2$$

As we discussed, the **Cost function** $J(\vec{\mathbf{w}},b)$ measures the average losses over all training examples.

$$J(\vec{\mathbf{w}},b) = \frac{1}{m} \sum\limits_{i = 1}^{m} L(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}), y^{(i)})$$

So, we can write the cost function for the squared error loss as:

$$J(\vec{\mathbf{w}},b) = \frac{1}{m} \sum\limits_{i = 1}^{m} \frac{1}{2}(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}) - y^{(i)})^2$$

> Note: The factor $\frac{1}{2}$ is introduced **purely for mathematical convenience** to simplify derivatives during gradient descent, as it cancels out the $2$ when taking the derivative of the squared term. It does not affect the optimization process or the final result.

This function is also called **Mean Squared Error (MSE)** which we moved the factor $\frac{1}{2}$ outside the sum.

$$J(\vec{\mathbf{w}},b) = \frac{1}{2m} \sum\limits_{i = 1}^{m} (f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}) - y^{(i)})^2$$


## Cross-Entropy Loss
Cross-Entropy measures the dissimilarity between the predicted probability distribution and the true (actual) distribution by quantifying how far the predictions are from perfectly matching the true labels. It originates from information theory, where it quantifies the "surprise" or "information" difference between two probability distributions.

Imagine you are playing a guessing game, and you have to guess which box has candy inside. Cross-Entropy Loss is like a score that tells you how bad your guess is. If your guess is very far from the candy box, the score (or "loss") will be high. But if you make your guesses closer to the right box, the score gets smaller.

When we try to make the score as small as possible (minimize the loss), we are learning to guess better. In this case, it means we are getting closer to saying the right box has the highest chance (probability) of having the candy.

Let's compare Cross-Entropy Loss with Mean Squared Error (MSE) for better understanding. We know that Mean Squared Error (MSE) and Cross-Entropy Loss both measure the error between the model's predictions, but they do so in fundamentally different ways. MSE does this by measuring the distance between the predicted and true values, treating them as points in space and calculating how far apart they are. On the other hand, Cross-Entropy measures the unlikelihood of the true class by evaluating how much the predicted probability distribution deviates from assigning high probability to the correct class. In essence, while MSE focuses on minimizing the numerical distance between points, Cross-Entropy focuses on reducing the uncertainty and increasing confidence in the true class by penalizing unlikely predictions.

**Cross-Entropy and Maximum Likelihood Estimation (MLE):**<br>
In machine learning, the cross-entropy loss has a direct connection to maximum likelihood estimation (MLE) in field of statistics. Minimizing the cross-entropy loss is equivalent to maximizing the likelihood of the observed data under the predicted probability distribution.

For a single example, Cross-Entropy Loss is calculated as:

$$
L = -\log(p_\text{true})
$$

where:
- $L$ is the loss for a single example.
- $p_\text{true}$ is the predicted probability for the correct label.

For a dataset with many examples, the average loss becomes:

$$
J = -\frac{1}{m} \sum_{i=1}^m \log(p_{\text{true}}^{(i)})
$$
where:
- $J$ is the average loss over all examples.
- $m$ is the number of examples.
- $p_{\text{true}}^{(i)}$ is the predicted probability for the correct label of the $i^{th}$ example.

By minimizing this loss, the model adjusts its predictions to increase the likelihood of the correct labels. This connection exists because minimizing Cross-Entropy Loss is mathematically identical to maximizing the likelihood of the data, which is the goal of MLE. In essence, both approaches aim to make the model's predictions align as closely as possible with the actual data.

### Binary Cross-Entropy Loss
Binary Cross-Entropy Loss is a variant of the Cross-Entropy Loss which is commonly used in binary classification problems such as predicting whether an email is spam or not, or whether a tumor is malignant or benign. Here, the output of our model is a probability that the given input point belongs to a certain class.

In binary classification, the true label is either 0 or 1, and the model outputs a probability. If the true label is 1, we want the predicted probability to be as close to 1 as possible, and vice versa. The binary cross-entropy loss is high when the model's predictions are confident but wrong, and it's low when the predictions are confident and correct.

Formally, the binary cross-entropy loss function $L$ for a single data point is defined as:
$$
\begin{aligned}
  L(\hat{y}^{(i)}, y^{(i)}) = \begin{cases}
    - \log(\hat{y}^{(i)}) & \text{if $y^{(i)}=1$}\\
    - \log(1-\hat{y}^{(i)}) & \text{if $y^{(i)}=0$}
  \end{cases}
\end{aligned}
$$
where:
- $\hat{y}^{(i)}$ is the predicted probability for the $i^{th}$ instance.
- $y^{(i)}$ is the true label for the $i^{th}$ instance.

We know $\hat{y}^{(i)} = f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$, so we can write the loss function as:

$$
L(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}), y^{(i)}) = \begin{cases}
    - \log(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})) & \text{if $y^{(i)}=1$}\\
    - \log(1 - f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})) & \text{if $y^{(i)}=0$}
  \end{cases}
$$

The following plots show the changes of the loss function for $f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$ as the predicted value $\hat{y}$ changes for the true label $y=1$ and $y=0$.

![binary_cross_entropy](images/binary_cross_entropy_loss.png)

As we can see in the above plot:

When $y_{(i)}=1$: The goal is to penalize the model more when the predicted probability is low (close to 0).
- As $f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$ approaches 1, the loss approaches 0
- As $f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$ approaches 0, the loss approaches $\infty$

When $y_{(i)}=0$: The goal is to penalize the model more when the predicted probability is high (close to 1).
- As $f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$ approaches 0, the loss approaches 0
- As $f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$ approaches 1, the loss approaches $\infty$

>  This loss function penalizes the model heavily when predictions of the model $f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$ goes further away from the true label $y_{(i)}$. Using this loss, the model is strongly encouraged not to predict something too close to 0 or 1.

We can write the loss function $L$ in a more simpler way:

$$
L(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}), y^{(i)}) = -y^{(i)} \log(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})) - (1 - y^{(i)}) \log(1 - f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}))
$$

The above notation is embedding the if-else condition in a single equation. Since we know that $y^{(i)}$ is either 0 or 1, the term $-y^{(i)} \log(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}))$ will be zero when $y^{(i)}=0$ and the term $-(1 - y^{(i)}) \log(1 - f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)}))$ will be zero when $y^{(i)}=1$.


Now, knowing that $\hat{y}^{(i)} = f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})$, we can write the loss function as:
$$
L(\hat{y}^{(i)}, y^{(i)}) = -y^{(i)} \log(\hat{y}^{(i)}) - (1 - y^{(i)}) \log(1 - \hat{y}^{(i)})
$$

And if factor out $-1$ and write it in a more general form:

$$
L(\hat{y}, y) = -[y \log(\hat{y}) + (1 - y) \log(1 - \hat{y})]
$$

In binary classification tasks, the final layer of the neural network typically consists of a single output node with a sigmoid activation function, which gives us the probability $a$ that an instance belongs to class 1 (consequently, the probability that it belongs to class 0 is $1-a$).

Given the true label $y$ (where $y=1$ for class 1 and $y=0$ for class 0) and the predicted probability $a$, the Binary Cross-Entropy Loss $L$ for an individual instance is:

$$
L(a, y) = -y \log(a) - (1 - y) \log(1 - a)
$$

This implies that if the true class is 1 ($y=1$), the loss becomes $-\log(a)$, and if the true class is 0 ($y=0$), the loss transforms to $-\log(1-a)$.

**Cost Function for Binary Cross-Entropy:**<br>
The cost function $J$ measures the average loss (error between the model's predictions and the true labels) for the entire training set of size $m$:

$$
J(W, \vec{\mathbf{b}}) = -\frac{1}{m} \sum_{i=1}^{m} \left[ y^{(i)} \log(f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})) + (1 - y^{(i)}) \log(1 - f_{\vec{\mathbf{w}},b}(\vec{\mathbf{x}}^{(i)})) \right]
$$

where:
- $m$ is the number of training examples.
- $W$ represents the matrix of weights for the model.
- $\vec{\mathbf{b}}$ is vector of the biases.
- $f_{W, \vec{\mathbf{b}}}\vec{\mathbf{x}}^{(i)}=\hat{y}^{(i)}$ is the predicted probability for the $i^{th}$ instance.

We can then write it in a simpler form:
$$
J(W, \vec{\mathbf{b}}) = -\frac{1}{m} \sum_{i=1}^{m} [y^{(i)} \log(\hat{y}^{(i)}) + (1 - y^{(i)}) \log(1 - \hat{y}^{(i)})]
$$

### Categorical Cross-Entropy Loss
The Cross-Entropy Loss function for multi-class classification is commonly referred to as **Categorical Cross-Entropy**.

**Categorical**: This term indicates that the problem at hand is a multi-class classification problem, where the aim is to predict the probability of each category. The target labels are categories (also called classes), typically represented as **one-hot encoded** vectors. In other word, each input example belongs to exactly one class.

For example, if there are $N=5$ classes, a label for "Class 2" is represented as:

$$y = [0, 1, 0, 0, 0]$$

Here, the label is a vector of length $N$ with a 1 at the index corresponding to the class and 0s elsewhere.


**For a Single Example:**

The cross-entropy loss for one example $(i)$ is:

$$
L^{(i)} = - \sum_{j=1}^{N} y_j^{(i)} \log(\hat{y}_j^{(i)})
$$

where:
- $L^{(i)}$ is the loss for example $i_{th}$.
- $N$ is the number of classes.
- $y_j^{(i)}$ is the true label (1 for the correct class, 0 for all others) for example $i_{th}$ and class $j$.
- $\hat{y}_j^{(i)}$ is the predicted probability for example $i_{th}$ and class $j$.



**Cost Function for the $m$ Examples:**

The **cost function** $J$ (average cross-entropy loss) is:

$$
J = \frac{1}{m} \sum_{i=1}^{m} L^{(i)} = - \frac{1}{m} \sum_{i=1}^{m} \sum_{j=1}^{N} y_j^{(i)} \log(\hat{y}_j^{(i)})
$$

where:
- $m$ is the number of examples in the batch.


### Sparse Categorical Cross-Entropy Loss
Sparse Categorical Cross-Entropy Loss is another version of Cross-Entropy Loss used specifically for multi-class classification tasks. However, unlike the standard Cross-Entropy Loss, it is applied when the true class labels are represented as integers instead of one-hot encoded vectors.


**Sparse**: This indicates that the labels are provided as integers, with each integer representing a class. For example, in a 10-class problem (like digit recognition, where classes are 0 to 9), the label for class 2 is simply the integer 2. Sparse representation is more memory-efficient comparing to the 'dense' representation, where each label is a one-hot encoded vector.

One-hot Encoding:
$$y = [0, 1, 0, 0, 0]$$

Sparse Encoding:
$$y = 2$$


Sparse Categorical Cross-Entropy Loss for $N$ classes is defined as:

$$
\begin{aligned}
  L(\mathbf{\vec{a}},y)=\begin{cases}
    -log(a_1), & \text{if $y=1$}.\\
        &\vdots\\
     -log(a_N), & \text{if $y=N$}
  \end{cases}
\end{aligned}
$$
where:
- $N$ is the number of classes.
- $y$ is the true class label for the instance.
- $\mathbf{\vec{a}}$ is the predicted probability vector for the instance. $\vec{\mathbf{a}} = [a_0, a_1, ..., a_{N-1}]$, where $a_i$ is the predicted probability of class $j_{th}$.

At anytime, only one of them true (the example can belong to one class), then the loss of class $j$ is:


$$
L(a_j, y) = -\log(a_j)
$$

Where:
- $a_j=\hat{y}_j$ is the predicted probability of the sample belonging to the correct class $j$.

>This is essentially equivalent to the standard Categorical Cross-Entropy Loss, but is computationally more efficient when the class labels are integers, as there's no requirement to convert them into one-hot encoded vectors.



We know that only the line that corresponds to the target contributes to the loss, other lines are zero. To write the cost equation we need an **indicator function** that will be 1 when the index matches the target and zero otherwise.

$$\mathbf{1}\{y == n\} =\begin{cases}
1, & \text{if $y==n$}.\\
0, & \text{otherwise}.
\end{cases}$$

Now the loss is:
$$
\begin{aligned}
L(\mathbf{\vec{a}},y) = - \sum_{j=1}^{N} \left[  1\left\{y^{(i)} == j\right\} \log \frac{e^{z^{(i)}_j}}{\sum_{k=1}^N e^{z^{(i)}_k} }\right]
\end{aligned}
$$

Where:
- $N$ is the number of outputs (classes).
- $i$ indicates that this is $i$-th example of the training dataset.
- $j$ is the index of the output element in the vector $\mathbf{\vec{a}}$.

To put this all together, if you're working on a multi-class classification problem with mutually exclusive classes (where each sample belongs to exactly one class), and you have class labels represented as integers, you would use Sparse Categorical Crossentropy as your loss function.


> **indicator function:** (denoted here as $\mathbf{1}\{y == n\}$) is a concept that behaves very similarly to the if-else construct in programming. It produces a binary output based on whether a specific condition is met.
>
>In this context, the condition is $y==n$, where $y$ is the target (actual) class and $n$ is the index of the class we're currently considering.
> The mathematical notation you're seeing is a piecewise function, which is a common way to represent indicator functions. Here's how it works:
>
>- $\mathbf{1}\{y == n\} = 1$: This line states that the indicator function outputs 1 when the condition $y==n$ is met.
>- $\mathbf{1}\{y == n\} = 0$: This line states that the indicator function outputs 0 when the condition $y==n$ is not met.


### Mutually Exclusive Multi-Class vs. Multi-Label Classification
**Mutually exclusive multi-class classification** refers to a type of classification problem where each instance belongs to exactly one class out of a predefined set of classes, and no overlap between classes is allowed. For example, in a task to classify images of animals into "cat," "dog," or "bird," each image is assumed to belong to only one of these categories. The model predicts a probability distribution across all classes, with the sum of probabilities equaling 1, ensuring that the instance is assigned to the most probable class.

**Multi-label classification** is a type of classification problem where each instance can belong to multiple classes simultaneously, rather than being restricted to just one. For example in a model which classify research papers, a model can classify a research paper into multiple relevant fields, such as "Deep Learning," "Natural Language Processing (NLP)," and "Computer Vision."

 A single paper about "transformers applied to image captioning" could be labeled with:
  - "Deep Learning"
  - "Natural Language Processing (NLP)"
  - "Computer Vision"

The model would predict independent probabilities for each label:
  - "Deep Learning: 0.95"
  - "NLP: 0.88"
  - "Computer Vision: 0.75"
  - "Robotics: 0.10"

Each label is treated **independently**, allowing the model to assign multiple tags to a single instance, which is essential in fields like document classification, multi-topic news categorization, or research paper tagging in online repositories like arXiv.

This means the model outputs a probability for each class, indicating the likelihood that the instance belongs to that class. **Binary Cross-Entropy** is typically used as the loss function for multi-label problems, as it calculates the loss for each class independently, treating the presence or absence of each label as a separate binary classification task.

This is a quick summary:

| Loss Function | Use Case | Description |
| --- | --- | --- |
| **Categorical Cross-Entropy** | Mutually Exclusive Multi-Class | Used when each instance belongs to exactly one class. |
| **Sparse Categorical Cross-Entropy** | Mutually Exclusive Multi-Class | Used when true labels are integers representing the class index. |
| **Binary Cross-Entropy** | Mutually Exclusive Multi-Class (N=2), and Multi-Label Classification | It works for both binary classification (mutually exclusive classes, $N=2$) and multi-label classification by treating each class independently, calculating loss for each output probability separately. |


### Implementation of Cross-Entropy In ML Libraries

### TensorFlow
Tensorflow has multiple variations of cross-entropy. A few of commonly used ones are:
- `CategoricalCrossEntropy`: (is the same as Cross-Entropy function) expects the target value of an example to be one-hot encoded where the value at the target index is 1 while the other N-1 entries are zero. An example with 10 potential target values, where the target is 2 would be [0,0,1,0,0,0,0,0,0,0].
- `SparseCategorialCrossentropy`: expects the target to be an integer corresponding to the index. For example, if there are 10 potential target values, y would be between 0 and 9. This is suitable when your classes are mutually exclusive, i.e., each instance belongs to exactly one class.
- `BinaryCrossEntropy`: Computes the cross-entropy loss between true labels and predicted labels. Used in binary classification tasks where each example belongs to exactly one of two classes.

For example:
```python
model.compile(loss=tf.keras.losses.SparseCategoricalCrossentropy())
```
