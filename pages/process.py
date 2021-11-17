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
        
            # Importing and Reading the Data
The first step to working on this project was finding a data set that would work for my purpose. I was able to find one via Kaggle. At first glance, I thought the data set would not be big enough for me to work with, but it ended up having over 600 rows of data to work with! Now that we have the dataset, I did a quick read to see my columns (features). All of the columns were looking pretty good besides needing cleaning besides two columns. Since I want to predict whether you would be pre-approved for a loan, I felt that the loan amount and loan term column would cause data leakage. I knew I would have to drop these when I fully began to clean my data. 

### Creating the Wrangle Function

```
#Creating Function
def trainwrangle(filepath):
  # Read in the CSV file
  df = pd.read_csv(filepath, index_col='Loan_ID')
```
### Cleaning My Target
For this step of wrangling my data, I had to turn my target column "Loan Status" from Yes and No into 1 and 0 to tell which accounts were approved or not. I also dropped all NaN values from these columns since we would cheat the model if we didn't fill those NaN values.

```
  # Turning my target into 1 and 0s
  # Dropping NaN Values from my Target column
  df['Loan_Status'] = (df['Loan_Status'] == 'Y').astype(int)
  df.dropna(subset=['Loan_Status'], inplace = True)
```
### Label Encoding
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

### Filling NaN Values
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

# Dropping Unneeded Columns and Data Leakage Columns
The last step was for me to drop the two data leakage columns called Loan Amount and Loan Amount Term. These were causing data leakage due to the fact we would not know how much of a loan you are approved for and the terms to the that loan. Last we dropped property area because this is not needed for a loan pre-approval.
```
  df.drop(columns=['LoanAmount','Loan_Amount_Term','Property_Area'], inplace=True)
return df 
```


            """
        ),

    ],
)

layout = dbc.Row([column1])