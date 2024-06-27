import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}


    def _creaGrafo(self, brand, anno):
        pass

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def archiPesanti(self):
        pass

    def percorso(self, partenza):
        pass

    def _ricorsione(self, nodo, parziale):
        pass

    def filtroNodi(self, v, parziale):      # no percorso semplice, non serve
        pass

    def filtroArchi(self, n, v, parziale):
        pass
