
#compute magic constant
def magic_constant(n):
    return n*(n**2 + 1) // 2

#verify that a matrix is a magic square
def is_magic_square(square):
    n=len(square)
    #check matrix dimension
    if n==0 or any(len(row)!=n for row in square):
        return False

    #check numbers from 1 to n^2
    numbers=[num for row in square for num in row]
    expected=set(range(1,n**2+1))
    if any(type(num) is not int for num in numbers):
        return False
    if set(numbers) != expected:
        return False
    
    #calculate magic constant, check rows and columns
    target = magic_constant(n)
    for row in square:
        if sum(row)!=target:
            return False
    for col in range(n):
        column_sum=sum(square[row][col] for row in range(n))

        if column_sum!=target:
            return False
    #check diagonals
    main_diagonal=sum(square[i][i] for i in range(n))

    secondary_diagonal=sum(
        square[i][n-1-i] for i in range(n)
    )

    if main_diagonal!=target:
        return False

    if secondary_diagonal!=target:
        return False

    return True


#print a magic square
def print_square(square):
    n=len(square)
    width=len(str(n**2))

    for row in square:
        print(" ".join(f"{num:>{width}}" for num in row))



