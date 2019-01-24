from typing import List, Dict
from bs4 import BeautifulSoup


class Mermaid:

    def __init__(self, results: List[Dict]):

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
            for s in p['statements']:
                if s.get('from_table'):
                    for t in s.get('from_table'):
                        arrow = f"{t['schema']}.{t['name']}" \
                                f"-->|{s['procedure']}|" \
                                f"{s['target_table']['schema']}" \
                                f".{s['target_table']['name']};"
                        if arrow not in self.tables_flow:
                            self.tables_flow.append(arrow)
                if s.get('join_table'):
                    for t in s.get('join_table'):
                        arrow = f"{t['schema']}.{t['name']}" \
                                f"-->|{s['procedure']}|" \
                                f"{s['target_table']['schema']}" \
                                f".{s['target_table']['name']};"
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
