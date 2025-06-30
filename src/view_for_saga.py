
import networkx as nx
from utils import (
    carregar_imagens_personagens,
    carregar_relacoes,
    carregar_imagem,
    construir_grafo_por_saga,
    imprimir_metricas,
    desenhar_grafo_com_imagens
)

PERSONAGENS_CSV = "data/personagens.csv"
RELACOES_CSV = "data/relacoes.csv"

def visualizar_saga(saga_nome):
    imagens_path = carregar_imagens_personagens(PERSONAGENS_CSV)
    relacoes = carregar_relacoes(RELACOES_CSV)

    G_saga = construir_grafo_por_saga(relacoes, saga_nome)
    imprimir_metricas(G_saga, f"Grafo Saga {saga_nome}")

    pos_saga = nx.spring_layout(G_saga, seed=42, k=5)
    imagens_saga = {}

    for node in G_saga.nodes():
        caminho_img = imagens_path.get(node)
        if caminho_img:
            img = carregar_imagem(caminho_img)
            if img:
                imagens_saga[node] = img

    nome_arquivo = f"grafo_saga_{saga_nome.lower().replace(' ', '_')}.png"
    desenhar_grafo_com_imagens(
        G_saga, pos_saga, imagens_saga,
        f"Grafo Saga {saga_nome}",
        nome_arquivo,
        saga=saga_nome
    )


