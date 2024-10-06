# AI and Machine Learning Overview
**Machine Learning (ML):** A way of achieving AI, where the machine learns from data to make predictions or decisions without being explicitly programmed.

Machine learning is a subfield of artificial intelligence (AI).

![Alt text](images/ai1.jpg)
Source: [Augmenting organizational decision-making with deep learning algorithms: Principles, promises, and challenges](https://www.sciencedirect.com/science/article/pii/S0148296320306512)

### Types of Machine Learning:
- Supervised Learning
- Unsupervised Learning
- Semi-Supervised Learning
- Reinforcement Learning (RL)
- Transfer Learning

## Supervised Learning
Supervised learning is a type of machine learning where the model is trained on a labeled dataset. This means that the input data is paired with the correct output. The model learns (optimizes) to make predictions based on the input data by comparing its predictions with the correct output during the training process.

**Labeled data**: Data that has pairs of both the input data $X$ and the "correct" output $Y$.

$Input(X) \rightarrow Output(Y)$

The model optimizes itself to make predictions based on the input data by comparing its predictions with the correct output during the training process.

| Input (X) | Output (Y) | Application |
| --- | --- | --- |
| Image | Label (e.g., cat, dog) | Image classification |
| Email | Spam or not spam | Email spam detection |
| Text | Sentiment (e.g., positive, negative) | Sentiment analysis |
| Audio | Transcription | Speech recognition |
| Stock prices | Future price | Stock price prediction |

### Example tasks:
- **Regression**: Predicting a continuous value (e.g., house prices, stock prices).
- **Classification**: Predicting a discrete label (e.g., spam vs. non-spam emails, speech recognition, or cat vs. dog in an image).

### Key supervised learning algorithms include:
- [Regression](linear_regression.md)
- [Classification](classification.md)
- [K-Nearest Neighbors (KNN)](knn.md)
- [Decision Forests, Random Forests, and Gradient Boosted Decision Trees](decision_forests.md)
- Neural Networks (when used with labeled data)
