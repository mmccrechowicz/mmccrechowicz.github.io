---
title: "UK University Research Excellence Framework 2014"
date: 2021-04-20T15:17:31.586474
draft: false
tags: ["SQL", "Jupyter"]
summary: Which are the best performing UK universities?
---

The [Research Excellence Framework](https://en.wikipedia.org/wiki/Research_Excellence_Framework) is a periodic evaluation of the quality of research produced by universities in the United Kingdom. It was first applied in 2014, with reference to research completed in the period 2008-2013.

This analysis takes data from the 2014 REF and uses SQLite, pandas and matplotlib in Jupyter Notebooks to understand the UK's higher education landscape and identify the top-performing universities, including:

 - Which institutions teach the broadest range of subjects, and which specialise in particular areas of learning?
 - Which subjects are the most widely taught at UK universities?
 - Which universities received the highest number of 4* quality ratings, and which universities received the lowest number?
 - Which universities were the most collaborative?

## Set up

### Define functions



<details>
<summary>Code</summary>

```python
import tempfile
from urllib import request
import sqlite3

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
  conn = sqlite3.connect(database_name)

  # Loads data from pandas objects into individual tables.
  for (key, sheet) in data.items():
    sheet = sheet.where(pd.notnull(sheet), None)
    sheet.to_sql(key, conn)


  # Return database.
  return conn

```

</details>


### Prepare the data

#### Import the dataset and create the database

The data comes from Research Excellence Framework 2014. It is an Excel workbook with two worksheets. The main worksheet contains the core data from the REF, the second worksheet provides some information about the REF.

I download the file from this [URL](https://public.tableau.com/s/sites/default/files/media/Resources/Research%20Excellence%20Framework%202014%20Results_Pivoted.xlsx"), and convert it into an SQL database to enable analysis in Jupyter Notebooks.


```python
database = excel_dataset_to_sqlite("https://public.tableau.com/s/sites/default/files/media/Resources/Research%20Excellence%20Framework%202014%20Results_Pivoted.xlsx")
```

    /Users/Matthew/Library/Caches/pypoetry/virtualenvs/notebooks-IW0Gw3EE-py3.8/lib/python3.8/site-packages/pandas/core/generic.py:2779: UserWarning: The spaces in these column names will not be changed. In pandas versions < 0.14, spaces were converted to underscores.
      sql.to_sql(


Once the database has been created, I change the names of some of the tables and columns to make the data easier to work with.



<details>
<summary>Code</summary>

```python
database.execute(
    """ALTER TABLE 'Sheet1-Tableau' RENAME TO REF_Results;""")

```

</details>





    <sqlite3.Cursor at 0x121fed2d0>





<details>
<summary>Code</summary>

```python
database.execute("""Alter Table REF_Results
   Rename Column `Institution Code (UKPRN)` To Institution_Code;""")

database.execute("""Alter Table REF_Results
   Rename Column `Institution Name` To Institution_Name;""")

database.execute("""Alter Table REF_Results
   Rename Column `Institution Sort Order` To Institution_Sort_Order;""")

database.execute("""Alter Table REF_Results
   Rename Column `Main Panel` To Main_Panel;""")

database.execute("""Alter Table REF_Results
   Rename Column `Unit of Assessment Number` To Unit_of_Assessment_Number;""")

database.execute("""Alter Table REF_Results
   Rename Column `Unit of Assessment Name` To Unit_of_Assessment_Name;""")

database.execute("""Alter Table REF_Results
   Rename Column `FTE Category A staff submitted` To FTE_Category_A_staff_submitted;""")

database.execute("""Alter Table REF_Results
   Rename Column `Star Rating` To Star_Rating;""")

database.execute("""Alter Table REF_Results
   Rename Column `Joint submission` To Joint_submission;""")


```

</details>





    <sqlite3.Cursor at 0x121fed110>



## Understand the data

There is one table of interest: REF_Results. The table has 38,220 rows and 14 columns. REF_Results contains data about the universities assessed in the REF, the subjects they were assessed in, how many staff were submitted, the ratings they receieved, and whether universities completed joint submissions with another institution.


```python
pd.read_sql("""
    SELECT *
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
      <th>index</th>
      <th>Institution_Code</th>
      <th>Institution_Name</th>
      <th>Institution_Sort_Order</th>
      <th>Main_Panel</th>
      <th>Unit_of_Assessment_Number</th>
      <th>Unit_of_Assessment_Name</th>
      <th>Multiple submission letter</th>
      <th>Multiple submission name</th>
      <th>Joint_submission</th>
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
<p>38220 rows ?? 14 columns</p>
</div>


154 institutions are included in the dataset, and they were assessed in 36 different subjects, across four profiles. Five different star ratings were available.

```python
pd.read_sql("""
    SELECT COUNT(DISTINCT Institution_Name) AS Institutions,
           COUNT(DISTINCT Unit_of_Assessment_Name) AS Units_of_Assessment,
           COUNT(DISTINCT Profile) AS Profiles,
           COUNT(DISTINCT Star_Rating) AS Star_Ratings
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
      <th>Units_of_Assessment</th>
      <th>Profiles</th>
      <th>Star_Ratings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>154</td>
      <td>36</td>
      <td>4</td>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



## Which universities were assessed across the widest range of subjects?

We know there are 36 unique subjects (units of assessment) in the database. No single institution was assessed on all of them - UCL has the widest range at 32 of the 36 subjects - and some universities were only assessed in one subject.


```python
result = pd.read_sql(
    """SELECT Institution_Name, COUNT(DISTINCT Unit_of_Assessment_Name)
       FROM REF_Results
       GROUP BY Institution_Name
       ORDER BY COUNT(DISTINCT Unit_of_Assessment_Name) DESC
       LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Institution_Name"], height=result["COUNT(DISTINCT Unit_of_Assessment_Name)"], color='red')
plt.title("Top 20 Universities by Number of Subjects Assessed", pad = 20, fontsize = 16)
plt.ylabel("Number of Subjects Assessed", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 60, ha = "right", fontsize = 10)
#plt.axhline(result["number_data_points"].mean(), color='blue', linewidth=2, label = "# Countries")
#plt.legend()
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_16_0.png)
    


We can look at the distribution of universities based on the number of subjects they were assessed on. Most universities were assessed on only a small number of subjects, with 26 universities having been evaluated in only one subject. 


```python
result = pd.read_sql(
    """WITH Institutions_By_Assessment_Count AS 
         (SELECT Institution_Name, 
          COUNT(DISTINCT Unit_of_Assessment_Name) AS Number_of_Assessment_Units
          FROM REF_Results GROUP BY Institution_Name)
                
        SELECT DISTINCT Number_of_Assessment_Units,
               COUNT(DISTINCT Institution_Name) AS Number_of_Institutions,
               SUM(COUNT(DISTINCT Institution_Name)) OVER 
                  (ORDER BY Number_of_Assessment_Units
                   ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) 
                   AS Running_Total
        FROM Institutions_By_Assessment_Count
        GROUP BY Number_of_Assessment_Units
        ORDER BY Number_of_Assessment_Units ASC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Number_of_Assessment_Units"].astype(str), height=result["Number_of_Institutions"], color='red')
plt.title("Distribution of Institutions by Number of Subjects Assessed", pad = 20, fontsize = 16)
plt.xlabel("Number of Subjects Assessed", labelpad=20, fontsize = 12)
plt.ylabel("Number of Institutions", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 0, ha = "center", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_19_0.png)
    


## And which subjects are the most common among the universities assessed?


```python
result = pd.read_sql("""
        SELECT Unit_of_Assessment_Name,
               COUNT(DISTINCT Institution_Name) AS Number_of_Institutions
        FROM REF_Results
        GROUP BY Unit_of_Assessment_Name
        ORDER BY COUNT(DISTINCT Institution_Name) DESC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Unit_of_Assessment_Name"].astype(str), height=result["Number_of_Institutions"], color='red')
plt.title("Subjects by Number of Institutions", pad = 20, fontsize = 16)
plt.ylabel("Number of Institutions", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 60, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_22_0.png)
    


## Which universities perform the best in the assessment?

Based on the data available, there are several ways we could try to establish which university performed the best across the assessment.

The REF assesses submitted research and awards it a classification based on its quality. One of five quality ratings is possible: 

 - **Four star**: Quality that is world-leading in originality, significance and rigour.
 - **Three star**: Quality that is internationally excellent in originality, significance and rigour but which falls short of the highest standards of excellence.
 - **Two star**: Quality that is recognised internationally in originality, significance and rigour.
 - **One star**: Quality that is recognised nationally in originality, significance and rigour.
 - **Unclassified Quality**: that falls below the standard of nationally recognised work. Or work which does not meet the published definition of research for the purposes of this assessment.

Each university is awarded a star rating for each subject assessed in three 'profiles': Outputs, Impact, Environment. They also receive an 'Overall' star rating.

To compare the performance of different universities, we can see which universities had the highest average percentage of submissions awarded an 'Overall' 4* evaluation.

London Business School and Courtauld Institute of Art performed the best against this measure. But by including the total number of subjects they were assessed against, we see that both of these institutes are specialised in one subject area. 


```python
result = pd.read_sql("""
WITH Four_Star_Percentages AS (SELECT DISTINCT Institution_Name, 
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
fig, axis1 = plt.subplots(figsize=(12, 4))
axis1.grid(False)
axis1.bar(x=result["Institution_Name"].astype(str), height=result["Average_4_Star_Percentage"], color='red')
axis1.set_title("Top 20 Universities by Average 4* Rating", pad = 20, fontsize = 16)
axis1.set_ylabel("Average % of 4* Evaluations", labelpad=20, color = 'r', fontsize = 12)
axis1.set_xticklabels(result["Institution_Name"].astype(str), horizontalalignment = "right")
axes2 = axis1.twinx()
axes2.plot(result["COUNT(Unit_of_Assessment_Name)"], marker = "o", linestyle = "")
axes2.set_ylabel("Number of Subjects Assessed", labelpad=20, color = 'b', fontsize = 12)
axes2.grid(False)
_ = axis1.set_xlim(-1, 20)
axis1.tick_params(axis='y', colors='r')
axis1.tick_params(axis='x', labelsize = 10, rotation = 45)
axes2.tick_params(axis='y', colors='b')
```

    <ipython-input-14-c40615171364>:6: UserWarning: FixedFormatter should only be used together with FixedLocator
      axis1.set_xticklabels(result["Institution_Name"].astype(str), horizontalalignment = "right")



    
![png](UK_REF_2014_files/UK_REF_2014_25_1.png)
    


## What about the institutions which were the weakest performers in this assessment?

The unclassified rating is the lowest possible rating in the assessment, and is given for 'quality that falls below the standard of nationally recognised work'.

We can find the universities whose submissions got the highest average percentage of Unclassified ratings. By this measure, Writtle College is the worst performing institution in the dataset, with an average of 35% of submissions receiving Unclassified ratings across its two subject areas.

Based on the previous chart, we might conclude that universities which specialise in one or a small number of subjects would perform better: the two universities with the highest average percentage of 4* evaluations were each assessed in only one subject. However, several of the universities with the highest percentage of Unclassified ratings also specialise in one subject. So, specialisation is no guarantee of quality.


```python
result = pd.read_sql("""
WITH Unclassified_Percentages AS (SELECT DISTINCT Institution_Name, 
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
fig, axis1 = plt.subplots(figsize=(12, 4))
axis1.grid(False)
axis1.bar(x=result["Institution_Name"].astype(str), height=result["Average_Unclassified_Percentage"], color='red')
axis1.set_title("Bottom 20 Universities by Average Unclassified Rating", pad = 20, fontsize = 16)
axis1.set_ylabel("Average % of Unclassified Evaluations", labelpad=20, color = 'r', fontsize = 12)
axis1.set_xticklabels(result["Institution_Name"].astype(str), horizontalalignment = "right")
axes2 = axis1.twinx()
axes2.plot(result["COUNT(Unit_of_Assessment_Name)"], marker = "o", linestyle = "")
axes2.set_ylabel("Number of Subjects Assessed", labelpad=20, color = 'b', fontsize = 12)
axes2.grid(False)
_ = axis1.set_xlim(-1, 20)
axis1.tick_params(axis='y', colors='r')
axis1.tick_params(axis='x', labelsize = 10, rotation = 45)
axes2.tick_params(axis='y', colors='b')
```

    <ipython-input-16-6954073e0042>:6: UserWarning: FixedFormatter should only be used together with FixedLocator
      axis1.set_xticklabels(result["Institution_Name"].astype(str), horizontalalignment = "right")



    
![png](UK_REF_2014_files/UK_REF_2014_28_1.png)
    


## Which universities have the largest number of staff?

The REF results show how many full-time equivalent (FTE) staff members were submitted for the assessment. Which universities have submitted the highest staff numbers for assessment?


```python
result = pd.read_sql("""
SELECT DISTINCT Institution_Name,
       SUM(FTE_Category_A_staff_submitted) AS Number_of_Staff_FTE
FROM REF_Results
WHERE Profile = "Overall" AND Star_Rating = "4*"
GROUP BY Institution_Name
ORDER BY SUM(FTE_Category_A_staff_submitted) DESC
LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Institution_Name"].astype(str), height=result["Number_of_Staff_FTE"], color='red')
plt.title("Top 20 Institutions by Number of Staff", pad = 20, fontsize = 16)
plt.ylabel("Number of Staff (FTE)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_31_0.png)
    


## And the smallest number of staff?


```python
result = pd.read_sql("""
SELECT DISTINCT Institution_Name,
       SUM(FTE_Category_A_staff_submitted) AS Number_of_Staff_FTE
FROM REF_Results
WHERE Profile = "Overall" AND Star_Rating = "4*"
GROUP BY Institution_Name
ORDER BY SUM(FTE_Category_A_staff_submitted) ASC
LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Institution_Name"].astype(str), height=result["Number_of_Staff_FTE"], color='red')
plt.title("20 Smallest Institutions by Number of Staff", pad = 20, fontsize = 16)
plt.ylabel("Number of Staff (FTE)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](UK_REF_2014_files/UK_REF_2014_34_0.png)
    


## Which universities are the most collaborative?

Institutions were able to prepare joint submissions with another institution and submit this to the assessment. A total of 23 universities prepared joint submissions.

The University of Edinburgh entered the highest number of joint submissions, at a total of six. Edinburgh also had the highest number of partners, at three. 


```python
pd.read_sql("""SELECT Institution_Name,
                      COUNT(DISTINCT Unit_of_Assessment_Name) AS Number_of_Joint_Submissions,
                      COUNT(DISTINCT Joint_submission) AS Number_of_Partners
               FROM REF_Results
               WHERE Joint_submission LIKE "%joint%"
               GROUP BY Institution_Name
               ORDER BY Number_of_Joint_Submissions DESC;""", database)
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
      <th>Institution_Name</th>
      <th>Number_of_Joint_Submissions</th>
      <th>Number_of_Partners</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>University of Edinburgh</td>
      <td>6</td>
      <td>3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Heriot-Watt University</td>
      <td>3</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bangor University</td>
      <td>3</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>University of Wales Trinity Saint David</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>University of St Andrews</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>5</th>
      <td>University College London</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Liverpool School of Tropical Medicine</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Cardiff Metropolitan University</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Birkbeck College</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Aberystwyth University</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>University of the Highlands and Islands</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>University of Warwick</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>University of Wales</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>University of Sussex</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>University of Strathclyde</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>University of South Wales</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>University of Liverpool</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>University of Kent</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>University of Greenwich</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>19</th>
      <td>University of Glasgow</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20</th>
      <td>University of Brighton</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>SRUC</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Robert Gordon University</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>


We can see these collaborations in more detail in the table below.

```python
pd.read_sql("""
    SELECT Institution_Name,
           Unit_of_Assessment_Name,
           Joint_submission
    FROM REF_Results
    WHERE Joint_submission LIKE "%joint%"
    GROUP BY Institution_Name, Unit_of_Assessment_Name, Joint_submission;""", database)
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
      <th>Institution_Name</th>
      <th>Unit_of_Assessment_Name</th>
      <th>Joint_submission</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aberystwyth University</td>
      <td>Agriculture, Veterinary and Food Science</td>
      <td>(joint submission with Bangor University)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Aberystwyth University</td>
      <td>Earth Systems and Environmental Sciences</td>
      <td>(joint submission with Bangor University)</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Bangor University</td>
      <td>Agriculture, Veterinary and Food Science</td>
      <td>(joint submission with Aberystwyth University)</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Bangor University</td>
      <td>Earth Systems and Environmental Sciences</td>
      <td>(joint submission with Aberystwyth University)</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Bangor University</td>
      <td>Sport and Exercise Sciences, Leisure and Tourism</td>
      <td>(joint submission with Cardiff Metropolitan Un...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Birkbeck College</td>
      <td>Biological Sciences</td>
      <td>(joint submission with University College London)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Birkbeck College</td>
      <td>Earth Systems and Environmental Sciences</td>
      <td>(joint submission with University College London)</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Cardiff Metropolitan University</td>
      <td>Art and Design: History, Practice and Theory</td>
      <td>(joint submission with University of South Wal...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Cardiff Metropolitan University</td>
      <td>Sport and Exercise Sciences, Leisure and Tourism</td>
      <td>(joint submission with Bangor University)</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Heriot-Watt University</td>
      <td>Architecture, Built Environment and Planning</td>
      <td>(joint submission with University of Edinburgh)</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Heriot-Watt University</td>
      <td>General Engineering</td>
      <td>(joint submission with University of Edinburgh)</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Heriot-Watt University</td>
      <td>Mathematical Sciences</td>
      <td>(joint submission with University of Edinburgh)</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Liverpool School of Tropical Medicine</td>
      <td>Clinical Medicine</td>
      <td>(joint submission with University of Liverpool)</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Liverpool School of Tropical Medicine</td>
      <td>Public Health, Health Services and Primary Care</td>
      <td>(joint submission with University of Warwick)</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Robert Gordon University</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td>(joint submission with University of the Highl...</td>
    </tr>
    <tr>
      <th>15</th>
      <td>SRUC</td>
      <td>Agriculture, Veterinary and Food Science</td>
      <td>(joint submission with University of Edinburgh)</td>
    </tr>
    <tr>
      <th>16</th>
      <td>University College London</td>
      <td>Biological Sciences</td>
      <td>(joint submission with Birkbeck College)</td>
    </tr>
    <tr>
      <th>17</th>
      <td>University College London</td>
      <td>Earth Systems and Environmental Sciences</td>
      <td>(joint submission with Birkbeck College)</td>
    </tr>
    <tr>
      <th>18</th>
      <td>University of Brighton</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td>(joint submission with University of Sussex)</td>
    </tr>
    <tr>
      <th>19</th>
      <td>University of Edinburgh</td>
      <td>Agriculture, Veterinary and Food Science</td>
      <td>(joint submission with SRUC)</td>
    </tr>
    <tr>
      <th>20</th>
      <td>University of Edinburgh</td>
      <td>Architecture, Built Environment and Planning</td>
      <td>(joint submission with Heriot-Watt University)</td>
    </tr>
    <tr>
      <th>21</th>
      <td>University of Edinburgh</td>
      <td>Chemistry</td>
      <td>(joint submission with University of St Andrews)</td>
    </tr>
    <tr>
      <th>22</th>
      <td>University of Edinburgh</td>
      <td>General Engineering</td>
      <td>(joint submission with Heriot-Watt University)</td>
    </tr>
    <tr>
      <th>23</th>
      <td>University of Edinburgh</td>
      <td>Mathematical Sciences</td>
      <td>(joint submission with Heriot-Watt University)</td>
    </tr>
    <tr>
      <th>24</th>
      <td>University of Edinburgh</td>
      <td>Physics</td>
      <td>(joint submission with University of St Andrews)</td>
    </tr>
    <tr>
      <th>25</th>
      <td>University of Glasgow</td>
      <td>Chemistry</td>
      <td>(joint submission with University of Strathclyde)</td>
    </tr>
    <tr>
      <th>26</th>
      <td>University of Greenwich</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td>(joint submission with University of Kent)</td>
    </tr>
    <tr>
      <th>27</th>
      <td>University of Kent</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td>(joint submission with University of Greenwich...</td>
    </tr>
    <tr>
      <th>28</th>
      <td>University of Liverpool</td>
      <td>Clinical Medicine</td>
      <td>(joint submission with Liverpool School of Tro...</td>
    </tr>
    <tr>
      <th>29</th>
      <td>University of South Wales</td>
      <td>Art and Design: History, Practice and Theory</td>
      <td>(joint submission with Cardiff Metropolitan Un...</td>
    </tr>
    <tr>
      <th>30</th>
      <td>University of St Andrews</td>
      <td>Chemistry</td>
      <td>(joint submission with University of Edinburgh)</td>
    </tr>
    <tr>
      <th>31</th>
      <td>University of St Andrews</td>
      <td>Physics</td>
      <td>(joint submission with University of Edinburgh)</td>
    </tr>
    <tr>
      <th>32</th>
      <td>University of Strathclyde</td>
      <td>Chemistry</td>
      <td>(joint submission with University of Glasgow)</td>
    </tr>
    <tr>
      <th>33</th>
      <td>University of Sussex</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td>(joint submission with University of Brighton)</td>
    </tr>
    <tr>
      <th>34</th>
      <td>University of Wales</td>
      <td>Modern Languages and Linguistics</td>
      <td>(joint submission with University of Wales Tri...</td>
    </tr>
    <tr>
      <th>35</th>
      <td>University of Wales Trinity Saint David</td>
      <td>Art and Design: History, Practice and Theory</td>
      <td>(joint submission with Cardiff Metropolitan Un...</td>
    </tr>
    <tr>
      <th>36</th>
      <td>University of Wales Trinity Saint David</td>
      <td>Modern Languages and Linguistics</td>
      <td>(joint submission with University of Wales)</td>
    </tr>
    <tr>
      <th>37</th>
      <td>University of Warwick</td>
      <td>Public Health, Health Services and Primary Care</td>
      <td>(joint submission with Liverpool School of Tro...</td>
    </tr>
    <tr>
      <th>38</th>
      <td>University of the Highlands and Islands</td>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
      <td>(joint submission with Robert Gordon University)</td>
    </tr>
  </tbody>
</table>
</div>



## How to find the best university for you

If you're trying to decide on a university and course, you can tailor this search to see which universities performed the best in the in the subject you're interested in.

As a reminder, these are the subjects covered by the assessment. You can amend the WHERE clause in the next code block to focus your search.


```python
pd.read_sql("""SELECT DISTINCT Unit_of_Assessment_Name
               FROM REF_Results
               ORDER BY Unit_of_Assessment_Name ASC;""", database)
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
      <th>Unit_of_Assessment_Name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Aeronautical, Mechanical, Chemical and Manufac...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Agriculture, Veterinary and Food Science</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Allied Health Professions, Dentistry, Nursing ...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Anthropology and Development Studies</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Architecture, Built Environment and Planning</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Area Studies</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Art and Design: History, Practice and Theory</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Biological Sciences</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Business and Management Studies</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Chemistry</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Civil and Construction Engineering</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Classics</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Clinical Medicine</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Communication, Cultural and Media Studies, Lib...</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Computer Science and Informatics</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Earth Systems and Environmental Sciences</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Economics and Econometrics</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Education</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Electrical and Electronic Engineering, Metallu...</td>
    </tr>
    <tr>
      <th>19</th>
      <td>English Language and Literature</td>
    </tr>
    <tr>
      <th>20</th>
      <td>General Engineering</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Geography, Environmental Studies and Archaeology</td>
    </tr>
    <tr>
      <th>22</th>
      <td>History</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Law</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Mathematical Sciences</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Modern Languages and Linguistics</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Music, Drama, Dance and Performing Arts</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Philosophy</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Physics</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Politics and International Studies</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Psychology, Psychiatry and Neuroscience</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Public Health, Health Services and Primary Care</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Social Work and Social Policy</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Sociology</td>
    </tr>
    <tr>
      <th>34</th>
      <td>Sport and Exercise Sciences, Leisure and Tourism</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Theology and Religious Studies</td>
    </tr>
  </tbody>
</table>
</div>




```python
pd.read_sql("""
SELECT Institution_Name,
       Unit_of_Assessment_Name,
       CAST(Percentage AS INTEGER) AS 'Percentage Overall 4* Ratings'
FROM REF_Results
--change the last part depending on the subject of interest
WHERE Star_Rating = "4*" AND Profile = "Overall" AND Unit_of_Assessment_Name = "Modern Languages and Linguistics" 
ORDER BY CAST(Percentage AS INTEGER) DESC
LIMIT 10;""", database)
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
      <th>Institution_Name</th>
      <th>Unit_of_Assessment_Name</th>
      <th>Percentage Overall 4* Ratings</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Queen Mary University of London</td>
      <td>Modern Languages and Linguistics</td>
      <td>62</td>
    </tr>
    <tr>
      <th>1</th>
      <td>University of York</td>
      <td>Modern Languages and Linguistics</td>
      <td>45</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University of Edinburgh</td>
      <td>Modern Languages and Linguistics</td>
      <td>45</td>
    </tr>
    <tr>
      <th>3</th>
      <td>University of Manchester</td>
      <td>Modern Languages and Linguistics</td>
      <td>41</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Bangor University</td>
      <td>Modern Languages and Linguistics</td>
      <td>41</td>
    </tr>
    <tr>
      <th>5</th>
      <td>University of Cambridge</td>
      <td>Modern Languages and Linguistics</td>
      <td>40</td>
    </tr>
    <tr>
      <th>6</th>
      <td>University of Essex</td>
      <td>Modern Languages and Linguistics</td>
      <td>40</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Queen's University Belfast</td>
      <td>Modern Languages and Linguistics</td>
      <td>40</td>
    </tr>
    <tr>
      <th>8</th>
      <td>University of Kent</td>
      <td>Modern Languages and Linguistics</td>
      <td>39</td>
    </tr>
    <tr>
      <th>9</th>
      <td>University of Southampton</td>
      <td>Modern Languages and Linguistics</td>
      <td>39</td>
    </tr>
  </tbody>
</table>
</div>


