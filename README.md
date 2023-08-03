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

    |Task                  | binderLink|
    |----------------------|-----|
      Heatmap  >15           |  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UdayLab/airPollutionAnalytics/main?labpath=preProcessing%2FPlotly.ipynb)
      Frequency_heatmap >35  | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UdayLab/airPollutionAnalytics/main?labpath=notebooks%2FFrequency_Heatmap.ipynb)
      K-long pattern         | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UdayLab/airPollutionAnalytics/main?labpath=notebooks%2FFP_Growth.ipynb)
_Students mention the four tasks assigned by me today_

1. Check sensor values; delete columns with values less than a user-specified value.
2. Impute missing values using linear regression or neural network (deep learning).
3. Build ML models for each sensor to predict future learning.  
4. Mine and visualize longest patterns using FP Growth and Plotly Express.
