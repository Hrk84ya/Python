# Get user input for the upper limit of the range
x = int(input("Enter a number: "))

# Generate a list of cubes for numbers from 1 to x (inclusive) using list comprehension
# Example: If x=3, output will be [1, 8, 27]
cubes = [i**3 for i in range(1, x + 1)]
print("\nResult:",cubes)