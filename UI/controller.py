import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        listaVoti=self._model.getAllVoti()
        for v in listaVoti:
            self._view._ddrating1.options.append(ft.dropdown.Option(v))
            self._view._ddrating2.options.append(ft.dropdown.Option(v))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._model.buildGraph(self._view._ddrating1.value, self._view._ddrating2.value)
        n, a = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato. "
                                                      f"Il grafo contiene {n} nodi e {a} archi."))
        self._view.txt_result.controls.append(ft.Text(f"I 5 archi maggiori sono:"))
        archiMaggiori=self._model.getTop5Archi()
        for arco in archiMaggiori:
            self._view.txt_result.controls.append(ft.Text(f"{arco[0]} - {arco[1]} - {arco[2]['weight']}"))

        lun, nodi=self._model.getConnessaInfo()
        self._view.txt_result.controls.append(ft.Text(f"Le componenti connesse sono {lun}"))
        self._view.txt_result.controls.append(ft.Text(f"La componente più grande ha {len(nodi)} nodi"))
        for n in nodi:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

    def handleCammino(self, e):
        pass