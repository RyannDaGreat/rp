#Pychess, written by Ryan Burgert, 2018
#Run me in Python 3! There are no dependencies.
#For an extra boost in performance, try running me in pypy3!
init='''
♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
· · · · · · · ·
· · · · · · · ·
· · · · · · · ·
· · · · · · · ·
♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜'''
#
vacant='·'
black='♙♖♘♗♕♔'
white='♟♜♞♝♛♚'
pawn  ='♟♙'
rook  ='♜♖'
knight='♞♘'
bishop='♝♗'
king  ='♚♔'
queen ='♛♕'
#
def group(*g):#g is vararg of strings
    from itertools import product#cartesian product
    return {x:y for x,y in product(''.join(g),g)if x in y}
piece   =group(pawn,rook,knight,bishop,king,queen)#{'♔':king,'♟':pawn,'♚':king, ... }
color   =group(black,white)#{'♔':black,'♘':black,'♚':white, ... }
value   ={pawn:1,rook:5,knight:3,bishop:3,king:1000,queen:9}
opponent={white:black,black:white}
#
def b2m(b):#board to matrix (make it mutable)
    b=b[1:]#get rid of the newline prefix
    return [x.split(' ')for x in b.split('\n')]
def m2b(m):#matrix to board (make it immutable)
    return '\n'+'\n'.join(' '.join(x)for x in m)
def move(b,x0,y0,x1,y1):#one-based from the bottom left
    assert legal(b, x0, y0, x1, y1),'illegal move'
    m=b2m(b)
    m[-y1][x1-1]=p=m[-y0][x0-1]
    assert p in piece,repr(p)+' is not a piece'
    m[-y0][x0-1]=vacant
    if p in pawn and y1 in{1,8}:#Not supported: promoting to non-queen
        m[-y1][x1-1],=set(queen)&set(color[p])#promote pawn to queen if pawn in a back row
    return m2b(m)
def flipb(b):#flip board:black/white's board positions
    return m2b(reversed([reversed(x)for x in b2m(b)]))
def flipm(*m):#flip move, *m in form x0,y0,x1,y1
    return (9-x for x in m)
def score(b,c):#the total value of all color c's pieces on board b
    return sum(value[piece[x]]for x in b if x in c)
def legal(b,x0,y0,x1,y1,print=lambda x:None):
    #Not supported: castling, en-passant
    m=b2m(b)
    if not 1<=x0<=8 or not 1<=y0<=8 or not 1<=x1<=8 or not 1<=y1<=8 or x0==x1 and y0==y1:#0 or 1 is off the board or piece didn't move
        print('Out of bounds or no movement')
        return False
    p0=m[-y0][x0-1]#piece before
    if p0 in black:
        m,x0,y0,x1,y1=b2m(flipb(b)),*flipm(x0,y0,x1,y1)#flip everything to make life easier
    try:
        p1=m[-y1][x1-1]#piece after
    except:
        print(-y1,x1-1)
        print(m)
        assert False,'Error?'
    Δ={abs(x1-x0),abs(y1-y0)}#In this function, the delta represents change in position
    if p0 in queen:#Queen can act as either bishop or rook
        print('Queen: Δ='+str(Δ))
        if 0 in Δ   :p0,=set(color[p0])&set(rook)
        elif len(Δ)==1:p0,=set(color[p0])&set(bishop)
        else:print('Queen neither acting as rook nor bishop, Δ='+str(Δ));return False
    if p0 in pawn:
        print('Pawn')
        if abs(x0-x1)>1:#Invalid horizontal movement
            print('Pawn cannot move horizontal')
            return False
        if x0==x1:#Not capturing a piece
            if y0==2 and y1==4:return p1 is vacant and m[-3][x0-1] is vacant#Move forward twice
            if y1==y0+1:       return p1 is vacant                          #Move forward once
            return False                                                    #Invalid move
        return y1==y0+1 and p1 in opponent[color[p0]]#Capturing a piece
    if p0 in rook:
        print('Rook')
        if x0==x1:#We moved on y axis
            x,={x0,x1}#basically, this says that x0 is equal to x1 and that x is just one of them. That way we don't have to choose arbitrarily, for more logically readable code.
            for y in range(min(y0,y1),max(y0,y1))[1:]:#make sure path BETWEEN 0 and 1 is vacant
                if m[-y][x-1] is not vacant:return False
            return p1 in vacant+opponent[color[p0]]#end must be opponent piece or vacant
        if y0==y1:#We moved on x axis
            y,={y0,y1}
            for x in range(min(x0,x1),max(x0,x1))[1:]:#make sure path BETWEEN 0 and 1 is vacant
                if m[-y][x-1] is not vacant:return False
            return p1 in vacant+opponent[color[p0]]#end must be opponent piece or vacant
        return False
    if p0 in knight:
        print('Knight')
        if not Δ=={1,2}:return False
        return p1 in vacant+opponent[color[p0]]
    if p0 in bishop:
        print('Bishop')
        if len(Δ)>1:return False#Not an equal difference
        Δ=Δ.pop()
        assert Δ,'Internal logic error: Piece should be guarenteed to move'
        for _ in range(Δ-1):
            x0+=1 if x0<x1 else -1
            y0+=1 if y0<y1 else -1
            if m[-y0][x0-1] is not vacant:return False#Must be clear path to target
        return p1 in vacant+opponent[color[p0]]
    if p0 in king:
        print('King')
        return Δ<={0,1} and p1 in vacant+opponent[color[p0]]
    print('Piece not recognized: '+repr(p0))
    return False
