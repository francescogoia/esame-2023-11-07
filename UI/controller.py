import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def fillDDAnno(self):
        years = self._model._years
        for y in years:
            y = int(y)
            self._view._ddAnno.options.append(ft.dropdown.Option(data=y, text=str(y), on_click=self._selectYear))
        self._view.update_page()

    def _selectYear(self, e):
        if e.control.data is None:
            self._choice_anno = None
        else:
            self._choice_anno = e.control.data
        self.fill_squadre(self._choice_anno)
        self._view._ddSquadre.disabled = False
        self._view.update_page()

    def fill_squadre(self, anno):
        teams = self._model.getAllTeams(anno)
        for t in teams:
            self._view.txtSquadre.controls.append(ft.Text(t))
            self._view._ddSquadre.options.append(ft.dropdown.Option(data=t, text=t, on_click=self._selectTeam))
        self._view.update_page()

    def _selectTeam(self, e):
        if e.control.data is None:
            self._choice_team = None
        else:
            self._choice_team = e.control.data

    def handle_graph(self, e):
        self._model._creaGrafo(self._choice_anno)
        nNodi, nArchi = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato.\n"
                                                       f"Il grafo ha {nNodi} nodi e {nArchi} archi."))
        self._view._btnAnalisi.disabled = False
        self._view._btnPercorso.disabled = False
        self._view.update_page()

    def handle_dettagli(self, e):
        adiacenti = self._model.dettagli(self._choice_team)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Adiacenti della squadra {self._choice_team}:"))
        for a in adiacenti:
            self._view.txt_result1.controls.append(ft.Text(f"{a[0]} --> {a[1]}"))
        self._view.update_page()


    def handle_percorso(self, e):
        path, weight = self._model.percorso(self._choice_team)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text(f"Trovato percorso di peso {weight}:"))
        for a in path:
            self._view.txt_result1.controls.append(ft.Text(f"{a[0]} --> {a[1]}: {a[2]}"))
        self._view.update_page()



