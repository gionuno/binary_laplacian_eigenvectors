#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 22:56:03 2019

@author: gionuno
"""

import numpy as np;

import scipy.io as sciio;
import scipy.sparse.linalg as sparselinalg;

import matplotlib.image as img;
import matplotlib.pyplot as plt;


def get_eigenfunc(D,n):
    x = np.argwhere(D);
    K = np.zeros((x.shape[0],x.shape[0]));
    print(K.shape);
    for i in range(x.shape[0]):
        for j in range(x.shape[0]):
            if i != j:
                dij = -0.5*np.linalg.norm(x[i,:]-x[j,:]);
                K[i,j] = dij;
    _,V = sparselinalg.eigs(K,k=n);
    rV = np.zeros((n,D.shape[0],D.shape[1]));
    for k in range(n):
        for l in range(K.shape[1]):
            rV[k,x[l,0],x[l,1]] = V[l,k];
    return x,K,rV;

A = sciio.loadmat("caltech101_silhouettes_28.mat");




classes = [a[0] for a in A['classnames'].reshape((-1,))];
X = A['X'];
Y = A['Y'].reshape((-1,));

T = {c:np.zeros((0,28,28)) for c in classes};

for i in range(X.shape[0]):
    c = classes[Y[i]-1];
    T[c] = np.concatenate((T[c],1.0-X[i].reshape((1,28,28))),axis=0);
    

s = 10;

D = np.copy(T['octopus'][16,:,:]).T;
xD,KD,VD = get_eigenfunc(D,s*s);

f, ax = plt.subplots(s,s);

for i in range(s):
    for j in range(s):
        ax[i,j].imshow(VD[s*i+j,:,:],cmap='seismic');
        ax[i,j].set_axis_off();
plt.show();



H = np.mean(img.imread("buddha_lotus.png"),axis=2);
H = 0.5*(np.fliplr(H)+H);

D = H<0.25;
xH,kH,vH = get_eigenfunc(D,s*s);

f, ax = plt.subplots(s,s);
for i in range(s):
    for j in range(s):
        ax[i,j].imshow(vH[s*i+j,:,:],cmap='seismic');
        ax[i,j].set_axis_off();
plt.show();

f,ax = plt.subplots(1,2);
ax[0].imshow(H,cmap='gray');
ax[0].set_axis_off();
ax[1].imshow(kH,cmap='gray');
ax[1].set_axis_off();
plt.show();