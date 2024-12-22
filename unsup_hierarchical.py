# -*- coding: utf-8 -*-
"""unsup_hierarchical.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10OIl6i1KGhwRUG3ZHl6cPZTGzdv34A7i

Hassan Mansoor - 403544 - CS12A

# **Unsupervised** **Algorithms**

**Data Preparation**

Mount Drive
"""

from google.colab import drive
drive.mount('/content/drive')

"""Import The Libraries"""

import os
import pandas as pd

"""Importing The Data"""

# Define the folder paths
base_path = '/content/drive/My Drive/Crop-dataset'
rice_folder = os.path.join(base_path, 'Rice')
cotton_folder = os.path.join(base_path, 'Cotton')

# Load CSV files
rice_2021 = pd.read_csv(os.path.join(rice_folder, 'rice2021.csv'))
rice_2022 = pd.read_csv(os.path.join(rice_folder, 'rice2022.csv'))
rice_2023 = pd.read_csv(os.path.join(rice_folder, 'rice2023.csv'))

cotton_2021 = pd.read_csv(os.path.join(cotton_folder, 'cotton2021.csv'))
cotton_2022 = pd.read_csv(os.path.join(cotton_folder, 'cotton2022.csv'))
cotton_2023 = pd.read_csv(os.path.join(cotton_folder, 'cotton2023.csv'))

"""Add Year Column To Each Datafile"""

# Add year column to each dataset
rice_2021['year'] = 2021
rice_2022['year'] = 2022
rice_2023['year'] = 2023

cotton_2021['year'] = 2021
cotton_2022['year'] = 2022
cotton_2023['year'] = 2023

# Verify the addition
print("Rice 2021 with year column:\n", rice_2021.head())
print("Cotton 2021 with year column:\n", cotton_2021.head())

"""Add Labels To Datasset"""

# Add labels
rice_2021['label'] = 'rice'
rice_2022['label'] = 'rice'
rice_2023['label'] = 'rice'

cotton_2021['label'] = 'cotton'
cotton_2022['label'] = 'cotton'
cotton_2023['label'] = 'cotton'

print("Rice 2021 data:\n", rice_2021.head())
print("Cotton 2021 data:\n", cotton_2021.head())

"""# Combining The Datasets"""

import pandas as pd

# Combine rice datasets
rice_combined = pd.concat([rice_2021, rice_2022, rice_2023], axis=0)

# Combine cotton datasets
cotton_combined = pd.concat([cotton_2021, cotton_2022, cotton_2023], axis=0)

# Merge rice and cotton datasets
all_data = pd.concat([rice_combined, cotton_combined], axis=0).reset_index(drop=True)

print("Combined dataset:\n", all_data.head())
print("Shape of the dataset:", all_data.shape)

"""# Data Normalization And Preprocessing

# Time Series Shifting
"""

# Identify NDVI columns
ndvi_columns = [col for col in all_data.columns if 'NDVI' in col]

# Shift cotton NDVI values forward to simulate earlier growth (by 2 months)
cotton_shifted = cotton_combined.copy()
cotton_shifted[ndvi_columns] = cotton_shifted[ndvi_columns].shift(periods=2, axis=0)

# Shift rice NDVI values backward to simulate later growth (by 2 months)
rice_shifted = rice_combined.copy()
rice_shifted[ndvi_columns] = rice_shifted[ndvi_columns].shift(periods=-2, axis=0)

# Combine the shifted datasets back with the original ones (for augmentation)
augmented_data = pd.concat([cotton_shifted, rice_shifted], axis=0).reset_index(drop=True)

# Combine original and shifted datasets
augmented_data = pd.concat([cotton_combined, rice_combined, cotton_shifted, rice_shifted], axis=0).reset_index(drop=True)

# Verify the augmented data
print(augmented_data.head())

"""Shifting the NDVI time series helps simulate different seasonal growth cycles for rice and cotton and introduces variability into the model.
This approach will make the model more adaptable to the natural seasonality of the crops, improving its performance.

Handle Missing Values
"""

# Check for missing values
missing_values = augmented_data.isnull().sum()

# Print missing values for each column
print("Missing values for each column:\n", missing_values)

"""Fill in missing values with mean"""

