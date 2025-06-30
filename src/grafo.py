from utils import (
    carregar_imagens_personagens, carregar_relacoes,
    construir_grafo_por_saga, imprimir_metricas,
    desenhar_grafo_com_imagens, desenhar_grafo_com_plotly,
    plotar_analise_metrica_grafo,
    bfs, dfs, dijkstra_aliados
)
import os
import networkx as nx

PERSONAGENS_CSV = "data/personagens.csv"
RELACOES_CSV = "data/relacoes.csv"
OUTPUT_DIR = "outputs/"

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    imagens_path = carregar_imagens_personagens(PERSONAGENS_CSV)
    relacoes = carregar_relacoes(RELACOES_CSV)

    chefes_finais = {
        "saiyajin": "Vegeta (saga Saiyajin)",
        "freeza": "Freeza",
        "cell": "Cell",
        "majin buu": "Majin Buu"
    }

    ordem_cronologica_sagas = ["saiyajin", "freeza", "cell", "majin buu"]
    sagas_presentes = set(r['saga'].lower() for r in relacoes)

    for saga in ordem_cronologica_sagas:
        if saga not in sagas_presentes:
            continue

        G_saga = construir_grafo_por_saga(relacoes, saga)
        imprimir_metricas(G_saga, f"Grafo Saga {saga.capitalize()}")

        origem_busca = "Goku"
        if origem_busca in G_saga.nodes():
            print(f"\nBFS a partir de {origem_busca} na saga {saga}:")
            bfs(G_saga, origem_busca)

            print(f"\nDFS a partir de {origem_busca} na saga {saga}:")
            dfs(G_saga, origem_busca)

            print(f"\nDijkstra (alianças) a partir de {origem_busca} na saga {saga}:")
            dijkstra_aliados(G_saga, origem_busca)

        chefe = None
        for chave in chefes_finais.keys():
            if chave in saga:
                chefe = chefes_finais[chave]
                break

        if chefe and chefe in G_saga.nodes():
            pos_init = {chefe: [0, 0]}
            pos_saga = nx.spring_layout(G_saga, seed=42, k=2.0, fixed=[chefe], pos=pos_init)
        else:
            pos_saga = nx.spring_layout(G_saga, seed=42, k=2.0)

        imagens_saga = {}
        for node in G_saga.nodes():
            caminho_img = imagens_path.get(node)
            if caminho_img and os.path.exists(caminho_img):
                imagens_saga[node] = caminho_img

        nome_arquivo_img = f"grafo_saga_{saga.replace(' ', '_')}.png"
        desenhar_grafo_com_imagens(
            G_saga, pos_saga, imagens_saga,
            f"Grafo Saga {saga.capitalize()}",
            nome_arquivo_img,
            saga=saga,
            boss_final_node=chefe
        )

        nome_arquivo_html = os.path.join(OUTPUT_DIR, f"grafo_saga_{saga.replace(' ', '_')}.html")
        desenhar_grafo_com_plotly(
            G_saga,
            titulo=f"Grafo Saga {saga.capitalize()}",
            nome_arquivo=nome_arquivo_html,
            boss_final_node=chefe
        )

        plotar_analise_metrica_grafo(G_saga, saga)

if __name__ == "__main__":
    main()