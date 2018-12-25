import ujson


class Mermaid:

    def __init__(self, path):

        self.graph_type = "graph TD;"
        self.tables_flow = []
        self.functions_flow = []

        with open(path, 'r') as file:
            self.results = ujson.loads(file.read())

        self.tables_relations()
        self.functions_relations()

    def tables_relations(self):

        for p in self.results:
            for q in self.results[p]['queries']:
                if q['from_table']:
                    for t in q['from_table']:
                        arrow = f"{t['name']}-->|{q['procedure']}|{q['target_table']['name']};"
                        if arrow not in self.tables_flow:
                            self.tables_flow.append(arrow)

        self.tables_flow = list(set(self.tables_flow))
        self.tables_flow.insert(0, self.graph_type)
        self.tables_flow = '\n'.join(self.tables_flow)

    def functions_relations(self):

        for p in self.results:
            self.functions_flow.append(f"{self.results[p]['name']}(({self.results[p]['name']}));")
            for q in self.results[p]['queries']:
                if q['target_table']:
                    arrow = f"{self.results[p]['name']}-->|{q['operation']}|{q['target_table']};"
                    if arrow not in self.functions_flow:
                        self.functions_flow.append(arrow)

        self.functions_flow = list(set(self.functions_flow))
        self.functions_flow.insert(0, self.graph_type)
        self.functions_flow = '\n'.join(self.functions_flow)

    def tables_parents(self, name):

        queries = []
        pass

    def tables_children(self, name):

        queries = []
        pass


