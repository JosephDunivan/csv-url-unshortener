# CSV URL Unshortener

This Python script unshortens URLs in a specified column of a CSV file. It's designed to work in Google Colab but can be adapted for local use.

## Features

- Uploads a CSV file in Google Colab
- Allows user to select which column contains the URLs to unshorten
- Processes URLs, following redirects to get the final destination
- Adds a new column with the unshortened URLs
- Downloads the processed CSV file

## Requirements

- Python 3.6+
- requests library
- Google Colab environment (for the current implementation)

## Usage

1. Open the `url_unshortener.py` file in a Google Colab notebook.
2. Run the script.
3. Upload your CSV file when prompted.
4. Select the column containing the shortened URLs.
5. Wait for processing to complete.
6. The results will be downloaded automatically as a new CSV file.

## Adapting for Local Use

To use this script locally:

1. Remove or comment out the `from google.colab import files` import.
2. Modify the `get_csv_file()` function to use local file input.
3. Modify the `save_and_download_csv()` function to save the file locally without downloading.

## Contributing

Contributions, issues, and feature requests are welcome!

## License

[MIT License](LICENSE)