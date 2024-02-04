import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from tkinter import Tk, Label, Button as TkButton 
from tkinter import Tk, Button, Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch
# Crear un grafo no dirigido (representando una topología de red)
G = nx.Graph()

# Diccionario para realizar un seguimiento de las subredes utilizadas
used_subnets = set()
pos_images = {}

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

# Inicializar un diccionario para rastrear la visibilidad de la información del nodo

def on_node_click(event):
    if event.xdata is not None and event.ydata is not None:
        for node, (x, y) in pos.items():
            if (x - 0.03 < event.xdata < x + 0.03) and (y - 0.03 < event.ydata < y + 0.03):
                if node in nodes_info:
                    bbox_props = dict(boxstyle="round,pad=0.3", ec="black", lw=1, alpha=0.8, facecolor='lightgray')
                    label = f"{nodes_info[node]['label']}\n"
                    if 'network_info' in nodes_info[node]:
                        label += f"Red: {nodes_info[node]['network_info']}\n"
                    if 'ip_address' in nodes_info[node]:
                        label += f"IP: {nodes_info[node]['ip_address']}"
                    
                    if "hidden" not in nodes_info[node] or not nodes_info[node]["hidden"]:
                        annotation = ax.annotate(label, (x, y), fontsize=8, color='blue', ha="center", va="center", bbox=bbox_props)
                        nodes_info[node]["annotation"] = annotation
                        nodes_info[node]["hidden"] = True
                    else:
                        annotation = nodes_info[node].get("annotation")
                        if annotation:
                            annotation.remove()
                        nodes_info[node]["hidden"] = False
                    plt.draw()
                break


# Importante salir del bucle después de procesar un nodo
 # Importante salir del bucle después de procesar un nodo
 # Importante salir del bucle después de procesar un nodo

# Asegúrate de conectar el evento de clic al manejador
fig.canvas.mpl_connect('button_press_event', on_node_click)


# Función para conectar el router y actualizar las imágenes de nodos conectados
# Función para conectar el router y actualizar las imágenes de nodos conectados
def connect_router(router_name):
    # Implementa la lógica para conectar el router aquí
    print(f"Conectando el router {router_name}")

    # Cambiar la imagen del router a "router_connected.png"
    update_node_image(router_name, "router.png")

    # Actualizar imágenes de nodos conectados
    update_connected_nodes_images(router_name, "router.png", "switch.png", "pc.png")

# Función para desconectar el router y actualizar las imágenes de nodos conectados
def disconnect_router(router_name):
    # Implementa la lógica para desconectar el router aquí
    print(f"Desconectando el router {router_name}")

    # Cambiar la imagen del router a "router_disconnected.png"
    update_node_image(router_name, "router2.png")

    # Actualizar imágenes de nodos conectados
    update_connected_nodes_images(router_name, "router2.png", "switch2.png", "pc2.png")

# Función para actualizar las imágenes de nodos conectados al router específico
def update_connected_nodes_images(router_name, new_router_image_path, new_switch_image_path, new_pc_image_path):
    for edge in G.edges(router_name):
        connected_node = edge[1]
        # Verificar si el nodo conectado es un switch
        if 'Switch' in connected_node:
            update_node_image(connected_node, new_switch_image_path)
            update_switched_nodes_images(connected_node, new_router_image_path, new_pc_image_path)
        elif 'PC' in connected_node:
            update_node_image(connected_node, new_pc_image_path)


# Función para actualizar la imagen de un nodo específico
def update_node_image(node_name, new_image_path):
    for node, imagebox in pos_images.items():
        if node_name == node:
            new_image = plt.imread(new_image_path)
            imagebox.get_children()[0].set_data(new_image)
            canvas.draw()
            break

# Función para actualizar las imágenes de nodos conectados al switch específico
def update_switched_nodes_images(switch_name, new_image_path_router, new_image_path_pc):
    for edge in G.edges(switch_name):
        connected_node = edge[1]
        # Verificar si el nodo conectado es una PC
        if 'PC' in connected_node:
            update_pc_image(connected_node, new_image_path_pc)
        else:
            update_node_image(connected_node, new_image_path_router)


# Función para actualizar la imagen de una PC específica
def update_pc_image(pc_name, new_image_path):
    update_node_image(pc_name, new_image_path)


# Función para actualizar la imagen de un switch específico
def update_switch_image(switch_name, new_image_path):
    update_node_image(switch_name, new_image_path)





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

    # Crear botones Conectar y Desconectar
    button_connect = TkButton(button_frame, text=f"Conectar {new_router_name}", command=lambda: connect_router(new_router_name))
    button_connect.pack(side='left', padx=5)

    button_disconnect = TkButton(button_frame, text=f"Desconectar {new_router_name}", command=lambda: disconnect_router(new_router_name))
    button_disconnect.pack(side='left', padx=5)






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

# Modificar la función redraw para usar nx.draw_networkx_labels y nx.draw_networkx_nodes
def redraw():
    ax.clear()

    # Dibujar nodos con imágenes
    
    for node, (x, y) in pos.items():
        image_path = 'router.png' if 'Router' in node else 'switch.png' if 'Switch' in node else 'pc.png'
        image = plt.imread(image_path)
        imagebox = OffsetImage(image, zoom=0.1)
        ab = AnnotationBbox(imagebox, (x, y), frameon=False, pad=0.0)
        ax.add_artist(ab)
        pos_images[node] = ab

    # Dibujar enlaces
    nx.draw_networkx_edges(G, pos, edge_color="gray", width=1, alpha=0.7)

    # Dibujar etiquetas
    labels = {node: nodes_info[node]["label"] if not nodes_info[node]["hidden"] else '' for node in pos}
    
    ax.set_title('Topología de Red')
    ax.axis('off')

    canvas.draw()

# Modificar la función update_router_image para cambiar la imagen de nodo directamente
def update_router_image(router_name, new_image_path):
    for node, imagebox in pos_images.items():
        if router_name == node:
            new_image = plt.imread(new_image_path)
            imagebox.get_children()[0].set_data(new_image)
            canvas.draw()
            break

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
