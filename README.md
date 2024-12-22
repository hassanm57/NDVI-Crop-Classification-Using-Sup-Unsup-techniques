## NDVI Crop Classification (rice-cotton) Using ML Algorithms
## Dataset

- **Data Source**: NDVI time-series values for 2021, 2022, and 2023.
- **Features**: 12 NDVI readings per crop representing bi-monthly measurements over six months.
- **Challenges**:
- Imbalanced dataset (more cotton samples than rice).
- Seasonal variations in NDVI patterns.

## Methodology

### Supervised Learning
- **Algorithms**:
- Random Forest
- XGBoost
- SVM
- **Validation**:
- Train on two years, test on the third year (cross-validation).
- **Optimization**:
- Grid Search for hyperparameter tuning.

### Unsupervised Learning
- **Algorithms**:
- K-Means, Hierarchical Clustering, DBSCAN
- **Evaluation**:
- Cluster Purity and Confusion Matrix (with and without PCA).

### Preprocessing
- NDVI normalization.
- Data augmentation with noise addition or time-series shifting.

## Deliverables

1. **Code**:
 - Clean, modular implementation with detailed comments.
 - Evaluation metrics for each model: Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
 - Visualization using Matplotlib and Seaborn.

2. **Report**:
 - Key insights on model performance and feature importance.
 - Comparisons of supervised and unsupervised techniques.

3. **Presentations**:
 - Summarized results with visual aids.

## Key Metrics

- **Supervised Models**:
- Accuracy, F1-Score, and feature importance (e.g., for Random Forest).
- **Unsupervised Models**:
- Cluster Purity and performance with PCA.

## Results

- Comparative performance of supervised models (Random Forest, XGBoost) and unsupervised clustering methods.
- Insights into NDVI patterns for rice and cotton classification.

## Future Improvements

- Experiment with deep learning models for time-series classification.
- Use larger datasets to improve generalization.
- Explore additional features like soil moisture or weather data.

---

This project highlights the use of data-driven techniques in agriculture, paving the way for better crop monitoring and decision-making.