def moves(b,x,y):
    #Returns the set of all possible resulting legal boards from moving that piece
    p=b2m(b)[-y][x-1]
    Δ=set()#set of different movements to try
    r=set(range(-7,8))#max possible movement range on the board
    if p in pawn        :Δ|={(0,1),(0,2),(1,1),(-1,1),(0,-1),(0,-2),(1,-1),(-1,-1)}
    if p in rook  +queen:Δ|={(0,n)for n in r}|{( n,0)for n in r}
    if p in bishop+queen:Δ|={(n,n)for n in r}|{(-n,n)for n in r}
    if p in knight      :Δ|={(1,2),(1,-2),(-1,2),(-1,-2),( 2,1),( 2,-1),(-2, 1),(-2,-1)}
    if p in king        :Δ|={(1,0),(1, 1),( 0,1),(-1, 1),(-1,0),(-1,-1),( 0,-1),( 1,-1)}
    out=set()
    for Δx,Δy in Δ:
        args=b,x,y,x+Δx,y+Δy
        if legal(*args):
            yield move(*args)#it's safe to assume every element is unique
def shuffled(l):
    from random import shuffle
    l=list(l)+[]
    shuffle(l)
    return l
def all_moves(b,c):#board,color
    out=set()
    m=b2m(b)
    for x in shuffled(range(1,9)):
        for y in shuffled(range(1,9)):
            if m[-y][x-1] in c:
                for move in moves(b,x,y):
                    if move not in out:
                        yield move
                        out|={move}
def all_n_moves(b,c,n):
    #All combinations of n moves ahead of b, starting with color c
    out={b}
    for _ in range(n):
        new_out=out|set()
        for x in out:
            for move in all_moves(x,c):
                if move not in new_out:
                    yield move
                    new_out|={move}
        out=new_out
def advantage(b,c):
    return score(b,c)-score(b,opponent[c])
#
search=lambda b,c:all_n_moves(b,c,1)
def think_1(b,c,bad=9999):
    out,ba=b,-9999#biggest advantage seen
    for s in search(b,c):#for search-board in search; s is a string containing a chess board
        a=advantage(s,c)
        if a>ba:#Must not be a >=, must be >. If it's >=, then it searches for the best move you could make to help your opponent win.
            out=s
            ba=a
        if a>=bad:#The score is too high! Ignore it. Any further searching is a waste of resources. This is how we prune our search tree.
            return s,bad#This gets propagated through future calls such as in think_2 and think_3 etc,
    return out,ba#out is the actual chess board, while the second parameter is a number that measures how good the move is: in the form (move where c has most advantage). (c's advantage)
def think_2(b,c,bad=-9999):
    out,sa=b,9999#smallest advantage seen
    for s in search(b,c):#for search-board in search
        _,a=think_1(s,opponent[c],bad=sa)
        if a<sa:
            out=s
            sa=a
        if a<=bad:#Again, this is just here for performance improvements
            return s,bad
    return out,sa#move where c's opponent has least advantage; c's largest advantage = -(c's opponent's smallest advantage)
def think_3(b,c,bad=9999):
    out,ba=b,-9999
    for s in search(b,c):
        _,a=think_2(s,opponent[c],bad=ba)
        if a>ba:
            out=s
            ba=a
        if a>=bad:
            return s,bad
    return out,ba
def think_4(b,c,bad=-9999):
    out,sa=b,9999
    for s in search(b,c):
        _,a=think_3(s,opponent[c],bad=sa)
        if a<sa:
            out=s
            sa=a
        if a<=bad:
            return s,bad
    return out,sa
def has_won(b,c):
    return not set(b)&set(king)&set(opponent[c])#If our opponent color's king is nowhere to be found, we win!
#######################################################################################################################################################################################
#Nothing in the above code depends on the below code.
#######################################################################################################################################################################################

