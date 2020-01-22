
Focus:
Predict house price in four different areas: Daly City, Pacifica, San Mateo and San Francisco.

Data:
Data is scraped from various real estate database company (e.g. Zillow) using Python package 'requests'.

Dataset Descriptions:
Dataset contains approximately 3000 recent sold real estate information from 2016 - 2018.

Highlight of Key Features:
Price (Target)
Year built
Last Sold On
Number of Parking
Address
Building Type (Apartment, House, Condo, etc.)
Square Foot
Model Highlights:
Applied various prediction approaches such as simple linear regression (OLS), regularized least squares regression (L1 and L2), with hyperparameter tuning
To meet linear regression assumptions, tried different transformations to make highly skewed distributions less skewed
For robust regression, that is less sensitive to outliers in data than the squared error loss, utilized Huber loss functio
