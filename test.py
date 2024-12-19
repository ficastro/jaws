from matplotlib import pyplot
import pandas as pd
import numpy as np

data = {
    "USA":{
        "Surfing": 34,
        "Swimming": 29
    },
    "BRAZIL":{
        "Surfing":20,
        "Swimming": 30
    }
}

countries = list(data.keys())
activities = list(data[countries[0]].keys())

values = {activity: [data[country][activity] for country in countries] for activity in activities}

x = np.arange(len(countries))
width = 0.35
fig, ax = pyplot.subplots()

for i, activity in enumerate(activities):
    ax.bar(x + i * width, values[activity], width, label=activity)

ax.set_xlabel("Countries")
ax.set_ylabel("Fatality rate (%)")
ax.set_title("Shark attacks fatality rate by activity and country")
ax.set_xticks(x + width / 2)
ax.set_xticklabels(countries)
ax.legend(title="Activities")

pyplot.tight_layout()
pyplot.show()