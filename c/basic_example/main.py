import ctypes

lib = ctypes.CDLL('./lib.so')  

a, b = 7, 3
print(f"{a} + {b} = {lib.add(a, b)}")        # 7 + 3 = 10
print(f"{a} - {b} = {lib.subtract(a, b)}")   # 7 - 3 = 4
