import pandas as pd

# Step 1: Load raw Titanic data
df = pd.read_csv("titanic.csv")

# Step 2: Basic null check
print("Before cleaning:")
print(df.isnull().sum())

# Step 3: Drop unnecessary columns
df.drop(['Cabin', 'Ticket'], axis=1, inplace=True)

# Step 4: Fill missing values
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Step 5: Encode categorical columns
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

# Step 6: Preview cleaned data
print("\nAfter cleaning:")
print(df.head())
