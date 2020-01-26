### VANREAPER : Vancouver Real Estate Analysis and Predictions

Introduction:

Buying a property is financially the biggest decision you make in life. Given the enormity of the purchase and complexity of the factors that go into the decision, the situation easily leads to decision paralysis. Our data product aims to simplify this problem by helping people make informed decisions by encapsulating our machine learning models inside a intuitive and easy to use web frontend. The web frontend provides property and rental recommendations to people based on their preferences thereby eliminating the need for visiting multiple websites to get property information.	

For people who are looking for places in a specific locality, our product provides area level predictive analytics of the real estate once the user selects name of the area from the dropdown. We have leveraged the power of Google Maps to visualize both - the results of recommendation systems and area level predictive analytics provided by our backend machine learning models. 

In addition to that, we have discovered intriguing correlations between the real estate price and other features like school rating, crime rate in the area and the lending interest rates prevalent at the time 

We have scraped data from multiple sources like rental data from craigslist, property tax data from BC Assessment Authority, property listings data from REW, school ratings data from Fraser Institute and historical interest rates from Bank of Canada. In the next step, we performed exploratory data analysis and feature engineering to get the data in proper shape for feeding it into predictive models. Regressions models like Gradient Boosting Trees, Random Forrest, Linear Regression, Ada Boost and Time Series models like ARIMA, LSTMs and Vector Auto Regressor were used to predict future prices of the properties. Property Recommendation System was implemented using k-nearest neighbors algorithm in scikit-learn. Finally all the statistical models were serialized, persisted and deployed using an interactive Flask Web Application.

More infor in the report - <a href="https://github.com/pavankosaraju/VanReaper/blob/master/VANREAPER%20%E2%80%93%20Vancouver%20Real%20Estate%20Analysis%20and%20Predictions.pdf" target="_blank">VanReaper</a>

Project video - <a href="https://www.youtube.com/watch?v=ucRwm4dBVGs" target="_blank">Youtube</a>

*** ***Original Data is removed due to confidentiality. For any enquireies, please contact through email. Thank you.*** ***

Instructions:

1. run 'pip install requirements.txt'
2. go to the 'deploy' folder
3. run 'python server.py'
4. open browser with 'localhost:5000' as url

>Property 
- Sample Inputs = Interest Rate : 3.5, PID : 017-393-400, Area: Kitsilano

>Recommendation
- Sample Inputs = Area : V3K, Bedroom : 3, Bathroom : 2, Area Square Feet : 1800, Fireplace : 1, Type : Townhouse 

>Trend
- Select area from the drop down list to visualize the trends

