


import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import time



# Base directory containing the APAD transportation datasets.
cartella = "C:/Users/marti/OneDrive/Desktop/Programmazione/Progetto/transportation"




def create_graph(c):
    """Create the directed and temporal transport graphs for one city.

    The function reads the node and temporal-connection CSV files and returns
    the graph, the stop-name mapping, the static edge list, stop coordinates,
    and temporal edges in the form (origin, destination, departure, duration).
    """
    
    temporal="temporal_day"
    
    
    
    G= nx.DiGraph() 
    diz_id = {} 
    tupla_edges = [] 
    diz_id_pos = {}  
    tupla_edges_temporal=[] 
    
    
    temporal_file = cartella+"/APADproject/"+c+"/network_"+temporal+".csv"
    nodi_file = cartella+"/APADproject/"+c+"/network_nodes.csv"
    
    
    nodi = pd.read_csv(nodi_file, sep=";", on_bad_lines='skip')

    
    for i in range(len(nodi)):
        
        stop_id = nodi.loc[i, 'stop_I'] 
        nome = nodi.loc[i, 'name'] 
        
        lat=nodi.loc[i,"lat"] 
        lon=nodi.loc[i,"lon"] 
        diz_id_pos[stop_id] = (lon, lat) 
        
        
        if stop_id not in diz_id:
            diz_id[stop_id] = nome

        
        G.add_node(stop_id)
       

    
    temporal = pd.read_csv(temporal_file, sep=";", on_bad_lines='skip')

    for i in range(len(temporal)):
        
        start = temporal.loc[i, 'from_stop_I'] 
        end = temporal.loc[i, 'to_stop_I'] 
        tupla_edges.append((start, end))  
        
        t_start=temporal.loc[i,'dep_time_ut'] 
        t_end=temporal.loc[i,'arr_time_ut'] 
        
        lambd=t_end-t_start 
        
        tupla_edges_temporal.append((start, end, t_start, lambd)) 
        
        
        G.add_edge(start, end)
        

    return G, diz_id, tupla_edges, diz_id_pos, tupla_edges_temporal


# Cities included in the analysis.
city = [
    "adelaide", "belfast", "berlin", "bordeaux", "brisbane", "canberra",
    "detroit", "dublin", "grenoble", "helsinki", "kuopio", "lisbon",
    "luxembourg", "melbourne", "nantes", "palermo", "paris", "prague",
    "rennes", "rome", "sydney", "toulouse", "turku", "venice", "winnipeg"
]





# Global dictionaries indexed by city.
grafo = {} 
dizionari_id = {} 
diz_edges={} 
diz_pos={} 
diz_edges_temporal={} 



start_time=time.time()

for c in city:
    
    
    G, diz_id, tupla_edges, diz_id_pos, tupla_edges_temporal = create_graph(c)
    
    
    grafo[c] = G 
    dizionari_id[c] = diz_id  
    diz_edges[c]=tupla_edges 
    diz_pos[c]=diz_id_pos 
    diz_edges_temporal[c]=tupla_edges_temporal 
   
    

end_time = time.time()

tot_time = (end_time - start_time) / 60
minuti = int(tot_time)
secondi = round((tot_time - minuti) * 60,4)
print("Elapsed time:", minuti, "minutes and", secondi, "seconds")



c = "canberra"
grafo_city = grafo[c]
print("Nodes:", len(grafo_city))
print("Connections:", grafo_city.number_of_edges())


pos_city = diz_pos[c]  


plt.figure(figsize=(20, 20))
nx.draw(grafo_city, pos=pos_city, with_labels=False, node_size=10, arrows=False)
plt.title("Complete Canberra Transport Network - Daily File")
plt.show()





  
def question_1(grafo, dizionari_id, diz_edges, city):
    """Return the ten stops with the largest number of departures per city.

    Complexity: O(C * (n + m)), where C is the number of cities, n the number
    of stops, and m the number of temporal connections.
    """
    risultato = {}
    
    for c in city: 
        
        diz_id = dizionari_id[c] 
        edges=diz_edges[c] 
        partenze = {} 

        
        for i, arrivo in edges: 
            
            if i not in partenze:
                partenze[i] = 0 
            partenze[i] += 1 

        
        partenze_lista = list(partenze.items()) 

        risultato_lista = []
        
       
       
        for j in range(10): 
            max_id = 0 
            
            
            
            for i in range(1, len(partenze_lista)): 
                
                
                if partenze_lista[i][1] > partenze_lista[max_id][1]:
                    max_id = i 
            
            risultato_lista.append(partenze_lista[max_id])
            
            partenze_lista.pop(max_id)

        
        
        
        top10_nomi = [(diz_id[nodo], count) for nodo, count in risultato_lista] 
        
        
        risultato[c] = top10_nomi 

    return risultato



