# Read the input file
with open('outdated.txt') as infile:
    lines = infile.readlines()[2:]  # Skip the first two lines

# Convert each line to freeze format
converted_lines = []
for line in lines:
    if line.strip():  # Skip empty lines
        parts = line.split()
        package_name = parts[0]
        latest_version = parts[2]
        converted_lines.append(f"{package_name}=={latest_version}")

# Write the converted data to a new file
with open('outdated_freeze.txt', 'w') as outfile:
    outfile.write('\n'.join(converted_lines))

print("Conversion completed. Output saved to 'outdated_freeze.txt'")