# Calculate the mean of each column (excluding non-numeric columns)
column_means = augmented_data.select_dtypes(include=['number']).mean()

# Fill missing values with the calculated means
augmented_data = augmented_data.fillna(column_means)

missing_values = augmented_data.isnull().sum()
# Print missing values for each column
print("Missing values for each column:\n", missing_values)

"""No missing values anymore!

Encode The Labels (1 for Rice - 0 For Cotton)
"""

from sklearn.preprocessing import LabelEncoder

# Encode the label column
label_encoder = LabelEncoder()
augmented_data['label_encoded'] = label_encoder.fit_transform(augmented_data['label'])
augmented_data = augmented_data.drop('label', axis=1)

"""# Feature Selection"""

from sklearn.feature_selection import SelectKBest, f_classif

# Separate features (X) and target labels (y)
X = augmented_data.drop(columns=['label_encoded','year'])
y = augmented_data['label_encoded']

# Perform feature selection
selector = SelectKBest(score_func=f_classif, k=10)  # Select top k features
X_selected = selector.fit_transform(X, y)

# Get the names of the selected features
selected_features = X.columns[selector.get_support()]
print("Selected features:", selected_features)

# Update the balanced_data with only the selected features
balanced_data = pd.DataFrame(X_selected, columns=selected_features)
balanced_data['label_encoded'] = y

"""# Apply Undersampling Of Cotton"""

from sklearn.utils import resample

# Separate rice and cotton data
rice_data = balanced_data[augmented_data['label_encoded'] == 1]  # 1 for rice
cotton_data = balanced_data[augmented_data['label_encoded'] == 0]  # 0 for cotton

# Perform undersampling on cotton data to match the number of rice samples
cotton_undersampled = resample(cotton_data,
                               replace=False,    # No replacement
                               n_samples=len(rice_data),    # Match rice sample size
                               random_state=42)  # For reproducibility

# Combine rice data and undersampled cotton data
balanced_data = pd.concat([rice_data, cotton_undersampled])

# Check the new distribution of classes
print("New class distribution after undersampling:\n", balanced_data['label_encoded'].value_counts())

balanced_data.head(-5)

"""# Normalize The NDVI Values"""

from sklearn.preprocessing import MinMaxScaler

# Normalize the selected feature columns
scaler = MinMaxScaler()
balanced_data[selected_features] = scaler.fit_transform(balanced_data[selected_features])  # Use selected features

print("Normalized selected feature values:\n", balanced_data[selected_features].head())

# Check unique labels and their counts
print("Unique labels in the dataset:", balanced_data['label_encoded'].unique())
print("Label distribution:\n", balanced_data['label_encoded'].value_counts())

"""# **Copy Dataframe With True Labels To Another**"""

# Create a copy of balanced_data
true_val_df = balanced_data.copy()

# Verify the copy
print(true_val_df.head())

"""# **Remove Labels For Unsupervised Algorithm**

View data columns
"""

print(balanced_data.columns)

"""Remove Unnecessary Columns"""

# Remove 'label_encoded' columns
balanced_data = balanced_data.drop(['label_encoded'], axis=1)
balanced_data_0 = balanced_data.copy() # for kmeans without pca
balanced_data_0 = balanced_data_0.sample(frac=1, random_state=42).reset_index(drop=True) # shuffle the data again for randomness (same state for reproducibility)

# Verify the changes
print(balanced_data.columns)
print(balanced_data_0.columns)

"""View Data to check"""

balanced_data.shape
balanced_data.head()

"""# **Hierarchical Clustering**
**Agglomerative Clustering**

**Without PCA**

Import Necessary Libraries
"""

from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

"""Apply Agglomerative Clustering"""

# Apply Agglomerative Clustering
agg_clust = AgglomerativeClustering(n_clusters=2,linkage='ward')
clusters_agg = agg_clust.fit_predict(balanced_data)

"""Add Cluster Labels And View The Dataset"""

# Add the cluster labels to the dataset
balanced_data['cluster_agg'] = clusters_agg

# Visualize the clusters (same as before but with hierarchical clustering)
plt.figure(figsize=(6, 6))
plt.scatter(balanced_data_0.iloc[:, 0], balanced_data_0.iloc[:, 1], c=clusters_agg, cmap='viridis', s=10)
plt.title('Hierarchical Clustering (Agglomerative) without PCA')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.show()

