import networkx as nx
import matplotlib.pyplot as plt

# Crear un grafo no dirigido (representando una topología de red)
G = nx.Graph()

# Agregar nodos con información adicional
nodes_info = {
    "Router1": {"label": "Router1\nRed: 192.168.1.0/24\nIP: 192.168.1.1"},
    "Router2": {"label": "Router2\nRed: 192.168.1.0/24\nIP: 192.168.1.2"},
    "Switch1": {"label": "Switch1"},
    "PC1": {"label": "PC1\nRed: 192.168.1.0/24\nIP: 192.168.1.3"},
    "PC2": {"label": "PC2\nRed: 192.168.1.0/24\nIP: 192.168.1.4"}
}

G.add_nodes_from(nodes_info.keys())

# Agregar conexiones entre nodos (enlaces) con información de IP
edges = [
    ("Router1", "Switch1", {"label": "Enlace1\nIPs: 192.168.1.1 - 192.168.1.5"}),
    ("Switch1", "PC1", {"label": "Enlace2\nIPs: 192.168.1.5 - 192.168.1.3"}),
    ("Switch1", "PC2", {"label": "Enlace3\nIPs: 192.168.1.5 - 192.168.1.4"}),
    ("Router2", "Switch1", {"label": "Enlace4\nIPs: 192.168.1.2 - 192.168.1.5"})
]

G.add_edges_from(edges)

# Dibujar la topología
pos = nx.spring_layout(G)  # Posicionamiento de los nodos
nx.draw(G, pos, with_labels=True, labels={node: info["label"] for node, info in nodes_info.items()}, node_size=700, node_color="skyblue", font_size=6, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)

# Agregar etiquetas a las conexiones
edge_labels = {(edge[0], edge[1]): edge[2]["label"] for edge in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=6)

# Mostrar el gráfico
plt.title('Topología de Red')
plt.show()
