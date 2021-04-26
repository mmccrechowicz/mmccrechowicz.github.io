---
title: "University Fundraising"
date: 2020-12-23T16:55:34.230158
draft: False
summary: Who were the university's top donors?
---

This analysis uses data from a university's development department to understand more about the donors who have given money to the university. This type of analysis could help the development department/alumni relations team answer some of the questions they might have about their work, such as:

*   Who are the donors and how much do they give?
*   What makes someone likely to be a donor? E.g. are people with particular majors particular likely to donate?
*   Did outreach and campaigns have any effect on donations?
*   Which demographics should the alumni relations team target and when?
*   Which donors should the alumni relations team cultivate because they are or could become major benefactors?
*   Does the alumni relations team need to do more to engage with alumni, or with any particular demographics within alumni?

The original dataset can be downloaded [here](https://public.tableau.com/s/sites/default/files/media/advancement_donations_and_giving_demo.xls).

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

I'm importing a dataset from a URL.


```python
database = excel_dataset_to_sqlite("https://public.tableau.com/s/sites/default/files/media/advancement_donations_and_giving_demo.xls")
```

    /Users/Matthew/Library/Caches/pypoetry/virtualenvs/notebooks-iGyxaocD-py3.8/lib/python3.8/site-packages/pandas/core/generic.py:2779: UserWarning: The spaces in these column names will not be changed. In pandas versions < 0.14, spaces were converted to underscores.
      sql.to_sql(


#### View the table names to make sure the correct tables have been created


```python
pd.read_sql(
    """SELECT name FROM sqlite_master WHERE type='table';""", database)
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
      <td>GiftRecords</td>
    </tr>
    <tr>
      <th>1</th>
      <td>GraduationYear</td>
    </tr>
  </tbody>
</table>
</div>



#### The table names look fine. But what about the column names?

The column names have spaces, which will make them annoying to work with in SQL queries. So, let's change the names to make queries easier.


```python
pd.read_sql("""Select * From GiftRecords
            LIMIT 5;""", database)
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
      <th>Allocation Subcategory</th>
      <th>City</th>
      <th>College</th>
      <th>Gift Allocation</th>
      <th>Gift Amount</th>
      <th>Gift Date</th>
      <th>Major</th>
      <th>Prospect ID</th>
      <th>State</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>College of Natural Science</td>
      <td>Denver</td>
      <td>College of Natural Science</td>
      <td>Scholarship</td>
      <td>5,088.00</td>
      <td>2010-07-28 00:00:00</td>
      <td>Biological Science Interdepartmental</td>
      <td>1000</td>
      <td>CO</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>College of Natural Science</td>
      <td>San Francisco</td>
      <td>College of Social Science</td>
      <td>Scholarship</td>
      <td>3,793.00</td>
      <td>2010-09-10 00:00:00</td>
      <td>Human Development and Family Studies</td>
      <td>1001</td>
      <td>CA</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Minority Scholarship Fund</td>
      <td>Los Angeles</td>
      <td>College of Business</td>
      <td>Scholarship</td>
      <td>2,952.00</td>
      <td>2010-06-30 00:00:00</td>
      <td>Accounting</td>
      <td>1002</td>
      <td>CA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>College of Communication Arts and Sciences</td>
      <td>Mesa</td>
      <td>College of Natural Science</td>
      <td>Scholarship</td>
      <td>2,872.00</td>
      <td>2010-11-23 00:00:00</td>
      <td>Mathematics</td>
      <td>1003</td>
      <td>AZ</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Diversity Fund</td>
      <td>West Valley City</td>
      <td>College of Social Science</td>
      <td>Endowment</td>
      <td>2,022.00</td>
      <td>2010-10-10 00:00:00</td>
      <td>Psychology</td>
      <td>1004</td>
      <td>UT</td>
    </tr>
  </tbody>
</table>
</div>



We can change the column names which have spaces.


```python
database.execute("""Alter Table GiftRecords
             Rename Column `Allocation Subcategory` To Allocation_Subcategory;""")

database.execute("""Alter Table GiftRecords
             Rename Column `Gift Allocation` To Gift_Allocation;""")

database.execute("""Alter Table GiftRecords
             Rename Column `Gift Amount` To Gift_Amount;""")

database.execute("""Alter Table GiftRecords
             Rename Column `Gift Date` To Gift_Date;""")

database.execute("""Alter Table GiftRecords
             Rename Column `Prospect ID` To Prospect_ID;""")
```




    <sqlite3.Cursor at 0x11aae39d0>



And then check that the changes went through.


```python
pd.read_sql("PRAGMA table_info(GiftRecords);", database)
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
      <th>cid</th>
      <th>name</th>
      <th>type</th>
      <th>notnull</th>
      <th>dflt_value</th>
      <th>pk</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>index</td>
      <td>INTEGER</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Allocation_Subcategory</td>
      <td>TEXT</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>City</td>
      <td>TEXT</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>College</td>
      <td>TEXT</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Gift_Allocation</td>
      <td>TEXT</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>5</td>
      <td>Gift_Amount</td>
      <td>REAL</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>6</td>
      <td>Gift_Date</td>
      <td>TIMESTAMP</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>7</td>
      <td>Major</td>
      <td>TEXT</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>8</td>
      <td>Prospect_ID</td>
      <td>INTEGER</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9</td>
      <td>State</td>
      <td>TEXT</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



There's a second table in this database, so we can do the same to the columns in this table.


```python
pd.read_sql("""Select * From GraduationYear
            LIMIT 5;""", database)
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
      <th>Prospect ID</th>
      <th>Year of Graduation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1515</td>
      <td>1970</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1588</td>
      <td>1992</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>2508</td>
      <td>1984</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>2589</td>
      <td>1981</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>3012</td>
      <td>1993</td>
    </tr>
  </tbody>
</table>
</div>




```python
database.execute("""Alter Table GraduationYear
             Rename Column `Prospect ID` To Prospect_ID;""")

database.execute("""Alter Table GraduationYear
             Rename Column `Year of Graduation` To Graduation_Year;""")
```




    <sqlite3.Cursor at 0x105492f80>




```python
pd.read_sql("PRAGMA table_info(GraduationYear);", database)
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
      <th>cid</th>
      <th>name</th>
      <th>type</th>
      <th>notnull</th>
      <th>dflt_value</th>
      <th>pk</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>index</td>
      <td>INTEGER</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>Prospect_ID</td>
      <td>INTEGER</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Graduation_Year</td>
      <td>INTEGER</td>
      <td>0</td>
      <td>None</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



## Understand the data

From the above queries, it's clear we can join the two tables in the database on the 'Prospect_ID' field. Let's do that and see what the joined tables look like.


```python
pd.read_sql("""
SELECT * From GiftRecords
LEFT JOIN GraduationYear ON GiftRecords.Prospect_ID = GraduationYear.Prospect_ID
LIMIT 5;""", database)
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
      <th>Allocation_Subcategory</th>
      <th>City</th>
      <th>College</th>
      <th>Gift_Allocation</th>
      <th>Gift_Amount</th>
      <th>Gift_Date</th>
      <th>Major</th>
      <th>Prospect_ID</th>
      <th>State</th>
      <th>index</th>
      <th>Prospect_ID</th>
      <th>Graduation_Year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>College of Natural Science</td>
      <td>Denver</td>
      <td>College of Natural Science</td>
      <td>Scholarship</td>
      <td>5,088.00</td>
      <td>2010-07-28 00:00:00</td>
      <td>Biological Science Interdepartmental</td>
      <td>1000</td>
      <td>CO</td>
      <td>871</td>
      <td>1000</td>
      <td>1993</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>College of Natural Science</td>
      <td>San Francisco</td>
      <td>College of Social Science</td>
      <td>Scholarship</td>
      <td>3,793.00</td>
      <td>2010-09-10 00:00:00</td>
      <td>Human Development and Family Studies</td>
      <td>1001</td>
      <td>CA</td>
      <td>1128</td>
      <td>1001</td>
      <td>1991</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>Minority Scholarship Fund</td>
      <td>Los Angeles</td>
      <td>College of Business</td>
      <td>Scholarship</td>
      <td>2,952.00</td>
      <td>2010-06-30 00:00:00</td>
      <td>Accounting</td>
      <td>1002</td>
      <td>CA</td>
      <td>630</td>
      <td>1002</td>
      <td>1989</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>College of Communication Arts and Sciences</td>
      <td>Mesa</td>
      <td>College of Natural Science</td>
      <td>Scholarship</td>
      <td>2,872.00</td>
      <td>2010-11-23 00:00:00</td>
      <td>Mathematics</td>
      <td>1003</td>
      <td>AZ</td>
      <td>2233</td>
      <td>1003</td>
      <td>1983</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>Diversity Fund</td>
      <td>West Valley City</td>
      <td>College of Social Science</td>
      <td>Endowment</td>
      <td>2,022.00</td>
      <td>2010-10-10 00:00:00</td>
      <td>Psychology</td>
      <td>1004</td>
      <td>UT</td>
      <td>1778</td>
      <td>1004</td>
      <td>1986</td>
    </tr>
  </tbody>
</table>
</div>



There are 3913 rows of data in the GiftRecords table. Selecting the unique values from the table shows that, for example, there are 25 Allocation_Subcategories donors can choose from, and that 95 cities, 120 majors, and 2317 individual donors are represented in the data.

There are only 2 Gift_Allocations categories, so it won't be possible to do detailed analysis using this field.

The data cover 6 years.


```python
pd.read_sql("""
With years As (SELECT substr(Gift_Date, 1, 4) as year
                              From GiftRecords)

Select Count(Distinct Allocation_Subcategory) As Allocation_Subcategories,
       Count(Distinct City) As Cities,
       Count(Distinct College) As Colleges,
       Count(Distinct Gift_Allocation) As Gift_Allocations,
       Count(Distinct Major) As Majors,
       Count(Distinct Prospect_ID) As Prospects,
       Count(Distinct State) As States,
       Count(Distinct year) As years
From GiftRecords
Join years;""", database)
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
      <th>Allocation_Subcategories</th>
      <th>Cities</th>
      <th>Colleges</th>
      <th>Gift_Allocations</th>
      <th>Majors</th>
      <th>Prospects</th>
      <th>States</th>
      <th>years</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>25</td>
      <td>95</td>
      <td>12</td>
      <td>3</td>
      <td>120</td>
      <td>2317</td>
      <td>40</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



## Analyze the data

### How much did the university raise each year?

The chart below shows total donations for each of the six years in the data.

Looking at the annual average donations made, there is no clear pattern or trend; rather we see fluctuations from year to year. Donations peaked in 2013 before falling in the two subsequent years.

It would be interesting to know whether the development team ran any initiatives or campaigns in 2013 that could explain that year's high level of donations, especially after 2012, which saw the lowest annual donations among the years covered.


```python
result = pd.read_sql("""
SELECT substr(Gift_Date, 1, 4) AS Year,
       SUM(Gift_Amount),
       COUNT(Gift_Amount)
FROM GiftRecords
GROUP BY Year;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["Year"].astype(str), height=result["SUM(Gift_Amount)"] / 1_000_000, color='red')
plt.title("Annual Gift Amount, 2010-2015", pad = 20, fontsize = 16)
plt.ylabel("Total gifts ($m)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 0, ha = "center", fontsize = 10)
plt.margins(0.01, 0.01)
```



![png](University_Donations_files/University_Donations_26_0.png)



### What is the distribution of gifts?

We looked at the data earlier, so we know there are 3913 unique gift records in the data.

To understand these gifts at a basic level, we can look at the distribution of gifts among different gift amounts.

By bucketing the gifts in this way, it is clear that the vast majority of gifts are below \\$10k, with only a small percentage above \\$20k.


```python
result = pd.read_sql("""
SELECT
    COUNT(CASE WHEN Gift_Amount <= 5000 THEN 1 END) AS [Less Than $5k],
    COUNT(CASE WHEN Gift_Amount > 5000 AND Gift_Amount <= 10000 THEN 1 END) AS [$5k-$10k],
    COUNT(CASE WHEN Gift_Amount > 10000 AND Gift_Amount <= 20000 THEN 1 END) AS [$10k-$20k],
    COUNT(CASE WHEN Gift_Amount > 20000 AND Gift_Amount <= 30000 THEN 1 END) AS [$20k-$30k],
    COUNT(CASE WHEN Gift_Amount > 30000 AND Gift_Amount <= 40000 THEN 1 END) AS [$30k-$40k],
    COUNT(CASE WHEN Gift_Amount > 40000 AND Gift_Amount <= 50000 THEN 1 END) AS [$40k-$50k],
    COUNT(CASE WHEN Gift_Amount > 50000 AND Gift_Amount <= 100000 THEN 1 END) AS [$50k-$100k],
    COUNT(CASE WHEN Gift_Amount > 100000 AND Gift_Amount <= 200000 THEN 1 END) AS [$100k-$200k],
    COUNT(CASE WHEN Gift_Amount > 200000 AND Gift_Amount <= 300000 THEN 1 END) AS [$200k-$300k],
    COUNT(CASE WHEN Gift_Amount > 300000 AND Gift_Amount <= 400000 THEN 1 END) AS [$300k-$400k],
    COUNT(CASE WHEN Gift_Amount > 400000 AND Gift_Amount <= 500000 THEN 1 END) AS [$400k-$500k]
FROM GiftRecords;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result.columns, height = result.iloc[0])
plt.title("Number of Gifts By Amount, 2010-2015", pad = 20, fontsize = 16)
plt.xlabel("Gift Amount ($)", labelpad=20, fontsize = 12)
plt.ylabel("Number of Gifts", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 60, ha = "center", fontsize = 10)
plt.annotate(1710, xy = ("Less Than $5k", 1760), ha='center')
plt.annotate(1796, xy = ("$5k-$10k", 1846), ha='center')
plt.annotate(333, xy = ("$10k-$20k", 383), ha='center')
plt.annotate(62, xy = ("$20k-$30k", 102), ha='center')
plt.annotate(8, xy = ("$30k-$40k", 58), ha='center')
plt.annotate(1, xy = ("$40k-$50k", 51), ha='center')
plt.annotate(1, xy = ("$50k-$100k", 51), ha='center')
plt.annotate(0, xy = ("$100k-$200k", 50), ha='center')
plt.annotate(1, xy = ("$200k-$300k", 51), ha='center')
plt.annotate(0, xy = ("$300k-$400k", 50), ha='center')
plt.annotate(1, xy = ("$400k-$500k", 51), ha='center')
plt.margins(0.01, 0.08)
```



![png](University_Donations_files/University_Donations_29_0.png)



#### Largest gifts in each year

From the chart above, we know who the top overall donors are.

But what does this look like on an annual basis? We can find the top five largest gifts each year to see if there are any patterns.


```python
result = pd.read_sql("""
SELECT * FROM (SELECT Prospect_ID,
               CAST(Gift_Amount AS INT) AS Gift_Amount,
               substr(Gift_Date, 1, 4) as Year,
               RANK () OVER (PARTITION BY substr(Gift_Date, 1, 4) ORDER BY Gift_Amount DESC) donor_rank
               From GiftRecords)
WHERE donor_rank <= 5;""", database)
```


```python
subset_first = result[result["donor_rank"] == 1]
subset_second = result[result["donor_rank"] == 2]
subset_third = result[result["donor_rank"] == 3]
subset_fourth = result[result["donor_rank"] == 4]
subset_fifth = result[result["donor_rank"] == 5]
#subset_sixth = result[result["donor_rank"] == 6]

x_first = np.arange(len(subset_first["Year"]))
x_second = np.arange(len(subset_second["Year"]))
x_third = np.arange(len(subset_third["Year"]))
x_fourth = np.arange(len(subset_fourth["Year"]))
x_fifth = np.arange(len(subset_fifth["Year"]))
#x_sixth = np.arange(len(subset_sixth["Year"]))

y_first = subset_first["Gift_Amount"]
y_second = subset_second["Gift_Amount"]
y_third = subset_third["Gift_Amount"]
y_fourth = subset_fourth["Gift_Amount"]
y_fifth = subset_fifth["Gift_Amount"]
#y_sixth = subset_sixth["Gift_Amount"]
width = 0.15
fig, ax = plt.subplots(figsize=(12, 4))
rects1 = ax.bar(x_first - 0.3, y_first, width, label="2010")
rects2 = ax.bar(x_second - 0.15, y_second, width, label="2011")
rects3 = ax.bar(x_third + 0.0, y_third, width, label="2012")
rects4 = ax.bar(x_fourth + 0.15, y_fourth, width, label="2013")
rects5 = ax.bar(x_fifth + 0.3, y_fifth, width, label="2014")
#rects6 = ax.bar(x_sixth + 1.05, y_sixth, width, label="2015")

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Gift Value ($)', fontsize = 12)
ax.yaxis.labelpad = 20

x = np.arange(len(result["Year"]))  # the label locations

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate("${:,}".format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='left', va='bottom', rotation = 60)

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)
autolabel(rects4)
autolabel(rects5)

ax.set_title('Top 5 Gifts, 2010-2015', pad=20, fontsize = 16)
ax.grid(False)
ax.set_xticks(x_first)
ax.set_xticklabels(subset_first["Year"], fontsize = 12)
ax.xaxis.labelpad = 20
#ax.legend()
_ = plt.xticks(rotation = 0, ha = "center", fontsize = 10)
plt.margins(0.03, 0.4)
plt.show()
```



![png](University_Donations_files/University_Donations_32_0.png)



### Most generous donors

Who are the most generous donors and how much have they given?

Based on the distribution chart, we know that two donors in particular have been very generous to the university, donating more than \\$400,000 and \\$200,000 respectively in single gifts.

A larger number of donors have also given amounts between \\$20,000 and \\$100,000.

But who made the largest cumulative donations in the period 2010-2015?


```python
result = pd.read_sql("""
With total_donations As (Select Sum(Gift_Amount) as total_donations
                         From GiftRecords)

Select Distinct(Prospect_ID),
       SUM(Gift_Amount),
       total_donations,
       (SUM(Gift_Amount) / total_donations) AS percentage_of_total
From GiftRecords
Join total_donations
Group By Prospect_ID
Order By Sum(Gift_Amount) DESC
Limit 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["Prospect_ID"].astype(str), height=result["SUM(Gift_Amount)"], color='red')
plt.title("Top 20 Donors, 2010-2015", pad = 20, fontsize = 16)
plt.xlabel("Donor ID", labelpad=20, fontsize = 12)
plt.ylabel("Total gifts ($)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 0, ha = "center", fontsize = 10)
plt.margins(0.01, 0.01)
```



![png](University_Donations_files/University_Donations_35_0.png)



### Most generous states

In which states were alumni the most generous?

Colorado was the most generous state, sending more than $3m in donations to the university. Montana was the least generous state.


```python
result = pd.read_sql(
"""Select State,
          SUM(Gift_Amount),
          COUNT(Gift_Amount),
          SUM(Gift_Amount) / COUNT(Gift_Amount) AS Average_Gift
From GiftRecords
Group By State
Order By SUM(Gift_Amount) DESC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["State"].astype(str), height=result["SUM(Gift_Amount)"] / 1_000, color='red')
plt.title("Gift Amount By State, 2010-2015", pad = 20, fontsize = 16)
plt.ylabel("Total gifts ($ '000)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 0, ha = "center", fontsize = 10)
plt.margins(0.01, 0.01)
```



![png](University_Donations_files/University_Donations_38_0.png)



Let's look at Colorado and Montana in more detail.

Colorado recorded more than 90 times as many gifts as Montana, and an average gift amount that was more than 60% higher than Montana's. The largest gift from a Colorado donor was \\$38,052, almost \\$30,000 more than the largest gift originating in Montana.

210 individual donors from Colorado made contributions to the univeristy, compared to just 2 from Montana.


```python
result = pd.read_sql("""
SELECT State,
       COUNT(Gift_Amount) AS Number_of_Gifts,
       MAX(Gift_Amount) Largest_Gift_Amount,
       AVG(Gift_Amount) Average_Gift_Amount,
       COUNT(DISTINCT City) Number_of_Cities,
       COUNT(DISTINCT Prospect_ID) Number_of_Donors
From GiftRecords
WHERE State = 'CO' OR State = 'MT'
Group By State;""", database)
result
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
      <th>State</th>
      <th>Number_of_Gifts</th>
      <th>Largest_Gift_Amount</th>
      <th>Average_Gift_Amount</th>
      <th>Number_of_Cities</th>
      <th>Number_of_Donors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CO</td>
      <td>368</td>
      <td>38,052.00</td>
      <td>8,651.94</td>
      <td>2</td>
      <td>210</td>
    </tr>
    <tr>
      <th>1</th>
      <td>MT</td>
      <td>4</td>
      <td>8,481.00</td>
      <td>5,300.50</td>
      <td>1</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>



### Most generous cities

Colorado was the most generous state, and its capital was the most generous city in the dataset.


```python
result = pd.read_sql("""
Select City,
       SUM(Gift_Amount),
       COUNT(Gift_Amount),
       SUM(Gift_Amount) / COUNT(Gift_Amount) AS Average_Gift
From GiftRecords
Group By City
Order By SUM(Gift_Amount) DESC
Limit 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["City"].astype(str), height=result["SUM(Gift_Amount)"] / 1_000, color='red')
plt.title("Top 20 Cities, 2010-2015", pad = 20, fontsize = 16)
plt.ylabel("Total gifts ($ '000)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 60, ha = "right")
plt.margins(0.01, 0.01)
```



![png](University_Donations_files/University_Donations_44_0.png)



Let's look at the data for Denver in more detail. We see that Denver accounts for most of the donations from the state of Colorado: 311 of the 368 total gifts, and 181 of the 210 individual donors from Colorado are from Denver.



```python
result = pd.read_sql("""
SELECT City,
       COUNT(Gift_Amount) AS Number_of_Gifts,
       MAX(Gift_Amount) Largest_Gift_Amount,
       AVG(Gift_Amount) Average_Gift_Amount,
       COUNT(DISTINCT City) Number_of_Cities,
       COUNT(DISTINCT Prospect_ID) Number_of_Donors
From GiftRecords
WHERE City = 'Denver'
Group By City;""", database)
result
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
      <th>City</th>
      <th>Number_of_Gifts</th>
      <th>Largest_Gift_Amount</th>
      <th>Average_Gift_Amount</th>
      <th>Number_of_Cities</th>
      <th>Number_of_Donors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Denver</td>
      <td>311</td>
      <td>38,052.00</td>
      <td>9,184.87</td>
      <td>1</td>
      <td>181</td>
    </tr>
  </tbody>
</table>
</div>



### Most generous majors

Are donors who studied particular majors more likely to donate money to the university after they graduate?

The chart below shows the top 20 most generous majors. Engineers were the most generous donors to the university, followed by Composition and Mathematics graduates.


```python
result = pd.read_sql("""
Select Major,
       SUM(Gift_Amount),
       COUNT(Gift_Amount),
       SUM(Gift_Amount) / COUNT(Gift_Amount) AS Average_Gift
From GiftRecords
Group By Major
Order By SUM(Gift_Amount) DESC
LIMIT 25;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["Major"].astype(str), height=result["SUM(Gift_Amount)"] / 1_000, color='red')
plt.title("Gift Amount By Major, 2010-2015", pad = 20, fontsize = 16)
plt.ylabel("Total gifts ($ '000)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 60, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```



![png](University_Donations_files/University_Donations_49_0.png)



We can take a closer look at the top three most generous majors.

Although Engineering graduates were the most generous overall, fewer Engineering graduates made gifts than did graduates from Composition or Mathematics. Of the three majors, Composition delivered the highest number of gifts and the highest number of individual donors, but the smallest overall and average gift values.


```python
result = pd.read_sql("""
SELECT Major,
       COUNT(Gift_Amount) AS Number_of_Gifts,
       MAX(Gift_Amount) Largest_Gift_Amount,
       AVG(Gift_Amount) Average_Gift_Amount,
       COUNT(DISTINCT Prospect_ID) Number_of_Donors
From GiftRecords
WHERE Major = 'Engineering-No Major'
        OR Major = 'Composition' OR Major = 'Mathematics'
Group By Major;""", database)
result
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
      <th>Major</th>
      <th>Number_of_Gifts</th>
      <th>Largest_Gift_Amount</th>
      <th>Average_Gift_Amount</th>
      <th>Number_of_Donors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Composition</td>
      <td>60</td>
      <td>37,080.00</td>
      <td>7,234.15</td>
      <td>37</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Engineering-No Major</td>
      <td>21</td>
      <td>455,821.00</td>
      <td>26,786.60</td>
      <td>14</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Mathematics</td>
      <td>32</td>
      <td>225,843.00</td>
      <td>12,993.22</td>
      <td>18</td>
    </tr>
  </tbody>
</table>
</div>



### Most popular gift allocations

Donors were able to direct their gifts to 25 funds or causes within the university. Where did the donations go?

The two most popular donation destinations were non-subject specific: the Diversity Fund and the University Annual Fund.

The College of Natural Science was the third highest overall recipient of donations, and received more donations than any other university faculty.


```python
result = pd.read_sql("""
Select Allocation_Subcategory,
       SUM(Gift_Amount),
       COUNT(Gift_Amount)
From GiftRecords
Group By Allocation_Subcategory
Order By SUM(Gift_Amount) DESC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["Allocation_Subcategory"].astype(str), height=result["SUM(Gift_Amount)"] / 1_000, color='red')
plt.title("Gift Amount By Destination, 2010-2015", pad = 20, fontsize = 16)
plt.ylabel("Total gifts ($ '000)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 60, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```



![png](University_Donations_files/University_Donations_54_0.png)



Let's have a look at the donation profiles for the three funds which received the highest number of donations.

Of these three, the University Annual Fund received the highest number of gifts from the highest number of individual donors. However, this fund had the lowest average gift.

We might assume that the Diversity Fund and the University Annual Fund would attract a more diverse group of donors in terms of the subjects they studied. However, the College of Natural Science had donors from all 12 colleges in the university, as did the other two funds, and had donors from only eight fewer majors than the general funds.


```python
result = pd.read_sql("""
SELECT Allocation_Subcategory,
       COUNT(Gift_Amount) AS Number_of_Gifts,
       SUM(Gift_Amount) AS Total_Gift_Amount,
       MAX(Gift_Amount) AS Largest_Gift_Amount,
       AVG(Gift_Amount) AS Average_Gift_Amount,
       COUNT(DISTINCT Prospect_ID) AS Number_of_Donors,
       COUNT(DISTINCT College) AS Number_of_Colleges,
       COUNT(DISTINCT Major) AS Number_of_Majors
From GiftRecords
WHERE Allocation_Subcategory = 'Diversity Fund' OR Allocation_Subcategory = 'University Annual Fund' OR Allocation_Subcategory = 'College of Natural Science'
Group By Allocation_Subcategory;""", database)
result
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
      <th>Allocation_Subcategory</th>
      <th>Number_of_Gifts</th>
      <th>Total_Gift_Amount</th>
      <th>Largest_Gift_Amount</th>
      <th>Average_Gift_Amount</th>
      <th>Number_of_Donors</th>
      <th>Number_of_Colleges</th>
      <th>Number_of_Majors</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>College of Natural Science</td>
      <td>308</td>
      <td>2,106,294.00</td>
      <td>225,843.00</td>
      <td>6,838.62</td>
      <td>280</td>
      <td>12</td>
      <td>105</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Diversity Fund</td>
      <td>351</td>
      <td>2,656,506.50</td>
      <td>455,821.00</td>
      <td>7,568.39</td>
      <td>335</td>
      <td>12</td>
      <td>113</td>
    </tr>
    <tr>
      <th>2</th>
      <td>University Annual Fund</td>
      <td>383</td>
      <td>2,492,738.00</td>
      <td>29,538.00</td>
      <td>6,508.45</td>
      <td>355</td>
      <td>12</td>
      <td>113</td>
    </tr>
  </tbody>
</table>
</div>



### When are graduates most generous?

The dataset covers donations made between 2010 and 2015 by individuals who graduated from the university between 1960 and 2009.

The first chart shows that, until about 25 years after graduation, graduates get more generous the longer they have been away from the university. After the 25-year mark, they gradually become less generous.


```python
result = pd.read_sql("""
SELECT (substr(Gift_Date, 1, 4) - Graduation_Year) AS Years_Since_Graduation,
       SUM(Gift_Amount),
       COUNT(Gift_Amount),
       SUM(Gift_Amount) / COUNT(Gift_Amount) AS Average_Gift
FROM GiftRecords
LEFT JOIN GraduationYear On
        GiftRecords.Prospect_ID = GraduationYear.Prospect_ID
GROUP BY Years_Since_Graduation;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["Years_Since_Graduation"].astype(str), height=result["SUM(Gift_Amount)"] / 1_000, color='red')
plt.title("Gift Amount By Years Since Graduation, 2010-2015", pad = 20, fontsize = 16)
plt.xlabel("Years Since Graduation", labelpad=20, fontsize = 12)
plt.ylabel("Total gifts ($ '000)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 0, ha = "center", fontsize = 10)
plt.margins(0.01, 0.01)
```



![png](University_Donations_files/University_Donations_59_0.png)


The second chart shows that the average gift does not change significantly over time. Rather, it is the number of gifts that changes significantly over time. The number of gifts increases steadily until the 24th year after graduation, after which there is a steep decline, with the number levelling out at approximately 35 years after graduation.

```python
fig, axis1 = plt.subplots(figsize=(12, 4))
axis1.grid(False)
axis1.bar(x=result["Years_Since_Graduation"].astype(str), height=result["Average_Gift"], color='red')
axis1.set_title("Average Gift Amount By Years Since Graduation, 2010-2015", pad = 20, fontsize = 16)
axis1.set_xlabel("Years Since Graduation", labelpad=20, fontsize = 12)
axis1.set_ylabel("Average Gift ($)", labelpad=20, color = 'r', fontsize = 12)
axes2 = axis1.twinx()
axes2.plot(result["COUNT(Gift_Amount)"], linewidth = 2)
axes2.set_ylabel("Number of Gifts", labelpad=20, color = 'b', fontsize = 12)
axes2.grid(False)
_ = axis1.set_xlim(-1, 55)
axis1.tick_params(axis='y', colors='r')
axis1.tick_params(axis='x', labelsize = 10)
axes2.tick_params(axis='y', colors='b')
```



![png](University_Donations_files/University_Donations_61_0.png)
