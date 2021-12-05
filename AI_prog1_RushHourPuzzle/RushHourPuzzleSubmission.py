# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import queue
import time

m=[]
for i in range(6):
    m.append([0]*6)

Input=[]
valid_dir=[] #every car's direction ; 0,2:left,right ; 1,3:up,down
valid_dir.append([-1,-1])
initial_state=""
state_dict={} #dictionary that saves states
car=0

def setting(file): #initialization
    global initial_state
    global car
    
    f=open("prog1_puzzle/"+file+".txt") #read file
    lines=f.readlines()
    
    for line in lines:
        I=[]
        for i in line.split():
            I.append(int(i))
        Input.append(I)
    
    for li in Input: #convert input file to structure the code need
        car+=1
        index=li[0]+1
        y=li[1]
        x=li[2]
        Len=li[3]
        direction=li[4]
        if direction==1:
            valid_dir.append([0,2])
            x1=x
            for i in range(Len):
                m[y][x1]=index
                x1+=1
        else:
            valid_dir.append([1,3])
            y1=y
            for i in range(Len):
                m[y1][x]=index
                y1+=1
             
    for i in m:
        for j in i:
            if j<10:
                initial_state+="0"
            initial_state+=str(j) #translate initial state to string, easy for dict to save

    state_dict[initial_state]=""

#direct: right=0, up=1, left=2, down=3
def move(ind, state, direct):
    tmp_m=[]
    tmp_s=state
    tmp=[]
    for i in range(0,72,2):
        s=int(tmp_s[i]+tmp_s[i+1])
        tmp.append(s)
        if i%12==10:
            tmp_m.append(tmp)
            tmp=[]
            
    target=[]
    for i in range(6):
        for j in range(6):
            if tmp_m[i][j]==ind:
                target.append([i,j])
    
    if direct==0:    #right
        t=target[-1]
        if t[1]<5 and tmp_m[t[0]][t[1]+1]==0:     #valid move
            t2=target[0]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]][t[1]+1]=ind
        else:
            return "0" #invaid move
    
    elif direct==1:  #up
        t=target[0]
        if t[0]>0 and tmp_m[t[0]-1][t[1]]==0:     #valid move
            t2=target[-1]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]-1][t[1]]=ind
        else:
            return "0" #invaid move
        
    elif direct==2:  #left
        t=target[0]
        if t[1]>0 and tmp_m[t[0]][t[1]-1]==0:     #valid move
            t2=target[-1]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]][t[1]-1]=ind
        else:
            return "0" #invaid move
        
    else:            #down
        t=target[-1]
        if t[0]<5 and tmp_m[t[0]+1][t[1]]==0:     #valid move
            t2=target[0]
            tmp_m[t2[0]][t2[1]]=0
            tmp_m[t[0]+1][t[1]]=ind
        else:
            return "0" #invaid move
    
    state_new=""
    for i in tmp_m:
        for j in i:
            if j<10:
                state_new+="0"
            state_new+=str(j) #encode the state to string
    return state_new

def output_route(route): #output all the route to solution.txt
    f=open("solution.txt","w")
    for r in route:
        board=[]
        for i in range(6):
            board.append([0]*6)
        
        row=0
        col=0
        for i in range(0,72,2):
            board[row][col]=int(r[i]+r[i+1])-1
            col+=1
            if (i+1)%12==11:
                row+=1
                col=0
        '''
        for i in board:
            for j in i:
                print(str(j-1),end=' ',file=f)
            print(file=f)
        print(file=f)
        '''
        
        for c in range(car):
            ok=False
            for i in range(6):
                for j in range(6):
                    if board[i][j]==c:
                        print(str(c)+' '+str(i)+' '+str(j),file=f)
                        ok=True
                        break
                if ok:
                    break
        print(file=f)
    f.close()
    

def find_route(state_dict,terminal_state): #find route by dictionary mapping
    route=[]                               #dict[new_state]=now_state
    route.append(terminal_state)
    st=terminal_state
    while st!="":                          #dict[initial_state]=""
        st=state_dict[st]
        route.append(st)
    route.pop()
    route.reverse()
    output_route(route)
    return route

def depth_state_analyze(depth_state_num): #output number of searched states for each depth
    print()
    m=max(depth_state_num)+1
    for i in range(m):
        print('depth '+str(i)+': '+str(depth_state_num.count(i))+' states')
    print()
            
