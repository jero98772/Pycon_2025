#pip install pyswip
from pyswip import Prolog
prolog = Prolog()
# Load the Prolog file
prolog.consult("math.pl")
a = 2;b = 2
query = f"sum({a}, {b}, X)"
result = list(prolog.query(query))
print(result[0]["X"])# it can give you multiples answer
