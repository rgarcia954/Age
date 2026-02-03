#!/usr/bin/env python3
"""
Age Calculator Program
Calculates ages for people based on birth dates and death dates (if applicable).
Supports CSV input/output and handles multiple date formats.
"""

import csv
import sys
from datetime import datetime
from pathlib import Path
from dateutil import parser
from typing import Optional, Dict, List, Tuple


class Person:
    """Represents a person with birth and optional death date."""
    
    def __init__(self, name: str, birthdate: str, death_date: Optional[str] = None):
        self.name = name
        self.birthdate_str = birthdate
        self.death_date_str = death_date if death_date else ""
        
        # Parse dates
        self.birthdate = self._parse_date(birthdate)
        self.death_date = self._parse_date(death_date) if death_date else None
        
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse date string in various formats."""
        if not date_str or date_str.strip() == "":
            return None
            
        try:
            # Use dateutil parser for flexible date parsing
            return parser.parse(date_str)
        except (ValueError, parser.ParserError) as e:
            print(f"Warning: Could not parse date '{date_str}': {e}")
            return None
    
    def calculate_ages(self, reference_date: datetime = None) -> Dict[str, any]:
        """
        Calculate age(s) for the person.
        
        Returns a dictionary with:
        - current_age: age if living, or age if they were alive today
        - deceased_age: age at death (if deceased)
        - is_deceased: boolean
        """
        if reference_date is None:
            reference_date = datetime.now()
        
        if self.birthdate is None:
            return {
                'current_age': 'Invalid birthdate',
                'deceased_age': '',
                'is_deceased': False
            }
        
        is_deceased = self.death_date is not None
        
        # Calculate current/living age (age if alive today)
        current_age = self._calculate_age(self.birthdate, reference_date)
        
        # Calculate deceased age if applicable
        deceased_age = ''
        if is_deceased and self.death_date:
            deceased_age = self._calculate_age(self.birthdate, self.death_date)
        
        return {
            'current_age': current_age,
            'deceased_age': deceased_age,
            'is_deceased': is_deceased
        }
    
    def _calculate_age(self, start_date: datetime, end_date: datetime) -> int:
        """Calculate age between two dates."""
        age = end_date.year - start_date.year
        
        # Adjust if birthday hasn't occurred yet this year
        if (end_date.month, end_date.day) < (start_date.month, start_date.day):
            age -= 1
            
        return age


class AgeCalculator:
    """Main application class for age calculation."""
    
    def __init__(self):
        self.people: List[Person] = []
        
    def run(self):
        """Main program loop."""
        print("=" * 60)
        print("Age Calculator Program")
        print("=" * 60)
        print()
        
        # Ask if user has a CSV file
        has_csv = self._get_yes_no_input("Do you have a CSV file with names and dates? (yes/no): ")
        
        if has_csv:
            self._load_from_csv()
        else:
            self._manual_entry()
        
        # Process and display results
        if self.people:
            self._display_results()
            self._save_to_csv()
        else:
            print("\nNo data to process. Exiting.")
    
    def _get_yes_no_input(self, prompt: str) -> bool:
        """Get yes/no input from user."""
        while True:
            response = input(prompt).strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'.")
    
    def _load_from_csv(self):
        """Load people from CSV file."""
        while True:
            filepath = input("\nEnter the path to your CSV file: ").strip()
            
            if not Path(filepath).exists():
                print(f"Error: File '{filepath}' not found.")
                retry = self._get_yes_no_input("Try another file? (yes/no): ")
                if not retry:
                    return
                continue
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    
                    # Check for required columns (flexible matching)
                    if not reader.fieldnames:
                        print("Error: CSV file appears to be empty.")
                        return
                    
                    # Find column names (case-insensitive)
                    fieldnames_lower = {fn.lower(): fn for fn in reader.fieldnames}
                    
                    name_col = None
                    birth_col = None
                    death_col = None
                    
                    # Try to find columns
                    for key in ['name', 'person', 'full name', 'fullname']:
                        if key in fieldnames_lower:
                            name_col = fieldnames_lower[key]
                            break
                    
                    for key in ['birthdate', 'birth date', 'birth_date', 'dob', 'date of birth']:
                        if key in fieldnames_lower:
                            birth_col = fieldnames_lower[key]
                            break
                    
                    for key in ['death date', 'deathdate', 'death_date', 'dod', 'date of death', 'deceased date']:
                        if key in fieldnames_lower:
                            death_col = fieldnames_lower[key]
                            break
                    
                    if not name_col or not birth_col:
                        print("\nError: Could not find required columns.")
                        print(f"Available columns: {', '.join(reader.fieldnames)}")
                        print("Required: 'name' and 'birthdate' (or similar)")
                        return
                    
                    # Read data
                    count = 0
                    for row in reader:
                        name = row.get(name_col, '').strip()
                        birthdate = row.get(birth_col, '').strip()
                        death_date = row.get(death_col, '').strip() if death_col else ''
                        
                        if name and birthdate:
                            person = Person(name, birthdate, death_date if death_date else None)
                            self.people.append(person)
                            count += 1
                    
                    print(f"\nSuccessfully loaded {count} person(s) from CSV.")
                    break
                    
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                retry = self._get_yes_no_input("Try another file? (yes/no): ")
                if not retry:
                    return
    
    def _manual_entry(self):
        """Manually enter person data."""
        print("\nManual Entry Mode")
        print("=" * 60)
        print("Date formats supported: YYYY-MM-DD, MM/DD/YYYY, DD-MM-YYYY, etc.")
        print("Press Enter without a name to finish entering data.")
        print()
        
        while True:
            name = input("Enter name: ").strip()
            
            if not name:
                break
            
            birthdate = input("Enter birthdate: ").strip()
            
            if not birthdate:
                print("Birthdate is required. Skipping this entry.\n")
                continue
            
            is_deceased = self._get_yes_no_input("Is this person deceased? (yes/no): ")
            
            death_date = None
            if is_deceased:
                death_date = input("Enter death date: ").strip()
                if not death_date:
                    death_date = None
            
            person = Person(name, birthdate, death_date)
            self.people.append(person)
            print(f"Added {name}\n")
    
    def _display_results(self):
        """Display calculated ages for all people."""
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)
        print()
        
        for person in self.people:
            ages = person.calculate_ages()
            
            print(f"Name: {person.name}")
            print(f"  Birthdate: {person.birthdate_str}")
            
            if ages['is_deceased']:
                print(f"  Death Date: {person.death_date_str}")
                print(f"  Age at Death: {ages['deceased_age']} years")
                print(f"  Would be Age Today: {ages['current_age']} years")
            else:
                print(f"  Current Age: {ages['current_age']} years")
            
            print()
    
    def _save_to_csv(self):
        """Save results to CSV file."""
        save = self._get_yes_no_input("Save results to CSV file? (yes/no): ")
        
        if not save:
            return
        
        default_filename = f"age_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filename = input(f"Enter filename (default: {default_filename}): ").strip()
        
        if not filename:
            filename = default_filename
        
        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['Name', 'Birthdate', 'Death Date', 'Current Age', 'Deceased Age', 'Status']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                
                for person in self.people:
                    ages = person.calculate_ages()
                    
                    writer.writerow({
                        'Name': person.name,
                        'Birthdate': person.birthdate_str,
                        'Death Date': person.death_date_str,
                        'Current Age': ages['current_age'],
                        'Deceased Age': ages['deceased_age'],
                        'Status': 'Deceased' if ages['is_deceased'] else 'Living'
                    })
            
            print(f"\nResults saved to: {filename}")
            
        except Exception as e:
            print(f"Error saving CSV file: {e}")


def main():
    """Main entry point."""
    try:
        calculator = AgeCalculator()
        calculator.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
