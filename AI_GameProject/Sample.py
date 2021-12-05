
import STcpClient
import random
from bitstring import BitStream, BitArray

'''
    輪到此程式移動棋子
    board : 棋盤狀態(list of list), board[l][i][j] = l layer, i row, j column 棋盤狀態(l, i, j 從 0 開始)
            0 = 空、1 = 黑、2 = 白、-1 = 四個角落
    is_black : True 表示本程式是黑子、False 表示為白子

    return Step
    Step : single touple, Step = (r, c)
            r, c 表示要下棋子的座標位置 (row, column) (zero-base)
'''
cnt = 0
b = False
corner = [(0,0),(0,1),(0,4),(0,5),(1,0),(1,5),(4,0),(4,5),(5,0),(5,1),(5,4),(5,5)]

Dir = [1, 5, 6, 7, 29, 30, 31, 35, 36, 37, 41, 42, 43]
block = [2, 3, 7, 10, 12, 17, 18, 23, 25, 28, 32, 33,
         38, 39, 43, 46, 48, 53, 54, 59, 61, 64, 68, 69,
         74, 75, 79, 82, 84, 89, 90, 95, 97, 100, 104, 105,
         110, 111, 115, 118, 120, 125, 126, 131, 133, 136, 140, 141,
         146, 147, 151, 154, 156, 161, 162, 167, 169, 172, 176, 177,
         182, 183, 187, 190, 192, 197, 198, 203, 205, 208, 212, 213]
