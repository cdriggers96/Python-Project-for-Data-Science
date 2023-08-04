##Analyzing Historical Stock/Revenue Data and Building a Dashboard

!pip install yfinance==0.1.67
!mamba install bs4==4.10.0 -y
!pip install nbformat==4.2.0

import yfinance as yf
import Pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Defining graphing function
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

#Using yfinance to Extract Tesla Stock Data
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

#Using Webscraping to Extract Tesla Revenue Data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text
print(html_data)
soup = BeautifulSoup(html_data)

#extracting table Tesla Revenue and storing it in a dataframe
soup.find_all("tbody")[1]
tesla_revenue = pd.DataFrame(columns=["Date","Revenue"])
for row in soup.find("tbody").find_all('tr'):
	col = row.find_all('td')
	date = col[0].text
	revenue = col[1].text
	tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index=True)
tesla_revenue.head()

#Provided code for formatting
tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
tesla_revenue.tail()

#Extracting GameStop info with yfinance
GameStop = yf.Ticker("GME")
gme_data = GameStop.history(period="max")
gme_data.reset_index(inplace=True)
gme_data.head()

#Webscraping to extract GME Revenue Data
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data = requests.get(url).text
print(html_data)

soup = BeautifulSoup(html_data)
soup.find_all('tbody')[1]

gme_revenue = pd.DataFrame(columns=["Date","Revenue"])
for row in soup.find('tbody').find_all('tr'):
	col = row.find_all('td')
	date = col[0].text
	revenue = col[1].text
	gme_revenue = gme_revenue.append({"Date":date, "Revenue": revenue}, ignore_index=True)

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"")
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

gme_revenue.tail()

#Plot stock graph
make_graph(tesla_data, tesla_revenue, "Tesla")
make_graph(gme_data, gme_revenue, "GameStop")
