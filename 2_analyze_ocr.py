# Load csv from '1_run_ocr.py', create dateframe and
# clean up. Different statistics and plots, output
# in /plots subfolder.
#
# Should be run as a second step of the analysis
# (after '1_run_ocr.py'). Specify csv data file
# in /data subfolder.

import os
import numpy as np
from tqdm import tqdm
import re
import matplotlib.pylab as plt
#plt.style.use('dark_background')
col1 = '#00bf6c'
col2 = '#5a5b5b'
import pandas as pd

# Input
fname = 'iOS_LL_2019-03-16.csv'

# Load csv data file
print('Loading data file ...')
dpath = os.path.join(os.getcwd(),"data")
df = pd.read_csv(os.path.join(dpath,fname),index_col=0)
df = df.reset_index()

# Create (binary) columns for MKII
df['R_MK2'] = df['Robot'].str.contains('MK').fillna(False)
df['W_MK2'] = df['Weapon'].str.contains('MK').fillna(False)

# Load equipment list
equplist = np.loadtxt(os.path.join(os.getcwd(),'other','equip_list.csv'),
                      skiprows=1,delimiter=',',dtype='str')
robotlist = equplist[equplist[:,0] == 'Robot',1:3]
weaponlist = equplist[equplist[:,0] == 'Weapon',1:3]

print('Cleaning data frame ...')
# Correct Robot and Weapon names via regex
for ii in range(len(equplist)):
    df[equplist[ii,0]] = df[equplist[ii,0]].replace('.*'
            + equplist[ii,2] + '.*',equplist[ii,1],regex=True)

# Convert gibberish into NaN by setting category tyoes
df['Robot'] = df['Robot'].astype(
    pd.api.types.CategoricalDtype(categories=robotlist[:,0],
                                  ordered=False))
df['Weapon'] = df['Weapon'].astype(
    pd.api.types.CategoricalDtype(categories=weaponlist[:,0],
                                  ordered=False))

# Make plot folder
pltpath = os.path.join(os.path.dirname(dpath),'plots',os.path.splitext(fname)[0])
if not os.path.exists(pltpath):
    os.makedirs(pltpath)

# Save clean dataframe to csv
df.to_csv(os.path.join(pltpath,'alldata.csv'))


# --------------------------
# Analysis
print('Analyzing and plotting ...')

# Ordered by total number of robots
rob_order = list(df['Robot'].value_counts(ascending=True).index)

# Total and mk1 robot counts (ordered)
totno_robots = (df['Robot'].value_counts()
        .reindex(rob_order)[df['Robot'].value_counts() != 0])
mk1no_robots = (df[~df['R_MK2']]['Robot'].value_counts()
        .reindex(rob_order)[df['Robot'].value_counts() != 0])

# Plot and save
plt.figure(figsize=(10,6))
totno_robots.plot.barh(color=col1,label='MK II')
mk1no_robots.plot.barh(color=col2,label='MK I')
plt.xlabel('Number')
plt.legend(loc='lower right')
plt.title('Robots in Legend League ('  +  fname[7:17] + ')')
plt.savefig(os.path.join(pltpath,'Robots.png'),dpi=200)


# Ordered by total number of weapons
weap_order = list(df['Weapon'].value_counts(ascending=True).index)

# Total and mk1 weapon counts (ordered)
totno_weapons = (df['Weapon'].value_counts()
        .reindex(weap_order)[df['Weapon'].value_counts() != 0])
mk1no_weapons = (df[~df['W_MK2']]['Weapon'].value_counts()
        .reindex(weap_order)[df['Weapon'].value_counts() != 0])

# Plot and save
plt.figure(figsize=(10,6))
totno_weapons.plot.barh(color=col1,label='MK II')
mk1no_weapons.plot.barh(color=col2,label='MK I')
plt.xlabel('Number')
plt.legend(loc='lower right')
plt.title('Weapons in Legend League ('  +  fname[7:17] + ')')
plt.savefig(os.path.join(pltpath,'Weapons.png'),dpi=200)
plt.close('all')

# Loop through each robot
for group, frame in df.groupby('Robot'):
    
    # Exclude those with zero counts
    if df['Robot'].value_counts()[group] !=0:
        
        # Ordered by total number of weapons
        weap_order = list(frame['Weapon'].value_counts(ascending=True).index)

        # Total and mk1 weapon counts (ordered)
        totno_weapons = (frame['Weapon'].value_counts()
                .reindex(weap_order)[frame['Weapon'].value_counts() != 0])
        mk1no_weapons = (frame[~frame['W_MK2']]['Weapon'].value_counts()
                .reindex(weap_order)[frame['Weapon'].value_counts() != 0])

        # Plot and save
        plt.figure(group,figsize=(7,4))     
        totno_weapons.plot.barh(color=col1,label='MK II')
        mk1no_weapons.plot.barh(color=col2,label='MK I')
        plt.xlabel('Number')
        plt.legend(loc='lower right')
        plt.title(group + ' (' + fname[7:17] + ')')
        plt.savefig(os.path.join(pltpath,group + '.png'),dpi=150)


### Loop through Rank
##ratio = np.zeros(len(df.Rank.unique()))
##for group, frame in df.groupby('Rank'):
##    
##    # Mk1/Mk2 ratio for all equipment (Robots + Weapons)
##    no_eqtotal = len(frame)/4 + len(frame.dropna())
##    no_eqmk2 = (len(frame[::4][frame[::4].R_MK2])
##            + len(frame.dropna()[frame.dropna().W_MK2]))
##    ratio[int(group)-1] = no_eqmk2/no_eqtotal
##
### PLot and save
##plt.figure('MK2equip')
##plt.plot(df.Rank.unique(),ratio*100,'o',label='Data')
##plt.plot([0,100],[np.mean(ratio*100),np.mean(ratio*100)],label='Average')
##plt.xlabel('Player rank')
##plt.title('MK2 equipment in Legend League ('  +  fname[7:17] + ')')
##plt.xlim(0,100)
##plt.legend(loc='lower right')
##plt.ylabel('Percentage (%)')
##plt.savefig(os.path.join(pltpath,'MK2equip.png'),dpi=150)

plt.close('all')
print('Done!')
