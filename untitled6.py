# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18cEyJQVOVM2mdWXA79p9eo3Il452hkmY
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pandas as pd
df=pd.read_csv(r"/content/hotel_bookings.csv")
df

df.info()

categorical_name = []
for col in df.columns:
    if df[col].dtype == 'object':
        categorical_name.append(col)
categorical_name

numerical = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col])]
numerical

#all numerical columns and assign in numerical variable

df.describe()

# EDA(Exploratory Data Analysis)

df.isna().sum()

# Feature 1 find null values and outliers 'country'

columns=['country','agent','company']
df[columns].isna().sum()

# Fill null values in specified columns with mode for categorical data
for col in columns:
    if df[col].dtype == 'object':
        df[col].fillna(df[col].mode()[0], inplace=True)
    else:
        df[col].fillna(df[col].mean(), inplace=True)

df['country'].isna().sum()

df['agent'].isna().sum()

df['company'].isna().sum()

df.boxplot()

df.info()

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import pandas as pd
import numpy as np

for col in categorical_name:
    if df[col].isnull().any():
      df[col].fillna(df[col].mode(), inplace=True)

    if df[col].nunique() <= 10:
        ohe = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        ohe_data = ohe.fit_transform(df[[col]])
        ohe_df = pd.DataFrame(ohe_data, columns=ohe.get_feature_names_out([col]))
        df = pd.concat([df, ohe_df], axis=1)
        df.drop(columns=[col], inplace=True)
    else:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
print(df.info())
print(df.head())

plt.figure(figsize=(10, 6))
sns.countplot(x='is_canceled', data=df)
plt.title('Cancellation Rates')
plt.show()

plt.figure(figsize=(10, 6))
sns.countplot(x='is_canceled', hue='lead_time', data=df)
plt.title('Cancellation Rates by Lead Time')
plt.show()

"""**Hypothesis**"""

# Hypothesis 1: Customers booking more than 6 months in advance are more likely to cancel.

group1 = df[df['lead_time'] <= 180]['is_canceled']
group2 = df[df['lead_time'] > 180]['is_canceled']


# Perform a Chi-Square test
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"Chi-Square test results for Hypothesis 1:")
print(f"t-statistic: {t_stat:.2f}")
print(f"p-value: {p_value:.3f}")

df.info()

df.corr()

plt.figure(figsize=(20, 16)) # Increased figure size
sns.heatmap(df.corr(), annot=True, cmap='PiYG', fmt=".2f")
plt.title('Corr Matrix ')
plt.show()

df.info()

# Split the data into training and testing sets BEFORE imputation
X = df.drop('is_canceled', axis=1)
y = df['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

numerical_cols = X_train.select_dtypes(include=np.number).columns
imputer = SimpleImputer(strategy='mean')
X_train[numerical_cols] = imputer.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = imputer.transform(X_test[numerical_cols])

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score

# Train Logistic Regression
logreg = LogisticRegression(solver='liblinear')  # Specify a solver
logreg.fit(X_train, y_train)
y_pred_logreg = logreg.predict(X_test)
accuracy_logreg = accuracy_score(y_test, y_pred_logreg)
print(f"Logistic Regression Accuracy: {accuracy_logreg}")

# Train Random Forest
rf = RandomForestClassifier(random_state=5)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print(f"Random Forest Accuracy: {accuracy_rf}")

# prompt: why the accuracy is showing 1.0 in random regression how to get near about random forest is 86.00

from sklearn.model_selection import train_test_split

# ... (Your existing code) ...

# Split the data into training and testing sets BEFORE imputation
X = df.drop('is_canceled', axis=1)
y = df['is_canceled']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5)

# Impute missing values AFTER splitting the data
numerical_cols = X_train.select_dtypes(include=np.number).columns
imputer = SimpleImputer(strategy='mean')
X_train[numerical_cols] = imputer.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = imputer.transform(X_test[numerical_cols])

# ... (rest of your code) ...