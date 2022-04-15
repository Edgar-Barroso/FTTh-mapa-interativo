import numbers
import os
import xml.etree.ElementTree as el
import simplekml.kml
import xmltodict
from geopy.distance import distance
from simplekml import *
import zipfile


class Ponto:
    def __init__(self, coordenada=None, nome='', descricao='', estilo='',estilokml=''):
        self._coordenada = coordenada
        self._nome = nome
        self._descricao = descricao
        self._estilo = estilo
        self._estilokml = estilokml

    @property
    def coordenada(self):
        return self._coordenada

    @coordenada.setter
    def coordenada(self, valor):
        if type(valor) is not list:
            raise ValueError('coordenada deve ser uma list')
        self._coordenada = valor

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
    def estilokml(self):
        return self._estilo

    @estilokml.setter
    def estilokml(self, valor):
        if type(valor) is not str:
            raise ValueError('estilo deve ser uma string')
        self._estilokml = valor


    @classmethod
    def extrair_pontos(cls, arq_name):
        lista = []
        if '.kmz' in arq_name:
            with zipfile.ZipFile(arq_name, 'r') as f:
                f.extract('doc.kml', 'TEMP')
                arq_name = 'TEMP\doc.kml'
        doc = el.parse(arq_name)
        root = doc.getroot()
        np = root.tag.split('}')[0] + '}'
        for c in root.iter(np + 'Placemark'):
            ponto = False
            pt = Ponto()
            for j in c:
                if j.tag == f'{np}name':
                    pt.nome = j.text
                elif j.tag == f'{np}description':
                    pt.descricao = j.text
                elif j.tag == f'{np}Point':
                    ponto = True
                    for q in j:
                        if q.tag == f'{np}coordinates':
                            pt.coordenada = [float(q.text.strip().split(',')[1]),float(q.text.strip().split(',')[0])]
                elif j.tag == f'{np}styleUrl':
                    pt.estilo = j.text
            if ponto is True:
                lista.append(pt)
        return lista

    def __sub__(self, other):
        return distance(self.coordenada, other.coordenada).meters