#BFS
def sol_BFS(initial_state):
    
    q=queue.Queue()              #queue which saves states
    q.put(initial_state)
    
    q_cnt=queue.Queue()          #queue which saves number of depth
    q_cnt.put(0)
    terminal_state=""
    depth_state_num_BFS=[]       #list which saves number of depth
    depth_state_num_BFS.append(0)
    
    while not q.empty():
        
        now_state=q.get()
        c=q_cnt.get()    
        
        if now_state[34]=="0" and now_state[35]=="1": #finish
            terminal_state=now_state
            for i in range(0,72,2):
                print(now_state[i]+now_state[i+1]+' ',end='')
                if (i+1)%12==11:
                    print()
            break
        
        for i in range(car):    
            new_state1=move(i+1,now_state,valid_dir[i+1][0]) #find valid move in one direction
            new_state2=move(i+1,now_state,valid_dir[i+1][1]) #find valid move in other direction 
            if new_state1!="0" and state_dict.get(new_state1)==None: #push valid state in queue
                q.put(new_state1)
                state_dict[new_state1]=now_state #put searched states in dictionary (dict[new_state]=now_state)
                q_cnt.put(c+1)
                depth_state_num_BFS.append(c+1)  #depth counter++
                
            if new_state2!="0" and state_dict.get(new_state2)==None: #push valid state in queue
                q.put(new_state2)
                state_dict[new_state2]=now_state #put searched states in dictionary (dict[new_state]=now_state)
                q_cnt.put(c+1)
                depth_state_num_BFS.append(c+1)  #depth counter++

    BFS_route=find_route(state_dict,terminal_state)
    print('BFS route: '+str(len(BFS_route)-1)+' steps.')
    depth_state_analyze(depth_state_num_BFS)

def BFS():
    print('BFS:')
    s=time.time()
    sol_BFS(initial_state)
    t=time.time()
    print('exe time: '+str(t-s))
    print('dict len: '+str(len(state_dict)))


solve=False
depth_state_num_DFS=[]
terminal_state=""
#DFS  
def sol_DFS(state,depth): #recursive to get the answer
    global solve
    global terminal_state
    if solve==True:       #if answer already got, return
        return
    
    depth_state_num_DFS.append(depth)

    if state[34]=="0" and state[35]=="1": #finish
        terminal_state=state
        for i in range(0,72,2):
            print(state[i]+state[i+1]+' ',end='')
            if (i+1)%12==11:
                print()
        solve=True
        return
    for i in range(car):
        new_state1=move(i+1,state,valid_dir[i+1][0])
        new_state2=move(i+1,state,valid_dir[i+1][1])
        if new_state1!="0" and state_dict.get(new_state1)==None:
            state_dict[new_state1]=state #put state in dict
            depth+=1
            sol_DFS(new_state1,depth)    #recursive
            if solve==True:
                return
            del state_dict[new_state1]   #backtracking
            depth-=1                     #backtracking
        if new_state2!="0" and state_dict.get(new_state2)==None:
            state_dict[new_state2]=state #put state in dict
            depth+=1
            sol_DFS(new_state2,depth)    #recursive
            if solve==True:
                return
            del state_dict[new_state2]   #backtracking
            depth-=1                     #backtracking
            
def DFS():
    print('DFS:')  
    state_dict.clear()
    state_dict[initial_state]=""
    s=time.time()          
    sol_DFS(initial_state,0)  
    t=time.time()   
    DFS_route=find_route(state_dict,terminal_state)   
    print('DFS route: '+str(len(DFS_route)-1)+' steps.')
    depth_state_analyze(depth_state_num_DFS)
    print('exe time: '+str(t-s))
    print('dict len: '+str(len(state_dict)))

depth_state_num=[]
dict_len=[]
solve=False
terminal_state=""
#IDS    
def sol_IDS(state,depth,max_depth): 
    global solve
    global terminal_state
    
    if depth>=max_depth:  #if depth exceeded the limit, forcing return 
        dict_len.append(str(len(state_dict)))
        depth_state_num.append(depth)
        return
    if solve==True:
        return

    if state[34]=="0" and state[35]=="1": #finish
        terminal_state=state
        for i in range(0,72,2):
            print(state[i]+state[i+1]+' ',end='')
            if (i+1)%12==11:
                print()
        
        solve=True
        return
    for i in range(car):
        new_state1=move(i+1,state,valid_dir[i+1][0])
        new_state2=move(i+1,state,valid_dir[i+1][1])
        if new_state1!="0" and state_dict.get(new_state1)==None:
            state_dict[new_state1]=state
            depth+=1
            sol_IDS(new_state1,depth,max_depth)  #recursive
            if solve==True:
                return
            depth-=1                             #backtracking
            del state_dict[new_state1]           #backtracking
        if new_state2!="0" and state_dict.get(new_state2)==None:
            state_dict[new_state2]=state
            depth+=1
            sol_IDS(new_state2,depth,max_depth)  #recursive
            if solve==True:
                return
            depth-=1                             #backtracking
            del state_dict[new_state2]           #backtracking
            
