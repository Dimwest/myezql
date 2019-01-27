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

    def arrow(self, statement, statement_part):

        if statement.get(statement_part):
            for table in statement.get(statement_part):

                arrow = f"{table['schema']}.{table['name']}" \
                        f"-->|{statement['procedure']}|" \
                        f"{statement['target_table']['schema']}" \
                        f".{statement['target_table']['name']};"

                # If arrow not already existing, add it to the chart
                if arrow not in self.tables_flow:
                    self.tables_flow.append(arrow)

    def tables_chart(self, path) -> None:

        # Creating Mermaid markdown string
        for p in self.input:
            # For all statements in parsed procedure/file
            for s in p['statements']:
                self.arrow(s, 'from_table')
                self.arrow(s, 'join_table')

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
