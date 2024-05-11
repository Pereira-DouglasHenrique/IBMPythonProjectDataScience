import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

# ---------- Question 3 ----------
# Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object.
# The stock is Tesla and its ticker symbol is GME.
ticker = yf.Ticker("GME")

# Using the ticker object and the function history extract stock information and save it in a dataframe named gme_data.
# Set the period parameter to max so we get information for the maximum amount of time.
gme_data = ticker.history(period="max")

# Reset the index using the reset_index(inplace=True) function on the gme_data DataFrame and display the first five rows of the gme_data dataframe
# using the head function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
gme_data.reset_index(inplace=True)
print(gme_data.head())

# ---------- Question 4 ----------
# Use the requests library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html.
# Save the text of the response as a variable named html_data.
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
response = requests.get(url)
html_data = response.content

# Parse the html data using beautiful_soup.
soup = BeautifulSoup(html_data, 'html.parser')

# Using BeautifulSoup or the read_html function extract the table with GameStop Revenue and store it into a dataframe named gme_revenue.
# The dataframe should have columns Date and Revenue.
# Make sure the comma and dollar sign is removed from the Revenue column using a method similar to what you did in Question 2.
table = soup.find("table")
gme_revenue = pd.read_html(str(table))[0]
gme_revenue.columns = ["Date", "Revenue"]

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue["Revenue"] = pd.to_numeric(gme_revenue["Revenue"], errors='coerce')

gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
#print(gme_revenue)

# Display the last five rows of the gme_revenue dataframe using the tail function. Take a screenshot of the results.
print(gme_revenue.tail())

# Convertendo a coluna Date para datetime
gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])

# ---------- Question 6 ----------
# Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph.
# The structure to call the make_graph function is make_graph(gme_data, gme_revenue, 'GameStop').
# Note the graph will only show data upto June 2021.
make_graph(gme_data, gme_revenue, 'GameStop')