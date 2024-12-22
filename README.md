NDVI-Based Crop Classification for Rice and Cotton

This repository contains the implementation of a machine learning project for NDVI (Normalized Difference Vegetation Index)-based crop classification. The project focuses on classifying rice and cotton crops using supervised and unsupervised learning techniques.

Project Overview

Agricultural crop classification using NDVI is crucial for monitoring and optimizing crop production. This project leverages time-series NDVI data spanning multiple years (2021-2023) and applies machine learning algorithms to accurately classify crops.

Goals

Classify crops (rice and cotton) using machine learning.

Optimize model performance using hyperparameter tuning.

Explore supervised learning techniques like Random Forest, XGBoost, Bagging, and SVM.

Investigate the use of unsupervised learning techniques for clustering and analysis.

Dataset Description

Files:

rice2021.csv, rice2022.csv, rice2023.csv

cotton2021.csv, cotton2022.csv, cotton2023.csv

Features:

NDVI values over time for different crop types.

Year column added during pre-processing.

Project Workflow

1. Pre-Processing

Pre-processing ensures the data is clean, normalized, and ready for training.

Key Steps:

Added a year column to track temporal data.

Labeled crops as rice or cotton.

Combined datasets into a single dataframe.

Applied data augmentation using time-series shifting:

Shifted cotton NDVI values forward by 2 months.

Shifted rice NDVI values backward by 2 months.

Filled missing values using column means.

Normalized NDVI values using MinMaxScaler.

Engineered features:

Added mean NDVI and max NDVI.

Applied SMOTE oversampling to handle class imbalance.

2. Supervised Learning

Implemented and evaluated the following supervised learning algorithms:

Random Forest

XGBoost (Extreme Gradient Boosting)

Bagging (Bootstrap Aggregation)

Support Vector Machine (SVM)

Performance Metrics:

Accuracy

Recall

Precision

F1-Score

Confusion Matrix (class-wise and overall)

Grid Search for Hyperparameter Optimization:

Parameters optimized for each algorithm:

XGBoost: learning_rate, max_depth, n_estimators

Bagging: n_estimators, base_estimator__max_depth

Random Forest: n_estimators, max_depth, min_samples_leaf

SVM: kernel, C, gamma

3. Unsupervised Learning

Explored clustering algorithms like K-Means and DBSCAN to identify patterns in NDVI data. Insights were compared with supervised models.

Results

Supervised Learning:

Models achieved high classification accuracy.

Best-performing algorithm: SVM.

Grid Search yielded optimized hyperparameters for each model.

Feature Importance analysis highlighted key NDVI-based features.

Unsupervised Learning:

Clustering provided insights into crop growth patterns.

Best-performing algorithm: Hierarchical Clustering
Validation metrics like silhouette score were used to evaluate clustering performance.
