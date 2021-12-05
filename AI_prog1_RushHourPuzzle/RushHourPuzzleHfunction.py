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

f=open("prog1_puzzle/L02.txt")
lines=f.readlines()
Input=[]
for line in lines:
    I=[]
    for i in line.split():
        I.append(int(i))
    Input.append(I)

#Input=[[0,2,3,2,1],[1,0,0,3,1],[2,1,3,3,1],[3,3,1,2,1],[4,5,0,3,1],[5,1,0,2,2],[6,3,0,2,2],[7,1,2,2,2],[8,3,3,3,2],[9,4,4,2,2],[10,2,5,2,2],[11,4,5,2,2]]


valid_dir=[]
valid_dir.append([-1,-1])
car=0

for li in Input:
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
            
initial_state=""
for i in m:
    for j in i:
        if j<10:
            initial_state+="0"
        initial_state+=str(j)

#easy_state="070202020000070000090011000101091011030303001011000008040400050508060600"
#initial_state=easy_state

state_dict={}
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
    
    #print(tmp_m)
    state_new=""
    for i in tmp_m:
        for j in i:
            if j<10:
                state_new+="0"
            state_new+=str(j)
    return state_new

def find_route(state_dict,terminal_state):
    route=[]
    route.append(terminal_state)
    st=terminal_state
    while st!="":
        st=state_dict[st]
        route.append(st)
    route.pop()
    route.reverse()
    return route

def depth_state_analyze(depth_state_num):
    print()
    m=max(depth_state_num)+1
    for i in range(m):
        print('depth '+str(i)+': '+str(depth_state_num.count(i))+' states')
    print()
            
#BFS
print('BFS:')

def BFS(initial_state):
    
    q=queue.Queue()
    q.put(initial_state)
    
    q_cnt=queue.Queue()
    q_cnt.put(0)
    terminal_state=""
    depth_state_num_BFS=[]
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
                
            #print('\nstep: '+str(c))
            break
        
        for i in range(car):    
            new_state1=move(i+1,now_state,valid_dir[i+1][0])
            new_state2=move(i+1,now_state,valid_dir[i+1][1])
            if new_state1!="0" and state_dict.get(new_state1)==None: #push in queue
                q.put(new_state1)
                state_dict[new_state1]=now_state
                q_cnt.put(c+1)
                depth_state_num_BFS.append(c+1)
                
            if new_state2!="0" and state_dict.get(new_state2)==None: #push in queue
                q.put(new_state2)
                state_dict[new_state2]=now_state
                q_cnt.put(c+1)
                depth_state_num_BFS.append(c+1)

    BFS_route=find_route(state_dict,terminal_state)
    #for r in BFS_route:
    #    print(r)
    
    print('BFS route: '+str(len(BFS_route)-1)+' steps.')
    #depth_state_analyze(depth_state_num_BFS)

s=time.time()
BFS(initial_state)
t=time.time()
print('exe time: '+str(t-s))
print('dict len: '+str(len(state_dict)))

class state_node:
    def __init__(self,s,n):
        self.state=s
        self.step=n
        
        self.board=[]
        tmp=[]
        for i in range(0,72,2):
            s1=int(s[i]+s[i+1])
            tmp.append(s1)
            if i%12==10:
                self.board.append(tmp)
                tmp=[]
        
        
    def g(self):
        return self.step
    '''
    def h(self):  
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
    '''
    
    def h(self): #count the number of car that block in front of the red car 
        blocking=[]
        target_row=[]
        s=self.state[24:36]
        for i in range(0,12,2):
            s1=int(s[i]+s[i+1])
            target_row.append(s1)
        
        for i in reversed(target_row):
            if i==1:
                break
            if i!=0:
                blocking.append(i)
        return blocking
    
    
    def num_block(self,car):
        tmp_j=-1
        b=2
        for i in range(6):
            for j in range(6):
                if self.board[i][j]==car:
                    tmp_j=j
        for i in range(1,5):
            if self.board[i][tmp_j]==car and self.board[i-1][tmp_j]==0:
                b-=1
            if self.board[i][tmp_j]==car and self.board[i+1][tmp_j]==0:
                b-=1
        return b        
        
    
    def advanced_h(self):
        blocking_red_car=self.h()
        cnt=len(blocking_red_car)
        for i in blocking_red_car:
            cnt+=self.num_block(i)
        return cnt
            
        
        car_visited=[]
        cnt=len(blocking_red_car)
        blocking_car=[]
        for i in blocking_red_car:
            blocking_car.append(i)
        
        while len(blocking_car)!=0:
            b=[]
            for i in blocking_car:
                if i not in car_visited:
                    b_tmp=self.get_blocking_car_index(i)
                    if b_tmp!=None:
                        cnt+=len(b_tmp)
                        for j in b_tmp:
                            b.append(j)
                    car_visited.append(i)
            blocking_car=b[:]
        
        return cnt
    
    
    def f(self): #f()=g()+h()
        return self.g()+self.advanced_h()
        #return self.g()+self.h()

def A_Star(initial_state):    
    state_dict.clear()
    state_dict[initial_state]=""
    
    start=state_node(initial_state,0)
    state_list=[]
    state_list.append(start)
    print('\nA*:')
    while True:
        #li=[]
        min_index=-1
        min_f=1000
        for i in range(len(state_list)):
            nodes=state_list[i]
            #li.append(nodes.f())
            if nodes.f()<min_f:
                min_f=nodes.f()
                min_index=i
        
        current_node=state_list[min_index] #current_node=node who has minimum f
        state_list.remove(current_node)
        
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

s=time.time()
A_Star(initial_state)
t=time.time()
print('exe time: '+str(t-s))
print('dict len: '+str(len(state_dict)))






