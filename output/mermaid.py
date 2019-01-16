from typing import List
from sql.objects import Procedure
from bs4 import BeautifulSoup


class Mermaid:

    def __init__(self, results: List[Procedure]):

        self.graph_type = "graph LR; \nlinkStyle default interpolate basis\n"
        self.tables_flow = []
        self.functions_flow = []
        self.input = results
        self.output = ''
        with open('./output/resources/template.html', 'r') as template:
            self.soup = BeautifulSoup(template.read(), features="html.parser")

    def tables_chart(self, path) -> None:

        # Creating Mermaid markdown string
        # TODO -> Rewrite in a more elegant way
        for p in self.input:
            for s in p.statements:
                if s.from_table:
                    for t in s.from_table:
                        arrow = f"{t.name}-->|{s.procedure}|{s.target_table.name};"
                        if arrow not in self.tables_flow:
                            self.tables_flow.append(arrow)
        self.tables_flow = list(set(self.tables_flow))
        self.tables_flow.insert(0, self.graph_type)
        self.output = '\n'.join(self.tables_flow)

        # Update <div class="mermaid"> in HTML template code with our Mermaid markdown
        mermaid = self.soup.find("div", {"class": "mermaid"})
        chart = self.soup.new_tag("div")
        chart.attrs["class"] = "mermaid"
        chart.string = self.output
        mermaid.replace_with(chart)

        # Save HTML file at specified path
        with open(path, 'w') as outfile:
            outfile.write(str(self.soup))

    def functions_chart(self) -> None:

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


