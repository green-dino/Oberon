import csv
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FileHandler:
    def save_results_to_file(self, results: List[Tuple[str, str]], filename: str = "analysis_results.csv"):
        """
        Saves the analysis results to a CSV file.

        Args:
            results (List[Tuple[str, str]]): A list of tuples containing the result type and value.
            filename (str): The name of the file to save the results in. Defaults to "analysis_results.csv".
        """
        logging.info(f"Saving results to file: {filename}")
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Result Type", "Value"])
                for result in results:
                    writer.writerow(result)
            logging.info(f"Results saved to file: {filename}")
        except Exception as e:
            logging.error(f"Error saving results to file: {e}")
            raise
