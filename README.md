# Simple Table Generator

## Project description
This statistical tabular data generator is a python application to generate synthetic tabular data from the empirical distribution of input data. This software offers a GUI (written with PySimpleGUI) to navigate the various options and make it easier for users to use it. It works based on statistical sampling of the empirical data distributions, allowing to extract data series from .cvs files selected from the dropdown menu, and generating a tabular array of data with disjointed distribution as it is actually based on the independent sampling of each distribution (each column is treated independently). 

## Data generation methods
The following methods of distribution sampling are availables:
- **Cumulative distribution function (CDF)**
- **Kernel Sampling (work in progress, not implemented yet!)**
- **Theoretical distribution fitting**

### Cumulative distribution function (CDF)
The cumulative distribution function (CDF) uses the cumulative distribution of input data and reproduces the synthetic values on the bases of their probability of being observed within the samples. The curves are uniquely identified by an upwards continuous monotonic increasing cumulative distribution. This method fits almost every possible case and distribution shape. 

### Kernel sampling (not currently implemented!)
Coming soon

### Theoretical distribution fitting 
The distribution fitting method uses an embedded mathematical solver (distfit package, see https://erdogant.github.io/distfit/pages/html/index.html for more info), in order to fit the data with more than 80 different distribution models, selecting the best fitting model at the end and using it to generate data. The goodness of fitting is determined through the least squares sum (LSS) method, where the best model is identified by the lowest LSS value.

## Data validation
The generated data is validated using different methods, including histograms and cumulative distribution functions, the Kolgomorov-Smirnoff test and the correlation matrix. These tests are performed to compare the distribution of real and generated (synthetic) data. The graphs are generated within the GUI window, but can also be saved using the designated button (bottom right corner), once you have selected a folder path.

## Requirements
Requirement.txt file is provided to ensure full compatibility with the python application. The application has been tested using Python 3.10.12 

## How to use

