def fibonacci(n):
    """
    This function takes a positive integer n and returns the Fibonacci sequence up to n terms as a list of integers.
    The function uses an iterative approach to calculate the Fibonacci sequence, starting with the first two terms 0 and 1.
    It then calculates each term in the sequence using the recurrence relation: F(n) = F(n-1) + F(n-2).
    The function returns a list of integers that represents the Fibonacci sequence up to n terms.
    """
    if n < 0:
        raise ValueError("n must be a positive integer")
    if n == 0:
        return [0]
    elif n == 1:
        return [0, 1]
    else:
        result = [0, 1]
        for i in range(2, n+1):
            result.append(result[i-1] + result[i-2])
        return result