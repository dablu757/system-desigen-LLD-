def cpu_heavy_task(n : int)->int:
    res = []

    def helper(i:int):
        if i==0 or i == 1:
            return i
    
        return helper(i-1)+helper(i-2)
    

    for i in range(n+1):
        fibo = helper(i)
        res.append(fibo)

    return res