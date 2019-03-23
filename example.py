# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 03:57:19 2019

@author: Sony
"""

map(lambda x:max(self.strike-x,0),tree_option[:,n-1])


a=am_q()
a.get_rate_f(0.02)
a.get_rate_d(-0.009)
a.get_strike(1)
a.fx_rate_0=0.94
a.risk_sec_0=0.5
a.corr=-0.01
a.fx_vol=0.078
a.risk_s_vol=0.1
(x1,y1,z1,b,up,down,apr_up,apr_down)=a.define_tree_params(0.5,125)


import matplotlib.pyplot as plt


plt.scatter(b[:,1],b[:,0],marker=1, color="black")
plt.scatter(apr_up[:,1],apr_up[:,0], marker='*', color="r")
plt.scatter(apr_down[:,1],apr_down[:,0], marker='*', color="b")
plt.scatter(up[:,1],up[:,0], marker=1,color = "g")
plt.scatter(down[:,1],down[:,0], marker=1, color="aqua")
plt.grid(color='k', linestyle='-', linewidth=0.2)
plt.show()