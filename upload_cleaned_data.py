import pandas as pd
import snowflake.connector

# Load and clean the Titanic data
df = pd.read_csv("titanic.csv")

# Drop unneeded columns
df.drop(['Cabin', 'Ticket'], axis=1, inplace=True)

# Fill missing values
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

# Encode categorical variables
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})
df['Embarked'] = df['Embarked'].map({'S': 0, 'C': 1, 'Q': 2})

# 🧠 Connect to Snowflake
conn = snowflake.connector.connect(
    user='PANDEYYASH12',
    password='Yashrajpandey12',
    account='zq00431.ap-southeast-1',
    warehouse='COMPUTE_WH',
    database='TITANIC',
    schema='PUBLIC'
)
cur = conn.cursor()

# 🗃️ Create new cleaned table
create_cleaned_table = """
CREATE OR REPLACE TABLE TITANIC_CLEANED (
    PassengerId INTEGER,
    Survived INTEGER,
    Pclass INTEGER,
    Name STRING,
    Sex INTEGER,
    Age FLOAT,
    SibSp INTEGER,
    Parch INTEGER,
    Fare FLOAT,
    Embarked INTEGER
);
"""
cur.execute(create_cleaned_table)

# 📤 Insert cleaned data
for _, row in df.iterrows():
    insert_query = f"""
    INSERT INTO TITANIC_CLEANED VALUES (
        {int(row['PassengerId'])},
        {int(row['Survived'])},
        {int(row['Pclass'])},
        $$ {row['Name']} $$,
        {int(row['Sex'])},
        {float(row['Age'])},
        {int(row['SibSp'])},
        {int(row['Parch'])},
        {float(row['Fare'])},
        {int(row['Embarked'])}
    );
    """
    cur.execute(insert_query)

print("✅ Cleaned data successfully uploaded to Snowflake as 'TITANIC_CLEANED'.")

cur.close()
conn.close()
