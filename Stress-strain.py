# -*- coding: utf-8 -*-
"""
Created on Wed Jan  5 20:32:56 2022

@author: KO
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import glob
import os
from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression
from io import StringIO



#%% Stress - strain graph
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import glob
import os

from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression

from io import StringIO
from natsort import natsorted

#Appearance stuff (colors, font size etc)

#My colors
# mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5'])
#                                                       0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry3


# mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#e41a1c','#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#dede00'])

# Nature colors
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['0C5DA5', 'FF2C00', 'FF9500', '00B945', '845B97', '474747', '9e9e9e'])

#Seaborn colors
# colors=sns.color_palette("rocket",3)

# Font size. Dictionary taking numerous parameters.
plt.rcParams.update({'font.size' : 12})

# Coupon dimensions in order of file loading
thickness=[2.93666288,2.883306388,2.966662919,2.963329587,2.933329548,2.914995712,2.966662919,2.973329599,2.926572111,2.893329496] #d in mm
width=[11.8633324,11.88666573,11.73333239,11.92666573,11.97666574,11.92666573,11.8533324,11.74999716,12.03999723,12.03999723] #b in mm
#Span length in mm
L=40.28

# Gets current working directory (cwd)
cwd=os.getcwd()

#Creates a folder to store the graphs inside the cwd
mesa= cwd+ '\\CF 80 mm graphs\\'
if not os.path.exists(mesa):
    os.makedirs(mesa)

#Path to data. Full path if in different folder than this script is. Otherwise *files common name part*".
file_list = [i for i in glob.glob(r"C:/Users/KO/OneDrive - University of Patras/Επιφάνεια εργασίας/PLA uncut data/*")]
#Sort in order of number appearing in front. Omit or adjust accordingly in case of different naming.
file_list=natsorted(file_list)

# Loading all the csv files to create a list of data frames
data = [pd.read_csv(file,names=["Displacement","Force",'Time'],skiprows=270, delimiter=' ') for file in file_list]

#Replaces the useless part of the dataframes' names to auto-generate a better suited legend.
file_list=[file.replace("C:/Users/KO/OneDrive - University of Patras/Επιφάνεια εργασίας/PLA uncut data\\", '') for file in file_list]
file_list=[file.replace('.dat','') for file in file_list]
file_list=[file.replace('s','#') for file in file_list]

file_list=[file.replace("1_", '') for file in file_list]
file_list=[file.replace("2_", '') for file in file_list]
file_list=[file.replace("3_", '') for file in file_list]
file_list=[file.replace("4_", '') for file in file_list]
file_list=[file.replace("5_", '') for file in file_list]
file_list=[file.replace("6_", '') for file in file_list]
file_list=[file.replace("7_", '') for file in file_list]
file_list=[file.replace("8_", '') for file in file_list]
file_list=[file.replace("9_", '') for file in file_list]
file_list=[file.replace("10_C", 'C') for file in file_list]

#Drop later points. Can also do it as: data[x]=data[x][:y]
data[0]=data[0].iloc[:5987]#5940 or with plain loc.
data[1]=data[1].iloc[:5920]
data[2]=data[2].iloc[:5672]
data[3]=data[3].iloc[:6970]
data[4]=data[4].iloc[:5245]
data[5]=data[5].iloc[:5493]
data[6]=data[6].iloc[:9260]
data[7]=data[7].iloc[:8230]
data[8]=data[8].iloc[:5600]
data[9]=data[9].iloc[:5420]

#Drops Nan values. Doesnt matter here but it does for Young's modulus cell (numpy least squares line messes it up)
for dataframe in data:
    dataframe.dropna(how='any',inplace=True)

#In case of messed up files, transform non numeric values to numeric.
for dataframe in data:
    for name in dataframe.columns:
        dataframe[name] = pd.to_numeric(dataframe[name],errors='coerce')

#Strain calculation for 3PB
for index,dataframe in enumerate(data):
    dataframe['Strain']=-(6*dataframe['Displacement']*thickness[index])/(L**2)

#Stress calculation for 3PB
for index,dataframe in enumerate(data):
    dataframe['Stress']=-1000*(3*dataframe['Force']*L)/(2*width[index]*(thickness[index]**2))

#Drop lines for cropped data. Second line doesnt work. Might as well place them in plotting. #whyf tf would i place them in plotting??
# for dataframe in data:
# #    # dataframe=dataframe[0:250]
#     dataframe=dataframe.drop(dataframe.index[6000:],inplace=True)

# Insert in the for loop to plt in different graph. If you do so, pass the colors at the beginning of the script as a list if you wish to get different ones for each line.
fig = plt.figure(figsize=(5,5),dpi=300)

#Markers tuple to get different marker for each line
markers=('o', 's', 'v', '^', '<', '>', '8', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')

#Drop lines for cropped data. Might as well place them in plotting loop.
# for dataframe in data:
    # dataframe=dataframe[0:250]
    # dataframe=dataframe.drop(dataframe.index[6000:],inplace=True)

# #Plot in the same graph. Can as well locate columns with name but .iloc is useful af. Do as I say, not as I do.
for index, dataframe in enumerate(data):
    # fig = plt.figure(figsize=(5,5),dpi=300)
    plt.plot(data[index]['Strain'],data[index]['Stress'],label=file_list[index],linestyle='-', marker=markers[index], mfc='w', markersize=8)
  
# Axes limits. Adjust accordingly.
# plt.xlim([0.0012,0.009])
# plt.ylim([-2,15])

# Ticks
plt.minorticks_on() #uses minor ticks
# plt.tick_params(direction='in',right=False, top=False) #Obsolete with following lines. Places MAJOR TICKS only on sides & handles direction. Avoid using it.
# plt.tick_params(labelsize=10) #Changes values' font, which we locked earlier.
# plt.tick_params(labelbottom=True, labeltop=False, labelright=False, labelleft=True) #Turns on/off axis values on all 4 sides
# xticks = np.arange(1, 100,10) #Numpy to place ticks in certain positions X axis
# yticks = np.arange(0,160.1,4) #Numpy to place ticks in certain positions Y axis
 
plt.tick_params(direction='in',which='minor', length=2, bottom=True, top=False, left=True, right=False) #Properly handles minor ticks
plt.tick_params(direction='in',which='major', length=4, bottom=True, top=False, left=True, right=False)# Bot/left by default True if memory serves me. All change with =False though.
#plt.xticks(xticks) #Plots ticks
#plt.yticks(yticks) #Plots ticks

#Plots grid in the background
plt.grid(True,linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)

# Axis labels
plt.xlabel(r'Strain')
plt.ylabel(r'Stress (MPa)')

# Legend
plt.legend(loc='center',bbox_to_anchor=(1.2,0.5),frameon=False)  # Adds the legend.

#Appends the UTS of each coupon in a list.
UTS=[]
for dataframe in data:
    max_value = dataframe['Stress'].max()
    UTS.append(max_value)

#Saving the fig. Insert in the for loop for different graph-----------------UNTICK------------------------------------------------------------------------------
plt.savefig(mesa+'#1 unedited stress strain.png', dpi=300,bbox_inches="tight")

# Saves the coupons data in excel
with pd.ExcelWriter('All coupons data.xlsx', engine='xlsxwriter') as writer:
  for num,count in enumerate(data,start=0):
    data[num].to_excel(writer, sheet_name=file_list[num]) #writes data in different sheets
    data[num].to_excel(writer, sheet_name=file_list[num]) # add directly after to write them in the yellow/green/blue fashion: style.background_gradient(axis=0,cmap='YlGnBu')

#%% Flexural modulus
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import glob
import os

from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression

from io import StringIO
from natsort import natsorted

#Appearance stuff
#My colors
# mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5'])
#                                                       0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry3
# Nature colors
mpl.rcParams['axes.prop_cycle'] = mpl.cycler(color=['0C5DA5', 'FF2C00', 'FF9500', '00B945', '845B97', '474747', '9e9e9e'])
#Seaborn colors
# colors=sns.color_palette("rocket",3)
# Font size. Dictionary taking numerous parameters.
plt.rcParams.update({'font.size' : 12})

# Coupon dimensions
thickness=[2.93666288,2.883306388,2.966662919,2.963329587,2.933329548,2.914995712,2.966662919,2.973329599,2.926572111,2.893329496] #d in mm
width=[11.8633324,11.88666573,11.73333239,11.92666573,11.97666574,11.92666573,11.8533324,11.74999716,12.03999723,12.03999723] #b in mm
L=40.28 #span length in mm

#Path to data
file_list = [i for i in glob.glob(r"C:/Users/KO/OneDrive - University of Patras/Επιφάνεια εργασίας/PLA uncut data\*")] 

# Loading all the csv files to create a list of data frames
data = [pd.read_csv(file,names=["Displacement","Force",'Time'],skiprows=270, delimiter=' ') for file in file_list]

#New addition to auto-generate the legend
file_list=[file.replace("C:/Users/KO/OneDrive - University of Patras/Επιφάνεια εργασίας/PLA uncut data\\", '') for file in file_list]
file_list=natsorted(file_list)

file_list=[file.replace('.dat','') for file in file_list]
file_list=[file.replace('s','#') for file in file_list]

file_list=[file.replace("1_", '') for file in file_list]
file_list=[file.replace("2_", '') for file in file_list]
file_list=[file.replace("3_", '') for file in file_list]
file_list=[file.replace("4_", '') for file in file_list]
file_list=[file.replace("5_", '') for file in file_list]
file_list=[file.replace("6_", '') for file in file_list]
file_list=[file.replace("7_", '') for file in file_list]
file_list=[file.replace("8_", '') for file in file_list]
file_list=[file.replace("9_", '') for file in file_list]
file_list=[file.replace("10_C", 'C') for file in file_list]

for dataframe in data:
    dataframe.dropna(how='any',inplace=True)

stiles=["Displacement","Force",'Time']

#Fucked up files need to be converted to numeric
for dataframe in data:
    for name in stiles:
        dataframe[name] = pd.to_numeric(dataframe[name],errors='coerce')

#Stress/Strain calculation
for index,dataframe in enumerate(data):
    dataframe['Strain']=-(6*dataframe['Displacement']*thickness[index])/(L**2)

for index,dataframe in enumerate(data):
    dataframe['Stress']=-1000*(3*dataframe['Force']*L)/(2*width[index]*(thickness[index]**2))

#Markers
markers=('o', 's', 'v', '^', '<', '>', '8', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')

for dataframe in data:
    # dataframe=dataframe[0:250]
    dataframe=dataframe.drop(dataframe.index[2500:],inplace=True) #or up to 5446

E=[]#list with all moduli

# #Plot in the same graph. Can as well locate columns with name but .iloc is useful af.
for index, dataframe in enumerate(data):
    fig = plt.figure(figsize=(5,5),dpi=300)
    plt.plot(data[index]['Strain'],data[index]['Stress'],label=file_list[index],linestyle='-', marker=markers[index], mfc='w', markersize=6)
  
    # Axes limits. Adjust accordingly.
    # plt.xlim([0.0012,0.009])
    # plt.ylim([-2,15])

    # Ticks
    plt.minorticks_on() #uses minor ticks
    # plt.tick_params(direction='in',right=False, top=False) #Obsolete with following lines. Places MAJOR TICKS only on sides & handles direction. Avoid using it.
    # plt.tick_params(labelsize=10) #Changes values' font, which we locked earlier.
    # plt.tick_params(labelbottom=True, labeltop=False, labelright=False, labelleft=True) #Turns on/off axis values on all 4 sides
    # xticks = np.arange(1, 100,10) #Numpy to place ticks in certain positions X axis
    # yticks = np.arange(0,160.1,4) #Numpy to place ticks in certain positions Y axis
    
    plt.tick_params(direction='in',which='minor', length=2, bottom=True, top=False, left=True, right=False) #Properly handles minor ticks
    plt.tick_params(direction='in',which='major', length=4, bottom=True, top=False, left=True, right=False)# Bot left by default True if memory serves me. All change with =False though.
    #plt.xticks(xticks) #Plots ticks
    #plt.yticks(yticks) #Plots ticks
    
    #Plots grid in the background
    plt.grid(True,linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)
    
    # Axis labels
    plt.xlabel(r'Strain')
    plt.ylabel(r'Stress (MPa)')
    
    # Legend
    plt.legend(frameon=False)  # Adds the legend. loc='best',bbox_to_anchor=(1,0.85)
    
    
    # https://realpython.com/linear-regression-in-python/
    # x_data=data[index]['Strain'].to_numpy().reshape(-1,1)
    # y_data=data[index]['Stress'].to_numpy()

    # model = LinearRegression()
    # model.fit(x_data, y_data)
    
    # model = LinearRegression().fit(x_data, y_data)
    # r_sq = model.score(x_data, y_data)
    # E.append(model.coef_)
    
    
    #My linear regression that works. Drawn in the same graph with the linear region of the curve.
    x_data=data[index]['Strain'].to_numpy()
    y_data=data[index]['Stress'].to_numpy()
    
    #Hard math don't bother.
    # def model_f(x, a, b):
    #     return a*x+b
    
    # popt, pcov = curve_fit(model_f, x_data, y_data, p0=[2,2])
    # a_opt,b_opt = popt
    # x_model = np.linspace(min(x_data), max(x_data), 100)
    # y_model = model_f(x_model, a_opt,b_opt)
    
    # plt.plot(x_model,y_model, color='r',label='Linear regression')
    # plt.legend(frameon=False)
    # a_opt=round(a_opt/1000,3)
    # plt.text(0.012,7,f"E={a_opt} GPa")#   plt.text(0.015,8,'E=%s GPa'%(a_opt)) #alternative # rotation="horizontal", ha="center"
    # E.append(a_opt)
    
    #Numpy least squares.
    A = np.vstack([x_data, np.ones(len(x_data))]).T
    m,c=np.linalg.lstsq(A,y_data,rcond=None)[0]
    slope=round(m/1000,3)
    E.append(slope)
    
    
    #plt.plot(x_data, y_data, 'o', label='Original data', markersize=10)
    plt.plot(x_data, m*x_data + c, 'r', label='Fitted line')
    plt.legend(frameon=False)
    plt.text(0.012,7,f"E={slope} GPa",va='center',ha='center')
    
    #Saving the fig. Insert in the for loop for different graph
    plt.savefig(mesa+file_list[index]+'.png', dpi=300,bbox_inches="tight")


#%% Intuitive stuff. Can definitely be improved
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import seaborn as sns
# import glob
# import os

# from scipy.optimize import curve_fit
# from sklearn.linear_model import LinearRegression

# from io import StringIO
# from natsort import natsorted

# plt.rcParams.update({'font.size' : 12})

# width = 0.3

# x = np.arange(len(file_list))

# fig, ax1 = plt.subplots(figsize=(10,5))
# ax2 = ax1.twinx()

# ax1.bar(x, UTS, color='#1f77b4',width=width, align='center',label='Ultimate strength')

# ax2.bar(x+width, E, color='#ff7f0e', width=width,align='center', label='Flexural modulus') 

# ax1.set_xticks(x+width/2,file_list) #POY PANE TA LABELS
# plt.grid(axis='y',linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)

# ax1.set_ylabel('Ultimate strength (MPa)')#,color='#1f77b4'
# ax2.set_ylabel('Flexural modulus (GPa)')#,color='#ff7f0e'

# ax1.legend(loc=(0.7,0.8),frameon=False)
# ax2.legend(loc=(0.7,0.9),frameon=False)

# ax1.set_xticklabels(file_list,rotation=45)

# #Colours the spines and ticks.
# # ax1.tick_params(axis='y', labelcolor='#1f77b4',)
# # ax2.tick_params(axis='y', labelcolor='#ff7f0e')
# # ax1.tick_params(axis='y',color='#1f77b4')
# # ax2.tick_params(color='#ff7f0e')
# # ax2.spines['left'].set_color('#1f77b4')
# # ax2.spines['right'].set_color('#ff7f0e')

# # plt.savefig(mesa+'#6 comparative bar char allt'+'.png', dpi=300,bbox_inches="tight")

#%% Seperate graphs for each sample and each material
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import glob
import os

from scipy.optimize import curve_fit
from sklearn.linear_model import LinearRegression

from io import StringIO
from natsort import natsorted

from statistics import mean
import statistics
from statistics import stdev


plt.rcParams['axes.axisbelow'] = True

x = np.arange(len(file_list))
fig = plt.figure(figsize=(10,5))

#UTS for each coupon
width=0.5
plt.bar(x,UTS,color='#1f77b4', width=width,align='center',label='Ultimate strength (MPa')
plt.xticks(x,file_list,rotation=45) #POY PANE TA LABELS
plt.ylabel('Ultimate Strength (MPa)')
plt.grid(axis='y',linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)
plt.savefig(mesa+'#2 uts all'+'.png', dpi=300,bbox_inches="tight")

#E for each coupon
fig = plt.figure(figsize=(10,5))
plt.bar(x, E, color='#ff7f0e', width=width,align='center', label='Flexural modulus (GPa')
plt.xticks(x,file_list,rotation=45) #POY PANE TA LABELS
plt.ylabel('Flexural modulus (GPa)')
plt.grid(axis='y',linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)
plt.savefig(mesa+'#3 E all'+'.png', dpi=300,bbox_inches="tight")

#for each material now. Automata UTS_all=[round(np.average(UTS[0:2]),3)
UTS_all=[round(mean(UTS[0:3]),3),round(mean(UTS[3:6]),3),round(mean(UTS[6:]),3)]
UTS_std=[stdev(UTS[0:3])/(3**0.5),stdev(UTS[3:6])/(3**0.5),stdev(UTS[6:])/(4**0.5)]


E_all=[round(mean(E[0:3]),3),round(mean(E[3:6]),3),round(mean(E[6:]),3)]
E_std = [stdev(E[0:3])/(3**0.5),stdev(E[3:6])/(3**0.5),stdev(E[6:])/(4**0.5)]

lista=['3D850', '3Devo', 'CR10']
x = np.arange(len(lista))
width=0.3


#UTS for each material
fig = plt.figure(figsize=(8,5))
plt.bar(x,UTS_all,color='#1f77b4', width=width,align='center',label='Ultimate strength (MPa')
plt.errorbar(x, UTS_all, yerr=UTS_std, fmt='none', color="black",capsize=6,ecolor='black')
plt.xticks(x,lista,rotation=0) #POY PANE TA LABELS
plt.ylabel('Ultimate Strength (MPa)')
plt.grid(axis='y',linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)

for graph in x:
    plt.text(x[graph],33.22, f'{UTS_all[graph]}', rotation="horizontal", ha="center")
plt.savefig(mesa+'#4 UTS per material'+'.png', dpi=300,bbox_inches="tight")

#E for each material
fig = plt.figure(figsize=(8,5))
plt.bar(x, E_all, color='#ff7f0e', width=width,align='center', label='Flexural modulus (GPa')
plt.errorbar(x, E_all, yerr=E_std, fmt='none', color="black",capsize=6)
plt.xticks(x,lista,rotation=0) #POY PANE TA LABELS
plt.ylabel('Flexural modulus (GPa)')
plt.grid(axis='y',linestyle='dashed', linewidth='0.3', color='grey',alpha=0.8)

for graph in x:
    plt.text(x[graph],1.205, f'{E_all[graph]}', rotation="horizontal", ha="center")
plt.savefig(mesa+'#5 E per material'+'.png', dpi=300,bbox_inches="tight")