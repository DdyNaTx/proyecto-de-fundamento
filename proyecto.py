import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tkinter import Tk, Label, Button as TkButton 
from tkinter import Tk, Button, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
nodes_info = {}
G.add_nodes_from(nodes_info.keys())

# Agregar conexiones entre nodos (enlaces) con información de IP
edges = []
G.add_edges_from(edges)

# Crear una figura
fig, ax = plt.subplots(figsize=(10, 8))

# Dibujar la topología
pos = nx.spring_layout(G)  # Posicionamiento de los nodos
nx.draw(G, pos, with_labels=True, labels={node: node for node in nodes_info},
        node_size=700, node_color="skyblue", font_size=6, font_color="black", font_weight="bold", edge_color="none", alpha=0.7)

# Función para manejar el evento de hacer clic en un nodo
def on_node_click(event):
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
def add_router():
    global G, pos, nodes_info
    new_router_name = f"Router{len([n for n in G.nodes if 'Router' in n]) + 1}"
    
    # Encontrar el último router existente, si hay uno
    routers = [node for node in G.nodes if 'Router' in node]
    last_router = routers[-1] if routers else None
    
    # Intentar agregar el nuevo router hasta que sea exitoso
    while True:
        try:
            G.add_node(new_router_name)
            if last_router:
                G.add_edge(new_router_name, last_router, label=f"Enlace\nIPs: {generate_ip(generate_subnet())} - {generate_ip(generate_subnet())}")
            new_pos = nx.spring_layout(G)
            pos.update(new_pos)
            break  # Salir del bucle si la adición fue exitosa
        except nx.NetworkXError:
            pass  # Ignorar el error y volver a intentar
    
    nodes_info[new_router_name] = {"label": f"{new_router_name}\nRed: {generate_subnet()}\nIP: {generate_ip(generate_subnet())}", "hidden": True}
    redraw()

# Función para agregar un PC al grafo
def add_pc():
    global G, pos, nodes_info
    new_pc_name = f"PC{len([n for n in G.nodes if 'PC' in n]) + 1}"
    
    # Encontrar el último switch existente, si hay uno
    switches = [node for node in G.nodes if 'Switch' in node]
    last_switch = switches[-1] if switches else None
    
    # Intentar agregar el nuevo PC hasta que sea exitoso
    while True:
        try:
            G.add_node(new_pc_name)
            if last_switch:
                G.add_edge(new_pc_name, last_switch, label=f"Enlace\nIPs: {generate_ip(generate_subnet())} - {generate_ip(generate_subnet())}")
            new_pos = nx.spring_layout(G)
            pos.update(new_pos)
            break  # Salir del bucle si la adición fue exitosa
        except nx.NetworkXError:
            pass  # Ignorar el error y volver a intentar
    
    nodes_info[new_pc_name] = {"label": f"{new_pc_name}\nRed: {generate_subnet()}\nIP: {generate_ip(generate_subnet())}", "hidden": True}
    redraw()

# Función para agregar un switch al grafo
def add_switch():
    global G, pos, nodes_info
    new_switch_name = f"Switch{len([n for n in G.nodes if 'Switch' in n]) + 1}"
    
    # Encontrar el último router existente, si hay uno
    routers = [node for node in G.nodes if 'Router' in node]
    last_router = routers[-1] if routers else None
    
    # Intentar agregar el nuevo switch hasta que sea exitoso
    while True:
        try:
            G.add_node(new_switch_name)
            if last_router:
                G.add_edge(new_switch_name, last_router, label=f"Enlace\nIPs: {generate_ip(generate_subnet())} - {generate_ip(generate_subnet())}")
            new_pos = nx.spring_layout(G)
            pos.update(new_pos)
            break  # Salir del bucle si la adición fue exitosa
        except nx.NetworkXError:
            pass  # Ignorar el error y volver a intentar
    
    nodes_info[new_switch_name] = {"label": f"{new_switch_name}\nRed: {generate_subnet()}\nIP: {generate_ip(generate_subnet())}", "hidden": True}
    redraw()

# Función para redibujar el gráfico con imágenes en lugar de nombres de nodo
def redraw():
    ax.clear()

    # Dibujar nodos con imágenes
    for node, (x, y) in pos.items():
        image_path = 'router.png' if 'Router' in node else 'switch.png' if 'Switch' in node else 'pc.png'
        image = plt.imread(image_path)
        imagebox = OffsetImage(image, zoom=0.1)  # Puedes ajustar el valor de zoom según tus preferencias
        ab = AnnotationBbox(imagebox, (x, y), frameon=False, pad=0.0)
        ax.add_artist(ab)

    # Dibujar enlaces
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1, alpha=0.7)

    ax.set_title('Topología de Red')
    ax.axis('off')

    canvas.draw()

# Crear una ventana Tkinter para los botones
root = Tk()
root.title("simulador")

# Crear un contenedor Frame
button_frame = Frame(root)
button_frame.pack(pady=10)

# Botones para agregar router, switch y PC en el contenedor
button_router = Button(button_frame, text="Agregar Router", command=add_router)
button_router.pack(side='left', padx=5)

button_switch = Button(button_frame, text="Agregar Switch", command=add_switch)
button_switch.pack(side='left', padx=5)

button_pc = Button(button_frame, text="Agregar PC", command=add_pc)
button_pc.pack(side='left', padx=5)

# Inicializar el lienzo para matplotlib
canvas = FigureCanvasTkAgg(fig, master=root)  
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side='top', fill='both', expand=1)

# Conectar la función de clic en el nodo
canvas.mpl_connect('button_press_event', on_node_click)

# Mostrar la ventana
root.mainloop()
