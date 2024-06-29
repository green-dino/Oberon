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
            print("Invalid choice. Please try again.")
            return None
        if max_val is not None and choice > max_val:
            print("Invalid choice. Please try again.")
            return None
        return choice
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def print_dictionary(ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data, indent_level=0):
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
    if not isinstance(dictionary, dict):
        raise TypeError("The provided input is not a dictionary.")
    
    # Extracting path and depth_limit from kwargs with defaults
    path = args[0] if args else []
    depth_limit = kwargs.get('depth_limit', float('inf'))
    
    while True:
        current_level = dictionary
        for key in path:
            current_level = current_level.get(key, {})
        
        # Printing current path
        print("\nCurrent Path:", " -> ".join(path) if path else "Root")
        print_dictionary(ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data)
        
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

if __name__ == "__main__":
    explore_dictionary_structure(ADMIN_GROUPS, CONTROL_GROUPS, PHASES, data)

