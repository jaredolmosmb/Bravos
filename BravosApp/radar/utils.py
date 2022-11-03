import matplotlib.pyplot as plt
import base64
from io import BytesIO
import numpy as np

def get_graph():
	buffer = BytesIO()
	plt.savefig(buffer, format='png')
	buffer.seek(0)
	image_png = buffer.getvalue()
	graph = base64.b64encode(image_png)
	graph = graph.decode('utf-8')
	buffer.close()
	return graph 


def get_plot(x,y):
	#...
	plt.switch_backend('AGG')
	plt.figure(figsize=(10,5))
	plt.title('games played')
	plt.plot(x,y)
	plt.xticks(rotation=45)
	plt.xlabel('player')
	plt.ylabel('games')
	plt.tight_layout()
	graph = get_graph()

	graph = get_graph
	return graph 

def get_radar():
	categories = ['primer', 'segunda', 'tercera', 'cuarta', 'quinta', '']

	vehicle1 = [3,5,1,5,6]
	vehicle1 = np.concatenate((vehicle1,[vehicle1[0]]))

	vehicle2 = [4,7,8,3,4]
	vehicle2 = np.concatenate((vehicle2,[vehicle2[0]]))


	label_placement = np.linspace(start=0, stop=2*np.pi, num=len(vehicle1))

	plt.figure(figsize=(6,6))
	plt.subplot(polar=True)
	plt.plot(label_placement, vehicle1)
	plt.plot(label_placement, vehicle2)

	lines, labels = plt.thetagrids(np.degrees(label_placement), labels = categories)
	plt.title('Compare Vehicles', y=1.1, fontdict={'fontsize': 18})
	plt.legend(labels=['vehicle1', 'vehicle2'], loc=(0.95, 0.8))

	graph = get_graph()
	graph = get_graph
	return graph

def get_radar2(categories, player1, player2, name1, name2):
	
	player1 = np.concatenate((player1,[player1[0]]))

	player2 = np.concatenate((player2,[player2[0]]))


	label_placement = np.linspace(start=0, stop=2*np.pi, num=len(player1))

	plt.figure(figsize=(6,6))
	plt.subplot(polar=True)
	plt.plot(label_placement, player1)
	plt.plot(label_placement, player2)

	lines, labels = plt.thetagrids(np.degrees(label_placement), labels = categories)
	plt.title('Compare Players', y=1.1, fontdict={'fontsize': 18})
	plt.legend(labels=[name1, name2], loc=(0.95, 0.8))

	graph = get_graph()
	graph = get_graph
	return graph