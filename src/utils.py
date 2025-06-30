import csv
import os
import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

FIGSIZE = (16, 9)

def desenhar_grafo_com_plotly(G, titulo="", nome_arquivo="grafo.html", boss_final_node=None):
    pos = nx.spring_layout(G, seed=42, k=0.5) 

    edge_traces = []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        color = 'green' if data['tipo'] == 'aliado' else 'red'
        width = max(1, data['peso'])
        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            line=dict(width=width, color=color),
            hoverinfo='text',
            mode='lines',
            text=f"{u} - {v} ({data['tipo']}, peso={data['peso']})",
            showlegend=False
        )
        edge_traces.append(edge_trace)

    node_x = []
    node_y = []
    node_text = []
    node_color = []
    node_size = []

    graus = dict(G.degree())

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        grau = graus.get(node, 1)
        node_size.append(20 + grau * 5)
        node_text.append(f"{node} (Grau: {grau})")
        node_color.append('red' if boss_final_node and node == boss_final_node else 'blue')

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        text=[node for node in G.nodes()],
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_color,
            size=node_size,
            line_width=2
        )
    )

    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        title=titulo,
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    fig.write_html(nome_arquivo)
    print(f"Arquivo HTML salvo: {nome_arquivo}")

def plotar_analise_metrica_grafo(G, saga):
    graus = dict(G.degree())
    centralidade = nx.betweenness_centrality(G)

    personagens = list(graus.keys())
    valores_grau = [graus[n] for n in personagens]
    valores_centralidade = [centralidade[n] for n in personagens]

    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Grau dos Nós", "Centralidade (Betweenness)"))

    fig.add_trace(
        go.Bar(x=personagens, y=valores_grau, name="Grau", marker_color='steelblue'),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=personagens, y=valores_centralidade, name="Centralidade", marker_color='darkorange'),
        row=1, col=2
    )

    fig.update_layout(
        title_text=f"Análise de Métricas - Saga {saga.capitalize()}",
        showlegend=False,
        height=500,
        width=1000,
        margin=dict(t=80)
    )

    output_path = os.path.join("outputs", f"analise_metricas_{saga.replace(' ', '_')}.html")
    fig.write_html(output_path)
    print(f"✅ Gráfico interativo salvo em: {output_path}")

def carregar_imagens_personagens(path):
    imagens_personagens = {}
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            imagens_personagens[row['nome']] = row['imagem']
    return imagens_personagens

def carregar_relacoes(path):
    relacoes = []
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            relacoes.append({
                "origem": row["origem"],
                "destino": row["destino"],
                "tipo": row["tipo"],
                "saga": row["saga"],
                "peso": int(row["peso"])
            })
    return relacoes

def carregar_imagem(caminho, zoom=0.25):
    try:
        imagem = Image.open(caminho)
        return OffsetImage(imagem, zoom=zoom)
    except FileNotFoundError:
        print(f"Imagem não encontrada: {caminho}")
        return None

def construir_grafo_por_saga(relacoes, saga_nome=None):
    G = nx.Graph()
    for r in relacoes:
        if saga_nome is None or r["saga"].lower() == saga_nome.lower():
            G.add_node(r["origem"])
            G.add_node(r["destino"])
            G.add_edge(
                r["origem"],
                r["destino"],
                tipo=r["tipo"],
                peso=r["peso"]
            )
    return G

def imprimir_metricas(G, nome_grafo):
    print(f"\nMétricas do grafo: {nome_grafo}")
    graus = dict(G.degree())
    print("Grau dos nós:")
    for k, v in graus.items():
        print(f"  {k}: {v}")

    centralidade = nx.betweenness_centrality(G)
    print("\nCentralidade (betweenness):")
    for k, v in centralidade.items():
        print(f"  {k}: {v:.3f}")

    componentes = nx.number_connected_components(G)
    print(f"\nComponentes conectados: {componentes}")

    if nx.is_connected(G):
        diametro = nx.diameter(G)
        print(f"Diâmetro da rede: {diametro}")
    else:
        print("Grafo desconexo, não tem diâmetro definido")

