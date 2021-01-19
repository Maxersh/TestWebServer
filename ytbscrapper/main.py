import json
import datetime as DT
import matplotlib.pyplot as plt
import ytbscrapper

channel_id = 'UCgtAOyEQdAyjvm9ATCi_Aig'

video_path, info_path = ytbscrapper.get_info(channel_id)

with open(info_path, 'r') as file:
    info = json.load(file)

deltas = []
views = []
now = DT.datetime.now()

for index, key in enumerate(info):
    date = DT.datetime.strptime(info[key]['date'], "%Y-%m-%dT%H:%M:%SZ")
    delta = now - date
    additive = delta.seconds / 3600 / 24
    days = delta.days + int(additive + (0.5 if additive > 0 else -0.5))
    view = info[key]['view']
    deltas.append(days)
    views.append(view)

plt.plot(deltas, views, color='red')
plt.show()
