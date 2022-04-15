import xmltodict
from geopy.distance import distance
from simplekml import *
import zipfile
import math
from ponto import Ponto

class Caminho:
    def __init__(self, coordenadas=None, nome='', descricao='', estilo=''):
        self._coordenadas = coordenadas
        self._nome = nome
        self._descricao = descricao
        self._estilo = estilo

    @property
    def coordenadas(self):
        return self._coordenadas

    @coordenadas.setter
    def coordenadas(self, valor):
        if type(valor) is not list:
            raise ValueError('coordenadas deve ser uma list')
        self._coordenadas = valor

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if type(valor) is not str:
            raise ValueError('nome deve ser uma string')
        self._nome = valor

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        if type(valor) is not str:
            raise ValueError('descrição deve ser uma string')
        self._descricao = valor

    @property
    def estilo(self):
        return self._estilo

    @estilo.setter
    def estilo(self, valor):
        if type(valor) is not str:
            raise ValueError('estilo deve ser uma string')
        self._estilo = valor

    @property
    def metragem(self):
        total = 0.0
        for n, coord in enumerate(self.coordenadas):
            if n > 0:
                total += distance(coord, self.coordenadas[n - 1]).meters
            else:
                continue
        return total


    def ancoragens(self,ang_aceitavel):
        pontos = []
        for n, coordenada in enumerate(self.coordenadas):
            if n > 0:
                coord1 = self.coordenadas[n-1]
                coord2 = coordenada
                if distance(coord1,coord2).meters > 3:
                    lat1 = float(coord1[0])
                    lat2 = float(coord2[0])
                    long1 = float(coord1[1])
                    long2 = float(coord2[1])
                    hipotenusa = distance((lat1, long1), (lat2, long2)).meters
                    catetoad = distance((lat1, long2), (lat1, long1)).meters
                    catetoop = math.sqrt((hipotenusa ** 2) - (catetoad ** 2))
                    seno = catetoop / hipotenusa
                    cos = catetoad / hipotenusa
                    if long1 <= long2:
                        if lat1 <= lat2:
                            tipo = 1
                        else:
                            tipo = 2
                    else:
                        if lat1 <= lat2:
                            tipo = 3
                        else:
                            tipo = 4
                    ang = (round(math.degrees(math.asin(round(seno, 2))), 2))
                    if tipo == 2:
                        ang = 360-ang
                    elif tipo == 4:
                        ang = ang+180
                    elif tipo == 3:
                        ang = 180-ang
                    p = Ponto()
                    p.coordenada = [lat1,long1]
                    if abs(ang-ang_ant) <= ang_aceitavel:
                        p.nome = 'passagem'
                    elif abs(ang-ang_ant) > ang_aceitavel:
                        p.nome = 'ancoragem'
                    pontos.append(p)
                    tipoant = tipo
                    seno_anterior = seno
                    cos_anterior = cos
                    ang_ant=ang
            else:
                tipoant = 0
                tipo = 0
                seno_anterior = 0
                cos_anterior = 0
                seno = 0
                ang_ant = 0
                cos = 0
                p = Ponto()
                p.coordenada = self.coordenadas[-1]
                p.nome = 'ancoragem'
                pontos.append(p)

        return pontos

    @classmethod
    def extrair_caminhos(cls, arq_name):
        """
        :param arq: kml a ser tratado
        :return: lista de objetos
        """
        if '.kmz' in arq_name:
            with zipfile.ZipFile(arq_name, 'r') as f:
                f.extract('doc.kml', 'TEMP')
                arq_name = 'TEMP\doc.kml'
        with open(f'{arq_name}', 'r+') as f:
            arq = f.read()
        arq = arq.replace('<Folder>', '').replace('</Folder>', '')
        arq = arq.replace('<Document>', '').replace('</Document>', '')
        lista = []
        arq = xmltodict.parse(arq)
        dicionario = arq['kml']['Placemark']
        for place in dicionario:
            try:
                coordenadas_texto = place['LineString']['coordinates']
                coordenadas_float = []
                for coordenada in coordenadas_texto.split():
                    coordenada = [float(coordenada.split(',')[1]), float(coordenada.split(',')[0])]
                    coordenadas_float.append(coordenada)
                try:
                    nome = place['name']
                except KeyError:
                    nome = ''
                try:
                    descricao = place['description']
                except KeyError:
                    descricao = ''
                try:
                    estilo = place['styleUrl']
                except KeyError:
                    estilo = ''
                pt = Caminho()
                pt.coordenadas = coordenadas_float
                pt.nome = nome
                pt.descricao = descricao
                pt.estilo = estilo
                lista.append(pt)
            except KeyError:
                continue
        return lista







if __name__ == '__main__':
    pass
