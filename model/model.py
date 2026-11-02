import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapActors = {}
        self._actors = []

    def buildGraph(self, voto1, voto2):
        self._graph.clear()
        self._actors = []
        self._actors=DAO.getAllNodes(voto1, voto2)

        for a in self._actors:
            self._idMapActors[a.id] = a

        self._graph.add_nodes_from(self._actors)

        allEdges = DAO.getAllEdges(voto1, voto2,self._idMapActors)
        for e in allEdges:
            self._graph.add_edge(e.Actor1, e.Actor2, weight=e.Peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    #il numero delle componenti connesse e la componente connessa maggiore.
    def getConnessaInfo(self):
        components = list(nx.connected_components(self._graph))
        largest = max(components, key=len)
        subgraph = self._graph.subgraph(largest).copy()
        nodi=[]
        for n in subgraph.nodes:
            nodi.append(n)
        return len(components), nodi

    def getTop5Archi(self):
        return sorted(self._graph.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getAllVoti(self):
        return DAO.getAllVoti()