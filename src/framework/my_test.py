import os
import sys
from frame_structure import ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data

def validate_input(prompt, min_val=None, max_val=None):
    """
    Helper function to validate integer inputs within a range.
    """
    try:
        choice = int(input(prompt))
        if min_val is not None and choice < min_val:
            raise ValueError("Choice is below the minimum allowed value.")
        if max_val is not None and choice > max_val:
            raise ValueError("Choice is above the maximum allowed value.")
        return choice
    except ValueError as ve:
        print(f"Invalid input: {ve}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def print_dictionary(dictionary, indent_level=0):
    """
    Function to recursively print a dictionary's keys and values.
    """
    if not isinstance(dictionary, dict):
        raise TypeError("The provided input is not a dictionary.")
    
    indent = "  " * indent_level
    for key, value in dictionary.items():
        if isinstance(value, dict):
            print(f"{indent}{key}:")
            print_dictionary(value, indent_level + 1)
        else:
            print(f"{indent}{key}: {value}")

def explore_dictionary_structure(dictionary, *args, **kwargs):
    """
    Function to explore and navigate through a nested dictionary.
    """
    if not isinstance(dictionary, dict):
        raise TypeError("The provided input is not a dictionary.")
    
    # Extracting path and depth_limit from kwargs with defaults
    path = list(args) if args else []
    depth_limit = kwargs.get('depth_limit', float('inf'))
    
    while True:
        current_level = dictionary
        for key in path:
            current_level = current_level.get(key, {})
        
        # Printing current path
        print("\nCurrent Path:", " -> ".join(path) if path else "Root")
        print_dictionary(current_level)
        
        # Listing sub-dictionaries
        subkeys = [key for key, value in current_level.items() if isinstance(value, dict)]
        if subkeys:
            print("\nSub-dictionaries:")
            for i, key in enumerate(subkeys, 1):
                print(f"{i}. {key}")
            print(f"{len(subkeys) + 1}. Go Back")
        
        # Providing options
        print(f"{len(subkeys) + 2}. Exit to Main Menu")

        choice = validate_input("Enter your choice: ", min_val=1, max_val=len(subkeys) + 2)
        if choice is None:
            continue
        
        if choice == len(subkeys) + 1:
            if path:
                path.pop()  # Go back one level
            else:
                break  # Exit if already at root
        elif choice == len(subkeys) + 2:
            break  # Exit to main menu
        else:
            path.append(subkeys[choice - 1])  # Navigate into selected sub-dictionary
        
        # Check depth limit
        if depth_limit > 0 and len(path) >= depth_limit:
            print("Reached maximum depth. Exiting...")
            break


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

def explore_relationships(ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data):
    while True:
        print("\nChoose an option to explore:")
        print("1. View Admin Groups")
        print("2. View Control Groups")
        print("3. View Phases")
        print("4. Data")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice (1-4): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue

        if choice == 1:
            explore_nested(ADMIN_GROUPS)
        elif choice == 2:
            explore_nested(CONTROL_GROUPS)
        elif choice == 3:
            explore_nested(PHASES)
        elif choice == 4:
            explore_nested(data)
        elif choice == 5:
            print("Exiting the explorer. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the explorer
if __name__ == "__main__":
    explore_relationships(ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data)
