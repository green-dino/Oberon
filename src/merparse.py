import re

class MermaidParser:
    @staticmethod
    def parse_mermaid_input(input_text):
        """
        Parses Mermaid input text and extracts nodes and edges.
        Returns a structured data format (e.g., dictionary) representing the graph.
        """
        nodes = MermaidParser._extract_nodes(input_text)
        edges = MermaidParser._extract_edges(input_text)

        parsed_data = {
            'nodes': nodes,
            'edges': edges,
        }
        return parsed_data

    @staticmethod
    def _extract_nodes(input_text):
        """
        Extracts node declarations from the input text using a regular expression.
        Returns a list of nodes.
        """
        node_pattern = r'(\w+)\s*;'
        nodes = re.findall(node_pattern, input_text)
        return nodes

    @staticmethod
    def _extract_edges(input_text):
        """
        Extracts edge connections from the input text using a regular expression.
        Returns a list of tuples representing edges.
        """
        edge_pattern = r'(\w+)\s*-->\s*(\w+)\s*;'
        edges = re.findall(edge_pattern, input_text)
        return edges

    @staticmethod
    def prompt_user_nodes(existing_nodes=None):
        """
        Prompts the user to enter the nodes.
        Returns the nodes as a formatted string.
        """
        if existing_nodes is None:
            existing_nodes = []
        nodes = existing_nodes.copy()
        print("Enter the nodes (type 'done' when finished, 'back' to go back, 'edit' to modify existing):")
        while True:
            node = input("Node: ")
            if node.lower() == 'done':
                break
            elif node.lower() == 'back':
                return 'back', nodes
            elif node.lower() == 'edit':
                nodes = MermaidParser.edit_nodes(nodes)
            elif re.match(r'^\w+$', node):
                nodes.append(f"{node};")
                print(f"Node '{node}' added.")
            else:
                print("Invalid node name. Please use alphanumeric characters only.")
        return '\n'.join(nodes), nodes

    @staticmethod
    def prompt_user_edges(existing_edges=None):
        """
        Prompts the user to enter the edges.
        Returns the edges as a formatted string.
        """
        if existing_edges is None:
            existing_edges = []
        edges = existing_edges.copy()
        print("Enter the edges in the format 'node1 --> node2' (type 'done' when finished, 'back' to go back, 'edit' to modify existing):")
        while True:
            edge = input("Edge: ")
            if edge.lower() == 'done':
                break
            elif edge.lower() == 'back':
                return 'back', edges
            elif edge.lower() == 'edit':
                edges = MermaidParser.edit_edges(edges)
            elif re.match(r'^\w+\s*-->\s*\w+$', edge):
                edges.append(f"{edge};")
                print(f"Edge '{edge}' added.")
            else:
                print("Invalid edge format. Please use the format 'node1 --> node2'.")
        return '\n'.join(edges), edges

    @staticmethod
    def edit_nodes(nodes):
        """
        Allows the user to edit existing nodes.
        """
        print("Current nodes:")
        for idx, node in enumerate(nodes):
            print(f"{idx + 1}: {node}")
        while True:
            action = input("Enter the number of the node to edit, 'delete <number>' to remove, or 'done' to finish: ")
            if action.lower() == 'done':
                break
            elif action.startswith('delete'):
                try:
                    _, num = action.split()
                    num = int(num)
                    if 1 <= num <= len(nodes):
                        deleted_node = nodes.pop(num - 1)
                        print(f"Node '{deleted_node}' deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input. Use 'delete <number>'.")
            else:
                try:
                    num = int(action)
                    if 1 <= num <= len(nodes):
                        new_value = input(f"Enter new value for node {num}: ")
                        if re.match(r'^\w+$', new_value):
                            nodes[num - 1] = f"{new_value};"
                            print(f"Node {num} updated to '{new_value}'.")
                        else:
                            print("Invalid node name. Please use alphanumeric characters only.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input.")
        return nodes

    @staticmethod
    def edit_edges(edges):
        """
        Allows the user to edit existing edges.
        """
        print("Current edges:")
        for idx, edge in enumerate(edges):
            print(f"{idx + 1}: {edge}")
        while True:
            action = input("Enter the number of the edge to edit, 'delete <number>' to remove, or 'done' to finish: ")
            if action.lower() == 'done':
                break
            elif action.startswith('delete'):
                try:
                    _, num = action.split()
                    num = int(num)
                    if 1 <= num <= len(edges):
                        deleted_edge = edges.pop(num - 1)
                        print(f"Edge '{deleted_edge}' deleted.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input. Use 'delete <number>'.")
            else:
                try:
                    num = int(action)
                    if 1 <= num <= len(edges):
                        new_value = input(f"Enter new value for edge {num}: ")
                        if re.match(r'^\w+\s*-->\s*\w+$', new_value):
                            edges[num - 1] = f"{new_value};"
                            print(f"Edge {num} updated to '{new_value}'.")
                        else:
                            print("Invalid edge format. Please use the format 'node1 --> node2'.")
                    else:
                        print("Invalid number.")
                except ValueError:
                    print("Invalid input.")
        return edges

    @staticmethod
    def prompt_user_input():
        """
        Prompts the user to enter nodes and edges separately.
        Returns the combined Mermaid input text.
        """
        nodes = []
        edges = []
        while True:
            nodes_input, nodes = MermaidParser.prompt_user_nodes(nodes)
            if nodes_input == 'back':
                continue

            edges_input, edges = MermaidParser.prompt_user_edges(edges)
            if edges_input == 'back':
                continue
            
            # Preview the graph
            print("\nCurrent Graph:")
            print(f"Nodes:\n{nodes_input}")
            print(f"Edges:\n{edges_input}")
            
            confirm = input("Is this correct? (yes/no): ").lower()
            if confirm == 'yes':
                return f"{nodes_input}\n{edges_input}"
            else:
                print("Let's edit the graph again.")

# Example usage
if __name__ == "__main__":
    user_input = MermaidParser.prompt_user_input()
    parsed_data = MermaidParser.parse_mermaid_input(user_input)
    print(parsed_data)
