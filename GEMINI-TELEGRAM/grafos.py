import networkx as nx
import matplotlib.pyplot as plt

# Función para crear un grafo
def create_graph():
    return nx.DiGraph()

# Función para agregar una relación al grafo
def add_relation(graph, subject, predicate, obj):
    graph.add_edge(subject, obj, label=predicate)


# Función para modificar una relación en el grafo
def modify_relation(graph, old_relation, new_relation):
    if graph.has_edge(*old_relation):
        graph.remove_edge(*old_relation)
    add_relation(graph,new_relation[0],new_relation[1],new_relation[2])

# Función para cargar datos desde un archivo
def load_data(graph, file_path, file_format):
    if file_format == 'adjlist':
        graph = nx.read_adjlist(file_path)
    elif file_format == 'edgelist':
        graph = nx.read_edgelist(file_path)
    else:
        raise ValueError("Formato de archivo no compatible")

# Función para guardar datos en un archivo
def save_data(graph, file_path, file_format):
    if file_format == 'adjlist':
        nx.write_adjlist(graph, file_path)
    elif file_format == 'edgelist':
        nx.write_edgelist(graph, file_path)
    else:
        raise ValueError("Formato de archivo no compatible")
    

# Función para representar gráficamente un grafo
def plot_graph(graph):
    pos = nx.spring_layout(graph)  # Calcula la posición de los nodos
    nx.draw(graph, pos, with_labels=True, node_size=5000, node_color="skyblue", font_size=10)  # Dibuja el grafo
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)  # Añade etiquetas a las aristas
    plt.show()



# Ejemplo de uso

# Creamos un grafo
g = create_graph()

# Agregamos relaciones al grafo
add_relation(g, "Marta", "es hija de", "Cristina")
add_relation(g, "Cristina", "es hija de", "Jesus")


plot_graph(g)