#Dir=[1,6,36,7,5,37,35,42,30,43,31,41,29]  
def evaluation(state):
    if b:
        player='01'
    else:
        player='10'
    
    state.pos = 504
    position = state.read('bin:9')
    position = BitStream(bin=position)
    position = position.uint
    state.pos = 0
    
    score = 0
    for d in Dir:
        explore = position
        Sum = 1
        
        left_block = False
        right_block = False
        
        state.pos = 0
        f1 = False
        if state.pos + (explore + d*2) <= 431:
            state.pos += (explore + d*2)
            if d == 1:
                if state.pos == 36 or state.pos == 108 or state.pos == 180 or state.pos == 252 or state.pos == 324 or state.pos == 396 :
                    f1 = True
            elif d == 5:
                if state.pos == 76 or state.pos == 148 or state.pos == 220 or state.pos == 292 or state.pos == 364 :
                    f1 = True
            elif d == 6:
                if state.pos == 76 or state.pos == 78 or state.pos == 148 or state.pos == 150 or state.pos == 220 or state.pos == 222 or state.pos == 292 or state.pos == 294 or state.pos == 364 or state.pos == 376 :
                    f1 = True
            elif d == 7:
                if state.pos == 78 or state.pos == 150 or state.pos == 222 or state.pos == 294 or state.pos == 366:
                    f1 = True    
            elif d == 29:
                if state.pos == 64 or state.pos == 136 or state.pos == 208 or state.pos == 280 or state.pos == 352 or state.pos == 424:
                    f1 = True
            elif d == 30:
                if state.pos == 64 or state.pos == 66 or state.pos == 136 or state.pos == 138 or state.pos == 208 or state.pos == 210 or state.pos == 280 or state.pos == 282 or state.pos == 352 or state.pos == 354  or state.pos == 424 or state.pos == 426:
                    f1 = True
            elif d == 31:
                if state.pos == 66 or state.pos == 96 or state.pos == 108 or state.pos == 138 or state.pos == 168 or state.pos == 180 or state.pos == 210 or state.pos == 240 or state.pos == 252 or state.pos == 282 or state.pos == 312 or state.pos == 324 or state.pos == 354 or state.pos == 384 or state.pos == 396 or state.pos == 426 :
                    f1 = True
            elif d == 35:
                 if state.pos == 106 or state.pos == 178 or state.pos == 250 or state.pos == 322 or state.pos == 394:
                     f1 = True
            elif d == 37:
                 if state.pos == 108 or state.pos == 180 or state.pos == 252 or state.pos == 324 or state.pos == 396:
                     f1 = True
            elif d == 41:
                if state.pos == 80 or state.pos == 118 or state.pos == 148 or state.pos == 152 or state.pos == 190 or state.pos == 220 or state.pos == 224 or state.pos == 262 or state.pos == 292 or state.pos == 296 or state.pos == 334 or state.pos == 364 or state.pos == 368 or state.pos == 406:
                    f1 = True
            elif d == 42:
                 if state.pos == 148 or state.pos == 150 or state.pos == 220 or state.pos == 222 or state.pos == 292 or state.pos == 294 or state.pos == 364 or state.pos == 366:
                    f1 = True
            elif d == 43:
                 if state.pos == 150 or state.pos == 222 or state.pos == 294 or state.pos == 366:
                    f1 = True
            
            if not f1:
                while True:
                    p = state.read('bin:2')
                    if p == player:
                        Sum += 1
                        
                        if (state.pos-2)/2 in block:
                            right_block = True
                            break
                        
                        if state.pos + (d*2 - 2) > 431:
                            break
                        state.pos += (d*2 - 2)
                        
                    else:
                        if p != '00':
                            right_block = True
                        break
                    
            else:
                right_block = True
        else:
            right_block = True
                    
                   
        state.pos = 0
        
        f2=False
        if state.pos + (explore - d*2) >= 0:
            state.pos += (explore - d*2)
            if d == 1 :
                if state.pos == 34 or state.pos == 106 or state.pos == 178 or state.pos == 250 or state.pos == 322 or state.pos == 394 :
                    f2=True
            elif d == 5:
                if state.pos == 66 or state.pos == 138 or state.pos == 210 or state.pos == 282 or state.pos == 354 :
                    f2=True
            elif d == 6:
                if state.pos == 64 or state.pos == 66 or state.pos == 136 or state.pos == 138 or state.pos == 208 or state.pos == 210 or state.pos == 280 or state.pos == 282 or state.pos == 352 or state.pos == 364 :
                    f2=True
            elif d == 7:
                if state.pos == 64 or state.pos == 136 or state.pos == 208 or state.pos == 280 or state.pos == 352:
                    f2=True    
            elif d == 29:
                if state.pos == 6 or state.pos == 78 or state.pos == 150 or state.pos == 222 or state.pos == 294 or state.pos == 366:
                    f2=True
            elif d == 30:
                if state.pos == 4 or state.pos == 6 or state.pos == 76 or state.pos == 78 or state.pos == 148 or state.pos == 150 or state.pos == 220 or state.pos == 222 or state.pos == 292 or state.pos == 294  or state.pos == 364 or state.pos == 366:
                    f2=True
            elif d == 31:
                if state.pos == 4 or state.pos == 34 or state.pos == 46 or state.pos == 76 or state.pos == 106 or state.pos == 112 or state.pos == 148 or state.pos == 178 or state.pos == 190 or state.pos == 220 or state.pos == 250 or state.pos == 262 or state.pos == 292 or state.pos == 322 or state.pos == 334 or state.pos == 364 :
                    f2=True
            elif d == 35:
                 if state.pos == 36 or state.pos == 108 or state.pos == 180 or state.pos == 252 or state.pos == 324:
                     f2=True
            elif d == 37 :
                 if state.pos == 34 or state.pos == 106 or state.pos == 178 or state.pos == 250 or state.pos == 322:
                     f2=True
            elif d == 41:
                if state.pos == 36 or state.pos == 66 or state.pos == 70 or state.pos == 108 or state.pos == 138 or state.pos == 142 or state.pos == 180 or state.pos == 210 or state.pos == 214 or state.pos == 252 or state.pos == 282 or state.pos == 286 or state.pos == 324:
                    f2=True
            elif d == 42:
                 if state.pos == 64 or state.pos == 66 or state.pos == 136 or state.pos == 138 or state.pos == 208 or state.pos == 210 or state.pos == 280 or state.pos == 282:
                    f2=True
            elif d == 43:
                 if state.pos == 64 or state.pos == 136 or state.pos == 208 or state.pos == 280:
                    f2=True
                    
            if not f2:
                while True:
                    p = state.read('bin:2')
                    if p == player:
                        Sum += 1
                        
                        if (state.pos-2)/2 in block:
                            left_block = True
                            break
                        
                        if state.pos - (d*2 + 2) < 0:
                            break
                        
                        state.pos -= (d*2 + 2)
                        
                    else:
                        if p != '00':
                            left_block = True
                        break
            else:
                left_block = True
        else:
                left_block = True
                    
                
        state.pos = 0
        
        if left_block and right_block:
            if Sum >= 4:
                score += 100000
            continue
        if Sum == 2:
            score += 20
        elif Sum == 3:
            score += 1000
        elif Sum >= 4:
            score += 100000
    
    return score

