# Age Calculator Program

A Python program that calculates ages for people based on their birth dates and death dates (if applicable).

## Features

- **Flexible Date Parsing**: Handles multiple date formats (YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, etc.)
- **CSV Input/Output**: Process data from CSV files and save results
- **Manual Entry**: Enter data interactively if you don't have a CSV file
- **Deceased Handling**: Calculates both age at death and current age (what they would be today)
- **Reusable Output**: Generated CSV files can be used as input for subsequent runs

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install python-dateutil
```

## Usage

Run the program:

```bash
python age_calculator.py
```

### CSV Input Mode

If you have a CSV file, the program will:
1. Ask for the file path
2. Automatically detect column names (flexible matching)
3. Process all records
4. Display results
5. Offer to save results to a new CSV file

**Required CSV Columns:**
- `Name` (or similar: person, full name, etc.)
- `Birthdate` (or similar: birth date, dob, date of birth, etc.)
- `Death Date` (optional: death date, dod, date of death, deceased date, etc.)

### Manual Entry Mode

If you don't have a CSV file:
1. Enter each person's information interactively
2. Press Enter without a name to finish
3. Results will be displayed
4. Option to save to CSV

## CSV Format Examples

### Input CSV
```csv
Name,Birthdate,Death Date
John Smith,1985-03-15,
Jane Doe,05/20/1990,
Albert Einstein,March 14 1879,April 18 1955
Marie Curie,1867-11-07,1934-07-04
```

### Output CSV
```csv
Name,Birthdate,Death Date,Current Age,Deceased Age,Status
John Smith,1985-03-15,,40,,Living
Jane Doe,05/20/1990,,34,,Living
Albert Einstein,March 14 1879,April 18 1955,146,76,Deceased
Marie Curie,1867-11-07,1934-07-04,158,66,Deceased
```

## Date Format Support

The program uses intelligent date parsing and supports formats including:
- ISO format: `2000-01-15`, `2000/01/15`
- US format: `01/15/2000`, `1/15/2000`
- European format: `15-01-2000`, `15/01/2000`
- Text format: `January 15, 2000`, `15 Jan 2000`, `Jan 15 2000`
- And many more variations

## Age Calculation Logic

### For Living People
- **Current Age**: Age as of today's date

### For Deceased People
- **Deceased Age**: Age at the time of death
- **Living Age** (Would be Age Today): What their age would be if they were alive today

## Examples

### Example 1: Processing Historical Figures

```
Name: Albert Einstein
  Birthdate: March 14 1879
  Death Date: April 18 1955
  Age at Death: 76 years
  Would be Age Today: 146 years
```

### Example 2: Living Person

```
Name: John Smith
  Birthdate: 1985-03-15
  Current Age: 40 years
```

## Error Handling

- Invalid dates are reported with warnings
- Missing required columns in CSV are clearly indicated
- File not found errors are handled gracefully
- User can retry operations after errors

## Tips

1. **Reusing Output**: The output CSV can be used as input for the program, making it easy to update calculations
2. **Column Flexibility**: Column names are matched case-insensitively and with various common variations
3. **Empty Death Dates**: Leave death date blank or empty for living people
4. **Date Ambiguity**: For best results, use unambiguous date formats like YYYY-MM-DD

## License

Free to use and modify.
