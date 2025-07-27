import json
import csv
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any, Union, Optional, TextIO
from tqdm import tqdm
import pandas as pd


def read_json_file(file_path: str, show_progress: bool = False) -> List[Dict[str, Any]]:
    """
    Read and parse JSON data from a file with optional progress bar.
    
    Args:
        file_path: Path to the JSON file
        show_progress: Whether to show progress bar for large files
        
    Returns:
        List of dictionaries containing the parsed JSON data
    """
    try:
        # Get file size for progress estimation
        file_size = os.path.getsize(file_path)
        
        # Use tqdm to show progress for large files
        with open(file_path, 'r', encoding='utf-8') as f:
            if show_progress and file_size > 1_000_000:  # Show progress for files > 1MB
                with tqdm(
                    total=file_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                    desc=f"Reading {os.path.basename(file_path)}",
                    leave=False
                ) as pbar:
                    # Read file in chunks to show progress
                    chunks = []
                    while True:
                        chunk = f.read(8192)  # 8KB chunks
                        if not chunk:
                            break
                        chunks.append(chunk)
                        pbar.update(len(chunk.encode('utf-8')))
                    
                    # Parse the complete JSON
                    data = json.loads(''.join(chunks))
            else:
                # For small files, just read normally
                data = json.load(f)
        
        # Ensure we return a list
        if not isinstance(data, list):
            data = [data]
            
        return data
        
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Failed to parse JSON file '{os.path.basename(file_path)}' at line {e.lineno}, column {e.colno}:\n"
            f"  {e.msg}\n"
            f"  Context: {e.doc[max(0, e.pos-20):e.pos+20].replace('\n', ' ')}..."
        )
    except UnicodeDecodeError as e:
        raise ValueError(
            f"Encoding error in file '{os.path.basename(file_path)}':\n"
            f"  {str(e)}\n"
            "  The file might be corrupted or not in UTF-8 encoding.\n"
            "  Try converting the file to UTF-8 encoding before processing."
        )
    except FileNotFoundError:
        raise FileNotFoundError(
            f"The file '{file_path}' does not exist.\n"
            "  Please check the file path and try again."
        )
    except PermissionError:
        raise PermissionError(
            f"Permission denied when trying to read '{file_path}'.\n"
            "  Please check file permissions and try again."
        )
    except Exception as e:
        raise Exception(
            f"Unexpected error while reading JSON file '{os.path.basename(file_path)}':\n"
            f"  {str(e)}\n"
            "  Please check if the file is a valid JSON file and not corrupted."
        )


