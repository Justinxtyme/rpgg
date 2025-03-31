#!/usr/bin/env python3
import argparse
import os
import sys

# Configuration mapping of module name to its file path.
MODULES = {
   'ARMOR SYSTEM': 'armor-system/armor.py',
   'WEAPONS SYSTEM': 'weapons-system/weapons.py',
   # Add additional modules here...
}

# Name of the combined file.
COMBINED_FILE = 'combined.py'

def combine_files(verbose=False):
   """
   Combines each module's file into one combined file.
   Wraps each module's code with start/end markers.
   """
   try:
       with open(COMBINED_FILE, 'w') as combined:
           for module, filepath in MODULES.items():
               start_marker = f"# ----- {module} START -----"
               end_marker = f"# ----- {module} END -----"
               if verbose:
                   print(f"Combining module: {module} from {filepath}")
               combined.write(f"{start_marker}\n")
               if os.path.exists(filepath):
                   try:
                       with open(filepath, 'r') as f:
                           combined.write(f.read())
                   except Exception as e:
                       combined.write(f"# Error reading {filepath}: {e}\n")
               else:
                   combined.write(f"# File {filepath} not found.\n")
               combined.write(f"\n{end_marker}\n\n")
       print(f"Combined file written to {COMBINED_FILE}")
   except Exception as e:
       print(f"Error writing to {COMBINED_FILE}: {e}")
       sys.exit(1)

def split_file(verbose=False):
   """
   Splits the combined file back into individual module files.
   Looks for markers in the combined file and extracts each section.
   Also logs any unrecognized lines (outside markers) for debugging.
   """
   if not os.path.exists(COMBINED_FILE):
       print(f"Error: {COMBINED_FILE} not found.")
       sys.exit(1)

   try:
       with open(COMBINED_FILE, 'r') as combined:
           lines = combined.readlines()
   except Exception as e:
       print(f"Error reading {COMBINED_FILE}: {e}")
       sys.exit(1)

   # Prepare a dictionary to hold the lines for each module.
   module_content = { module: [] for module in MODULES.keys() }
   current_module = None
   unrecognized_lines = []

   # We'll also keep track of markers found for sanity checking.
   markers_found = { module: {"start": False, "end": False} for module in MODULES.keys() }

   for line in lines:
       stripped = line.strip()
       marker_detected = False
       # Check for module start and end markers.
       for module in MODULES.keys():
           start_marker = f"# ----- {module} START -----"
           end_marker = f"# ----- {module} END -----"
           if stripped == start_marker:
               if current_module is not None:
                   print(f"Warning: Nested start marker found for {module} while already in {current_module}")
               current_module = module
               markers_found[module]["start"] = True
               marker_detected = True
               break
           elif stripped == end_marker:
               if current_module != module:
                   print(f"Warning: End marker for {module} found while current module is {current_module}")
               else:
                   markers_found[module]["end"] = True
                   current_module = None
               marker_detected = True
               break
       # If no marker detected and we are inside a module, record the line.
       if not marker_detected:
           if current_module:
               module_content[current_module].append(line)
           elif stripped:  # Unrecognized non-blank lines outside any markers.
               unrecognized_lines.append(line)

   # Log warnings if any module is missing markers.
   for module, found in markers_found.items():
       if not found["start"]:
           print(f"Warning: No start marker found for module '{module}'.")
       if not found["end"]:
           print(f"Warning: No end marker found for module '{module}'.")

   if unrecognized_lines and verbose:
       print("Unrecognized lines (outside of any module markers):")
       for l in unrecognized_lines:
           print(l.strip())

   # Write the extracted content back to their respective files.
   for module, filepath in MODULES.items():
       directory = os.path.dirname(filepath)
       if directory and not os.path.exists(directory):
           try:
               os.makedirs(directory)
               if verbose:
                   print(f"Created directory: {directory}")
           except OSError as e:
               print(f"Error creating directory {directory}: {e}")
               continue
       try:
           with open(filepath, 'w') as f:
               f.writelines(module_content[module])
           if verbose:
               print(f"Updated {filepath} from combined file.")
       except Exception as e:
           print(f"Error writing to {filepath}: {e}")

def main():
   parser = argparse.ArgumentParser(
       description="Script to combine module files into one combined file, or split them back into individual files."
   )
   parser.add_argument('--mode', choices=['combine', 'split'], required=True,
                       help="Choose 'combine' to merge module files into combined.py or 'split' to extract changes back into individual files.")
   parser.add_argument('--verbose', action='store_true', help="Enable verbose logging for debugging.")
   args = parser.parse_args()

   if args.mode == 'combine':
       combine_files(verbose=args.verbose)
   elif args.mode == 'split':
       split_file(verbose=args.verbose)

if __name__ == '__main__':
   main()