expand_li=[(2,2),(2,3),(3,3),(3,2),(3,1),(2,1),(1,1),(1,2),(1,3),(1,4),(2,4),(3,4),
           (4,4),(4,3),(4,2),(4,1),(3,0),(2,0),(0,2),(0,3),(2,5),(3,5),(5,3),(5,2)]


def expand(state, is_black):
    li=[]
    if is_black:
        tmp=1
    else:
        tmp=2
        
    state.pos = 0
    board = state.read('bin:432')
    Height = state.read('bin:72')
    brd = BitStream(bin=board)
    height=''
    state.pos = 432
    
    for i,j in expand_li:
        h = state.read('bin:3')
        if h != '110': #valid move, height+1
            x = BitArray(bin=h)
            x = x.uint
            pos = ((x*72)+(i*12)+(j*2))
            pos = BitStream(uint=pos, length=9)
            t = tmp << (432-((x*72)+(i*12)+(j*2))-2)
            d = BitStream(uint=t, length=432)
            k = brd | d
            x += 1 #height++
            x = str(BitArray(uint=x,length=3))[2:]
            s = height + x + Height[len(height + x):]
            res = str(k.bin) + s + str(pos.bin)
            res = BitStream(bin=res)
            li.append(res)
        height += h
            
    return li

old_board = [[0]*6 for i in range(6)]

def defence(board):
    global cnt
    global old_board
    new_board = board
    opponent_i = -1
    opponent_j = -1
    for i in range(6):
        for j in range(6):
            if new_board[i][j] != old_board[i][j] and new_board[i][j] == 1:
                opponent_i = i
                opponent_j = j
                
    if (opponent_i, opponent_j) == (1, 1):   #7
        
    elif (opponent_i, opponent_j) == (1, 2): #8
    
    elif (opponent_i, opponent_j) == (1, 3): #9
    
    elif (opponent_i, opponent_j) == (1, 4): #10
    
    elif (opponent_i, opponent_j) == (2, 1): #13
    
    elif (opponent_i, opponent_j) == (2, 2): #14
    
    elif (opponent_i, opponent_j) == (2, 3): #15
    
    elif (opponent_i, opponent_j) == (2, 4): #16
    
    elif (opponent_i, opponent_j) == (3, 1): #19
    
    elif (opponent_i, opponent_j) == (3, 2): #20
    
    elif (opponent_i, opponent_j) == (3, 3): #21
    
    elif (opponent_i, opponent_j) == (3, 4): #22
    
    elif (opponent_i, opponent_j) == (4, 1): #25
    
    elif (opponent_i, opponent_j) == (4, 2): #26
    
    elif (opponent_i, opponent_j) == (4, 3): #27
    
    elif (opponent_i, opponent_j) == (4, 4): #28
    
    
        
    old_board = board
    

