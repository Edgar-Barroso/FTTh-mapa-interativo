import sys
import io
import time

import folium  # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
    QWidget, QGridLayout, QLineEdit, QSizePolicy, QLabel
from PyQt5 import QtGui
from ponto import Ponto
from caminho import Caminho
import shutil
import os
import zipfile

postes = Ponto.extrair_pontos('setortest.kmz')
caminhos = Caminho.extrair_caminhos('setortest.kmz')


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 800, 600
        self.setMinimumSize(self.window_width, self.window_height)
        layout = QVBoxLayout()
        self.setLayout(layout)
        coordinate = (postes[0].coordenada)
        m = folium.Map(
            tiles='OpenStreetMap',
            zoom_start=300,
            location=coordinate
        )
        for c in postes:
            folium.Marker(
                    location=c.coordenada,
                    popup=f'{c.nome}').add_to(m)

        for c in caminhos:
            folium.PolyLine(
                c.coordenadas
            ).add_to(m)
        # save map data to data object

        data = io.BytesIO()
        m.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