def IDS():
    print('IDS:')
    s=time.time()
    for i in range(1,100):                       #gradually add the limit by 1
        state_dict.clear()
        state_dict[initial_state]=""
        sol_IDS(initial_state,0,i)
        if solve==True:
            break
    t=time.time()
    IDS_route=find_route(state_dict,terminal_state)
    print('IDS route: '+str(len(IDS_route)-1)+' steps.')
    depth_state_analyze(depth_state_num)
    
    print('exe time: '+str(t-s))    
    print('dict len: '+str(max(dict_len)))


class state_node:  #node use for A* and IDA*
    def __init__(self,s,n):
        self.state=s
        self.step=n          
        
    def g(self):
        return self.step
        
    def h(self): #count the number of car that block in front of the red car 
        target_row=[]
        s=self.state[24:36]
        for i in range(0,12,2):
            s1=int(s[i]+s[i+1])
            target_row.append(s1)
        cnt=0
        for i in reversed(target_row):
            if i==1:
                break
            if i!=0:
                cnt+=1
        return cnt
        
    
    def f(self): #f()=g()+h()
        return self.g()+self.h()

def sol_A_Star(initial_state):    
    state_dict.clear()
    state_dict[initial_state]=""
    
    start=state_node(initial_state,0)
    state_list=[]
    state_list.append(start)
    while True:
        li=[]
        for nodes in state_list:
            li.append(nodes.f())
        
        current_node=state_list[li.index(min(li))] #current_node = node who has minimum f
        state_list.remove(current_node)            #remove current node in state_list
        
        now_state=current_node.state  
        
        if now_state[34]=="0" and now_state[35]=="1": #finish
            terminal_state=now_state
            for i in range(0,72,2):
                print(now_state[i]+now_state[i+1]+' ',end='')
                if (i+1)%12==11:
                    print()
            break
        
        for i in range(car):    
            new_state1=move(i+1,now_state,valid_dir[i+1][0])
            new_state2=move(i+1,now_state,valid_dir[i+1][1])
            if new_state1!="0" and state_dict.get(new_state1)==None: #push in state_list
                new_node=state_node(new_state1,current_node.step+1)
                state_list.append(new_node)
                state_dict[new_state1]=now_state
                
            if new_state2!="0" and state_dict.get(new_state2)==None: #push in state_list
                new_node=state_node(new_state2,current_node.step+1)
                state_list.append(new_node)
                state_dict[new_state2]=now_state
                
        
    A_star_route=find_route(state_dict,terminal_state)
    print('A* route: '+str(len(A_star_route)-1)+' steps.')

def A_Star():   
    print('A*:')
    s=time.time()
    sol_A_Star(initial_state)
    t=time.time()
    print('exe time: '+str(t-s))
    print('dict len: '+str(len(state_dict)))


terminal_state=""
solve=False
depth_state_num=[]
dict_len=[]
def sol_IDA_star(node,limit):
    global solve
    global terminal_state
    if node.f()>=limit:  #if node's f exceed the limit, forcing return
        depth_state_num.append(limit)
        dict_len.append(str(len(state_dict)))
        return
    if solve==True:
        return
    state=node.state
    if state[34]=="0" and state[35]=="1": #finish
        terminal_state=state
        for i in range(0,72,2):
            print(state[i]+state[i+1]+' ',end='')
            if (i+1)%12==11:
                print()
        solve=True
        return
    for i in range(car):
        new_state1=move(i+1,state,valid_dir[i+1][0])
        new_state2=move(i+1,state,valid_dir[i+1][1])
        if new_state1!="0" and state_dict.get(new_state1)==None:
            new_node=state_node(new_state1,node.step+1)
            state_dict[new_state1]=state
            sol_IDA_star(new_node,limit)  #recursive
            if solve==True:
                return
            del state_dict[new_state1]    #backtracking
        if new_state2!="0" and state_dict.get(new_state2)==None:
            new_node=state_node(new_state2,node.step+1)
            state_dict[new_state2]=state
            sol_IDA_star(new_node,limit)  #recursive
            if solve==True:
                return
            del state_dict[new_state2]    #backtracking

def IDA_Star():
    print('IDA*:')
    s=time.time()
    for i in range(1,100):                #gradually add the limit by 1
        state_dict.clear()
        state_dict[initial_state]=""
        start=state_node(initial_state,0)
        sol_IDA_star(start,i)
        if solve==True:
            break
    t=time.time()
    
    IDA_star_route=find_route(state_dict,terminal_state)
    print('IDA* route: '+str(len(IDA_star_route)-1)+' steps.') 
    depth_state_analyze(depth_state_num)
    print('exe time: '+str(t-s))
    print('dict len: '+str(max(dict_len)))


select_algo=int(input('1: BFS  2: DFS  3: IDS  4: A*  5: IDA*  input: '))
select_file=input('file: ')
print()
setting(select_file)
if select_algo==1:
    BFS()
elif select_algo==2:
    DFS()
elif select_algo==3:
    IDS()
elif select_algo==4:
    A_Star()
else:
    IDA_Star()

    


