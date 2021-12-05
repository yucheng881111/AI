# -*- coding: utf-8 -*-
"""
Created on Sat May 29 01:55:50 2021

@author: user
"""

import numpy as np
import pandas as pd
from sklearn import datasets, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import random

def use_sklearn(x_train, x_test, y_train, y_test):
    clf = DecisionTreeClassifier(criterion='gini',max_depth=5)
    clf = clf.fit(x_train,y_train)
    y_pred = clf.predict(x_test)
    
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    '''
    export_graphviz(clf, out_file='ttt.txt',  
                    filled=True, rounded=True,
                    special_characters=True,feature_names=['mcg','gvh','lip','chg','aac','alm1','alm2'],class_names=echoli_target_t)
    '''
    clf = RandomForestClassifier(n_estimators=20, max_depth=5)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

def iris():
    iris = datasets.load_iris()
    x_train, x_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.3)
    #use_sklearn(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test
def wine():
    wine = datasets.load_wine()
    x_train, x_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.3)
    #use_sklearn(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test
def breast_cancer():
    breast_cancer = datasets.load_breast_cancer()
    x_train, x_test, y_train, y_test = train_test_split(breast_cancer.data, breast_cancer.target, test_size=0.3)
    #use_sklearn(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test
def digits():
    digits = datasets.load_digits()
    x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.3)
    #use_sklearn(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test

def ecoli():
    ecoli = pd.read_csv('ecoli.data', header=None)
    ecoli_data = []
    ecoli_target = []
    for i in range(len(ecoli)):
        a = ecoli[0][i].split()
        li = [float(i) for i in a[1:8]]
        ecoli_data.append(li)
        ecoli_target.append(a[8])
        
    ecoli_data = np.array(ecoli_data)
    
    echoli_target_t = list(set(ecoli_target))
    e = []
    for i in ecoli_target:
        for j in range(len(echoli_target_t)):
            if echoli_target_t[j] == i:
                e.append(j)
                break
    
    ecoli_target = np.array(e)
    x_train, x_test, y_train, y_test = train_test_split(ecoli_data, ecoli_target, test_size=0.3)
    #use_sklearn(x_train, x_test, y_train, y_test)
    return x_train, x_test, y_train, y_test

x_train, x_test, y_train, y_test = wine()
feature_size = len(x_train[0])
target_size = len(set(y_train))


class node:
    def __init__(self,feature,target):
        self.feature=feature
        self.target=target
        self.attr_ind=-1
        self.attr_val=-1
        self.left=None
        self.right=None
        self.attr=-1
    
    def get_attr(self):
        global target_size
        cnt = []
        for i in range(target_size):
            cnt.append(self.target.tolist().count(i))
            
        m = -1
        ind = -1
        for i in range(len(cnt)):
            if cnt[i] > m:
                m = cnt[i]
                ind = i
                
        self.attr = ind       
        
        
    def is_terminate(self):
        global target_size
        cnt = []
        for i in range(target_size):
            cnt.append(self.target.tolist().count(i))
        
        if cnt.count(0) == len(cnt) - 1:
            for i in range(len(cnt)):
                if cnt[i] != 0:
                    self.attr = i
                    break
            return True
        return False
    
        

def calc_gini(li,li_y):    
    global feature_size
    l = len(li_y)
    g_min = 10000
    g_ind = -1
    g_m = 10000
    
    if li.size == 0:
        return 0,0
    
    #i = random.randint(0,feature_size-1)
    for i in range(feature_size):
        attr = li[:,i]
        tmp_attr = sorted(attr)
        m_li = []
        for j in range(len(attr)-1):
            m_li.append((tmp_attr[j]+tmp_attr[j+1])/2)
        
        for m in m_li:
            y_right = []
            y_left = []
            for j in range(l):
                if li[j][i] > m:
                    y_right.append(li_y[j])
                else:
                    y_left.append(li_y[j])
                    
            gini_right = 0
            gini_left = 0
            if len(y_right) != 0:
                gini_right = 1 - ((y_right.count(0)/len(y_right))**2 + (y_right.count(1)/len(y_right))**2 + (y_right.count(2)/len(y_right))**2)
            else:
                continue
            if len(y_left) != 0:
                gini_left = 1 - ((y_left.count(0)/len(y_left))**2 + (y_left.count(1)/len(y_left))**2 + (y_left.count(2)/len(y_left))**2)
            else:
                continue
            gini = len(y_right) * gini_right + len(y_left) * gini_left
            if gini < g_min:
                g_min = gini
                g_ind = i
                g_m = m
            
    return g_ind, g_m


def tree(n,depth):
    if n.is_terminate():
        return
    
    if depth == 5:
        n.get_attr()
        return
    
    x = n.feature
    y = n.target
    a,m = calc_gini(x,y)
    n.attr_ind = a
    n.attr_val = m
    
    y_right = []
    x_right = []
    y_left = []
    x_left = []
    for i in range(len(y)):
        if x[i][a] > m:
            y_right.append(y[i])
            x_right.append(x[i])
        else:
            y_left.append(y[i])
            x_left.append(x[i])
            
    x_left = np.array(x_left)
    y_left = np.array(y_left)
    x_right = np.array(x_right)
    y_right = np.array(y_right)
    
    node_left = node(x_left,y_left)
    node_right = node(x_right,y_right)
    n.left = node_left
    n.right = node_right
    
    tree(n.left, depth+1)
    tree(n.right, depth+1)
    
root = node(x_train,y_train)
tree(root,0)
    

def evaluation(root,t):
    curr = root
    ans = -1
    while curr != None:
        if t[curr.attr_ind] > curr.attr_val:
            ans = curr.attr
            curr = curr.right
        else:
            ans = curr.attr
            curr = curr.left
            
    return ans

correct = 0
pred = []
for i in range(len(y_test)):
    result = evaluation(root,x_test[i])
    pred.append(result)
    if result == y_test[i]:
        correct += 1

print('Decision Tree:')
print(confusion_matrix(y_test, pred))
print(classification_report(y_test, pred))

def confusion_matrix_element_precision(cm, i):
    try:
        cm2 = cm[i].tolist()
    except:
        return 0
    acc = 0
    if sum(cm2) != 0:
        acc = cm2[i]/sum(cm2)
    return acc
    
# random forest tree bagging
trees = []
ac_score = []
for i in range(20):
    num = random.randint(1,1000)
    x_train1, x_test1, y_train1, y_test1 = train_test_split(x_train, y_train, test_size=0.3, random_state=num)
    root = node(x_train1,y_train1)
    tree(root,0)
    trees.append(root)
    pred = []
    for j in range(len(y_test1)):
        result = evaluation(root,x_test1[j])
        pred.append(result)
    cm = confusion_matrix(y_test1, pred)
    ele = []
    for j in range(target_size):
        ele.append(confusion_matrix_element_precision(cm, j))
        ac_score.append(ele)

rf_pred = []
for i in range(len(y_test)):
    vote = []
    for r in trees:
        res = evaluation(r,x_test[i])
        vote.append(res)
    #rf_pred.append(max(vote))
    k = [0] * target_size
    for j in range(target_size):
        for v in range(20):
            if vote[v] == j:
                k[j] += ac_score[v][j]
    m = -1
    ind = -1
    for j in range(target_size):
        if k[j] > m:
            m = k[j]
            ind = j
    rf_pred.append(ind)
        

print('Random Forest:')
print(confusion_matrix(y_test, rf_pred))
print(classification_report(y_test, rf_pred))








