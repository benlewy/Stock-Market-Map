import requests
from bs4 import BeautifulSoup
import squarify
import matplotlib.pyplot as plt

inputs = input('What companies do you want to visualize? Enter either "Tech", "World", or "USA": ').upper()

TECH = "https://companiesmarketcap.com/tech/largest-tech-companies-by-market-cap/"
WORLD = "https://companiesmarketcap.com"
USA = "https://companiesmarketcap.com/usa/largest-companies-in-the-usa-by-market-cap/"

if inputs == TECH:
    response = requests.get(TECH)
elif inputs == WORLD:
    response = requests.get(WORLD)
else:
    response = requests.get(USA)

soup = BeautifulSoup(response.text, "lxml")

rows = soup.findChildren('tr')

symbols = []
market_caps = []
sizes = []

for row in rows:
    try:
        symbol = row.find('div', {'class': 'company-code'}).text
        market_cap = row.findAll('td')[2].text
        market_caps.append(market_cap)
        symbols.append(symbol)

        if market_cap.endswith('T'):
            sizes.append(float(market_cap[1:-2]) * 10 ** 12)
        elif market_cap.endswith('B'):
            sizes.append(float(market_cap[1:-2]) * 10 ** 9)
    except AttributeError:
        pass

labels = [f"{symbols[i]}\n ({market_caps[i]})" for i in range(len(symbols))]
colors = [plt.cm.terrain(i / float(len(symbols))) for i in range(len(symbols))]
plt.rcParams["figure.figsize"] = (14, 8)
plt.rcParams["figure.autolayout"] = True
plt.axis('off')
squarify.plot(sizes=sizes, label=labels, color=colors, bar_kwargs={"linewidth": 0.5, "edgecolor": "#111111"})
plt.show()