first_step=[0,0]
def GetStep(board, is_black):
    """
    Example:

    x = random.randint(0, 5)
    y = random.randint(0, 5)
    return (x, y)
    """
    global b
    global cnt
    if cnt == 32:
        cnt = 0
    if is_black:
        b = True
    else:
        b = False
    
    if cnt == 0:
        if board[0][2][2] != 0:
            cnt+=1
            first_step[0], first_step[1] = 3,3
            return (3,3)
        if board[0][2][3] != 0:
            cnt+=1
            first_step[0], first_step[1] = 3,2
            return (3,2)
        if board[0][3][2] != 0:
            cnt+=1
            first_step[0], first_step[1] = 2,3
            return (2,3)
        cnt+=1
        first_step[0], first_step[1] = 2,2
        return (2,2)
    elif cnt == 1:
        if first_step[0]==2 and first_step[1]==2:
            if board[0][2][3] == 0:
                cnt+=1
                return (2,3)
            if board[0][3][2] == 0:
                cnt+=1
                return (3,2)
            if board[0][3][3] == 0:
                cnt+=1
                return (3,3)
            
        if first_step[0]==2 and first_step[1]==3:
            if board[0][2][2] == 0:
                cnt+=1
                return (2,2)
            if board[0][3][3] == 0:
                cnt+=1
                return (3,3)
            if board[0][3][2] == 0:
                cnt+=1
                return (3,2)
            
        if first_step[0]==3 and first_step[1]==2:
            if board[0][2][2] == 0:
                cnt+=1
                return (2,2)
            if board[0][3][3] == 0:
                cnt+=1
                return (3,3)
            if board[0][2][3] == 0:
                cnt+=1
                return (2,3)
            
        if first_step[0]==3 and first_step[1]==3:
            if board[0][3][2] == 0:
                cnt+=1
                return (3,2)
            if board[0][2][3] == 0:
                cnt+=1
                return (2,3)
            if board[0][2][2] == 0:
                cnt+=1
                return (2,2)
            
    
    s=''
    height = [[0]*6 for i in range(6)]
    # 432 bits board
    for l in range(6):
        for i in range(6):
            for j in range(6):
                if board[l][i][j] == -1:
                    s+='11' #corner
                elif board[l][i][j] == 0:
                    s+='00' #empty
                elif board[l][i][j] == 1:
                    s+='01' #black
                    height[i][j]+=1
                elif board[l][i][j] == 2:
                    s+='10' #white
                    height[i][j]+=1
    # 72 bits height
    for i,j in expand_li:
        if height[i][j]==0:
            s+='000'
        elif height[i][j]==1:
            s+='001'
        elif height[i][j]==2:
            s+='010'
        elif height[i][j]==3:
            s+='011'
        elif height[i][j]==4:
            s+='100'
        elif height[i][j]==5:
            s+='101'
        elif height[i][j]==6:
            s+='110'
    # 9 bits pos
    for i in range(9):
        s+='0'
        
    
    initial = BitStream(bin=s)  
    result = minimax(initial, 0, True, -1, float("inf"))
    cnt += 1
    print('cnt: '+str(cnt))
    return result[0]
    
def game_over(depth):
    global cnt
    if cnt + (depth+1)/2 > 32:
        return True

def get_pos(state):
    state.pos = 504
    position = state.read('bin:9')
    position = BitStream(bin=position)
    position = position.uint
    
    position = position % 72
    row = int(position / 12)
    col = int((position % 12) / 2)
    
    return (row, col)
    
    
                    
def minimax(state, depth, player, alpha, beta):
    global b
    if depth == 3 or game_over(depth):
        return [(-1,-1), evaluation(state)]
    
    if player:
        v = -1
        position = (-1, -1)
        for a in expand(state,b):
            pos = get_pos(a)
            if depth == 0:
                val = evaluation(a)*10
            else:
                val=0
            value = minimax(a, depth+1, False, alpha, beta)
            value[1] += val
            if value[1] > v:
                v = value[1]
                position = pos
            
            #pruning
            if depth != 0:
                if v >= beta:
                    return [position, v]
                alpha=max(alpha,v)
            ###
            
        return [position, v]

    else :
        v = float("inf")
        position = (-1, -1)
        for a in expand(state, not b):
            pos = get_pos(a)
            value = minimax(a, depth+1, True, alpha, beta)
            if value[1] < v:
                v = value[1]
                position = value[0]
            
            #pruning
            if v <= alpha:
                return [position, v]
            beta = min(beta, v)
            ###
            
            
        return [position, v]                


while(True):
    (stop_program, id_package, board, is_black) = STcpClient.GetBoard()
    if(stop_program):
        break

    Step = GetStep(board, is_black)
    STcpClient.SendStep(id_package, Step)
