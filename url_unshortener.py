#!/usr/bin/env python3
"""
URL Unshortener for CSV files

This script unshortens URLs in a specified column of a CSV file.
It's designed to work in Google Colab but can be adapted for local use.

Usage:
1. Run the script in a Google Colab notebook.
2. Upload a CSV file when prompted.
3. Select the column containing shortened URLs.
4. The script will process the URLs and download the results.

Requirements:
- requests
- google.colab (for Colab environment)

Note: For local use, modify the file input/output methods.
"""

import csv
import io
import requests
from urllib.parse import urlparse
from typing import List, Tuple
from google.colab import files  # Comment this out for local use

def unshorten_url(url: str) -> str:
    """
    Attempt to unshorten a given URL.

    Args:
    url (str): The URL to unshorten.

    Returns:
    str: The unshortened URL or an error message.
    """
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        final_url = response.url
        
        parsed_url = urlparse(final_url)
        shortener_domains = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'shorturl.at', 'lnkd.in']
        if parsed_url.netloc in shortener_domains:
            return "Error: Still on shortener domain"
        
        return final_url
    except requests.RequestException as e:
        return f"Error: {str(e)}"

def get_csv_file() -> Tuple[str, bytes]:
    """
    Prompt user to upload a CSV file.

    Returns:
    Tuple[str, bytes]: Filename and file content.
    """
    print("Please upload your CSV file.")
    uploaded = files.upload()
    filename = next(iter(uploaded))
    return filename, uploaded[filename]

def get_column_selection(header: List[str]) -> int:
    """
    Prompt user to select a column from the CSV header.

    Args:
    header (List[str]): List of column names.

    Returns:
    int: Index of the selected column.
    """
    print("Available columns:")
    for i, col in enumerate(header):
        print(f"{i}: {col}")

    while True:
        try:
            column_index = int(input("Enter the number of the column containing the URLs to unshorten: "))
            if 0 <= column_index < len(header):
                return column_index
            else:
                print("Invalid selection. Please choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def process_csv(file_content: bytes, column_index: int) -> str:
    """
    Process the CSV file, unshortening URLs in the specified column.

    Args:
    file_content (bytes): Content of the CSV file.
    column_index (int): Index of the column containing URLs to unshorten.

    Returns:
    str: Processed CSV content as a string.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    with io.TextIOWrapper(io.BytesIO(file_content), encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)
        header.append('Unshortened URL')
        writer.writerow(header)

        for row in reader:
            if len(row) > column_index:
                shortened_url = row[column_index]
                unshortened_url = unshorten_url(shortened_url)
                row.append(unshortened_url)
            else:
                row.append("Error: Column index out of range")
            writer.writerow(row)
            print(f"Processed: {row[0]} - {shortened_url} -> {unshortened_url}")

    return output.getvalue()

def save_and_download_csv(content: str, filename: str):
    """
    Save the processed CSV content and trigger download in Colab.

    Args:
    content (str): Processed CSV content.
    filename (str): Name of the file to save.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        f.write(content)
    files.download(filename)

def main():
    try:
        filename, file_content = get_csv_file()
        with io.TextIOWrapper(io.BytesIO(file_content), encoding='utf-8') as infile:
            header = next(csv.reader(infile))
        column_index = get_column_selection(header)
        processed_content = process_csv(file_content, column_index)
        output_filename = 'unshortened_' + filename
        save_and_download_csv(processed_content, output_filename)
        print(f"Processing complete. Results downloaded as {output_filename}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()