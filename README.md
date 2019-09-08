### Coming Soon

Introduction:

Buying a property is financially the biggest decision you make in life. Given the enormity of the purchase and complexity of the factors that go into the decision, the situation easily leads to decision paralysis. Our data product aims to simplify this problem by helping people make informed decisions by encapsulating our machine learning models inside a intuitive and easy to use web frontend. The web frontend provides property and rental recommendations to people based on their preferences thereby eliminating the need for visiting multiple websites to get property information.	

For people who are looking for places in a specific locality, our product provides area level predictive analytics of the real estate once the user selects name of the area from the dropdown. We have leveraged the power of Google Maps to visualize both - the results of recommendation systems and area level predictive analytics provided by our backend machine learning models. 

In addition to that, we have discovered intriguing correlations between the real estate price and other features like school rating, crime rate in the area and the lending interest rates prevalent at the time 

We have scraped data from multiple sources like rental data from craigslist, property tax data from BC Assessment Authority, property listings data from REW, school ratings data from Fraser Institute and historical interest rates from Bank of Canada. In the next step, we performed exploratory data analysis and feature engineering to get the data in proper shape for feeding it into predictive models. Regressions models like Gradient Boosting Trees, Random Forrest, Linear Regression, Ada Boost and Time Series models like ARIMA, LSTMs and Vector Auto Regressor were used to predict future prices of the properties. Property Recommendation System was implemented using k-nearest neighbors algorithm in scikit-learn. Finally all the statistical models were serialized, persisted and deployed using an interactive Flask Web Application.


Instructions:

1. git clone git@csil-git1.cs.surrey.sfu.ca:quad_squad/housing_market_analysis.git
2. go to the directory
3. open cmd/bash
4. run 'pip install requirements.txt'
5. go to the 'deploy' folder
6. run 'python server.py'
7. open browser with 'localhost:5000' as url

>Property 
- Sample Inputs = Interest Rate : 3.5, PID : 017-393-400, Area: Kitsilano

>Recommendation
- Sample Inputs = Area : V3K, Bedroom : 3, Bathroom : 2, Area Square Feet : 1800, Fireplace : 1, Type : Townhouse 

>Trend
- Select area from the drop down list to visualize the trends

