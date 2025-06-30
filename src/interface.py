import sys
import os
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

OUTPUT_DIR = "outputs"

SAGAS_HTML = {
    "Saga Saiyajin": "grafo_saga_saiyajin.html",
    "Saga Freeza": "grafo_saga_freeza.html",
    "Saga Cell": "grafo_saga_cell.html",
    "Saga Majin Buu": "grafo_saga_majin_buu.html",
}

class GrafoDBZApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visualizador de Grafos - Dragon Ball Z")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()
        label = QLabel("Clique em uma saga para visualizar seu grafo interativo:")
        layout.addWidget(label)

        botoes_layout = QHBoxLayout()
        for saga, filename in SAGAS_HTML.items():
            botao = QPushButton(saga)
            botao.clicked.connect(lambda _, f=filename: self.abrir_html(f))
            botoes_layout.addWidget(botao)

        layout.addLayout(botoes_layout)
        self.setLayout(layout)

    def abrir_html(self, filename):
        caminho_completo = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(caminho_completo):
            webbrowser.open(f"file://{os.path.abspath(caminho_completo)}")
        else:
            print(f"Arquivo HTML não encontrado: {caminho_completo}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = GrafoDBZApp()
    janela.show()
    sys.exit(app.exec_())
