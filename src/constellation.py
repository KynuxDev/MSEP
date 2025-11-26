import networkx as nx
import json

class Constellation:
    def __init__(self):
        self.graph = nx.Graph()
        
    def add_node(self, node_id, node_type, attributes=None):
        if attributes is None:
            attributes = {}
        self.graph.add_node(node_id, type=node_type, **attributes)
        
    def add_edge(self, source, target, relationship):
        self.graph.add_edge(source, target, relation=relationship)
        
    def ingest_data(self, data_source, data_content):
        self.add_node("TARGET", "PERSON")
        
        if "http" in data_source:
            self.add_node(data_source, "URL")
            self.add_edge("TARGET", data_source, "FOUND_IN")
            
    def generate_ascii_map(self):
        report = "\n[CONSTELLATION NETWORK MAP]\n"
        report += f"Nodes: {self.graph.number_of_nodes()} | Edges: {self.graph.number_of_edges()}\n"
        report += "-" * 40 + "\n"
        
        for node, data in self.graph.nodes(data=True):
            node_type = data.get('type', 'UNKNOWN')
            connections = list(self.graph.neighbors(node))
            if connections:
                report += f"[{node_type}] {node} --Linked To--> {len(connections)} entities\n"
                
        return report

    def export_json(self):
        return json.dumps(nx.node_link_data(self.graph))
