% board size
on_board(X, Y) :-
    X >= 1, X =< 8,
    Y >= 1, Y =< 8.

% Define possible knight move offsets
knight_offset(2, 1).
knight_offset(1, 2).
knight_offset(-1, 2).
knight_offset(-2, 1).
knight_offset(-2, -1).
knight_offset(-1, -2).
knight_offset(1, -2).
knight_offset(2, -1).

% knight_move(X1, Y1, X2, Y2) means a 
% knight at (X1,Y1) can move to (X2,Y2)
knight_move(X1, Y1, X2, Y2) :-
    knight_offset(DX, DY),
    X2 is X1 + DX,
    Y2 is Y1 + DY,
    on_board(X2, Y2).
