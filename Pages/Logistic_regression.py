import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import joblib
import numpy as np
import os
import graphics
from Preprocessing import preprocess



def train_model(X_train, y_train):
    """
    Trains a logistic regression model using TF-IDF vectorization and SMOTE oversampling.

    Args:
    - X_train: Features (tweets) for training.
    - y_train: Labels for training.

    Returns:
    - best_model: Trained logistic regression model.
    - vectorizer: TF-IDF vectorizer used for feature extraction.
    """
    # Initialize TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 3))
    X_train_tfidf = vectorizer.fit_transform(X_train)

    # Upsample minority class
    X_train_resampled, y_train_resampled = upsample_minority_class(X_train_tfidf, y_train, vectorizer)

    # Tune logistic regression model
    best_model = tune_logistic_regression(X_train_resampled, y_train_resampled)

    return best_model, vectorizer



def upsample_minority_class(X_train_tfidf, y_train, vectorizer):
    """
    Upsamples the minority class (depressed tweets) using SMOTE.

    Args:
    - X_train_tfidf: TF-IDF transformed features for training.
    - y_train: Labels for training.
    - vectorizer: TF-IDF vectorizer used for feature extraction.

    Returns:
    - X_train_resampled: Upsampled features.
    - y_train_resampled: Upsampled labels.
    """
    # Determine minority class samples
    minority_class_samples = sum(1 for label in y_train if label == '1')
    
    desired_ratio = {'1': minority_class_samples + 100}

    # Apply SMOTE for oversampling
    smote = SMOTE(sampling_strategy=desired_ratio, random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_tfidf, y_train)
    
    upsampled_minority_class_samples = sum(1 for label in y_train_resampled if label == '1')

    print("Total number of depressed tweets after upsampling:", upsampled_minority_class_samples)

    return X_train_resampled, y_train_resampled


def tune_logistic_regression(X_train_resampled, y_train_resampled):
    """
    Performs grid search to tune logistic regression hyperparameters.

    Args:
    - X_train_resampled: Upsampled features for training.
    - y_train_resampled: Upsampled labels for training.

    Returns:
    - best_model: Best logistic regression model.
    """
    # Define parameter grid for grid search
    param_grid_lr = {'C': [0.00001, 0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000], 'max_iter': [100, 200, 300, 400, 500]}
    grid_search_lr = GridSearchCV(LogisticRegression(), param_grid_lr, cv=5,scoring='accuracy')
    grid_search_lr.fit(X_train_resampled, y_train_resampled)

    # Get best model from grid search
    best_model = grid_search_lr.best_estimator_
    print("Best Logistic Regression Parameters:", grid_search_lr.best_params_)

    # Fit best model
    best_model.fit(X_train_resampled, y_train_resampled)

    return best_model


def test_model(model, vectorizer, X_test, y_test):
    """
    Tests the trained model on the test set.

    Args:
    - model: Trained model.
    - vectorizer: TF-IDF vectorizer used for feature extraction.
    - X_test: Features (tweets) for testing.
    - y_test: Labels for testing.

    Returns:
    - y_pred: Predicted labels.
    """
    # Transform the test set features using the TF-IDF vectorizer
    X_test_tfidf = vectorizer.transform(X_test)

    # Predict labels for the test set using the trained model
    y_pred = model.predict(X_test_tfidf)

    # Calculate the accuracy of the model by comparing predicted labels with true labels
    accuracy = accuracy_score(y_test, y_pred)

    print(f'accuracy : {accuracy*100:.2f}')
    
    # Get top depression terms
    top_depression_terms = get_depression_terms(vectorizer, model)
    graphics.CreateWordCloud(top_depression_terms, "dataset")


    return y_pred


def analyze_user_tweets(userFile, vectorizer, model):
    """
    Analyzes a user's tweets for depression indicators.

    Args:
    - userFile: File containing user's tweets.
    - vectorizer: TF-IDF vectorizer used for feature extraction.
    - model: Trained logistic regression model.

    Returns:
    - depression_percentage: Percentage of tweets predicted as depressed.
    """
    # Store the original path to the user file
    UserImagePath = userFile

    # Update the user file path to include the directory where the datasets are stored
    userFile = '../Datasets/' + userFile

    # Read the CSV file containing user tweets into a DataFrame
    unlabeled_df = pd.read_csv(userFile)

    # Apply preprocessing to the tweet text
    unlabeled_df["Tweets"] = unlabeled_df['Tweets'].apply(lambda x: preprocess(x))

    # Clean the unlabeled data (remove NaN and empty tweets)
    unlabeled_df = clean_unlabeled_data(unlabeled_df)
    depression_percentage = 0
    
    
    if not unlabeled_df.empty:

        # Transform the preprocessed tweet text into TF-IDF features
        X_unlabeled_tfidf = vectorizer.transform(unlabeled_df['Tweets'])

        # Predict labels for the unlabeled data using the trained model
        y_unlabeled_pred = model.predict(X_unlabeled_tfidf)

        # Add predicted labels to the DataFrame
        unlabeled_df['Prediction'] = y_unlabeled_pred

        # Calculate the percentage of depressed tweets in the unlabeled data
        depression_percentage = calculate_depression_percentage(y_unlabeled_pred)

        # Create a word cloud visualization of the top depression terms
        depressed_wordcloud_text = unlabeled_df['Tweets'][y_unlabeled_pred == '1']
        graphics.CreateWordCloud(depressed_wordcloud_text, UserImagePath)

        # Remove the user file after processing
        os.remove(userFile)


        return True,depression_percentage
    else:
        return False,depression_percentage