help_message="""PYCHESS:
    Welcome to Pychess, created by Ryan Burgert
    on planet Earth, Milky Way Galaxy, 2018.

    In this game, you play a chess game against an AI.
    There are a few differences in the rules between
    normal chess and the chess in this game, though.
        1. En-Passant and Castling are not allowed
        2. You are allowed to put yourself in check 
        3. There are no stalemates
        4. Pawns always promote to queens
        5. In order to win the game, you 
           must capture your opponent's king
        6. You always play white

    Special commands:
        1. "HELP" - brings up this menu
        2. "AUTO" - lets the AI make one move for you
        3. "L1"   - sets the AI to level 1
        4. "L2"   - sets the AI to level 2
        5. "L3"   - sets the AI to level 3
        6. "L4"   - sets the AI to level 4
        7. "L?"   - display current AI level
        8. "abcd", where a, b, c, and d are digits 
            between 1 and 8, inclusively - 
            Moves a piece from square (a,b) to square (c,d), 
            where coordinates (x,y) represent the positions
            of each square on the board. 
            EXAMPLE: To move your king's pawn two forward on 
            the first turn, you would enter "5254"
        9. The up/down arrow keys let you scroll
            through commands, for the sake of 
            convenience.
        10. "FLIP" - Flips the board visually.
            You still play white, though.
            This is useful for comparing 
            pychess to other chess engines.
        11. "SAVE *" - Saves the current game state to path *
            EXAMPLE: "SAVE test.txt"
        12. "LOAD *" - Loads the current game state from path *
            EXAMPLE: "LOAD test.txt"
        13. "EXIT" - Exits the game

    Other Notes: 
        • Commands are not case sensitive
        • Saved games include the ai level, and the sequence of
            moves since the beginning of the game. In other words,
            the UNDO command will work immediately after loading a game.
        • Immediately after you make a move, the chess board with
            that move (before your opponent makes their move)
            will be displayed in yellow
        • Your terminal must be capable of rendering unicode
            chess characters to display this game properly.
        • The AUTO command will make a move for you using the same
            AI level as your opponent AI, which will move immediately
            afterwards. This prevents cheating, as this function 
            is really meant to see how the AI thinks when playing 
            against itself."""
flip=False
def print_board(b,print=print):
    b=b.split('\n')[1:]
    h=' '
    for i in range(len(b)):
        b[i]=str(8-i)+h+b[i]
    b.append(h+' 1 2 3 4 5 6 7 8')
    if flip:
        b=[x[::-1]for x in b[::-1]]
    b='\n'+'\n'.join(b)
    print(b)
def color_print(s,n):
    print('\033[3'+str(n)+'m'+s+'\033[0m')#Using ansi-escape codes to change the output color in the terminal
def red_print(s):
    color_print(s,1)
def blue_print(s):
    color_print(s,6)#(Technically supposed to be cyan, but on my terminal it looks blue)
def yellow_print(s):
    color_print(s,3)
yellow_print(help_message)
game=[init]
game_over=lambda:has_won(game[-1],white) or has_won(game[-1],black)#Though usually "game over" means you lose by connotation, it doesn't technically mean that...
import readline#This lets us use the up/down arrow keys to navigate
if __name__=='__main__' or True:
    ai_level=4
    ai_move=lambda b,c=black:{1:think_1,2:think_2,3:think_3,4:think_4}[ai_level](b,c)[0]
    while True:
        if not game_over():
            print_board(game[-1])
        try:
            s=input(">>").strip()
            assert s,'Please input a command'
            if s.upper()=="UNDO":
                assert len(game)>1,'There are no moves left to UNDO, we are already at the beginning of the game'
                del game[-1]
                blue_print("Went back one move, it's your turn.")
            elif s.upper()=="HELP":
                yellow_print(help_message)
            elif s.upper()=="FLIP":
                blue_print("Flipping the board (for visual purposes only)...")
                flip^=True
            elif s.upper()=="EXIT":
                blue_print("Exiting the game...goodbye!")
                break
            elif s.upper().startswith("SAVE "):
                path=s[len("SAVE "):]
                file=open(path,'w')
                file.write(repr((ai_level,game)))
                file.close()
                blue_print("Saved the current game state to "+repr(path))
            elif s.upper().startswith("LOAD "):
                path=s[len("LOAD "):]
                file=open(path,'r')
                import ast
                try:
                    (ai_level,game)=ast.literal_eval(file.read())#It's like the eval function, except it's completely safe
                    blue_print("Loaded game state from "+repr(path))
                except:
                    blue_print("Error while loading game state! Failed to load "+repr(path))
                finally:
                    file.close()
            elif s.upper().startswith("L"):
                s=s[1:]
                assert s in {'1','2','3','4','?'},'Level must be either 1, 2, 3 or 4; or "?" to display current level'
                if s=='?':
                    blue_print("Current AI level: L"+str(ai_level))
                else:
                    ai_level=int(s)
                    blue_print("Set AI to level "+s)
            else:
                assert not game_over(),"The game's over - you can't make any more moves. You can still use other commands, though."
                if s.upper()=="AUTO":
                    blue_print("Letting the AI make this move for you...")
                    game.append(ai_move(game[-1],white))
                else:
                    assert len(s)==4 and all([x in '12345678' for x in s]),'Invalid move command! Your move command must be in the form "abcd", where a,b,c and d are digits between 1 and 8 inclusively.'
                    game.append(move(game[-1],*map(int,list(s))))
                print_board(game[-1],yellow_print)
                if has_won(game[-1],white):
                    blue_print("You win! You've saved humanity from this robot. Game over.")
                game[-1]=ai_move(game[-1])
                if has_won(game[-1],black):
                    blue_print("You Get Nothing! You Lose! Good Day, Sir! Game over.")
        except Exception as e:
            print(end='\007')#Ring the terminal's bell alert the user of an error
            red_print("ERROR: "+str(e))
assert False,'Game over. Re-import pychess to play again.'