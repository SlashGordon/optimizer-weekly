import os
import json

def merge_json_files(result_files):
    merged_results = []

    for file in result_files:
        with open(file, 'r') as f:
            results = json.load(f)
            merged_results.extend(results)

    return merged_results

def main():
    # Get all JSON result files from current directory
    result_files = [file for file in os.listdir('.') if file.startswith('result_') and file.endswith('.json')]

    # Merge the JSON files
    merged_results = merge_json_files(result_files)

    # Save the merged results to a new JSON file
    with open('merged_results.json', 'w') as f:
        json.dump(merged_results, f, indent=4)

if __name__ == "__main__":
    main()