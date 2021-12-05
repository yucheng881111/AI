# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import queue
import os
import time

m=[]
for i in range(6):
    m.append([0]*6)

Input=[[0,2,3,2,1],[1,0,0,3,1],[2,1,3,3,1],[3,3,1,2,1],[4,5,0,3,1],[5,1,0,2,2],[6,3,0,2,2],[7,1,2,2,2],[8,3,3,3,2],[9,4,4,2,2],[10,2,5,2,2],[11,4,5,2,2]]

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

state_dict={}
state_dict[initial_state]=""

#direct: right=0, up=1, left=2, down=3
def shift(ind, state, direct):
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
            

q=queue.Queue()
q.put(initial_state)

q_cnt=queue.Queue()
q_cnt.put(0)
terminal_state=""

while not q.empty():
    
    now_state=q.get()
    c=q_cnt.get()    
    
    if now_state[34]=="0" and now_state[35]=="1": #finish
        terminal_state=now_state
        for i in range(0,72,2):
            print(now_state[i]+now_state[i+1]+' ',end='')
            if (i+1)%12==11:
                print()
            
        print('\nstep: '+str(c))
        break
    
    for i in range(car):    
        new_state1=shift(i+1,now_state,valid_dir[i+1][0])
        new_state2=shift(i+1,now_state,valid_dir[i+1][1])
        if new_state1!="0" and state_dict.get(new_state1)==None: #push in queue
            q.put(new_state1)
            state_dict[new_state1]=now_state
            q_cnt.put(c+1)
            
        if new_state2!="0" and state_dict.get(new_state2)==None: #push in queue
            q.put(new_state2)
            state_dict[new_state2]=now_state
            q_cnt.put(c+1)
            
route=[]
route.append(terminal_state)
st=terminal_state
while st!="":
    st=state_dict[st]
    route.append(st)
route.pop()
route.reverse()

time.sleep(0.5)
os.system('cls||clear')
from colored import fg, bg, attr

for r in route:
    for i in range(0,72,2):
        #print(r[i]+r[i+1]+' ',end='')
        tmp_r=r[i]+r[i+1]
        if int(tmp_r)==1:
            print('%s%s%s ' % (fg(1),'█',attr(0)), end='')
        elif int(tmp_r)==2:
            print('%s%s%s ' % (fg(11),'█',attr(0)), end='')
        elif int(tmp_r)==3:
            print('%s%s%s ' % (fg(127),'█',attr(0)), end='')
        elif int(tmp_r)==4:
            print('%s%s%s ' % (fg(93),'█',attr(0)), end='')
        elif int(tmp_r)==5:
            print('%s%s%s ' % (fg(2),'█',attr(0)), end='')
        elif int(tmp_r)==6:
            print('%s%s%s ' % (fg(190),'█',attr(0)), end='')
        elif int(tmp_r)==7:
            print('%s%s%s ' % (fg(199),'█',attr(0)), end='')
        elif int(tmp_r)==8:
            print('%s%s%s ' % (fg(214),'█',attr(0)), end='')
        elif int(tmp_r)==9:
            print('%s%s%s ' % (fg(21),'█',attr(0)), end='')
        elif int(tmp_r)==10:
            print('%s%s%s ' % (fg(14),'█',attr(0)), end='')
        elif int(tmp_r)==11:
            print('%s%s%s ' % (fg(27),'█',attr(0)), end='')
        elif int(tmp_r)==12:
            print('%s%s%s ' % (fg(79),'█',attr(0)), end='')
        else:
            print('%s%s%s ' % (fg(255),'█',attr(0)), end='')

        if (i+1)%12==11:
            print('\n')
    #print()
    time.sleep(0.8)
    os.system('cls||clear')



    


            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


