#horse moves in chess board
from pyswip import Prolog
prolog = Prolog()
prolog.consult("puzzle.pl")
# the hourse is at (x,y) postion
x, y = 8, 8
print(f"Knight at ({x},{y}) can move to:")
for result in prolog.query(f"knight_move({x}, {y}, X2, Y2)"):
    print(f"→ ({result['X2']}, {result['Y2']})")
