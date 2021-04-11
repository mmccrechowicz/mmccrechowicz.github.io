---
title: "New post"
date: 2021-04-10T15:17:31.586474
draft: true
summary: Post summary.
---

# UK University Research Excellence Framework Ratings 2014



## Set up

### Install SQLite


```python
!pip install -q pysqlite3-binary
```

    [K     |████████████████████████████████| 5.2MB 21.9MB/s 
    [?25h

### Define functions


```python
# #@title Define functions
import tempfile
from urllib import request
import sqlite3
import pysqlite3

from typing import Dict

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
%matplotlib inline

import seaborn as sns
sns.set()

#%load_ext google.colab.data_table

# Set float display options for pandas dataframes.
pd.options.display.float_format = "{:,.2f}".format

def excel_dataset_to_sqlite(url: str, database_name: str = ":memory:") -> sqlite3.Connection:
  """Downloads an excel dataset and loads it into an sqlite database."""

  # Download the data into a local variable.
  data = request.urlopen(url).read()

  # Write it out to afiles
  with tempfile.TemporaryFile() as fle:
    fle.write(data)

    # Read into pandas from excel file.
    data = pd.read_excel(fle, sheet_name=None)

  # Create a database.
  conn = pysqlite3.connect(database_name)

  # Loads data from pandas objects into individual tables.
  for (key, sheet) in data.items():
    sheet = sheet.where(pd.notnull(sheet), None)
    sheet.to_sql(key, conn)


  # Return database.
  return conn
```

## Prepare the data

### Import the dataset and create the database


```python
database = excel_dataset_to_sqlite("https://public.tableau.com/s/sites/default/files/media/Resources/Research%20Excellence%20Framework%202014%20Results_Pivoted.xlsx")
```

    /usr/local/lib/python3.7/dist-packages/pandas/core/generic.py:2615: UserWarning: The spaces in these column names will not be changed. In pandas versions < 0.14, spaces were converted to underscores.
      method=method,


### View the table names to make sure the correct tables have been created


```python
pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", database)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Sheet1-Tableau</td>
    </tr>
    <tr>
      <th>1</th>
      <td>About</td>
    </tr>
  </tbody>
</table>
</div>



### That table name isn't very helpful. Let's change it to something more meaningful.


```python
pd.read_sql("ALTER TABLE 'Sheet1-Tableau' RENAME TO REF_Results;", database)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>1</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>




```python
pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", database)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>REF_Results</td>
    </tr>
    <tr>
      <th>1</th>
      <td>About</td>
    </tr>
  </tbody>
</table>
</div>



### Now let's have a look at the column names to make sure they won't make it difficult to work with this dataset.


```python
pd.read_sql("SELECT * FROM REF_Results;", database)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>Institution code (UKPRN)</th>
      <th>Institution name</th>
      <th>Institution sort order</th>
      <th>Main panel</th>
      <th>Unit of assessment number</th>
      <th>Unit of assessment name</th>
      <th>Multiple submission letter</th>
      <th>Multiple submission name</th>
      <th>Joint submission</th>
      <th>Profile</th>
      <th>FTE Category A staff submitted</th>
      <th>Star Rating</th>
      <th>Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>4*</td>
      <td>6.4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>3*</td>
      <td>68.1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>2*</td>
      <td>25.5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>1*</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>unclassified</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>38215</th>
      <td>38215</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>4*</td>
      <td>21</td>
    </tr>
    <tr>
      <th>38216</th>
      <td>38216</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>3*</td>
      <td>39</td>
    </tr>
    <tr>
      <th>38217</th>
      <td>38217</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>2*</td>
      <td>22</td>
    </tr>
    <tr>
      <th>38218</th>
      <td>38218</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>1*</td>
      <td>12</td>
    </tr>
    <tr>
      <th>38219</th>
      <td>38219</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>unclassified</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
<p>38220 rows × 14 columns</p>
</div>



### Those column names are going to make working with this table painful. Let's change them to make life easier for ourselves.


```python
pd.read_sql("""Alter Table REF_Results
             Rename Column `Institution Code (UKPRN)` To Institution_Code;""", database)

pd.read_sql("""Alter Table REF_Results
             Rename Column `Institution Name` To Institution_Name;""", database)

pd.read_sql("""Alter Table REF_Results
             Rename Column `Institution Sort Order` To Institution_Sort_Order;""", database)

pd.read_sql("""Alter Table REF_Results
             Rename Column `Main Panel` To Main_Panel;""", database)

pd.read_sql("""Alter Table REF_Results
             Rename Column `Unit of Assessment Number` To Unit_of_Assessment_Number;""", database)

pd.read_sql("""Alter Table REF_Results
             Rename Column `Unit of Assessment Name` To Unit_of_Assessment_Name;""", database)

pd.read_sql("""Alter Table REF_Results
             Rename Column `FTE Category A staff submitted` To FTE_Category_A_staff_submitted;""", database)

pd.read_sql("""Alter Table REF_Results
             Rename Column `Star Rating` To Star_Rating;""", database)

pd.read_sql("SELECT * FROM REF_Results;", database)

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>Institution_Code</th>
      <th>Institution_Name</th>
      <th>Institution_Sort_Order</th>
      <th>Main_Panel</th>
      <th>Unit_of_Assessment_Number</th>
      <th>Unit_of_Assessment_Name</th>
      <th>Multiple submission letter</th>
      <th>Multiple submission name</th>
      <th>Joint submission</th>
      <th>Profile</th>
      <th>FTE_Category_A_staff_submitted</th>
      <th>Star_Rating</th>
      <th>Percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>4*</td>
      <td>6.4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>3*</td>
      <td>68.1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>2*</td>
      <td>25.5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>1*</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>10000291</td>
      <td>Anglia Ruskin University</td>
      <td>10</td>
      <td>A</td>
      <td>3</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Outputs</td>
      <td>11.30</td>
      <td>unclassified</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>38215</th>
      <td>38215</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>4*</td>
      <td>21</td>
    </tr>
    <tr>
      <th>38216</th>
      <td>38216</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>3*</td>
      <td>39</td>
    </tr>
    <tr>
      <th>38217</th>
      <td>38217</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>2*</td>
      <td>22</td>
    </tr>
    <tr>
      <th>38218</th>
      <td>38218</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>1*</td>
      <td>12</td>
    </tr>
    <tr>
      <th>38219</th>
      <td>38219</td>
      <td>10007807</td>
      <td>University of Ulster</td>
      <td>7630</td>
      <td>D</td>
      <td>36</td>
      <td>Communication, Cultural and Media Studies, Lib...</td>
      <td></td>
      <td>None</td>
      <td>None</td>
      <td>Overall</td>
      <td>16.40</td>
      <td>unclassified</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
<p>38220 rows × 14 columns</p>
</div>



## Understand the data

The dataset has 38,220 rows. But how many unique records do we have in each of the 14 columns?

We can see that 154 institutions are included in the dataset, and that they were assessed in 36 different subjects.


```python
pd.read_sql("""SELECT COUNT(DISTINCT Institution_Name) AS Institutions,
                COUNT(DISTINCT Institution_Sort_Order) AS Institution_Sort_Order,
                COUNT(DISTINCT Unit_of_Assessment_Name) AS Units_of_Assessment
                FROM REF_Results;""", database)

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Institutions</th>
      <th>Institution_Sort_Order</th>
      <th>Units_of_Assessment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>154</td>
      <td>154</td>
      <td>36</td>
    </tr>
  </tbody>
</table>
</div>



## Analyze the data

### Let's start by seeing which universities were assessed across the widest range of subjects.

We know there are 36 unique subjects in the database. It seems that no single institution was assessed on all of them - UCL has the widest range at 32 of the 36 subjects - and some universities were only assessed in one subject.


```python
result = pd.read_sql("""SELECT Institution_Name, COUNT(DISTINCT Unit_of_Assessment_Name)
                FROM REF_Results
                GROUP BY Institution_Name
                ORDER BY COUNT(DISTINCT Unit_of_Assessment_Name) DESC
                LIMIT 20;""", database)
```


```python
plt.figure(figsize=(20, 8))
plt.bar(x=result["Institution_Name"], height=result["COUNT(DISTINCT Unit_of_Assessment_Name)"], color='red')
plt.title("Top 20 Universities by Number of Subjects Assessed", pad = 30)
plt.xlabel("Institution", labelpad=20)
plt.ylabel("Number of Subjects Assessed", labelpad=20)
_ = plt.xticks(rotation = 60, ha = "right")
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_23_0.png)
    


We can look at the distribution of universities based on the number of subjects they were assessed on. It seems that most universities were assessed on only a small number of subjects, with 26 universities having been evaluated in only one subject. No university was evaluated on all 36 possible subject areas.


```python
result = pd.read_sql("""WITH Institutions_By_Assessment_Count AS 
                            (SELECT Institution_Name, 
                             COUNT(DISTINCT Unit_of_Assessment_Name) AS Number_of_Assessment_Units
                             FROM REF_Results GROUP BY Institution_Name)
                
                SELECT DISTINCT Number_of_Assessment_Units,
                COUNT(DISTINCT Institution_Name) AS Number_of_Institutions,
                SUM(COUNT(DISTINCT Institution_Name)) OVER (
                    ORDER BY Number_of_Assessment_Units
                    ROWS BETWEEN UNBOUNDED PRECEDING
                    AND CURRENT ROW
                    ) AS Running_Total
                FROM Institutions_By_Assessment_Count
                GROUP BY Number_of_Assessment_Units
                ORDER BY Number_of_Assessment_Units ASC;""", database)
```


```python
plt.figure(figsize=(20, 8))
plt.bar(x=result["Number_of_Assessment_Units"].astype(str), height=result["Number_of_Institutions"], color='red')
plt.title("Distribution of Institutions by Number of Subjects Assessed", pad = 30)
plt.xlabel("Number of Subjects Assessed", labelpad=20)
plt.ylabel("Number of Institutions", labelpad=20)
_ = plt.xticks(rotation = 0, ha = "center")
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_26_0.png)
    


### And which subjects are the most common among the universities assessed?


```python
result = pd.read_sql("""SELECT Unit_of_Assessment_Name,
               COUNT(DISTINCT Institution_Name) AS Number_of_Institutions
               FROM REF_Results
               GROUP BY Unit_of_Assessment_Name
               ORDER BY COUNT(DISTINCT Institution_Name) DESC;""", database)
```


```python
plt.figure(figsize=(20, 8))
plt.bar(x=result["Unit_of_Assessment_Name"].astype(str), height=result["Number_of_Institutions"], color='red')
plt.title("Subjects by Number of Institutions", pad = 30)
plt.xlabel("Subject", labelpad=20)
plt.ylabel("Number of Institutions", labelpad=20)
_ = plt.xticks(rotation = 45, ha = "right")
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_29_0.png)
    


###Which universities perform the best in the assessment?

Based on the data available, there are several ways we could try to establish which university performed the best across the assessment.

Each university gets an overall star rating for each subject it is assessed on. We can see which universities had the highest average percent 4* evaluations.

London Business School and Courtauld Institute of Art performed the best against this measure. But by including the total number of subjects they were assessed against, we see that both of these institutes are specialised in one subject area. It seems understandable that specialist institutions would perform better than those offering a large range of courses. However, the two worst performing institutions are also specialised in one subject each. 


```python
result = pd.read_sql("""WITH Four_Star_Percentages AS (SELECT DISTINCT Institution_Name, 
                                                      Unit_of_Assessment_Name,
                                                      Star_Rating,
                                                      Percentage
                                              FROM REF_Results
                                              WHERE Profile = "Overall" AND Star_Rating = "4*")
                                              
               SELECT Institution_Name,
                      COUNT(Unit_of_Assessment_Name),
                      CAST(SUM(Percentage) AS REAL) / COUNT(Star_Rating) AS Average_4_Star_Percentage
               FROM Four_Star_Percentages
               GROUP BY Institution_Name
               ORDER BY CAST(SUM(Percentage) AS REAL) / COUNT(Star_Rating) DESC
               LIMIT 20;""", database)
```


```python
plt.figure(figsize=(20, 8))
plt.bar(x=result["Institution_Name"].astype(str), height=result["Average_4_Star_Percentage"], color='red')
plt.title("Top 20 Universities by Average 4* Rating", pad = 30)
plt.xlabel("University", labelpad=20)
plt.ylabel("Average % of 4* Evaluations", labelpad=20)
_ = plt.xticks(rotation = 45, ha = "right")
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_32_0.png)
    