"""Calculate Cluster Purity"""

from sklearn.metrics import confusion_matrix
import numpy as np

def calculate_purity(y_true, y_pred):
    """
    Calculates the cluster purity by comparing the predicted clusters with the true labels.
    Purity is the proportion of correctly assigned samples in the dataset.

    Parameters:
    ----------
    y_true : array-like of shape (n_samples,)
        True class labels for each sample in the dataset.

    y_pred : array-like of shape (n_samples,)
        Predicted cluster labels for each sample, as output by the clustering algorithm.

    Returns:
    -------
    float
        The purity score (percentage of correctly assigned samples).
    """
    # Create the confusion matrix (contingency matrix)
    contingency_matrix = confusion_matrix(y_true, y_pred)

    # Purity is calculated as the sum of the maximum values in each column, divided by the total number of samples
    purity = np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix)

    return purity

# Now you can use this function to calculate the purity score for your clustering results

# Calculate the cluster purity for hierarchical clustering (without PCA)
purity_agg = calculate_purity(true_val_df['label_encoded'], clusters_agg)
print(f"Cluster Purity with Hierarchical Clustering (without PCA): {round(purity_agg * 100, 1)}%")

"""Confusion Matrix"""

import seaborn as sns  # Import the library for use
# Plot the confusion matrix for Hierarchical Clustering
cm = confusion_matrix(true_val_df['label_encoded'], clusters_agg)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Cotton', 'Rice'], yticklabels=['Cotton', 'Rice'])
plt.title('Confusion Matrix for Agglomerative Clustering (without PCA)')
plt.xlabel('Predicted Clusters')
plt.ylabel('True Labels')
plt.show()
print(cm)

"""**Plot The Dendrogram**"""

# Dendrogram
plt.figure(figsize=(10, 7))
sch.dendrogram(sch.linkage(balanced_data.iloc[:, :-1], method='ward'))  # Exclude the target column ('label_encoded')
plt.title('Dendrogram for Agglomerative Clustering (without PCA)')
plt.xlabel('Samples')
plt.ylabel('Euclidean Distance')
plt.show()

"""# **Hierarchical Clustering With PCA**

Import necessary libraries
"""

from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
import numpy as np

"""Scale The Data"""

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(balanced_data[selected_features])

"""Apply PCA"""

pca = PCA(n_components=0.95)  # Reduce to 2 components
X_pca = pca.fit_transform(X_scaled)

"""Apply Agg Clustering"""

agg_clust_pca = AgglomerativeClustering(n_clusters=2, linkage='ward')
clusters_agg_pca = agg_clust_pca.fit_predict(X_pca)

balanced_data.shape

"""Add To Dataset"""

# Add the cluster labels to the dataset
balanced_data['cluster_agg_pca'] = clusters_agg_pca

"""# Visualize Clusters With PCA"""

# Visualize the clusters formed by Agglomerative Clustering
plt.figure(figsize=(6, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=clusters_agg_pca, cmap='viridis', s=10)
plt.title('Agglomerative Clustering with PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.show()

"""# Calculate The Cluster Purity"""

purity_agg_pca = calculate_purity(true_val_df['label_encoded'], clusters_agg_pca)
print(f"Cluster Purity with Agglomerative Clustering and PCA: {round(purity_agg_pca * 100, 1)}%")

"""Confusion Matrix"""

# Plot the confusion matrix for Agglomerative Clustering with PCA
cm = confusion_matrix(true_val_df['label_encoded'], clusters_agg_pca)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Cotton', 'Rice'], yticklabels=['Cotton', 'Rice'])
plt.title('Confusion Matrix for Agglomerative Clustering with PCA')
plt.xlabel('Predicted Clusters')
plt.ylabel('True Labels')
plt.show()
print(cm)

"""Visualize The Dendrogram"""

import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt

# Plot the dendrogram for PCA-transformed data
plt.figure(figsize=(10, 7))
sch.dendrogram(sch.linkage(X_pca, method='ward'))
plt.title('Dendrogram for PCA-transformed Data')
plt.xlabel('Samples')
plt.ylabel('Euclidean Distance')
plt.show()