def flatten_json(nested_json: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary structure.
    
    Args:
        nested_json: The nested dictionary to flatten
        parent_key: Used for recursion, leave as default
        sep: Separator between nested keys
        
    Returns:
        Flattened dictionary
    """
    items = {}
    
    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], f"{name}{a}{sep}")
        elif isinstance(x, list):
            # Convert lists to JSON strings to preserve structure
            items[name.rstrip(sep)] = json.dumps(x, ensure_ascii=False)
        else:
            items[name.rstrip(sep)] = x
    
    flatten(nested_json)
    return items

def get_all_fieldnames(data: List[Dict[str, Any]]) -> List[str]:
    """
    Get all unique field names from a list of dictionaries, including nested ones.
    
    Args:
        data: List of dictionaries to extract field names from
        
    Returns:
        Sorted list of all unique field names
    """
    fieldnames = set()
    
    for item in data:
        flat_item = flatten_json(item)
        fieldnames.update(flat_item.keys())
    
    return sorted(fieldnames)

def write_csv(data: List[Dict[str, Any]], output_path: str, delimiter: str = ',', 
             show_progress: bool = False) -> None:
    """
    Write data to a CSV/TSV file with optional progress bar.
    Handles nested JSON structures by flattening them.
    
    Args:
        data: List of dictionaries to write
        output_path: Path to the output file
        delimiter: Field delimiter to use
        show_progress: Whether to show progress bar for large datasets
    """
    if not data:
        return
    
    try:
        # Get all possible fieldnames from all records
        fieldnames = get_all_fieldnames(data)
        
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.', exist_ok=True)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            writer.writeheader()
            
            if show_progress and len(data) > 100:  # Show progress for >100 rows
                for row in tqdm(data, desc="Writing CSV", unit="rows", leave=False):
                    writer.writerow(flatten_json(row))
            else:
                for row in data:
                    writer.writerow(flatten_json(row))
                
    except PermissionError:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise PermissionError(
            f"Permission denied when trying to write to '{output_path}'.\n"
            "  The file might be open in another program or you don't have write permissions.\n"
            "  Please close any programs that might be using the file and try again."
        )
    except csv.Error as e:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise ValueError(
            f"Error writing CSV/TSV file '{os.path.basename(output_path)}':\n"
            f"  {str(e)}\n"
            f"  This might be due to invalid characters in the data or issues with the delimiter '{delimiter}'.\n"
            "  Try using a different delimiter or check your data for special characters."
        )
    except Exception as e:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
            except:
                pass
        raise Exception(
            f"Unexpected error while writing to '{os.path.basename(output_path)}':\n"
            f"  {str(e)}\n"
            "  The output directory might not exist or the disk might be full."
        )


def write_excel(data: List[Dict[str, Any]], output_path: str, show_progress: bool = False) -> None:
    """
    Write data to an Excel file with optional progress bar.
    
    Args:
        data: List of dictionaries to write
        output_path: Path to the output Excel file
        show_progress: Whether to show progress bar for large datasets
    """
    if not data:
        return
    
    try:
        # Convert data to DataFrame
        if show_progress and len(data) > 1000:  # Show progress for >1000 rows
            # Process in chunks to show progress
            chunk_size = 1000
            chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
            
            with tqdm(total=len(data), desc="Processing data", unit="rows", leave=False) as pbar:
                dfs = []
                for chunk in chunks:
                    dfs.append(pd.DataFrame(chunk))
                    pbar.update(len(chunk))
                
                df = pd.concat(dfs, ignore_index=True)
        else:
            df = pd.DataFrame(data)
        
        # Write to Excel with progress for large DataFrames
        if show_progress and len(df) > 1000:
            with tqdm(total=100, desc="Writing Excel", unit="%", leave=False) as pbar:
                # Create a temporary file to write to
                temp_path = f"{output_path}.tmp"
                
                # Write to Excel with chunks to show progress
                writer = pd.ExcelWriter(temp_path, engine='openpyxl')
                df.to_excel(writer, index=False)
                
                # Manually save with progress updates
                writer.book.save(temp_path)
                pbar.update(100)
                
                # Rename temp file to final name
                if os.path.exists(output_path):
                    os.remove(output_path)
                os.rename(temp_path, output_path)
        else:
            # For smaller files, just write directly
            df.to_excel(output_path, index=False, engine='openpyxl')
            
    except ImportError as e:
        if 'openpyxl' in str(e):
            raise ImportError(
                "The 'openpyxl' package is required for Excel support.\n"
                "  Please install it by running:\n"
                "  pip install openpyxl"
            )
        else:
            raise ImportError(
                f"Missing required dependency: {str(e)}\n"
                "  Please install the required packages with:\n"
                "  pip install pandas openpyxl"
            )
    except Exception as e:
        # Clean up any temporary files on error
        temp_path = f"{output_path}.tmp"
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        
        error_msg = str(e).lower()
        if 'workbook' in error_msg and 'contains no worksheets' in error_msg:
            raise ValueError(
                "Failed to create Excel file: No data to write.\n"
                "  The input data might be empty or in an unexpected format."
            )
        elif 'permission' in error_msg:
            raise PermissionError(
                f"Permission denied when writing to '{os.path.basename(output_path)}'.\n"
                "  The file might be open in another program like Excel.\n"
                "  Please close any programs that might be using the file and try again."
            )
        else:
            raise Exception(
                f"Error writing Excel file '{os.path.basename(output_path)}':\n"
                f"  {str(e)}\n"
                "  This might be due to invalid data or unsupported Excel features.\n"
                "  Try saving as CSV/TSV instead or check your data for issues."
            )


def convert_json_to_format(
    input_path: str, 
    output_path: str, 
    output_format: str = 'csv',
    delimiter: str = ',',
    show_progress: bool = True
) -> None:
    """
    Convert JSON file to specified format with progress tracking.
    
    Args:
        input_path: Path to input JSON file
        output_path: Path for output file
        output_format: Output format ('csv', 'tsv', or 'excel')
        delimiter: Delimiter to use for CSV/TSV (default: ',' for CSV, '\t' for TSV)
        show_progress: Whether to show progress bars
    """
    # Set default delimiter based on format if not specified
    if output_format == 'tsv' and delimiter == ',':
        delimiter = '\t'
    
    # Determine if we should show progress (only for non-quiet mode and TTY)
    show_progress = show_progress and sys.stdout.isatty()
    
    try:
        # Read with progress
        if show_progress:
            print(f"Reading {os.path.basename(input_path)}...")
            
        data = read_json_file(input_path, show_progress=show_progress)
        
        if not data:
            print("Warning: No data found in the input file")
            return
            
        # Write with progress
        if show_progress:
            print(f"Converting to {output_format.upper()}...")
        
        if output_format in ('csv', 'tsv'):
            write_csv(data, output_path, delimiter, show_progress=show_progress)
        elif output_format == 'excel':
            if not output_path.lower().endswith(('.xlsx', '.xls')):
                output_path = f"{os.path.splitext(output_path)[0]}.xlsx"
            write_excel(data, output_path, show_progress=show_progress)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")
            
    except ValueError as e:
        if os.path.exists(output_path):
            os.remove(output_path)
        # Re-raise with additional context
        if 'Unsupported output format' in str(e):
            raise ValueError(
                f"{str(e)}\n"
                "  Supported formats are: 'csv', 'tsv', 'excel'\n"
                "  Example usage: --format csv"
            )
        raise
    except Exception as e:
        # Clean up any partial output file on error
        if os.path.exists(output_path):
            os.remove(output_path)
        
        # Add more context to the error message
        error_msg = str(e).lower()
        if 'no such file or directory' in error_msg and 'input' in error_msg.lower():
            raise FileNotFoundError(
                f"Input file not found: {input_path}\n"
                "  Please check the file path and try again."
            )
        elif 'permission' in error_msg:
            raise PermissionError(
                f"Permission error: {str(e)}\n"
                f"  Please check file permissions for: {input_path}"
            )
        elif 'empty' in error_msg or 'no data' in error_msg:
            raise ValueError(
                "The input file appears to be empty or contains no valid data.\n"
                "  Please check the file contents and try again."
            )
        else:
            # For any other error, include the original error message with some context
            raise Exception(
                f"Failed to convert {os.path.basename(input_path)}: {str(e)}\n"
                f"  Input: {input_path}\n"
                f"  Output: {output_path}\n"
                "  Please check the input file format and try again."
            )


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert JSON to various formats (CSV, TSV, Excel)')
    parser.add_argument('input', help='Input JSON file path')
    parser.add_argument('-o', '--output', help='Output file path (default: input.<format>)')
    parser.add_argument('-f', '--format', 
                      choices=['csv', 'tsv', 'excel'], 
                      default='csv',
                      help='Output format (default: csv)')
    parser.add_argument('--no-progress', 
                      action='store_false', 
                      dest='show_progress',
                      help='Disable progress bars')
    
    args = parser.parse_args()
    
    # Validate input file exists and is accessible
    if not os.path.exists(args.input):
        print(f"\nError: Input file not found: {args.input}", file=sys.stderr)
        print(f"  Current working directory: {os.getcwd()}")
        if not os.path.isabs(args.input):
            print("  Note: You're using a relative path. Try using an absolute path.")
        return 1
    
    if not os.path.isfile(args.input):
        print(f"\nError: Not a file: {args.input}", file=sys.stderr)
        if os.path.isdir(args.input):
            print("  The specified path is a directory, not a file.")
        return 1
        
    try:
        # Try to open the file to check for read permissions
        with open(args.input, 'r', encoding='utf-8'):
            pass
    except PermissionError:
        print(f"\nError: Permission denied when trying to read: {args.input}", file=sys.stderr)
        print("  Please check file permissions and try again.")
        return 1
    except UnicodeDecodeError:
        print(f"\nWarning: The file '{args.input}' doesn't appear to be a text file or uses an unusual encoding.", file=sys.stderr)
        print("  The converter might not work correctly with binary files.")
        # Continue anyway, as the file might still be valid JSON
    
    # Set default output filename if not provided
    if not args.output:
        base_name = Path(args.input).stem
        ext = 'xlsx' if args.format == 'excel' else args.format
        args.output = f"{base_name}.{ext}"
    
    try:
        # Get start time for duration calculation
        import time
        start_time = time.time()
        
        # Perform the conversion
        convert_json_to_format(
            input_path=args.input,
            output_path=args.output,
            output_format=args.format,
            delimiter='\t' if args.format == 'tsv' else ',',
            show_progress=args.show_progress
        )
        
        # Calculate and show duration
        duration = time.time() - start_time
        print(f"\nSuccessfully converted {os.path.basename(args.input)} to {os.path.basename(args.output)} "
              f"in {duration:.2f} seconds")
              
    except Exception as e:
        # Don't print the full traceback for expected errors
        if isinstance(e, (ValueError, FileNotFoundError, PermissionError, ImportError)):
            print(f"\n{str(e)}", file=sys.stderr)
        else:
            # For unexpected errors, print the full error with traceback
            import traceback
            print("\nAn unexpected error occurred:", file=sys.stderr)
            traceback.print_exc()
            print("\nPlease report this issue with the above error message.", file=sys.stderr)
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())