What about the institutions which were the weakest performers in this assessment?

The unclassified rating is the lowest possible rating in the assessment. How often did institutions receive this rating?


```python
result = pd.read_sql("""WITH Unclassified_Percentages AS (SELECT DISTINCT Institution_Name, 
                                                      Unit_of_Assessment_Name,
                                                      Star_Rating,
                                                      Percentage
                                              FROM REF_Results
                                              WHERE Profile = "Overall" AND Star_Rating = "unclassified")
                                              
               SELECT Institution_Name,
                      COUNT(Unit_of_Assessment_Name),
                      CAST(SUM(Percentage) AS REAL) / COUNT(Star_Rating) AS Average_Unclassified_Percentage
               FROM Unclassified_Percentages
               GROUP BY Institution_Name
               ORDER BY CAST(SUM(Percentage) AS REAL) / COUNT(Star_Rating) DESC
               LIMIT 20;""", database)
```


```python
plt.figure(figsize=(20, 8))
plt.bar(x=result["Institution_Name"].astype(str), height=result["Average_Unclassified_Percentage"], color='red')
plt.title("Bottom 20 Universities by Average Unclassified Rating", pad = 30)
plt.xlabel("University", labelpad=20)
plt.ylabel("Average % of 'Unclassified' Evaluations", labelpad=20)
_ = plt.xticks(rotation = 45, ha = "right")
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_35_0.png)
    


## Which universities have the largest number of staff?

The REF results show how many full-time equivalent (FTE) staff members were submitted for the assessment. Which universities have submitted the highest staff numbers for assessment?


```python
result = pd.read_sql("""SELECT DISTINCT Institution_Name,
                                SUM(FTE_Category_A_staff_submitted) AS Number_of_Staff_FTE
               FROM REF_Results
               WHERE Profile = "Overall" AND Star_Rating = "4*"
               GROUP BY Institution_Name
               ORDER BY SUM(FTE_Category_A_staff_submitted) DESC
               LIMIT 20;""", database)
