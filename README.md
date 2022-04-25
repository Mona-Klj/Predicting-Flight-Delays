# LHL Midterm Project
## Flight Delays Prediction

This repo contains data and codes of Lighthouse Labs midterm project completed by me and my teammate (the other contributor). <br>

The goal is to predict arrival delays of commercial flights. Often, there isn't much airlines can do to avoid the delays, therefore, they play an important role in both profits and loss of the airlines. It is critical for airlines to estimate flight delays as accurate as possible because the results can be applied to both, improvements in customer satisfaction and income of airline agencies.
- regression (predict delay time in minutes)
- classification (4 class: no delay; minor delay; moderate delay; severe delay)


### Data

- The original data are stored in the Postgres database and contains four separate tables: 

    1. **flights**: The departure and arrival information about flights in US in years 2018 and 2019.
    2. **fuel_comsumption**: The fuel comsumption of different airlines from years 2015-2019 aggregated per month.
    3. **passengers**: The passenger totals on different routes from years 2015-2019 aggregated per month.
    4. **flights_test**: The departure and arrival information about flights in US in January 2020. This table will be used for evaluation.

- We have pulled some samples from the database and uploaded [here](data/raw). Modules for random pull and balance pull can be found in [here](src/modules).

### Data Preprocessing and Feature Engineering
Data preprocessing module can be found [here](src/modules). Preprocessed data was also uploaded [here](data/preprocessed). <br>

### Exploratory Data Analysis
A lot of insights were extracted from data analysis, the process and results are shown in the [Jupyter notebook](src/notebooks/EDA_and_more_feature_engineering.ipynb). All the plots are stored [here](plots).

### Encoding and Modeling
- Categorical feature encoding: We have tried some encoding methods on categorical features as below.
    - Target Mean encoding: encode categorical features with group target mean on training set, and map the value to the test set.
    - Leave-One-Out Target Encoding: similar to mean encoding except leave the target value of the row out when calculating the group mean.
- Models (regression and classification): XGBoost, Random Forest

### Folder submission.csv: <br>
* Final submission for evaluation. <br>
<br>
Notice: Experiments folder is just a mess for my teammate and I updating each others activities.

#### Folder data
* [raw](data/raw):<br>
    Contains raw data directly pulled from database. Modules for random pull and balance pull can be found in src/modules. <br>
* [preprocessed](data/preprocessed):<br>
    Contains preprocessed data including cleanning and most of feature engineering. Preprocessing module can be found in src/modules. <br>
#### Folder src <br>
* [modules](src/modules): <br>
    Contains self-written codes for pulling data from database and preprocessing for this project. <br>
* [Notebooks](src/notebooks) <br>
    Final Jupyter Notebooks. <br>
#### Folder plots <br>
* Exploratory data analysis [plots](plots). <br>
#### Folder submission.csv: <br>
* Final submission for evaluation. <br>
<br>
Notice: Experiments folder is just a mess for from our first tries on project then updating each others activities.
