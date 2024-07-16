from oberon_module import FileExaminer


def main():
    # Prompt the user for a file path or directory
    file_path = input("Enter the path to the file or directory: ").strip()

    # Create a FileExaminer instance
    examiner = FileExaminer(file_path)
    
    # Print the metadata
    print("\nFile Metadata:")
    for key, value in examiner.metadata.items():
        print(f"{key}: {value}")
    
    # If it's a file, print the hashes
    if examiner.metadata.get('is_file', False):
        print("\nFile Hashes:")
        try:
            for hash_type in ["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]:
                hash_value = examiner.hasher.hash_file(hash_type)
                print(f"{hash_type}: {hash_value}")
        except RuntimeError as e:
            print(str(e))
    else:
        print("\nHashing is only available for files.")

if __name__ == "__main__":
    main()