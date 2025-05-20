# Open xsdat binary file
file_path = "C:/Users/Quentin/Games/Age of Empires 2 DE/76561198007343704/profile/Testing_MODIFIED.xsdat"
with open(file_path, "rb") as file:
    # Read the entire file content
    file_content = file.read()

# File contains 2 integers, read them
int1 = int.from_bytes(file_content[0:4], byteorder="little")
int2 = int.from_bytes(file_content[4:8], byteorder="little")

# Print them
print(f"Integer 1: {int1}")
print(f"Integer 2: {int2}")
