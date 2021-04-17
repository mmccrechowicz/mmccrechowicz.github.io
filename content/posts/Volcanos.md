---
title: "Significant Volcanic Eruptions"
date: 2021-04-10T15:17:35.702320
draft: true
summary: Which countries have been most affected by volcanic incidents?
---

Note: some map-based visualisations would be good in this analysis. Ask Maciej for help with this: https://colab.research.google.com/github/jakevdp/PythonDataScienceHandbook/blob/master/notebooks/04.13-Geographic-Data-With-Basemap.ipynb#scrollTo=HhB0JKS0_l4s

This analysis uses a [dataset](https://public.tableau.com/s/sites/default/files/media/Resources/significantvolcanoeruptions.xlsx) about 658 significant volcanic eruptions that occurred between 4360 BCE and 2014 CE. 

Using the data available, I identify the most active volcanoes in this period; the countries which experienced the most volcanic activity; the eras with the greatest number of volcanic eruptions; and the impact these volcanoes have had in terms of human lives lost and damage done.

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
database = excel_dataset_to_sqlite("https://public.tableau.com/s/sites/default/files/media/Resources/significantvolcanoeruptions.xlsx")
```

    /Users/Matthew/Library/Caches/pypoetry/virtualenvs/notebooks-iGyxaocD-py3.8/lib/python3.8/site-packages/pandas/core/generic.py:2779: UserWarning: The spaces in these column names will not be changed. In pandas versions < 0.14, spaces were converted to underscores.
      sql.to_sql(


#### View the table names to make sure the correct tables have been created


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
      <td>volerup</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Metadata</td>
    </tr>
  </tbody>
</table>
</div>



#### Now let's have a look at the column names to make sure they won't make it difficult to work with this dataset.


```python
pd.read_sql("""SELECT * FROM volerup;""", database)
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
      <th>Year</th>
      <th>Month</th>
      <th>Day</th>
      <th>Associated Tsunami?</th>
      <th>Associated Earthquake?</th>
      <th>Name</th>
      <th>Location</th>
      <th>Country</th>
      <th>Latitude</th>
      <th>...</th>
      <th>TOTAL_DEATHS</th>
      <th>TOTAL_DEATHS_DESCRIPTION</th>
      <th>TOTAL_MISSING</th>
      <th>TOTAL_MISSING_DESCRIPTION</th>
      <th>TOTAL_INJURIES</th>
      <th>TOTAL_INJURIES_DESCRIPTION</th>
      <th>TOTAL_DAMAGE_MILLIONS_DOLLARS</th>
      <th>TOTAL_DAMAGE_DESCRIPTION</th>
      <th>TOTAL_HOUSES_DESTROYED</th>
      <th>TOTAL_HOUSES_DESTROYED_DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>None</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>-4,360.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Macauley Island</td>
      <td>Kermadec Is</td>
      <td>New Zealand</td>
      <td>-30.20</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>-4,350.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Kikai</td>
      <td>Ryukyu Is</td>
      <td>Japan</td>
      <td>30.78</td>
      <td>...</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>NaN</td>
      <td>3.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>-4,050.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Masaya</td>
      <td>Nicaragua</td>
      <td>Nicaragua</td>
      <td>11.98</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4</td>
      <td>-4,000.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Pago</td>
      <td>New Britain-SW Pac</td>
      <td>Papua New Guinea</td>
      <td>-5.58</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
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
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>654</th>
      <td>654</td>
      <td>2,014.00</td>
      <td>2.00</td>
      <td>1.00</td>
      <td>None</td>
      <td>None</td>
      <td>Sinabung</td>
      <td>Sumatra</td>
      <td>Indonesia</td>
      <td>3.17</td>
      <td>...</td>
      <td>17.00</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>655</th>
      <td>655</td>
      <td>2,014.00</td>
      <td>2.00</td>
      <td>13.00</td>
      <td>None</td>
      <td>None</td>
      <td>Kelut</td>
      <td>Java</td>
      <td>Indonesia</td>
      <td>-7.93</td>
      <td>...</td>
      <td>7.00</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>4,098.00</td>
      <td>4.00</td>
    </tr>
    <tr>
      <th>656</th>
      <td>656</td>
      <td>2,014.00</td>
      <td>9.00</td>
      <td>27.00</td>
      <td>None</td>
      <td>None</td>
      <td>On-take</td>
      <td>Honshu-Japan</td>
      <td>Japan</td>
      <td>35.90</td>
      <td>...</td>
      <td>55.00</td>
      <td>2.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>70.00</td>
      <td>2.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>657</th>
      <td>657</td>
      <td>2,014.00</td>
      <td>11.00</td>
      <td>10.00</td>
      <td>None</td>
      <td>None</td>
      <td>Kilauea</td>
      <td>Hawaiian Is</td>
      <td>United States</td>
      <td>19.43</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>14.50</td>
      <td>3.00</td>
      <td>1.00</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>658</th>
      <td>658</td>
      <td>2,014.00</td>
      <td>11.00</td>
      <td>23.00</td>
      <td>None</td>
      <td>None</td>
      <td>Fogo</td>
      <td>Cape Verde Is</td>
      <td>Cape Verde</td>
      <td>14.95</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>1.00</td>
    </tr>
  </tbody>
</table>
<p>659 rows × 37 columns</p>
</div>



A few of these column headers will make it difficult to work with the database. Let's change them to make life easier.


```python
database.execute("""
    Alter Table volerup
    Rename Column `Associated Tsunami?` To Associated_Tsunami;""")

database.execute("""
    Alter Table volerup
    Rename Column `Associated Earthquake?` To Associated_Earthquake;""")

database.execute("""
    Alter Table volerup
    Rename Column `Volcano Explosivity Index (VEI)` To VEI;""")

```




    <sqlite3.Cursor at 0x11df87180>



The first row doesn't seem to have any data in it, so let's get rid of it.




```python
database.execute("""DELETE FROM volerup
                    WHERE Year IS NULL;""")
```




    <sqlite3.Cursor at 0x11df87500>



When we select all, we now have the new column names, and 658 rows instead of 659.


```python
pd.read_sql("""SELECT * FROM volerup;""", database)
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
      <th>Year</th>
      <th>Month</th>
      <th>Day</th>
      <th>Associated_Tsunami</th>
      <th>Associated_Earthquake</th>
      <th>Name</th>
      <th>Location</th>
      <th>Country</th>
      <th>Latitude</th>
      <th>...</th>
      <th>TOTAL_DEATHS</th>
      <th>TOTAL_DEATHS_DESCRIPTION</th>
      <th>TOTAL_MISSING</th>
      <th>TOTAL_MISSING_DESCRIPTION</th>
      <th>TOTAL_INJURIES</th>
      <th>TOTAL_INJURIES_DESCRIPTION</th>
      <th>TOTAL_DAMAGE_MILLIONS_DOLLARS</th>
      <th>TOTAL_DAMAGE_DESCRIPTION</th>
      <th>TOTAL_HOUSES_DESTROYED</th>
      <th>TOTAL_HOUSES_DESTROYED_DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>-4,360.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Macauley Island</td>
      <td>Kermadec Is</td>
      <td>New Zealand</td>
      <td>-30.20</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>-4,350.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Kikai</td>
      <td>Ryukyu Is</td>
      <td>Japan</td>
      <td>30.78</td>
      <td>...</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>NaN</td>
      <td>3.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>-4,050.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Masaya</td>
      <td>Nicaragua</td>
      <td>Nicaragua</td>
      <td>11.98</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>-4,000.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Pago</td>
      <td>New Britain-SW Pac</td>
      <td>Papua New Guinea</td>
      <td>-5.58</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>-3,580.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>None</td>
      <td>None</td>
      <td>Taal</td>
      <td>Luzon-Philippines</td>
      <td>Philippines</td>
      <td>14.00</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
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
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>653</th>
      <td>654</td>
      <td>2,014.00</td>
      <td>2.00</td>
      <td>1.00</td>
      <td>None</td>
      <td>None</td>
      <td>Sinabung</td>
      <td>Sumatra</td>
      <td>Indonesia</td>
      <td>3.17</td>
      <td>...</td>
      <td>17.00</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>654</th>
      <td>655</td>
      <td>2,014.00</td>
      <td>2.00</td>
      <td>13.00</td>
      <td>None</td>
      <td>None</td>
      <td>Kelut</td>
      <td>Java</td>
      <td>Indonesia</td>
      <td>-7.93</td>
      <td>...</td>
      <td>7.00</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>3.00</td>
      <td>4,098.00</td>
      <td>4.00</td>
    </tr>
    <tr>
      <th>655</th>
      <td>656</td>
      <td>2,014.00</td>
      <td>9.00</td>
      <td>27.00</td>
      <td>None</td>
      <td>None</td>
      <td>On-take</td>
      <td>Honshu-Japan</td>
      <td>Japan</td>
      <td>35.90</td>
      <td>...</td>
      <td>55.00</td>
      <td>2.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>70.00</td>
      <td>2.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>656</th>
      <td>657</td>
      <td>2,014.00</td>
      <td>11.00</td>
      <td>10.00</td>
      <td>None</td>
      <td>None</td>
      <td>Kilauea</td>
      <td>Hawaiian Is</td>
      <td>United States</td>
      <td>19.43</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>14.50</td>
      <td>3.00</td>
      <td>1.00</td>
      <td>1.00</td>
    </tr>
    <tr>
      <th>657</th>
      <td>658</td>
      <td>2,014.00</td>
      <td>11.00</td>
      <td>23.00</td>
      <td>None</td>
      <td>None</td>
      <td>Fogo</td>
      <td>Cape Verde Is</td>
      <td>Cape Verde</td>
      <td>14.95</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.00</td>
      <td>NaN</td>
      <td>1.00</td>
    </tr>
  </tbody>
</table>
<p>658 rows × 37 columns</p>
</div>



## Let's do a little work to understand the database better.

There are 658 rows, but how many unique values do we have in the important columns?

We can see that the dataset covers 234 volcanoes in 73 locations across 48 countries. There are also 8 distinct values assigned to Volcanic Explosivity Index.


```python
pd.read_sql("""SELECT COUNT(DISTINCT Name) AS Volcano_Name,
                      COUNT(DISTINCT Location) AS Location,
                      COUNT(DISTINCT Country) AS Country,
                      COUNT(DISTINCT VEI) AS VEI
               FROM volerup;""", database)
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
      <th>Volcano_Name</th>
      <th>Location</th>
      <th>Country</th>
      <th>VEI</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>234</td>
      <td>73</td>
      <td>48</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
</div>



## Analyze the data

### Where do volcanic eruptions happen?

Let's start by identifying the geographical location of these volcanic eruptions.

Indonesia has the highest number of volcanoes, as well as the highest number of volcanic incidents.


```python
result = pd.read_sql("""SELECT Country, 
                        COUNT(DISTINCT Name) AS Volcanos_Per_Country
                        FROM volerup
                        GROUP BY Country
                        ORDER BY COUNT(DISTINCT Name) DESC
                        LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Country"], height=result["Volcanos_Per_Country"], color='red')
plt.title("Top 20 Countries by Number of Volcanoes", pad = 20, fontsize = 16)
plt.ylabel("Number of Volcanoes", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_23_0.png)
    



```python
result = pd.read_sql("""SELECT Country, 
                        COUNT(Country) AS Incidents_Per_Country 
                        FROM volerup
                        GROUP BY Country
                        ORDER BY COUNT(Country) DESC
                        LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Country"], height=result["Incidents_Per_Country"], color='red')
plt.title("Top 20 Countries by Number of Volcanic Eruptions", pad = 20, fontsize = 16)
plt.ylabel("Number of Volcanic Eruptions", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_25_0.png)
    


However, Italy's volcanoes experience the highest number of eruptions per volcano.


```python
pd.read_sql("""
    SELECT Country, 
           COUNT(Country) AS Incidents_Per_Country, 
           COUNT(DISTINCT Name) AS Volcanos_Per_Country,
           CAST(COUNT(Country) AS REAL) / COUNT(DISTINCT Name) AS Incidents_Per_Volcano
    FROM volerup
    GROUP BY Country
    ORDER BY CAST(COUNT(Country) AS REAL) / COUNT(DISTINCT Name) DESC
    LIMIT 20;""", database)
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
      <th>Country</th>
      <th>Incidents_Per_Country</th>
      <th>Volcanos_Per_Country</th>
      <th>Incidents_Per_Volcano</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Italy</td>
      <td>44</td>
      <td>5</td>
      <td>8.80</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Greece</td>
      <td>7</td>
      <td>1</td>
      <td>7.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Montserrat</td>
      <td>6</td>
      <td>1</td>
      <td>6.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Guatemala</td>
      <td>16</td>
      <td>3</td>
      <td>5.33</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Comoros</td>
      <td>5</td>
      <td>1</td>
      <td>5.00</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Philippines</td>
      <td>38</td>
      <td>8</td>
      <td>4.75</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Iceland</td>
      <td>51</td>
      <td>11</td>
      <td>4.64</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Martinique</td>
      <td>4</td>
      <td>1</td>
      <td>4.00</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Indonesia</td>
      <td>152</td>
      <td>39</td>
      <td>3.90</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Japan</td>
      <td>97</td>
      <td>30</td>
      <td>3.23</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Ecuador</td>
      <td>16</td>
      <td>5</td>
      <td>3.20</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Pacific Ocean</td>
      <td>9</td>
      <td>3</td>
      <td>3.00</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Cape Verde</td>
      <td>3</td>
      <td>1</td>
      <td>3.00</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Tanzania</td>
      <td>5</td>
      <td>2</td>
      <td>2.50</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Vanuatu</td>
      <td>12</td>
      <td>5</td>
      <td>2.40</td>
    </tr>
    <tr>
      <th>15</th>
      <td>St. Vincent &amp; the Grenadines</td>
      <td>2</td>
      <td>1</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Samoa</td>
      <td>2</td>
      <td>1</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Costa Rica</td>
      <td>4</td>
      <td>2</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Congo, DRC</td>
      <td>4</td>
      <td>2</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>19</th>
      <td>United States</td>
      <td>41</td>
      <td>21</td>
      <td>1.95</td>
    </tr>
  </tbody>
</table>
</div>



Mount Etna in Italy is the single most active volcano in the dataset, with 19 incidents. 


```python
result = pd.read_sql("""
    SELECT Name, 
           Location, 
           Country, 
           COUNT(Name) AS Number_of_Incidents
    FROM volerup
    GROUP BY Name
    ORDER BY COUNT(Name) DESC
    LIMIT 20;""", database)          
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Name"] + ", " + result["Country"], height=result["Number_of_Incidents"], color='red')
plt.title("Top 20 Most Active Volcanoes", pad = 20, fontsize = 16)
plt.xlabel("Volcano", labelpad=20)
plt.ylabel("Number of Volcanic Eruptions", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_30_0.png)
    


#### Indonesia

Let's have a more detailed look at Indonesia, the country with the highest number of volcanoes and volcanic eruptions.

We can look at the regions in Indonesia to see which are the most volcanically active. Java is the most volcanic region in Indonesia, with 13 volcanoes and 76 incidents.


```python
result = pd.read_sql("""
    SELECT Location, 
           COUNT(DISTINCT Name) AS Number_of_Volcanoes, 
           COUNT(Location) AS Number_of_Incidents
    FROM volerup
    WHERE Country = 'Indonesia'
    GROUP BY Location
    ORDER BY COUNT(Location) DESC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Location"], height=result["Number_of_Incidents"], color='red')
plt.title("Indonesia's Most Volcanically Active Regions", pad = 20, fontsize = 16)
plt.xlabel("Region", labelpad=20, fontsize = 12)
plt.ylabel("Number of Volcanic Eruptions", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_33_0.png)
    


The dataset includes the [Volcanic Explosivity Index (VEI)](https://en.wikipedia.org/wiki/Volcanic_Explosivity_Index) figure for each eruption. The VEI measures the relative explosiveness of an eruption, with 0 (non-explosive) being the smallest possible value, and 8 the largest.

The majority of Indonesia's volcanic eruptions sit on this lower end of this scale, with most being a 2 or 3 on the scale.


```python
result = pd.read_sql("""SELECT COUNT(Name) AS Number_of_Incidents,
                               CAST(VEI AS INT) AS VEI
                        FROM volerup
                        WHERE Country = 'Indonesia'
                        GROUP BY VEI
                        ORDER BY VEI ASC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["VEI"].astype(str), height=result["Number_of_Incidents"], color='red')
plt.title("Indonesia's Volcanic Eruptions by VEI", pad = 20, fontsize = 16)
plt.xlabel("Volcanic Explosivity Index Value", labelpad=20, fontsize = 12)
plt.ylabel("Number of Volcanic Eruptions", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_36_0.png)
    


### When did these eruptions happen?

The data covers the period from 4360 BCE to 2014 CE. 

Were there any centuries in this timespan that were particularly affected by volcanic eruptions?

The period between 1000 CE and 2000 CE has the highest number of recorded volcanic incidents. The availability of data regarding the volcanic incidents is dependent on humans' ability to record and measure this activity, so it should not be a surprise that we have more information about the most recent volcanic eruptions than about the ones which occurred centuries or millennia ago.


```python
result = pd.read_sql("""
  SELECT COUNT(Name),
         CASE 
            WHEN Year >= -5000 AND Year < -4001 THEN "5th Millennium BCE"
            WHEN Year >= -4000 AND Year < -3001 THEN "4th Millennium BCE"
            WHEN Year >= -3000 AND Year < -2001 THEN "3rd Millennium BCE"
            WHEN Year >= -2000 AND Year < -1001 THEN "2nd Millennium BCE"
            WHEN Year >= -1000 AND Year <= 0 THEN "1st Millennium BCE"
            WHEN Year > 0 AND Year <= 1000 THEN "1st Millennium CE"
            WHEN Year > 1000 AND Year <= 2000 THEN "2nd Millennium CE"
            WHEN Year > 2000 AND Year <= 3000 THEN "3rd Millennium CE"
         END Century 
  FROM volerup
  GROUP BY Century
  ORDER BY 
          CASE 
             WHEN Century = "5th Millennium BCE" THEN 1
             WHEN Century = "4th Millennium BCE" THEN 2
             WHEN Century = "3rd Millennium BCE" THEN 3
             WHEN Century = "2nd Millennium BCE" THEN 4
             WHEN Century = "1st Millennium BCE" THEN 5
             WHEN Century = "1st Millennium CE" THEN 6
             WHEN Century = "2nd Millennium CE" THEN 7
             WHEN Century = "3rd Millennium CE" THEN 8
           END;""", database)
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
      <th>COUNT(Name)</th>
      <th>Century</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3</td>
      <td>5th Millennium BCE</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3</td>
      <td>4th Millennium BCE</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>3rd Millennium BCE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10</td>
      <td>2nd Millennium BCE</td>
    </tr>
    <tr>
      <th>4</th>
      <td>6</td>
      <td>1st Millennium BCE</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25</td>
      <td>1st Millennium CE</td>
    </tr>
    <tr>
      <th>6</th>
      <td>552</td>
      <td>2nd Millennium CE</td>
    </tr>
    <tr>
      <th>7</th>
      <td>58</td>
      <td>3rd Millennium CE</td>
    </tr>
  </tbody>
</table>
</div>



We can look at the data for 1000 CE to 2000 CE in more detail.

We saw above that there are more data points for the period 1001 CE to 2000 CE than for any millennium. This pattern is seen again in the individual centuries which made up this millennium, as we have a steady increase in the number of data points as the centuries progress. 


```python
result = pd.read_sql("""SELECT COUNT(Name),
               CASE 
                    WHEN Year >= 1001 AND Year <= 1100 THEN "11th Century CE"
                    WHEN Year >= 1101 AND Year <= 1200 THEN "12th Century CE"
                    WHEN Year >= 1201 AND Year <= 1300 THEN "13th Century CE"
                    WHEN Year >= 1301 AND Year <= 1400 THEN "14th Century CE"
                    WHEN Year >= 1401 AND Year <= 1500 THEN "15th Century CE"
                    WHEN Year >= 1501 AND Year <= 1600 THEN "16th Century CE"
                    WHEN Year >= 1601 AND Year <= 1700 THEN "17th Century CE"
                    WHEN Year >= 1701 AND Year <= 1800 THEN "18th Century CE"
                    WHEN Year >= 1801 AND Year <= 1900 THEN "19th Century CE"
                    WHEN Year >= 1901 AND Year <= 2000 THEN "20th Century CE"
               END Century 
               FROM volerup
               WHERE Year >= 1001 AND Year <=2000
               GROUP BY Century
               ORDER BY Century;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.grid(False)
plt.bar(x=result["Century"].astype(str), height=result["COUNT(Name)"], color = "red")
plt.title("Volcanic Eruptions 1000 - 2000 CE", pad = 20, fontsize = 16)
plt.ylabel("Number of Volcanic Eruptions", fontsize = 12)
_ = plt.xticks(rotation = 60, ha = "center", fontsize = 10)
plt.margins(0.00, 0.01)
```


    
![png](Volcanos_files/Volcanos_41_0.png)
    


The 20th century saw 260 recorded volcanic incidents. Let's have a look at those incidents in more detail. 

1902 was the most active year in the twentieth century, with 8 volcanic incidents.


```python
result = pd.read_sql("""
    SELECT CAST(Year AS INTEGER) AS Year, 
           COUNT(Year) AS Number_of_Incidents
    FROM volerup
    WHERE Year >= 1901 AND Year <= 2000
    GROUP BY Year          
    ORDER BY Year ASC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Year"], height=result["Number_of_Incidents"], color='red')
plt.title("Volcanic Eruptions in the 20th Century", pad = 20, fontsize = 16)
plt.xlabel("Year", labelpad=20, fontsize = 12)
plt.ylabel("Number of Incidents", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_44_0.png)
    


The highest number of twentieth-century volcanic eruptions occurred in Indonesia. This is not surprising, as we know from above that Indonesia had the highest number of volcanic incidents overall, as well as the largest number of volcanoes.


```python
result = pd.read_sql("""SELECT Country, 
                               COUNT(Country) AS Number_of_Incidents
                        FROM volerup
                        WHERE Year >= 1901 AND Year <= 2000
                        GROUP BY Country
                        ORDER BY COUNT(Country) DESC
                        LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Country"], height=result["Number_of_Incidents"], color='red')
plt.title("Volcanic Eruptions in the 20th Century by Location", pad = 20, fontsize = 16)
plt.ylabel("Number of Incidents", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_47_0.png)
    


### Impact - Fatalities

For many of the incidents covered in the database, we have figures for the number of people killed. Which volcanos have killed the most people?


```python
result = pd.read_sql("""SELECT DISTINCT(Name), 
                               Country, 
                               SUM(Deaths) AS Total_Deaths
                        FROM volerup
                        WHERE Deaths NOTNULL
                        GROUP BY Name
                        ORDER BY SUM(Deaths) DESC
                        LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Name"] + ", " + result["Country"], height=result["Total_Deaths"], color='red')
plt.title("Deadliest Volcanoes", pad = 20, fontsize = 16)
plt.xlabel("Volcano", labelpad=20, fontsize = 12)
plt.ylabel("Number of Deaths", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_50_0.png)
    


And which country suffered the greatest death toll from volcanic incidents?


```python
result = pd.read_sql("""SELECT Country, 
                               SUM(Deaths) AS Total_Deaths
                        FROM volerup
                        WHERE Deaths NOTNULL
                        GROUP BY Country
                        ORDER BY SUM(Deaths) DESC
                        LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Country"], height=result["Total_Deaths"], color='red')
plt.title("Countries with Highest Death Tolls from Volcanic Eruptions", pad = 20, fontsize = 16)
plt.ylabel("Number of Deaths", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_53_0.png)
    


And which year was the deadliest?


```python
result = pd.read_sql("""SELECT CAST(Year AS INTEGER) AS Year, 
                               COUNT(Name) AS Number_of_Incidents, 
                               SUM(Deaths) AS Total_Deaths
                        FROM volerup
                        WHERE Deaths NOTNULL
                        GROUP BY Year
                        ORDER BY Year ASC
                        LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Year"].astype(str), height=result["Total_Deaths"], color='red')
plt.title("Years with Highest Death Tolls from Volcanic Eruptions", pad = 20, fontsize = 16)
plt.xlabel("Year", labelpad=20, fontsize = 12)
plt.ylabel("Number of Deaths", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_56_0.png)
    


### Impact - Financial Cost

Which volcanic incidents did the most damage?

Although the query limits search results to 20, only 10 records in the database have a dollar value for damages. 

The eruption of St Helens in 1980 is the most damaging incident in the dataset.


```python
result = pd.read_sql("""
    SELECT Name, 
           Country, 
           CAST(Year AS INTEGER) AS Year, 
           CAST(SUM(TOTAL_DAMAGE_MILLIONS_DOLLARS) AS INTEGER) AS 'Total Damage ($m)'
    FROM volerup
    WHERE TOTAL_DAMAGE_MILLIONS_DOLLARS NOTNULL
    GROUP BY TOTAL_DAMAGE_MILLIONS_DOLLARS
    ORDER BY SUM(TOTAL_DAMAGE_MILLIONS_DOLLARS) DESC
    LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Name"] + ", " + result["Country"] + " (" + result["Year"].astype(str) + ")", height=result["Total Damage ($m)"], color='red')
plt.title("Most Damaging Volcanic Eruptions", pad = 20, fontsize = 16)
plt.xlabel("Volcano", labelpad=20, fontsize = 12)
plt.ylabel("Total Damage ($m)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_59_0.png)
    


### Impact - Destructiveness

We can also find out how many homes were destroyed by each incident.


```python
result = pd.read_sql("""
 SELECT Name,  
        Country, 
        CAST(Year AS INTEGER) AS Year, 
        CAST(SUM(TOTAL_HOUSES_DESTROYED) AS INTEGER) AS Houses_Destroyed
 FROM volerup
 WHERE TOTAL_HOUSES_DESTROYED NOTNULL
 GROUP BY TOTAL_HOUSES_DESTROYED
 ORDER BY SUM(TOTAL_HOUSES_DESTROYED) DESC
 LIMIT 20;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Name"] + ", " + result["Country"] + " (" + result["Year"].astype(str) + ")", height=result["Houses_Destroyed"], color='red')
plt.title("Most Damaging Volcanic Eruptions", pad = 20, fontsize = 16)
plt.xlabel("Volcanic Eruption", labelpad=20, fontsize = 12)
plt.ylabel("Total Damage ($m)", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_62_0.png)
    


### Associated Phenomena - Tsunamis and Earthquakes

The dataset also records where these volcanic eruptions are linked to tsunamis or earthquakes. How many of the eruptions are associated with tsunamis or earthquakes, and which countries are the most affected?

#### Tsunamis

Of the 658 incidents recorded in the dataset, 133 are linked to tsunamis.

Indonesia faced the highest number of volcano-related tsunamis. This is not surprising given its high number of volcanoes, and its geography -- Indonesia consists of more than 17,000 islands.


```python
result = pd.read_sql("""
   SELECT Country, 
          COUNT(Country) AS Number_of_Tsunamis
   FROM volerup
   WHERE Associated_Tsunami = "TSU"
   GROUP BY Country
   ORDER BY COUNT(Country) DESC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Country"], height=result["Number_of_Tsunamis"], color='red')
plt.title("Countries with Highest Number of Volcano-Related Tsunamis", pad = 20, fontsize = 16)
plt.ylabel("Number of Tsunamis", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_66_0.png)
    


#### Earthquakes

Fewer volcanis eruptions are linked to earthquakes than to tsunamis. 55 of the eruptions in the dataset have an associated earthquake.

The United States and Japan are the two countries most affected by volcano-related earthquakes. 


```python
result = pd.read_sql("""
     SELECT Country, 
            COUNT(Country) AS Number_of_Earthquakes
     FROM volerup
     WHERE Associated_Earthquake = "EQ"
     GROUP BY Country
     ORDER BY COUNT(Country) DESC;""", database)
```


```python
plt.figure(figsize=(12, 4))
plt.bar(x=result["Country"], height=result["Number_of_Earthquakes"], color='red')
plt.title("Countries with Highest Number of Volcano-Related Earthquakes", pad = 20, fontsize = 16)
plt.ylabel("Number of Earthquakes", labelpad=20, fontsize = 12)
_ = plt.xticks(rotation = 45, ha = "right", fontsize = 10)
plt.margins(0.01, 0.01)
```


    
![png](Volcanos_files/Volcanos_69_0.png)
    


And what about volcanic eruptions linked to tsunamis and earthquakes?

36 incidents in the dataset were linked to both an earthquake and a tsunami.


```python
pd.read_sql("""
    SELECT Name,
           Country,
           COUNT(Name)
    FROM volerup
    WHERE Associated_Earthquake = "EQ" AND Associated_Tsunami = "TSU"
    GROUP BY Name
    ORDER BY COUNT(Name) DESC;""", database)
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
      <th>Name</th>
      <th>Country</th>
      <th>COUNT(Name)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Taal</td>
      <td>Philippines</td>
      <td>4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Yasur</td>
      <td>Vanuatu</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Sakura-jima</td>
      <td>Japan</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Mauna Loa</td>
      <td>United States</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Etna</td>
      <td>Italy</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Westdahl</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Vesuvius</td>
      <td>Italy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Unzen</td>
      <td>Japan</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Umboi</td>
      <td>Papua New Guinea</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>St. Helens</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Soputan</td>
      <td>Indonesia</td>
      <td>1</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Sarigan</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Santorini</td>
      <td>Greece</td>
      <td>1</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Rabaul</td>
      <td>Papua New Guinea</td>
      <td>1</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Puyehue</td>
      <td>Chile</td>
      <td>1</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Peuet Sague</td>
      <td>Indonesia</td>
      <td>1</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Oshima-Oshima</td>
      <td>Japan</td>
      <td>1</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Okmok</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Miyake-jima</td>
      <td>Japan</td>
      <td>1</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Komaga-take</td>
      <td>Japan</td>
      <td>1</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Kilauea</td>
      <td>United States</td>
      <td>1</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Kharimkotan</td>
      <td>Russia</td>
      <td>1</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Hibok-Hibok</td>
      <td>Philippines</td>
      <td>1</td>
    </tr>
    <tr>
      <th>23</th>
      <td>Gamalama</td>
      <td>Indonesia</td>
      <td>1</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Epi</td>
      <td>Vanuatu</td>
      <td>1</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Cosiguina</td>
      <td>Nicaragua</td>
      <td>1</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Banua Wuhu</td>
      <td>Indonesia</td>
      <td>1</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Awu</td>
      <td>Indonesia</td>
      <td>1</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Avachinsky</td>
      <td>Russia</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>


