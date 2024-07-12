import re
from typing import List, Tuple, Dict, Union

class MermaidParser:
    def __init__(self) -> None:
        self.nodes: List[str] = []
        self.edges: List[Tuple[str, str]] = []

    def parse_mermaid_input(self, input_text: str) -> Dict[str, Union[List[str], List[Tuple[str, str]]]]:
        """
        Parses Mermaid input text and extracts nodes and edges.
        Returns a structured data format (e.g., dictionary) representing the graph.
        """
        self.nodes = self._extract_nodes(input_text)
        self.edges = self._extract_edges(input_text)

        return {'nodes': self.nodes, 'edges': self.edges}

    def _extract_nodes(self, input_text: str) -> List[str]:
        """
        Extracts node declarations from the input text using a regular expression.
        Returns a list of nodes.
        """
        node_pattern = r'(\w+)\s*;'
        return re.findall(node_pattern, input_text)

    def _extract_edges(self, input_text: str) -> List[Tuple[str, str]]:
        """
        Extracts edge connections from the input text using a regular expression.
        Returns a list of tuples representing edges.
        """
        edge_pattern = r'(\w+)\s*-->\s*(\w+)\s*;'
        return re.findall(edge_pattern, input_text)

    def prompt_user_nodes(self) -> Union[str, None]:
        """
        Prompts the user to enter the nodes.
        Updates the internal nodes list.
        """
        print("Enter the nodes (type 'done' when finished, 'back' to go back, 'edit' to modify existing):")
        while True:
            node = input("Node: ")
            if node.lower() == 'done':
                break
            elif node.lower() == 'back':
                return 'back'
            elif node.lower() == 'edit':
                self.edit_nodes()
            elif re.match(r'^\w+$', node):
                self.nodes.append(f"{node};")
                print(f"Node '{node}' added.")
            else:
                print("Invalid node name. Please use alphanumeric characters only.")

    def prompt_user_edges(self) -> Union[str, None]:
        """
        Prompts the user to enter the edges.
        Updates the internal edges list.
        """
        print("Enter the edges in the format 'node1 --> node2' (type 'done' when finished, 'back' to go back, 'edit' to modify existing):")
        while True:
            edge = input("Edge: ")
            if edge.lower() == 'done':
                break
            elif edge.lower() == 'back':
                return 'back'
            elif edge.lower() == 'edit':
                self.edit_edges()
            elif re.match(r'^\w+\s*-->\s*\w+$', edge):
                self.edges.append((edge.split('-->')[0].strip(), edge.split('-->')[1].strip()))
                print(f"Edge '{edge}' added.")
            else:
                print("Invalid edge format. Please use the format 'node1 --> node2'.")

    def edit_nodes(self) -> None:
        """
        Allows the user to edit existing nodes.
        """
        print("Current nodes:")
        for idx, node in enumerate(self.nodes):
            print(f"{idx + 1}: {node}")
        while True:
            action = input("Enter the number of the node to edit, 'delete <number>' to remove, or 'done' to finish: ")
            if action.lower() == 'done':
                break
            elif action.startswith('delete'):
                try:
                    _, num = action.split()
                    num = int(num)
                    if 1 <= num <= len(self.nodes):
                        deleted_node = self.nodes.pop(num - 1)
                        print(f"Node '{deleted_node}' deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input. Use 'delete <number>'.")
            else:
                try:
                    num = int(action)
                    if 1 <= num <= len(self.nodes):
                        new_value = input(f"Enter new value for node {num}: ")
                        if re.match(r'^\w+$', new_value):
                            self.nodes[num - 1] = f"{new_value};"
                            print(f"Node {num} updated to '{new_value}'.")
                        else:
                            print("Invalid node name. Please use alphanumeric characters only.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input.")

    def edit_edges(self) -> None:
        """
        Allows the user to edit existing edges.
        """
        print("Current edges:")
        for idx, edge in enumerate(self.edges):
            print(f"{idx + 1}: {edge[0]} --> {edge[1]}")
        while True:
            action = input("Enter the number of the edge to edit, 'delete <number>' to remove, or 'done' to finish: ")
            if action.lower() == 'done':
                break
            elif action.startswith('delete'):
                try:
                    _, num = action.split()
                    num = int(num)
                    if 1 <= num <= len(self.edges):
                        deleted_edge = self.edges.pop(num - 1)
                        print(f"Edge '{deleted_edge}' deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input. Use 'delete <number>'.")
            else:
                try:
                    num = int(action)
                    if 1 <= num <= len(self.edges):
                        new_value = input(f"Enter new value for edge {num}: ")
                        if re.match(r'^\w+\s*-->\s*\w+$', new_value):
                            self.edges[num - 1] = (new_value.split('-->')[0].strip(), new_value.split('-->')[1].strip())
                            print(f"Edge {num} updated to '{new_value}'.")
                        else:
                            print("Invalid edge format. Please use the format 'node1 --> node2'.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input.")

    def prompt_user_input(self) -> str:
        """
        Prompts the user to enter nodes and edges separately.
        Returns the combined Mermaid input text.
        """
        while True:
            if self.prompt_user_nodes() == 'back':
                continue

            if self.prompt_user_edges() == 'back':
                continue

            # Preview the graph
            print("\nCurrent Graph:")
            print(f"Nodes:\n{'; '.join(self.nodes)}")
            print(f"Edges:\n{'; '.join([f'{edge[0]} --> {edge[1]}' for edge in self.edges])}")

            confirm = input("Is this correct? (yes/no): ").lower()
            if confirm == 'yes':
                return '; '.join(self.nodes) + '\n' + '; '.join([f'{edge[0]} --> {edge[1]}' for edge in self.edges])
            else:
                print("Let's edit the graph again.")

# Example usage
if __name__ == "__main__":
    parser = MermaidParser()
    user_input = parser.prompt_user_input()
    parsed_data = parser.parse_mermaid_input(user_input)
    print(parsed_data)