class Poste(Ponto):
    def __init__(self, tipo='', altura=0, tracao=0, rede='', casa=0, comercio=0, predio=0, \
                 equipamento='', codigo='', ocupante=0, img=''):
        super().__init__(coordenada=None, nome='', descricao='', estilo='')
        self._tipo =  tipo # 00
        self._altura = altura  # 01
        self._tracao = tracao  # 02
        self._rede = rede  # 03
        self._casa = casa  # 04
        self._comercio = comercio  # 05
        self._predio = predio  # 06
        self._equipamento = equipamento  # 07
        self._codigo = codigo  # 08
        self._ocupante = ocupante  # 09
        self._img = img  # imagem

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        if type(valor) is not str:
            raise ValueError('tipo deve ser uma string')
        self._tipo = valor

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, valor):
        if type(valor) is not int and type(valor) is not float:
            raise ValueError('tipo deve ser um numero float ou int')
        self._altura = float(valor)

    @property
    def tracao(self):
        return self._tracao

    @tracao.setter
    def tracao(self, valor):
        if type(valor) is not int:
            raise ValueError('tipo deve ser um numero int')
        self._tracao = int(valor)

    @property
    def rede(self):
        return self._rede

    @rede.setter
    def rede(self, valor):
        if type(valor) is not str:
            raise ValueError('tipo deve ser uma string')
        self._rede = valor

    @property
    def casa(self):
        return self._casa

    @casa.setter
    def casa(self, valor):
        if type(valor) is not int:
            raise ValueError('tipo deve ser um numero int')
        self._casa = int(valor)

    @property
    def comercio(self):
        return self._comercio

    @comercio.setter
    def comercio(self, valor):
        if type(valor) is not int:
            raise ValueError('tipo deve ser um numero int')
        self._comercio = int(valor)

    @property
    def predio(self):
        return self._predio

    @predio.setter
    def predio(self, valor):
        if type(valor) is not str:
            raise ValueError('tipo deve ser uma string ex: 2x3')
        self._predio = eval(valor.lower().replace('x', '*').replace(' ', '+'))

    @property
    def equipamento(self):
        return self._equipamento

    @equipamento.setter
    def equipamento(self, valor):
        if type(valor) is not str:
            raise ValueError('tipo deve ser uma string')
        self._equipamento = valor

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        if type(valor) is not str:
            raise ValueError('tipo deve ser uma string')
        self._codigo = valor

    @property
    def ocupante(self):
        return self._ocupante

    @ocupante.setter
    def ocupante(self, valor):
        if type(valor) is not int:
            raise ValueError('tipo deve ser um numero int')
        self._ocupante = int(valor)

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, valor):
        if type(valor) is not str:
            raise ValueError('tipo deve ser uma string')
        self._img = valor

    @classmethod
    def extrair_postes(cls, arq_name):
        lista = []
        if '.kmz' in arq_name:
            with zipfile.ZipFile(arq_name, 'r') as f:
                f.extract('doc.kml', 'TEMP')
                arq_name = 'TEMP\doc.kml'
        doc = el.parse(arq_name)
        root = doc.getroot()
        np = root.tag.split('}')[0] + '}'
        for c in root.iter(np + 'Placemark'):
            ponto = False
            pt = Poste()
            for j in c:

                if j.tag == f'{np}ExtendedData':
                    for t in j:
                        if t[0].text == '00.tipo':
                            try:
                                pt.tipo = t[1].text
                            except IndexError:
                                pass
                        elif t[0].text == '01.altura':
                            try:
                                pt.altura = float(t[1].text)
                            except IndexError:
                                pass
                        elif t[0].text == '02.esforco':
                            try:
                                pt.tracao = int(t[1].text)
                            except IndexError:
                                pass
                        elif t[0].text == '03.rede':
                            try:
                                pt.rede = t[1].text
                            except IndexError:
                                pass
                        elif t[0].text == '04.casa':
                            try:
                                pt.casa = int(t[1].text)
                            except IndexError:
                                pass
                        elif t[0].text == '05.comercio':
                            try:
                                pt.comercio = int(t[1].text)
                            except IndexError:
                                pass
                        elif t[0].text == '06.predio':
                            try:
                                pt.predio = t[1].text
                            except IndexError:
                                pass
                        elif t[0].text == '07.equipamento':
                            try:
                                pt.equipamento = t[1].text
                            except IndexError:
                                pass
                        elif t[0].text == '08.codigo':
                            try:
                                pt.codigo = t[1].text
                            except IndexError:
                                pass
                        elif t[0].text == '09.ocupante':
                            try:
                                pt.ocupante = int(t[1].text)
                            except IndexError:
                                pass
                        elif t.attrib["name"] == 'pictures':
                            try:
                                pt.img = str(t[0].text)
                            except IndexError:
                                pass
                elif j.tag == f'{np}name':
                    pt.nome = j.text
                elif j.tag == f'{np}description':
                    pt.descricao = j.text
                elif j.tag == f'{np}Point':
                    ponto = True
                    for q in j:
                        if q.tag == f'{np}coordinates':
                            pt.coordenada = [float(q.text.strip().split(',')[1]), float(q.text.strip().split(',')[0])]
                elif j.tag == f'{np}styleUrl':
                    pt.estilo = j.text
            if ponto is True:
                lista.append(pt)
        return lista


if __name__ == '__main__':
    kmz = simplekml.Kml()
    postes = Poste.extrair_postes('postes.kmz')
    pontos = Ponto.extrair_pontos('pontos.kmz')
    for ponto in pontos:
        for poste in postes:

            if (poste-ponto) < 1:

                poste.img = poste.img.replace('<br/><img src="','').replace('"/>','')
                kmz.addfile(f'TEMP/{poste.img}')
                pnt = kmz.newpoint(coords=[[poste.coordenada[1], poste.coordenada[0]]])
                pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_square.png'
                pnt.extendeddata.newdata(name='00.tipo', value=poste.tipo, displayname="00.tipo")
                pnt.extendeddata.newdata(name='01.altura', value=poste.altura, displayname="01.altura")
                pnt.extendeddata.newdata(name='02.esforco', value=poste.tracao, displayname="02.esforco")
                pnt.extendeddata.newdata(name='03.rede', value=poste.rede, displayname="03.rede")
                pnt.extendeddata.newdata(name='04.casa', value=poste.casa, displayname="04.casa")
                pnt.extendeddata.newdata(name='05.comercio', value=poste.comercio, displayname="05.comercio")
                pnt.extendeddata.newdata(name='06.predio', value=poste.predio, displayname="06.predio")
                pnt.extendeddata.newdata(name='07.equipamento', value=poste.equipamento, displayname="07.equipamento")
                pnt.extendeddata.newdata(name='08.codigo', value=poste.codigo, displayname="08.codigo")
                pnt.extendeddata.newdata(name='09.ocupante', value=poste.ocupante, displayname="09.ocupante")
                pnt.extendeddata.newdata(name='pictures', value=f'<![CDATA[<br/><img src="{poste.img}"/>]]>')
    kmz.savekmz('Obs/Tratados.kmz',format = False)