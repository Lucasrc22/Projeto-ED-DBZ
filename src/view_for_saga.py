import os
import webbrowser
from utils import (
    carregar_relacoes,
    construir_grafo_por_saga,
    desenhar_grafo_com_plotly
)

RELACOES_CSV = "data/relacoes.csv"
OUTPUT_DIR = "outputs/"

def visualizar_saga_com_plotly(saga_nome):
    relacoes = carregar_relacoes(RELACOES_CSV)
    G_saga = construir_grafo_por_saga(relacoes, saga_nome)

    nome_arquivo = os.path.join(
        OUTPUT_DIR, f"grafo_saga_{saga_nome.lower().replace(' ', '_')}.html"
    )
    
    boss_finais = {
        "saiyajin": "Vegeta (saga Saiyajin)",
        "freeza": "Freeza",
        "cell": "Cell",
        "majin buu": "Majin Buu"
    }

    chefe = boss_finais.get(saga_nome.lower())

    desenhar_grafo_com_plotly(
        G_saga,
        titulo=f"Grafo Saga {saga_nome.capitalize()}",
        nome_arquivo=nome_arquivo,
        boss_final_node=chefe
    )

    print(f"🌐 Abrindo visualização no navegador: {nome_arquivo}")
    webbrowser.open(f"file://{os.path.abspath(nome_arquivo)}")

if __name__ == "__main__":
    todas_sagas = ["saiyajin", "freeza", "cell", "majin buu"]
    for saga in todas_sagas:
        print(f"🔍 Gerando visualização interativa da saga: {saga.capitalize()}")
        visualizar_saga_com_plotly(saga)
