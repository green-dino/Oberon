import os
import sys
from frame_structure import ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data

def print_dictionary(dictionary, indent_level=0):
    indent = "  " * indent_level
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(f"{indent}{key}:")
            print_dictionary(value, indent_level + 1)
        else:
            print(f"{indent}{key}: {value}")

def explore_nested(dictionary, path=[]):
    while True:
        current_level = dictionary
        for key in path:
            current_level = current_level[key]
        
        print("\nCurrent Path:", " -> ".join(path) if path else "Root")
        print_dictionary(current_level)
        
        subkeys = [key for key, value in current_level.items() if isinstance(value, dict)]
        if subkeys:
            print("\nSub-dictionaries:")
            for i, key in enumerate(subkeys, 1):
                print(f"{i}. {key}")
            print(f"{len(subkeys) + 1}. Go Back")
        
        print(f"{len(subkeys) + 2}. Exit to Main Menu")

        try:
            choice = int(input("Enter your choice: "))
            if choice == len(subkeys) + 1:
                if path:
                    path.pop()
                else:
                    break
            elif choice == len(subkeys) + 2:
                break
            elif 1 <= choice <= len(subkeys):
                path.append(subkeys[choice - 1])
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def explore_relationships(admin_groups, control_groups, phases, data):
    while True:
        print("\nChoose an option to explore:")
        print("1. View Admin Groups")
        print("2. View Control Groups")
        print("3. View Phases")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice (1-4): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue

        if choice == 1:
            explore_nested(admin_groups)
        elif choice == 2:
            explore_nested(control_groups)
        elif choice == 3:
            explore_nested(phases)
        elif choice == 4:
            print("Exiting the explorer. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the explorer
if __name__ == "__main__":
    explore_relationships(ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data)
