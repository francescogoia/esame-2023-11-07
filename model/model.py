import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._idMap = {}
        self._years = DAO.getYears()

    def getAllTeams(self, anno):
        self._teams = DAO.getAllTeams(anno)
        return self._teams

    def _creaGrafo(self, anno):
        self._nodes = self._teams
        self._grafo.add_nodes_from(self._nodes)
        for u in self._nodes:
            for v in self._nodes:
                if u != v:
                    peso = u.salarioSquadra + v.salarioSquadra
                    self._grafo.add_edge(u, v, weight=peso)
            self._idMap[u.ID] = u

    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def dettagli(self, nodo):
        vicini = self._grafo.neighbors(nodo)
        result = []
        for v in vicini:
            peso_arco = self._grafo[nodo][v]["weight"]
            result.append((v, peso_arco))
        result.sort(key=lambda x: x[1], reverse=True)
        return result

    def percorso(self, partenza):
        self._bestPath = []
        self._bestSol = 0
        if partenza == 2777:
            partenza = self._idMap[partenza]
            print(partenza)
            self._ricorsione(partenza, [])
            return self._bestPath, self._bestSol

        self._ricorsione(partenza, [])
        return self._bestPath, self._bestSol

    def _ricorsione(self, nodo, parziale):
        pesoParziale = self.getPesoParziale(parziale)
        if pesoParziale > self._bestSol:
            self._bestPath = copy.deepcopy(parziale)
            self._bestSol = pesoParziale

        vicini = self._grafo.neighbors(nodo)
        result = []
        for v in vicini:
            peso_arco = self._grafo[nodo][v]["weight"]
            result.append((nodo, v, peso_arco))
        result.sort(key=lambda x: x[2], reverse=True)  # ordino i vicini

        for a in result:            # a = nodo, vicino, peso
            if len(parziale) == 0:
                parziale.append((a[0], a[1], a[2]))
                self._ricorsione(a[1], parziale)
                parziale.pop()
            else:
                lastPeso = parziale[-1][2]
                if self.filtroNodi(a[1], parziale) and lastPeso > a[2]:
                    parziale.append((a[0], a[1], a[2]))
                    self._ricorsione(a[1], parziale)
                    parziale.pop()
                    return

    def filtroNodi(self, v, parziale):
        for a in parziale:
            if a[0] == v or a[1] == v:
                return False
        return True

    def filtroArchi(self, n, v, parziale):
        pass

    def getPesoParziale(self, parziale):
        totP = 0
        for a in parziale:
            totP += a[2]
        return totP
