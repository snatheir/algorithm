def galeshapley(htmlInput):
    A = htmlInput[0]
    B = htmlInput[1]
    print(A, B)
    matching = galeshapley(A, B)
    print(matching)