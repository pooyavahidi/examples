# Machine Learning Workflow

Machine Learning development is an [empirical process](https://www.deeplearning.ai/the-batch/iteration-in-ai-development/). So, when you start, don’t overthink and spend too much time on the design of the system, types of algorithms, model architecture, hyperparameters, and so on. Build the first version quick, get the feedback, analyze the result and improve your system iteratively.

The common steps of a machine learning project:
1. **Data Engineering**: Define, collect and preprocess data.
2. **Exploratory Data Analysis (EDA)**: Data Analysis, cleansing and visualization of data to understand its structure, relations, patterns, and potential issues.
3. **Feature Engineering**: The process of transforming and selecting data representations to best capture information relevant for model training and performance.
3. **Modeling**: Training, Validation, Evaluation, Tuning and iterate until the model is ready for deployment.
4. **Operation**: Deployment, Monitor the ongoing predictions, manage models and versions (artifacts organization), feedback loops and continuous learning/retraining, scaling, MLOps, etc.





![](images/ml_workflow_mlflow.png)
Source: [mlflow.org](https://mlflow.org/docs/latest/introduction/index.html)

> The is not a linear process, but an **iterative** one. It's like a loop, and you may need to go back and forth between the steps.
>
> Steps 2 to 6 usually repeated in a loop until you get the desired results. However, in many cases you may need to go back to step 0 to collect more data or improve the quality of the data.


## Data Engineering

## Exploratory Data Analysis (EDA)

## Feature Engineering
See [Feature Engineering](ai/feature_engineering.md) for more details.

## Modeling

## Operation