start_time = time.time()  
risultato = question_1(grafo, dizionari_id, diz_edges, city)


for c in city: 
    print("")
    print(c.upper(), ": TOP 10 STOPS BY NUMBER OF DEPARTURES:")
    
    for nome, num in risultato[c]:
        print(nome, num, ": departures")
      
end_time = time.time()  

tot_time = (end_time - start_time) / 60
minuti = int(tot_time)
secondi = round((tot_time - minuti) * 60,4)
print("")
print("Elapsed time:", minuti, "minutes and", secondi, "seconds")




def question_2(grafo, diz_id):
    """Return the ten nodes with the highest out-degree for each city.

    The resulting nodes are subsequently used in Questions 3 and 5.
    Complexity: O(C * n).
    """

    diz_top10={} 

    for c in city: 
        
        G = grafo[c] 
        
        
        list_degree = list(G.out_degree())
        
        top10_degree = []
        
        for j in range(10): 
            
            max_degree = 0  

            for i in range(1, len(list_degree)): 
                
                if list_degree[i][1] > list_degree[max_degree][1]:
                    
                    max_degree= i 
                    
            
            top10_degree.append(list_degree[max_degree])
            
            list_degree.pop(max_degree)

        diz_top10[c] = top10_degree 

    return diz_top10  

start_time = time.time() 

diz_top10 = question_2(grafo, dizionari_id)

for c in diz_top10:
    print("")
    print(c.upper(), "TOP 10 NODES BY OUT-DEGREE:")
    
    for nodo, grado in diz_top10[c]:
        nome = dizionari_id[c].get(nodo)
        print(nome, "ID:", nodo, "degree:", grado)
 
end_time = time.time()  
tot_time = (end_time - start_time) / 60
minuti = int(tot_time)
secondi = round((tot_time - minuti) * 60,4)
print("")
print("Elapsed time:", minuti, "minutes and", secondi, "seconds")



def eccentricity_bfs(G, nodo_x):
    """Compute a node's eccentricity using breadth-first search."""
    
    lengths = nx.single_source_shortest_path_length(G, nodo_x) 
    return max(lengths.values()) 

def iFUB(G, u): 
    """Compute the exact diameter using iterative fringe upper bounds."""
    
    i = eccentricity_bfs(G, u) 
    lb = eccentricity_bfs(G, u) 
    ub = 2 * eccentricity_bfs(G, u) 
    
    diz_u= nx.single_source_shortest_path_length(G, u) 
    diz_bfs_u = {} 
    for v, d in diz_u.items(): 
        if d not in diz_bfs_u:
            diz_bfs_u[d] = [] 
        diz_bfs_u[d].append(v) 
    while ub > lb:  
        Bi = diz_bfs_u.get(i, [])  
        Bi_u = 0 
        
        for v in Bi: 
            ecc_v = eccentricity_bfs(G, v) 
            
            Bi_u = max(Bi_u, ecc_v)

        if Bi_u > 2 * (i - 1):
            return Bi_u 
        else: 
            lb=max(Bi_u, lb)
            ub=2*(i-1)
        i -= 1 
    return lb



start_time = time.time()

