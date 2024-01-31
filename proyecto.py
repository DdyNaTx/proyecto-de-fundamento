import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Crear un grafo no dirigido (representando una topología de red)
G = nx.Graph()

# Diccionario para realizar un seguimiento de las subredes utilizadas
used_subnets = set()

# Función para generar una nueva subred única
def generate_subnet():
    subnet = "192.168."
    i = 1
    while f"{subnet}{i}" in used_subnets:
        i += 1
    used_subnets.add(f"{subnet}{i}")
    return f"{subnet}{i}.0/24"

# Función para generar una nueva IP única dentro de una subred
def generate_ip(subnet):
    i = 2
    while f"{subnet[:-4]}{i}" in G.nodes:
        i += 1
    return f"{subnet[:-4]}{i}"

# Agregar nodos con información adicional
nodes_info = {
    "Router1": {"label": f"Router1\nRed: {generate_subnet()}\nIP: {generate_ip(generate_subnet())}", "hidden": True},
    "Router2": {"label": f"Router2\nRed: {generate_subnet()}\nIP: {generate_ip(generate_subnet())}", "hidden": True},
    "Switch1": {"label": "Switch1", "hidden": True},
    "PC1": {"label": f"PC1\nRed: {generate_subnet()}\nIP: {generate_ip(generate_subnet())}", "hidden": True},
    "PC2": {"label": f"PC2\nRed: {generate_subnet()}\nIP: {generate_ip(generate_subnet())}", "hidden": True}
}

G.add_nodes_from(nodes_info.keys())

# Agregar conexiones entre nodos (enlaces) con información de IP
edges = [
    ("Router1", "Switch1", {"label": f"Enlace1\nIPs: {generate_ip(generate_subnet())} - {generate_ip(generate_subnet())}"}),
    ("Switch1", "PC1", {"label": f"Enlace2\nIPs: {generate_ip(generate_subnet())} - {generate_ip(generate_subnet())}"}),
    ("Switch1", "PC2", {"label": f"Enlace3\nIPs: {generate_ip(generate_subnet())} - {generate_ip(generate_subnet())}"}),
    ("Router2", "Switch1", {"label": f"Enlace4\nIPs: {generate_ip(generate_subnet())} - {generate_ip(generate_subnet())}"})
]

G.add_edges_from(edges)

# Dibujar la topología
pos = nx.spring_layout(G)  # Posicionamiento de los nodos
nx.draw(G, pos, with_labels=True, labels={node: node for node in nodes_info},
        node_size=700, node_color="skyblue", font_size=6, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)

# Función para manejar el evento de hacer clic en un nodo
def on_click(event):
    if event.xdata is not None and event.ydata is not None:
        for node, (x, y) in pos.items():
            if (x - 0.03 < event.xdata < x + 0.03) and (y - 0.03 < event.ydata < y + 0.03):
                if node in nodes_info:
                    if nodes_info[node]["hidden"]:
                        bbox_props = dict(boxstyle="round,pad=0.3", ec="black", lw=1, alpha=0.8)
                        plt.text(x, y, nodes_info[node]["label"], fontsize=8, bbox=bbox_props, ha="center")
                        nodes_info[node]["hidden"] = False
                    else:
                        plt.text(x, y, node, fontsize=8, bbox=dict(facecolor='white', alpha=0.0), ha="center")
                        nodes_info[node]["hidden"] = True
                    plt.draw()

# Función para agregar un router al grafo
def add_router(event):
    global G, pos, nodes_info
    new_router_name = f"Router{len([n for n in G.nodes if 'Router' in n]) + 1}"
    connected_node = "Switch1"  # Puedes ajustar el nodo al que está conectado el router
    subnet = generate_subnet()
    ip_address = generate_ip(subnet)
    
    # Intentar agregar el nuevo router hasta que sea exitoso
    while True:
        try:
            G.add_node(new_router_name)
            G.add_edge(new_router_name, connected_node, label=f"Enlace\nIPs: {ip_address} - {generate_ip(subnet)}")
            new_pos = nx.spring_layout(G)
            pos.update(new_pos)
            break  # Salir del bucle si la adición fue exitosa
        except nx.NetworkXError:
            pass  # Ignorar el error y volver a intentar
    
    nodes_info[new_router_name] = {"label": f"{new_router_name}\nRed: {subnet}\nIP: {ip_address}", "hidden": True}
    redraw()

# Función para agregar un PC al grafo
def add_pc(event):
    global G, pos, nodes_info
    new_pc_name = f"PC{len([n for n in G.nodes if 'PC' in n]) + 1}"
    connected_router = f"Router{len([n for n in G.nodes if 'Router' in n])}"  # Conectar a un router existente
    subnet = generate_subnet()
    ip_address = generate_ip(subnet)
    
    # Intentar agregar el nuevo PC hasta que sea exitoso
    while True:
        try:
            G.add_node(new_pc_name)
            G.add_edge(new_pc_name, connected_router, label=f"Enlace\nIPs: {ip_address} - {generate_ip(subnet)}")
            new_pos = nx.spring_layout(G)
            pos.update(new_pos)
            break  # Salir del bucle si la adición fue exitosa
        except nx.NetworkXError:
            pass  # Ignorar el error y volver a intentar
    
    nodes_info[new_pc_name] = {"label": f"{new_pc_name}\nRed: {subnet}\nIP: {ip_address}", "hidden": True}
    redraw()

# Función para redibujar el gráfico
def redraw():
    plt.clf()
    nx.draw(G, pos, with_labels=True, labels={node: node for node in nodes_info},
            node_size=700, node_color="skyblue", font_size=6, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, alpha=0.7)
    plt.title('Topología de Red')

# Crear botones para agregar routers y PCs
ax_button_router = plt.axes([0.8, 0.11, 0.1, 0.05])  # [left, bottom, width, height]
button_router = Button(ax_button_router, 'Agregar Router', color='lightgoldenrodyellow', hovercolor='0.975')
button_router.on_clicked(add_router)

ax_button_pc = plt.axes([0.8, 0.06, 0.1, 0.05])  # [left, bottom, width, height]
button_pc = Button(ax_button_pc, 'Agregar PC', color='lightgoldenrodyellow', hovercolor='0.975')
button_pc.on_clicked(add_pc)

# Conectar la función de manejo de eventos
plt.gcf().canvas.mpl_connect('button_press_event', on_click)

# Mostrar el gráfico
plt.title('Topología de Red')
plt.show()