def desenhar_grafo_com_imagens(G, pos, imagens, titulo="", nome_arquivo="grafo.png", saga=None, boss_final_node=None):
    fig, ax = plt.subplots(figsize=FIGSIZE)

    if saga:
        saga_normalizada = saga.strip().lower()
        mapa_arquivo = None

        if "saiyajin" in saga_normalizada:
            mapa_arquivo = "mapaSaiyajin.png"
        elif "freeza" in saga_normalizada:
            mapa_arquivo = "mapaNamekZ.png"
        elif "cell" in saga_normalizada:
            mapa_arquivo = "arenaCell.png"
        elif "majin" in saga_normalizada:
            mapa_arquivo = "PlanetaSenhorKaioshin.png"

        if mapa_arquivo:
            caminho_mapa = os.path.join("imagens", "mapas", mapa_arquivo)
            if os.path.exists(caminho_mapa):
                try:
                    img = Image.open(caminho_mapa)
                    x_vals = [p[0] for p in pos.values()]
                    y_vals = [p[1] for p in pos.values()]
                    ax.imshow(img, extent=[min(x_vals)-1, max(x_vals)+1, min(y_vals)-1, max(y_vals)+1], aspect='auto', alpha=0.8)
                except Exception as e:
                    print(f"Erro ao carregar plano de fundo da saga {saga}: {e}")

    
    for u, v, data in G.edges(data=True):
        cor = 'green' if data['tipo'] == 'aliado' else 'red'
        largura = max(1, data['peso'])
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color=cor,
            linewidth=largura,
            alpha=0.7
        )

    graus = dict(G.degree())

    for node in G.nodes():
        zoom = 0.20 + (graus.get(node, 1) * 0.01) 

        if node in imagens:
            img_obj = carregar_imagem(imagens[node], zoom=zoom)
            if img_obj:
                ab = AnnotationBbox(img_obj, pos[node], frameon=False)
                ax.add_artist(ab)

                if boss_final_node and node == boss_final_node:
                    from matplotlib.patches import Circle
                    circle = Circle(pos[node], radius=0.15, edgecolor='red', facecolor='none', linewidth=2)
                    ax.add_patch(circle)

                ax.text(*pos[node], node, fontsize=6, ha='center', va='top', color='white', weight='bold',
                        bbox=dict(facecolor='black', alpha=0.5, boxstyle='round,pad=0.2'))
        else:
            ax.text(*pos[node], node, fontsize=8, ha='center', va='center', weight='bold')

    import matplotlib.patches as mpatches
    aliado_patch = mpatches.Patch(color='green', label='Aliado')
    inimigo_patch = mpatches.Patch(color='red', label='Inimigo')
    plt.legend(handles=[aliado_patch, inimigo_patch], loc='best')

    ax.set_title(titulo, fontsize=16)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(os.path.join("outputs", nome_arquivo))
    plt.show()



def dijkstra_aliados(G, origem):
    G_aliados = nx.Graph()
    for u, v, data in G.edges(data=True):
        if data['tipo'] == 'aliado':
            custo = 1 / data['peso'] if data['peso'] > 0 else 10
            G_aliados.add_edge(u, v, weight=custo)

    if origem not in G_aliados:
        print(f"Origem '{origem}' não está conectada por alianças nesta saga.")
        return

    caminhos = nx.single_source_dijkstra_path(G_aliados, origem)
    distancias = nx.single_source_dijkstra_path_length(G_aliados, origem)

    print(f"\nCaminhos de aliados mais fortes a partir de {origem}:")
    for destino in caminhos:
        if destino != origem:
            caminho = " -> ".join(caminhos[destino])
            print(f"  {destino}: {caminho} (Custo: {distancias[destino]:.2f})")

def dfs(G, origem):
    visitados = list(nx.dfs_preorder_nodes(G, source=origem))
    print(f"\nBusca em profundidade (DFS) a partir de {origem}:")
    print(" -> ".join(visitados))

def bfs(G, origem):
    visitados = list(nx.bfs_tree(G, source=origem))
    print(f"\nBusca em largura (BFS) a partir de {origem}:")
    print(" -> ".join(visitados))

def mst_kruskal_aliados(G):
    G_aliados = nx.Graph()
    for u, v, data in G.edges(data=True):
        if data['tipo'] == 'aliado':
            G_aliados.add_edge(u, v, weight=1 / data['peso'] if data['peso'] > 0 else 10)

    mst = nx.minimum_spanning_tree(G_aliados, algorithm='kruskal')
    print("\nÁrvore Geradora Mínima (Kruskal) com alianças:")
    for u, v, data in mst.edges(data=True):
        print(f"  {u} - {v} (peso: {1/data['weight']:.2f})")
