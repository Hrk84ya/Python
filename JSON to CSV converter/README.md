# JSON to CSV/TSV/Excel Converter

A powerful and flexible command-line tool to convert JSON files to CSV, TSV, or Excel formats with support for nested JSON structures and advanced features.

## ✨ Features

- **Multiple Formats**: Convert JSON to CSV, TSV, or Excel (XLSX) formats
- **Nested JSON Support**: Automatically flattens nested objects and arrays
- **Smart Type Handling**: Preserves data types including numbers, booleans, and dates
- **Progress Tracking**: Shows progress bars for large files
- **Robust Error Handling**: Clear error messages with helpful suggestions
- **Command-line Interface**: Easy-to-use with intuitive options
- **Unicode Support**: Full UTF-8 support for international characters
- **Memory Efficient**: Processes large files in chunks

## 🚀 Installation

1. Clone this repository or download the script:
   ```bash
   git clone https://github.com/hrk84ya/Python.git
   cd json-to-csv-converter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
   For Excel support, make sure to install the optional dependency:
   ```bash
   pip install openpyxl
   ```

## 🛠️ Usage

### Basic Conversion

```bash
# Convert JSON to CSV (default format)
python converter.py input.json

# Specify output file
python converter.py input.json -o output.csv

# Convert to TSV (Tab-separated values)
python converter.py input.json -f tsv -o output.tsv

# Convert to Excel format
python converter.py input.json -f excel -o output.xlsx
```

### Advanced Usage

```bash
# Convert a large file with progress bars disabled
python converter.py large_data.json --no-progress

# Convert to CSV with custom delimiter (default: ,)
python converter.py data.json -f csv --delimiter ';' -o output.csv

# Convert to TSV (same as --delimiter '\t')
python converter.py data.json -f tsv -o output.tsv
```

### Handling Nested JSON

The converter automatically flattens nested JSON structures using dot notation:

```json
{
  "user": {
    "name": "John",
    "address": {
      "city": "New York",
      "zip": "10001"
    },
    "skills": ["Python", "JavaScript"]
  }
}
```

Becomes in CSV:
```
user.name,user.address.city,user.address.zip,user.skills
John,New York,10001,["Python", "JavaScript"]
```

## 📋 Command-line Options

```
positional arguments:
  input                 Input JSON file path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (default: input.<format>)
  -f {csv,tsv,excel}, --format {csv,tsv,excel}
                        Output format (default: csv)
  -d DELIMITER, --delimiter DELIMITER
                        Field delimiter for CSV/TSV output (default: , for CSV, \t for TSV)
  --no-progress         Disable progress bars
```

### Command
```bash
python converter.py input.json -o employees.csv
```

### Output (employees.csv)
```csv
address.city,address.street,department,email,id,name,skills
San Francisco,123 Tech Street,Engineering,john.smith@example.com,1,John Smith,["Python", "JavaScript"]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## Examples

1. Convert a JSON file to CSV with default settings:
   ```bash
   python converter.py data.json
   ```
   This will create `data.csv` in the same directory.

2. Convert to TSV with a custom output filename:
   ```bash
   python converter.py data.json -f tsv -o results/data.tsv
   ```

3. Convert to Excel format:
   ```bash
   python converter.py data.json -f excel -o report.xlsx
   ```