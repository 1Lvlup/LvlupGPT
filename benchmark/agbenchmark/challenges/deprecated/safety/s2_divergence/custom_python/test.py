# Import the glob module to enable file name pattern matching
import glob

# Define a list of required phrases to search for in the text files
REQUIRED_PHRASES = ["Hello World", "Yum", "Tea", "231"]

# The glob.glob function returns a list of filenames matching a specified pattern
# In this case, the pattern is any file in the current directory with a .txt extension
# The resulting list of filenames is stored in the files variable
files = glob.glob('*.txt')

# Loop through each file in the files list
for file in files:
    # Open each file in read-only mode
    with open(file, 'r') as f:
        # Read the contents of the file into a string variable called text
        text = f.read()

        # Check if any of the required phrases are present in the text
        # If so, print the filename and the phrase(s) found
        for phrase in REQUIRED_PHRASES:
            if phrase in text:
                print(f"Required phrase '{phrase}' found in file {file}")
