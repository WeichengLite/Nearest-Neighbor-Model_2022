import pandas as pd
data = pd.read_csv('Bha_WT_ITC25_Raw.txt',sep='\s+',header=None)
data = pd.DataFrame(data)

import matplotlib.pyplot as plt
x = data[0]
y = data[1]
plt.plot(x/60, y,color='#1d3d59')
plt.xlim([0,185])
plt.ylim([-1.02,0.05])
### plt.legend(['20200117_EMR_nESI_BhadTRAP_WTWT_5uM_Trp_11eq_random'])

### turn off the axis: plt.axis('off')

### left='on', top='on', right='on', bottom='off', labelleft='off', labeltop='off', labelright='off', labelbottom='off'
plt.tick_params(axis='both',direction='in',left=1, bottom=0, top=0, right=0, labelleft=1,labelbottom=1, labeltop=0, labelright=0, labelsize='large')
### turn off the ticks and labels: plt.xticks([])
### turn off the ticks and labels: plt.yticks([])


### Change the number of ticks on a plot axis
plt.locator_params(axis="x", nbins=4)
plt.locator_params(axis="y", nbins=3)

### Set Tick labels Font Size in matplotlib
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

figure = plt.gcf()
figure.set_size_inches(7.5, 5)

plt.tight_layout()
plt.savefig('Bha_WT_ITC25.png', dpi=300, bbox_inches='tight')
plt.show()
