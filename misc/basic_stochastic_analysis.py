import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import math

def simulation(price, capital, total_days):
    shares = []
    for ind in range(len(price)):
        shares.append(int(divmod(capital[ind],price[ind])[0]))

    total_days = 100
    current_days = 0
    price_history = []
    while current_days < total_days:
        temp = []
        for item in price:
            if item > 0:
                item = item + random.uniform(-.25,.25)
                item = round(item,2)
                if item <= 0:
                    item = 0
            elif item <= 0:
                item = 0
            temp.append(item)
        price = temp
        price_history.append(price)
        current_days += 1
        random.seed()

    price_history = map(list, zip(*price_history))

    total_diff = []
    for ind in range(len(price_history)):
        total_diff.append(round(shares[ind]*price_history[ind][99] - capital[ind],2))

    return total_diff


#TODO: Figure out if variations in capital affect the outcome

def generate_stats(n_times_run):
    price = [.1,.2,.3,.4,.5,.6,.7,.8,.9,.10]
    capital = [1,2,3,4,5,6,7,8,9,10]
    total_days = 100

    results = []
    sum_results = []
    for i in range(n_times_run):
        results.append(simulation(price,capital,total_days))
        sum_results.append(round(sum(simulation(price,capital,total_days)),2))

    stats = np.array(sum_results)
    mean = round(np.mean(stats),2)
    std = round(np.std(stats),2)

mu, std = generate_stats(20)

x = np.linspace(mu-(3*std),mu+(3*std), 100)
plt.plot(x,mlab.normpdf(x, mu, std))
plt.show()
