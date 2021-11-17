# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app

# 1 column layout
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """



## Importing and Reading the Data
The first step to working on this project was finding a data set that would work for my purpose. I was able to find one via Kaggle. At first glance, I thought the data set would not be big enough for me to work with, but it ended up having over 600 rows of data to work with! Now that we have the dataset, I did a quick read to see my columns (features). All of the columns were looking pretty good besides needing cleaning besides two columns. Since I want to predict whether you would be pre-approved for a loan, I felt that the loan amount and loan term column would cause data leakage. I knew I would have to drop these when I fully began to clean my data. 

#### Wrangling The Data
```
#### Creating the Function
def trainwrangle(filepath):
  # Read in the CSV file
  df = pd.read_csv(filepath, index_col='Loan_ID')
```
#### Cleaning My Target
For this step of wrangling my data, I had to turn my target column "Loan Status" from Yes and No into 1 and 0 to tell which accounts were approved or not. I also dropped all NaN values from these columns since we would cheat the model if we didn't fill those NaN values.

```
  # Turning my target into 1 and 0s
  # Dropping NaN Values from my Target column
  df['Loan_Status'] = (df['Loan_Status'] == 'Y').astype(int)
  df.dropna(subset=['Loan_Status'], inplace = True)
```
#### Label Encoding
Next, I decided to Label encode the rest of my columns into a binary format. I could have used an encoder for this step, but I decided to do this in my wrangle function.

```
  # Label Encoding Columns so they are represent by numbers
  df['Gender'] = df['Gender'].map({'Male':1, 'Female':0})
  df['Married'] = df['Married'].map({'Yes':1, 'No':0})
  df['Dependents'] = df['Dependents'].map({'0':0, '1':1, '2':2, '3+':3})
  df['Education'] = df['Education'].map({'Graduate':1, 'Not Graduate':0})
  df['Self_Employed'] = df['Self_Employed'].map({'Yes':1, 'No':0})
  df['Property_Area'] = df['Property_Area'].map({'Rural':0, 'Semiurban':1, 'Urban':2})
```

#### Filling NaN Values
After doing label encoding, I decided to start working on filling NaN values. I used the median for most of the columns to fill the NaN values, but for Loan Amount, I had to use mean since I was dealing with multiple float values.

```
  # Filling NaN values
  df['Gender'].fillna(df['Gender'].median(),inplace=True)
  df['Married'].fillna(df['Married'].median(),inplace=True)
  df['Dependents'].fillna(df['Dependents'].median(),inplace=True)
  df['Self_Employed'].fillna(df['Self_Employed'].median(),inplace=True)
  df['LoanAmount'].fillna(df['LoanAmount'].mean(),inplace=True)
  df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].median(),inplace=True)
  df['Credit_History'].fillna(df['Credit_History'].median(),inplace=True)
```

#### Dropping Unneeded Columns and Data Leakage Columns
The last step was for me to drop the two data leakage columns called Loan Amount and Loan Amount Term. These were causing data leakage due to the fact we would not know how much of a loan you are approved for and the terms to the that loan. Last we dropped property area because this is not needed for a loan pre-approval.
```
  df.drop(columns=['LoanAmount','Loan_Amount_Term','Property_Area'], inplace=True)
return df 
```

## MODEL BUILDING
#### Before the Model
So, before we jump into which machine learning models we are using, we must split our data into an X matrix and a y vector, if you remember from the Introduction text above. We are trying to predict if someone would be pre-approved for a home loan or not, To do this, we will set our target as 'loan_status' Our X will be all the columns beside the target. The y will be the target.

```
# Splitting into my X Matrix and y vector
target = 'Loan_Status'
y = df[target]
X = df.drop(target, axis=1)
```

Now I have to split X matrix into a X train and X Validation set. Same with the Y vector.

```
# Using a random train test split
X_train, X_val, y_train, y_val = train_test_split(X, y , test_size=0.2, random_state = 1)
```

Now it is time to determine our baseline. Since we are dealing with a categorical Y vector we will have to use the majority in the categorical values.

```
# Establishing a baseline
#Checking to see what the current y counts look like.
y.value_counts()

# Turning the y counts into floats(percents)
y.value_counts(normalize=True)

# The baseline will always be the majority in categorical
baseline = y.value_counts(normalize=True).max()
```

## My 5 Models
Now it is time for me to start diving into building a couple of different models. I decided to use Logistic Regression, Decision Tree, Random Forest, XG Boost, and Gradiant Boost Models to test different ways to solve this solution. I won't go too far into the code, but below are the models labeled. While looking at the models, you will notice a Training Accuracy and a Validation accuracy. I used my Train and Validation sets on my models to get these percent numbers.


#### Model 1: Logistic Regression
```
model_lr = make_pipeline(
    SimpleImputer(),
    StandardScaler(),
    LogisticRegression()
)

model_lr.fit(X_train,y_train);

Training Accuracy (LOGR): 0.814663951120163
Validation Accuracy (LOGR): 0.7967479674796748
              precision    recall  f1-score   support

           0       0.89      0.41      0.56        39
           1       0.78      0.98      0.87        84

    accuracy                           0.80       123
   macro avg       0.83      0.69      0.71       123
weighted avg       0.82      0.80      0.77       123
```

#### Model 2: DecisionTree
```
model_dt = make_pipeline(
    SimpleImputer(strategy='median'),
    DecisionTreeClassifier(random_state=1, max_depth=2)
)

model_dt.fit(X_train, y_train);

Training Accuracy (DT): 0.8167006109979633
Validation Accuracy (DT): 0.7967479674796748
              precision    recall  f1-score   support

           0       0.89      0.41      0.56        39
           1       0.78      0.98      0.87        84

    accuracy                           0.80       123
   macro avg       0.83      0.69      0.71       123
weighted avg       0.82      0.80      0.77       123
```

#### Model 3: Random Forest
```
model_rf = RandomForestClassifier(max_depth=10,n_estimators=75, random_state=1, n_jobs=-1,max_features=5,max_leaf_nodes=113,min_samples_leaf=25)                     



model_rf.fit(X_train,y_train);

Training Accuracy (RF): 0.8105906313645621
Validation Accuracy (RF): 0.8048780487804879
              precision    recall  f1-score   support

           0       0.89      0.41      0.56        39
           1       0.78      0.98      0.87        84

    accuracy                           0.80       123
   macro avg       0.83      0.69      0.71       123
weighted avg       0.82      0.80      0.77       123
```

#### Model 4: XG BOOST
```
model_xg = make_pipeline(
    XGBClassifier(random_state=42, n_estimators=15,n_jobs=-1,max_depth=2,),)                     


model_xg.fit(X_train,y_train);


Training Accuracy (XG): 0.8105906313645621
Validation Accuracy (XG): 0.8048780487804879
              precision    recall  f1-score   support

           0       0.94      0.41      0.57        39
           1       0.78      0.99      0.87        84

    accuracy                           0.80       123
   macro avg       0.86      0.70      0.72       123
weighted avg       0.83      0.80      0.78       123
```

#### Model 5: Gradiant Boost
```
model_gb = make_pipeline(
    GradientBoostingClassifier(random_state=42, n_estimators=75, learning_rate=0.1),                     


)
model_gb.fit(X_train,y_train);


Training Accuracy (GB): 0.8513238289205702
Validation Accuracy (GB): 0.7967479674796748
              precision    recall  f1-score   support

           0       0.89      0.41      0.56        39
           1       0.78      0.98      0.87        84

    accuracy                           0.80       123
   macro avg       0.83      0.69      0.71       123
weighted avg       0.82      0.80      0.77       123
```

## Conculsion
As you can see there are a few models that give pretty much the same results. Juding from that I would be able to use any of those models to move foward with anything else I need to do with these pipelines. Personally. I choose to go with the Random Forest model.


            """
        ),

    ],
)

layout = dbc.Row([column1])