```


```python
plt.figure(figsize=(20, 8))
plt.bar(x=result["Institution_Name"].astype(str), height=result["Number_of_Staff_FTE"], color='red')
plt.title("Top 20 Institutions by Number of Staff", pad = 30)
plt.xlabel("University ", labelpad=20)
plt.ylabel("Number of Staff (FTE)", labelpad=20)
_ = plt.xticks(rotation = 45, ha = "right")
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_38_0.png)
    


## And the smallest number of staff?


```python
result = pd.read_sql("""SELECT DISTINCT Institution_Name,
                                SUM(FTE_Category_A_staff_submitted) AS Number_of_Staff_FTE
               FROM REF_Results
               WHERE Profile = "Overall" AND Star_Rating = "4*"
               GROUP BY Institution_Name
               ORDER BY SUM(FTE_Category_A_staff_submitted) DESC
               LIMIT 20;""", database)
```


```python
plt.figure(figsize=(20, 8))
plt.bar(x=result["Institution_Name"].astype(str), height=result["Number_of_Staff_FTE"], color='red')
plt.title("20 Smallest Institutions by Number of Staff", pad = 30)
plt.xlabel("University ", labelpad=20)
plt.ylabel("Number of Staff (FTE)", labelpad=20)
_ = plt.xticks(rotation = 45, ha = "right")
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_41_0.png)
    


## Which universities are the most collaborative?

Institutions were able to prepare joint submissions with another institution and submit this to the assessment.

Which universities submitted the most joint submissions?


```python
pd.read_sql("""SELECT * FROM REF_Results
                        WHERE 'Joint submission' LIKE "%joint%";""", database)
```

## How to find the best university for you

If you're trying to decide on a univeristy and course, you can tailor this search to see which universities performed the best in the in the subject you're interested in.

As a reminder, these are the subjects covered by the assessment. You can amend the WHERE clause in the next code block to focus your search.


```python
pd.read_sql("""SELECT DISTINCT Unit_of_Assessment_Name
               FROM REF_Results
               ORDER BY Unit_of_Assessment_Name ASC;""", database)
```


```python
pd.read_sql("""SELECT Institution_Name,
                      Unit_of_Assessment_Name,
                      CAST(Percentage AS INTEGER) AS 'Percentage Overall 4* Ratings'
                FROM REF_Results
                WHERE Star_Rating = "4*" AND Profile = "Overall" AND Unit_of_Assessment_Name = "Modern Languages and Linguistics" --change the last part depending on the subject of interest
                ORDER BY CAST(Percentage AS INTEGER) DESC
                LIMIT 10;""", database)
```
