import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo no dirigido (representando una topología de red)
G = nx.Graph()

# Agregar nodos
G.add_nodes_from(["Router1", "Router2", "Switch1", "PC1", "PC2"])

# Agregar conexiones entre nodos (enlaces)
G.add_edges_from([("Router1", "Switch1"), ("Switch1", "PC1"), ("Switch1", "PC2"), ("Router2", "Switch1")])

# Dibujar la topología
pos = nx.spring_layout(G)  # Posicionamiento de los nodos
nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)

# Mostrar el gráfico
plt.show()