def clean_unlabeled_data(unlabeled_df):
    """
    Cleans the unlabeled data by removing NaN and empty tweets.

    Args:
    - unlabeled_df: DataFrame containing unlabeled data.

    Returns:
    - cleaned_df: Cleaned DataFrame.
    """
    unlabeled_df = unlabeled_df.dropna(subset=['Tweets'])
    unlabeled_df = unlabeled_df[unlabeled_df['Tweets'].str.strip() != ""]
    
    return unlabeled_df


def calculate_depression_percentage(y_unlabeled_pred):
    """
    Calculates the percentage of depressed tweets.

    Args:
    - y_unlabeled_pred: Predicted labels.

    Returns:
    - depression_percentage: Percentage of depressed tweets.
    """
    return (np.sum(y_unlabeled_pred == '1') / len(y_unlabeled_pred)) * 100


def get_depression_terms(vectorizer, model):
    """
    Retrieves top depression terms based on model coefficients.

    Args:
    - vectorizer: TF-IDF vectorizer used for feature extraction.
    - model: Trained logistic regression model.

    Returns:
    - top_depression_terms: Top depression terms.
    """
    # Get the feature names from the TF-IDF vectorizer
    feature_names = np.array(vectorizer.get_feature_names_out())

    # Get the coefficients of the logistic regression model
    coef_indices = model.coef_[0]

    # Sort the coefficients in descending order to find top depression indicators
    top_depression_indices = np.argsort(-coef_indices)

    # Select top 50 depression terms if available, otherwise select all terms
    if len(top_depression_indices) >= 50:
        top_depression_terms = [feature_names[index] for index in np.argsort(top_depression_indices)[-50:]]
    else:
        # If fewer than 50 terms available, select all terms
        top_depression_terms = [feature_names[index] for index in np.argsort(top_depression_indices)[-len(coef_indices):]]

    # Return the top depression terms
    return top_depression_terms



def split_data(X, Y):
    """
    Splits the dataset into training and testing sets.

    Args:
    - X: Features (tweets).
    - Y: Labels.

    Returns:
    - X_train, y_train: Training data.
    - X_test, y_test: Testing data.
    """
    # Combine tweets and labels into tuples
    combined_tweets = [(tweet, label) for tweet, label in zip(X, Y.astype(str))]

    # Separate depressed and non-depressed tweets
    depressed_tweets = [(tweet, label) for tweet, label in combined_tweets if label == '1']
    non_depressed_tweets = [(tweet, label) for tweet, label in combined_tweets if label == '2']

    # Split depressed tweets into training and testing sets
    X_train_depressed, X_test_depressed, y_train_depressed, y_test_depressed = train_test_split(
        [tweet for tweet, _ in depressed_tweets], [label for _, label in depressed_tweets],
        test_size=0.2, random_state=42, stratify=[label for _, label in depressed_tweets]
    )

    # Split non-depressed tweets into training and testing sets
    X_train_non_depressed, X_test_non_depressed, y_train_non_depressed, y_test_non_depressed = train_test_split(
        [tweet for tweet, _ in non_depressed_tweets], [label for _, label in non_depressed_tweets],
        test_size=0.2, random_state=42, stratify=[label for _, label in non_depressed_tweets]
    )

    # Combine depressed and non-depressed training sets
    X_train = X_train_depressed + X_train_non_depressed
    y_train = y_train_depressed + y_train_non_depressed

    # Combine depressed and non-depressed testing sets
    X_test = X_test_depressed + X_test_non_depressed
    y_test = y_test_depressed + y_test_non_depressed

    # Return the combined training and testing sets
    return X_train, y_train, X_test, y_test


def main(dataset_path):
    """
    Main function to train the model, test it, and analyze user tweets.

    Args:
    - dataset_path: Path to the dataset.

    Returns:
    - vectorizer: TF-IDF vectorizer.
    - depression_percentage: Percentage of depression in the dataset.
    - best_model: Trained logistic regression model.
    """
    # Load dataset
    df = pd.read_csv(dataset_path)

    # Preprocess tweets
    df["Tweets"] = df['Tweets'].apply(lambda x: preprocess(x))

    X = df['Tweets']
    y = df['Label']

    # Split dataset into training and testing sets
    X_train, y_train, X_test, y_test = split_data(X, y)

    # Train the model
    best_model, vectorizer = train_model(X_train, y_train)

    # Test the model
    y_pred = test_model(best_model, vectorizer, X_test, y_test)

    # Calculate depression percentage
    depression_percentage = calculate_depression_percentage(y_pred)

    return vectorizer, depression_percentage, best_model


# Execute main function
vectorizer, depression_percentage, best_model = main('../Datasets/Github-All-Twitter-dataset-Experts.csv')

# Save the trained model, and vectorizer
joblib.dump(best_model, 'Extras/LR_Model.pkl')
joblib.dump(vectorizer, 'Extras/vectorizer.pkl')
