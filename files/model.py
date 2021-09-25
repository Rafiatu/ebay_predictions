import pandas as pd
import pickle
from scraper import eBay
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder


bags = eBay().scrape(keyword='bag', quantity=1000)
shoes = eBay().scrape(keyword='shoe', quantity=1000)
pants = eBay().scrape(keyword='pants', quantity=1000)
gold = eBay().scrape(keyword='gold', quantity=1000)
watches = eBay().scrape(keyword='watch', quantity=1000)
earrings = eBay().scrape(keyword='earring', quantity=1000)
shirts = eBay().scrape(keyword='shirt', quantity=1000)
dresses = eBay().scrape(keyword='dress', quantity=1000)
phones = eBay().scrape(keyword='phone', quantity=1000)
laptops = eBay().scrape(keyword='laptop', quantity=1000)


data = pd.concat([bags, shoes, pants, gold, watches, earrings,
                  shirts, dresses, phones, laptops], ignore_index=True)

print("Data acquisition was successful. Modelling has started. Please be patient.")

one_hot_encoder = OneHotEncoder(handle_unknown='ignore')
one_hot_encoder.fit(data[['title', 'category']])
relevant = one_hot_encoder.transform(data[['title', 'category']]).todense()


data['price'] = [price.strip('$') for price in data.price]
data['price'] = data['price'].str.split(expand=True).iloc[:, 0]
data['price'] = data['price'].str.replace(',', '')
data['price'] = data['price'].astype('float32')


X_train, X_test, y_train, y_test = train_test_split(relevant, data['price'])


classifier = RandomForestRegressor()
classifier.fit(X_train, y_train)

with open("classifier.pkl", "wb") as file:
    pickle.dump(classifier, file)


with open("one_hot_encoder.pkl", "wb") as f:
    pickle.dump(one_hot_encoder, f)


print("Modelling successful and pickle files have been created.")
