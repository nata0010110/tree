# -*- coding: utf-8 -*-
import numpy as np
class am_q:
    def get_risky_sec_vector(self,vec):
        self.risk_sec_0=vec[0]
        self.risk_sec=get_return(vec)*len(vec)
    def get_fx_rate_vector(self,vec):
        self.fx_rate_0=vec[0]
        self.fx_rate=get_return(vec)*len(vec)
    def get_rate_f(self,rate):
        self.rate_f=rate
    def get_rate_d(self,rate):
        self.rate_d=rate
    def get_strike(self,strike):
        self.strike=strike
    def compute_vol_corr(self):
        self.corr=np.corrcoef(self.risk_s,self.fx_rate)
        self.fx_vol=np.std(self.fx_rate)
        self.risk_s_vol=np.std(self.risk_s)
    def define_tree_params(self,maturity,n,type_of_quanto=1):
        self.dt=maturity/n
        self.u=np.exp(self.risk_s_vol*self.dt**0.5)
        self.d=np.exp(-self.risk_s_vol*self.dt**0.5)
        self.mu=(self.rate_f-self.corr*self.fx_vol*self.risk_s_vol)
        self.q=(np.exp(self.mu*self.dt)-self.d)/(self.u-self.d)
        print(self.dt)
        print(self.u)
        print(self.d)
        print(self.mu)
        print(self.q)
        
        tree=np.zeros((n+1,n+1))
        tree_option=np.zeros((n+1,n+1))
        tree_flag=np.zeros((n+1,n+1))
        tree[0,0]=self.risk_sec_0
        for i in range(1,n+1):
            tree[0,i]=tree[0,i-1]*self.u
            for j in range(1,i+1):
                tree[j,i]=tree[j-1,i-1]*self.d
        for j in range(n+1):
            tree_option[j,n]=max(float(self.strike)-tree[j,n],0)
            if float(self.strike)-tree[j,n]>0:
                tree_flag[j,n]=1
            else:
                tree_flag[j,n]=0
                
        for i in range(n-1,-1,-1):
            for j in range(0,i+1):
                tree_option[j,i]=max(self.strike-tree[j,i],
                        np.exp(-self.rate_d*self.dt)*
                        (self.q*(tree_option[j,i+1])+(1-self.q)*(tree_option[j+1,i+1])))
                if self.strike-tree[j,i]> np.exp(-self.rate_d*self.dt)*(self.q*(tree_option[j,i+1])+(1-self.q)*(tree_option[j+1,i+1])):
                    tree_flag[j,i]=1
                else:
                    tree_flag[j,i]=0
        (tree_borders,tree_up_b,tree_down_b)=for_graph_am_q(tree,tree_option,tree_flag,self.dt)
        (appr_up,appr_down)=self.bound_appr(maturity,tree)
        return(tree,tree_option,tree_flag,tree_borders,tree_up_b,tree_down_b,appr_up,appr_down)
    def bound_appr(self,T,tree):
            dt=T/(len(tree[0])-1)
            tree_up_b=np.empty(shape=[0, 2])
            tree_down_b=np.empty(shape=[0, 2])
            for i in range(len(tree[0])):
                max_tree=tree[0,i]
                min_tree=tree[i,i]
                up=self.strike*(1-self.risk_s_vol*(
                                (T-i*dt)*np.log(
                                self.risk_s_vol**2/8/np.pi
                                /(self.rate_f-self.fx_vol*self.risk_s_vol)**2)
                                )**0.5)
                down=self.rate_d*self.strike/(self.rate_d-(self.rate_f-self.corr*self.fx_vol*self.risk_s_vol))*(1+0.638*self.risk_s_vol*(T-dt*i)**0.5)
                print(up)
                print(down)
                if up<=max_tree:
                    tree_up_b=np.append(tree_up_b,[[up,i*dt]],axis=0)
                if down>=min_tree:
                    tree_down_b=np.append(tree_down_b,[[down,i*dt]],axis=0)
            return(tree_up_b,tree_down_b)
            

def get_return(vec):
    ret=np.fromiter(range((len(vec)-1)), dtype="float")
    for i in range(len(vec)-1):
        ret[i]=np.log(float(vec[i+1])/float(vec[i]))
    return(ret)
def for_graph_am_q(tree,tree_option,tree_flag,dt):
    tree_borders=np.empty(shape=[0, 2])
    tree_up_b=np.empty(shape=[0, 2])
    tree_down_b=np.empty(shape=[0, 2])
    for i in range(len(tree[0])):
        tree_borders=np.append(tree_borders,[[tree[0,i],i*dt]],axis=0)
        tree_borders=np.append(tree_borders,[[tree[i,i],i*dt]],axis=0)
        for j in range(i-1):
            if tree_flag[j,i]==0 and tree_flag[j+1,i]==1:
                tree_up_b=np.append(tree_up_b,[[tree[j+1,i],i*dt]],axis=0)
            if tree_flag[j,i]==1 and tree_flag[j+1,i]==0:
                tree_down_b=np.append(tree_down_b,[[tree[j+1,i],i*dt]],axis=0)
    return(tree_borders,tree_up_b,tree_down_b)
        