# QUESTION 3 - Exact diameter of the largest connected component.
for c in city:
    print("City: " + c)

    G_dir = grafo[c]
    G = G_dir.to_undirected()

    
    componenti = list(nx.connected_components(G))
    Cmax = max(componenti, key=len)
    sottografo = G.subgraph(Cmax)

    top_nodi = diz_top10.get(c, [])  

    for nodo, grado in top_nodi:
        nodo = int(nodo)
        if nodo in sottografo.nodes: 
            r = nodo 
            break

    
    a = nx.single_source_shortest_path_length(sottografo, r) 
    a_max = max(a, key=a.get) 

    b = nx.single_source_shortest_path_length(sottografo, a_max) 
    b_max = max(b, key=b.get) 
    
    dist= nx.shortest_path(sottografo, a_max, b_max) 

    nodo_start = dist[len(dist) // 2]     

    diam_ifub = iFUB(sottografo, nodo_start) 
    
    
    print("Selected starting node:", nodo_start, dizionari_id[c].get(nodo_start))
    print("Diameter (iFUB):", diam_ifub)
    print("Nodes in the main component:", len(sottografo))



end_time = time.time()
tot_time = (end_time - start_time) / 60
minuti = int(tot_time)
secondi = round((tot_time - minuti) * 60, 4)
print("\nElapsed time:", minuti, "minutes and", secondi, "seconds")





def question_4(grafo, diz_edges, file_type, intervallo_ore=1):
    """Analyze temporal traffic volumes and runtime for every city.

    Departures are aggregated into hourly intervals and plotted over time.
    A final scatter plot compares graph size with execution time.
    Complexity: O(C * (n + r + k log k)).
    """
    n_conn_list = [] 
    time_list = [] 
    for c in city:
        start_time = time.time() 
        
        nodi=grafo[c]
        archi=diz_edges[c]
        
        
        n_location=len(nodi) 
        n_connessioni = len(archi) 
        
        
        temporal_file = cartella+"/APADproject/"+c+"/network_temporal_"+file_type+".csv"
        df = pd.read_csv(temporal_file, sep=";", usecols=["dep_time_ut"], on_bad_lines='skip') 

        
        df["datetime"] = pd.to_datetime(df["dep_time_ut"], unit="s")
        frequenza = str(intervallo_ore) + "h" 
        df["fascia_oraria"] = df["datetime"].dt.floor(frequenza) 

        
        
        conteggio = df["fascia_oraria"].value_counts().sort_index() 
        x = conteggio.index 
        y = conteggio.values 

        
        plt.figure(figsize=(12, 5)) 
        plt.plot(x, y, color='blue', linestyle='-', marker='o')
        plt.xlabel("One-hour time interval")
        plt.ylabel("Number of edges (connections)")
        plt.title("City: " + c)
        plt.grid(True) 
        plt.show() 
        
        end_time = time.time() 
        tempo_impiegato = round(end_time - start_time,4) 
        
        
        print("City:", c.upper(), "Temporal file analyzed:", file_type)
        print("Unique locations:", n_location)
        print("Direct connections:", n_connessioni)
        print("Response time:", tempo_impiegato, "seconds")

        n_conn_list.append(n_connessioni)
        time_list.append(tempo_impiegato)

    
    plt.figure(figsize=(10, 5))
    plt.scatter(n_conn_list, time_list, c='pink', label='vs Connections')
    plt.xlabel("Number of edges")
    plt.ylabel("Execution time (s)")
    plt.title("Execution Time vs Graph Size - " + file_type + " File")
    plt.legend() 
    plt.tight_layout() 
    plt.show()



question_4(grafo, diz_edges, file_type="day", intervallo_ore=1)








def earliest_arrival_time(city, diz_edges_temporal, nodo_x, t_alpha, t_omega):
    """Calculate the earliest feasible arrival time at every reachable stop.

    A connection can be used only after reaching its origin, and its arrival
    time must not exceed the upper limit ``t_omega``.
    """

    t_arrivo = {} 

    
    for u, v, start_time, lambd in diz_edges_temporal[city]: 
        if u not in t_arrivo:
            t_arrivo[u] = float("inf")
        if v not in t_arrivo:
            t_arrivo[v] = float("inf")

    t_arrivo[nodo_x] = t_alpha 
    
    edges = sorted(diz_edges_temporal[city], key=lambda x: x[2])  

    
    
    for u, v, start_time, lambd in edges: 
        
        
        
        if start_time+lambd <= t_omega and start_time >= t_arrivo.get(u): 
                
                
                if start_time+lambd < t_arrivo.get(v): 
                    
                    
                    
                    t_arrivo[v] = start_time+lambd 
               
    return t_arrivo 

def question_5(grafo, diz_edges_temporal, top10_nodi):
    """Count stops reachable within 30 minutes, one hour, and two hours."""
    for c in city: 
        print("CITY:", c.upper())
        
        edges_temporal = diz_edges_temporal[c]

        
        for nodo_x, grado in top10_nodi[c]:  
            
            
            partenze = [e for e in edges_temporal if e[0] == nodo_x] 

            
            t_alpha = min(e[2] for e in partenze) 
            
            t_omega = t_alpha + 7200  
            tempi_arrivo = earliest_arrival_time(c, diz_edges_temporal, nodo_x, t_alpha, t_omega) 
            
            entro_30min = 0
            entro_1h = 0
            entro_2h = 0
            for t in tempi_arrivo.values():
                if t <= t_alpha + 1800: 
                    entro_30min += 1
                if t <= t_alpha + 3600: 
                    entro_1h += 1
                if t <= t_alpha + 7200: 
                    entro_2h += 1
           
            print("Node:", nodo_x, "30 min:", entro_30min,
                  "1 hour:", entro_1h, "2 hours:", entro_2h)



start_time = time.time()  

question_5(grafo, diz_edges_temporal, diz_top10)

end_time = time.time()  

tot_time = (end_time - start_time) / 60
minuti = int(tot_time)
secondi = round((tot_time - minuti) * 60,4)
print("Elapsed time:", minuti, "minutes and", secondi, "seconds")
    
