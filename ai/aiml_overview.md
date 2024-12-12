# AI and Machine Learning Overview
**Machine Learning (ML):** A way of achieving AI, where the machine learns from data to make predictions or decisions without being explicitly programmed.

Machine learning is a subfield of artificial intelligence (AI).

![Alt text](images/ai1.jpg)
Source: [Augmenting organizational decision-making with deep learning algorithms: Principles, promises, and challenges](https://www.sciencedirect.com/science/article/pii/S0148296320306512)

To learn more about the machine learning development workflow and process, see [Machine Learning Workflow](aiml_overview_workflow.md).

**Types of Machine Learning:**
- Supervised Learning
- Unsupervised Learning
- Semi-Supervised Learning
- Self-supervised Learning
- Reinforcement Learning (RL)
- Transfer Learning

## Supervised Learning
Supervised learning is a type of machine learning where the model is trained on a labeled dataset. This means that the input data is paired with the correct output. The model learns (optimizes) to make predictions based on the input data by comparing its predictions with the correct output during the training process.

**Labeled data**: Data that has pairs of both the input data $X$ and the "correct" output $Y$. These $X$ and $Y$ mappings are used to train the model.

$Input(X) \rightarrow Output(Y)$


Supervised learning is when we provide our learning algorithm with examples (labeled data), where each example includes the correct answer $Y$ to learn from.

The model is trained on this labeled data to make predictions on new, unseen data. During the training process, the model optimizes itself by comparing its predictions with the correct output.

| Input (X) | Output (Y) | Application |
| --- | --- | --- |
| House features (e.g., size, location) | Price | House price prediction |
| Image | Label (e.g., cat, dog) | Image classification |
| Email | Spam or not spam | Email spam detection |
| Text | Sentiment (e.g., positive, negative) | Sentiment analysis |
| Audio | Transcription | Speech recognition |
| Stock prices | Future price | Stock price prediction |


A supervised learning algorithm typically consists of three key components:
- **Model (hypothesis function)**: A function that maps the input features to the predicted target value.
- **Cost Function**: A function that measures how well the model is performing by comparing the predicted versus actual target values.
- **Optimization Algorithm**: A method to minimize the cost function (the error between the predicted and actual target values) by adjusting the model parameters.

### Example tasks:
- [Regression](regression.md): Predicting a number (continuous value) such as house prices, stock prices, etc.
- [Classification](classification.md) : Predicting discrete classes or categories from a limited set of possible values, such as cat or dog, or numeric labels like 0, 1, 2, etc. (e.g., spam vs. non-spam emails, speech recognition, or cat vs. dog in an image).

> Regression models predict a number from infinitely many possible values, while classification models predict a category from a finite set of categories (or classes).

### Main supervised learning algorithms:
- [Regression](regression.md): Predict a number.
- [Classification](classification.md): Predict a category.
- [K-Nearest Neighbors (KNN)](knn.md)
- [Decision Forests, Random Forests, and Gradient Boosted Decision Trees](decision_forests.md)
- Neural Networks (when used with labeled data)

## Unsupervised Learning
Unsupervised learning is a type of machine learning where the model is trained on an **unlabeled** dataset. This means the model learns to make predictions based on the input data without being explicitly told what the correct output is. The model learns to identify patterns and structures in the data.

Unlike the supervised learnign where the training data comes with both $input(X)$ and $output(Y)$, in unsupervised learning, the data comes with only $input(X)$. The model learns to find structures in the data without being explicitly told what to look for.

### Main unsupervised learning algorithms:
- [Clustering](clustering.md): Grouping similar data points together, into clusters. e.g. Google News which groups similar news articles together. This happens without any supervision or labeled data. The algorithm learns to group similar data points together based on their features. Another example is customer segmentation in marketing.
- **Anomaly detection:** Identifying rare items, events, or observations that raise suspicions by differing significantly from the majority of the data. e.g. fraud detection.
- **Dimensionality reduction:** Compress data using fewer numbers.

## Semi-Supervised Learning
This is a hybrid of supervised and unsupervised learning, where the model is trained on a small amount of labeled data and a large amount of unlabeled data. Semi-supervised learning is useful when labeling data is expensive or time-consuming, but there is a large amount of unlabeled data available.

Example tasks:
- Image classification with limited labeled images.
- Text categorization with few labeled documents and many unlabeled ones.

## Self-supervised Learning
Self-supervised learning is a specific form of unsupervised learning where the model generates its own supervisory signals from the data itself. This is a common approach in modern neural networks, particularly in natural language processing (NLP) and computer vision.

Example tasks:
- Word embeddings (e.g., models like Word2Vec or BERT) where relationships between words are learned from large corpora.
- Learning image representations by predicting missing parts of images or predicting future frames in a video.

## Transfer Learning
Though not a traditional type of learning, transfer learning refers to using a pre-trained model on one task and adapting it to a different but related task. This is especially useful when there is not enough labeled data for the new task, but the knowledge gained from a different domain can be reused.

Example tasks:
- Using a model trained on ImageNet to classify medical images with a smaller labeled dataset.
- Fine-tuning a language model like GPT for specific text classification tasks.

## Neural Networks
**Neural Networks (NNs)** are a type of machine learning where interconnected nodes (or "neurons") are layered to create an **artificial neural network**. This can be shallow (with one hidden layer) or deep (with multiple hidden layers). This [Neural Network Overview](/nn_overview.md) covers the basics.

Neural networks and deep learning can be used for all types of learning: supervised learning (e.g., image recognition, speech recognition, and language translation), unsupervised learning (e.g., clustering, dimensionality reduction, generative models), reinforcement learning (e.g., game playing and robotics), and semi-supervised learning.

**Deep neural networks**: These networks have more than two layers of nodes between the input and output layers, unlike shallow networks that have at most one layer between inputs and outputs.

Deep learning is a subfield of machine learning that employs algorithms inspired by the structure and function of the brain's neural networks. While it is correct to say that deep learning involves the use of neural networks, it specifically refers to networks with multiple layers.

On the other hand, there are algorithms with a simplified structure, typically having one or no hidden layers, called _shallow networks_. Examples of shallow learning methods include Linear Regression, Logistic Regression, Perceptron, Radial Basis Function Network (RBFN), and Single-Layer Autoencoder.

> [Shallow Learning](https://www.sciencedirect.com/science/article/pii/S2666165921000041) refers to the majority of machine learning models proposed prior to 2006, including shallow neural networks (neural networks with only one or no hidden layers).

### Deep Learning
Deep learning is based on **deep** neural networks. As discussed, not all neural networks are used for deep learning. The neural networks used in deep learning are **deep** neural networks, which have multiple layers of neurons. These include:

- **Multilayer Perceptrons (MLPs):** The simplest form of a neural network with multiple layers.
- **Convolutional Neural Networks (CNNs):** Designed to process grid-like data such as images, applying convolutional layers that pre-process data for the layers that follow.
- **Recurrent Neural Networks (RNNs):** Designed to work with sequence data, with neurons that have feedback connections, effectively forming a memory over the sequence.
- **Transformer Networks:** Designed to work with sequence data, but unlike RNNs, they allow for parallel computation and can directly attend to any point in the sequence.

While other machine learning algorithms can create models with multiple layers (like decision trees and support vector machines), the term "deep learning" is almost exclusively used to refer to techniques involving deep neural networks.

## Math for AI/ML
Although you don't need to be a math expert to work in the field of AI/ML, a solid understanding of the underlying math concepts is essential. The followings are the key concepts you should be familiar with:

**College Calculus and Linear Algebra**: You should be comfortable with (multivariable) derivatives and understand matrix/vector notation and operations.

**Probability Theory**: You should be familiar with basic probability distributions (e.g., continuous, Gaussian, Bernoulli) and be able to define concepts for both continuous and discrete random variables, including expectation, independence, probability distribution functions, and cumulative distribution functions.


## Machine Learning Workflow

Machine Learning development is an [empirical process](https://www.deeplearning.ai/the-batch/iteration-in-ai-development/). So, when you start, don’t overthink and spend too much time on the design of the system, types of algorithms, model architecture, hyperparameters, and so on. Build the first version quick, get the feedback, analyze the result and improve your system iteratively.

The common steps of a machine learning project:
1. **Data Engineering**: Define, collect and preprocess data.
2. **Exploratory Data Analysis (EDA) and Feature Engineering**: Data Analysis, cleansing and visualization of data to understand its structure, relations, patterns, and potential issues. Then in an iterative process, transform and select data representations to best capture information relevant for model training and performance.
3. **Modeling**: Training, Validation, Evaluation, Tuning and iterate until the model is ready for deployment.
4. **Operation**: Deployment, Monitor the ongoing predictions, manage models and versions (artifacts organization), feedback loops and continuous learning/retraining, scaling, MLOps, etc.


![](images/ml_workflow_mlflow.png)
Source: [mlflow.org](https://mlflow.org/docs/latest/introduction/index.html)

> The is not a linear process, but an **iterative** one. It's like a loop, and you may need to go back and forth between the steps.
>
> The above diagram shows **Feature Engineering** as a separate step, but in the real world, it's an ongoing activity during the EDA process. You explore, clean, and engineer features iteratively until you are satisfied with the read-to-training dataset.
>
> Steps 1 to 6 usually repeated in a loop until you get the desired results. However, in many cases you may need to go back to step 0 to collect more data or improve the quality of the data.


### Data Engineering

### Exploratory Data Analysis (EDA) and Feature Engineering

#### Visualization Techniques
Visualzation techniques are key tools for EDA (Cleaning and Feature Engineering). So, this is not a separate step, but it's an ongoing activity during the EDA process.

Visualization is like a guide for you to help you to understand the data (stats, outliers, patterns, etc), and to make decisions about before and after data cleaning and feature engineering.

We use the following visualization techniques:

- **Histograms**: To show the distribution of a single variable.
- **Scatter Plots**: To show the relationship between two variables (feature vs feature, and feature vs target).
- **Pairplot**: To show the relationship between multiple variables. Similar to Scatter Plots, but it shows all possible combinations of variables.
- **Heatmaps**: To show the correlation between variables. To detect multi-collinearity between features. i.e. when two features move together (positive or negative correlation).
- **Box Plots**: To show the distribution of a single variable. It shows the median, quartiles, and outliers of the variable.

For seeing these visualizations in action, go to [Linear Regression using Scikit-Learn](labs/linear_regression_scikit_learn.ipynb).


#### Feature Engineering
Feature engineering is the process of selecting the right features (feature reduction), creating new features from the existing features, and transforming the existing ones to new ones. It's a crucial step in the machine learning process, as it can significantly impact the performance of the model.

In feature engineering to verify our hypothesis, we use the visualization techniques (discussed above) to make the right decisions.

See further details here at [Feature Engineering](ai/feature_engineering.md).

### Modeling

**Model Evaluation:**
Cross Validation, Metrics, Confusion Matrix, ROC Curve, etc. For more details, see [Model Evaluation](model_evaluation.md).



### Operation

## Resources
- [AI/ML Resources](aiml_resources.md)
- [Machine Learning Workflow and Process](aiml_overview_workflow.md).
- [Glossary](glossary.md)
