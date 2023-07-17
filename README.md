# airPollutionAnalytics

### Tasks (10-July-2023 USA Time): 
__Preprocessing:__
   1. Download the CSV file https://drive.google.com/file/d/1x7Jj5HKiqG083I3VSHDJK4U-uzAoMaiZ/view?usp=drive_link
   2. Read the file as a data frame.
   3. Remove the first column, which is just a row number.
   4. Keep the second and remaining columns.
   5. Fill up the missing values in the data frame with 0.
   6. Replace the values greater than 200 to 0.

__Understanding the Statistics:__
   1. Given any user condition (say, >, < <=, >=, ==, etc) and a threshold value (say, 15), for each sensor point, count the number of rows satisfies the condition and output it as a hashmap with Key= sensorPoint and value=numberOfRowsSatisfiyingTheCondition.
   2. Using the plotly express with 'open street maps,' draw the heatmap of each point.

__Coding tips:__
1. Try to write generic Python class files without hardcoding the downloaded CSV file.
2. Do the proper documentation of your Python Programs.
3. Distribute among yourselves properly, and mention the tasks that each student will carry out.

    |student name | task|
    |-------------|-----|
    
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UdayLab/airPollutionAnalytics/main?labpath=Data_Preprocessing.ipynb)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UdayLab/airPollutionAnalytics/main?labpath=Hashmap.ipynb)
