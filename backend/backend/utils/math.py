def round_to_nearest_ten( n ): 
    """
    Given an integer, this function returns that integer rounded to its nearest multiple of 10
    """
    # Smaller multiple 
    a = (n // 10) * 10
      
    # Larger multiple 
    b = a + 10
      
    # Return of closest of two 
    return (b if n - a > b - n else a) 