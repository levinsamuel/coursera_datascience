
# coding: utf-8
# Use the following data for this assignment:

import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650),
                   np.random.normal(43000,100000,3650),
                   np.random.normal(43500,140000,3650),
                   np.random.normal(48000,70000,3650)],
                  index=[1992,1993,1994,1995])
df

# new code
column_count = df.shape[1]   # aka sample size for yerr

# get mean values over all columns per year (== index)
df_mean = df.mean(axis=1)
# same for standard deviation
df_std = df.std(axis = 1)
# needed for yerr - CONFIDENCE INTERVAL FOR A POPULATION MEAN WHEN YOU KNOW ITS STANDARD DEVIATION
yerr = df_std / np.sqrt(column_count) * stats.t.ppf(1-0.05/2, column_count-1) # 95% calculation (only half due positioned in middle)

# TODO: get user input in case of different difficult level (but also will be then default value)
y_voi = 42000 # value of interest for y-axis; hard coded


import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.get_backend()

# color map imports
import matplotlib.colors as mcol
import matplotlib.cm as cm

fig, (ax1, ax2) = plt.subplots(2,1)

# reset y_voi just in case
y_voi = 42000

## 1) simple bar chart for transformed data
bars = ax1.bar( range(len(df.index)),
               df_mean,
               yerr = yerr,
               #hatch='-', hatch provides pattern on columns, not the error lines
               align='center', alpha=0.5
               )#, color = 'b')
# Todo: found way to have T shaped error lines but seems not to exists in default packages

# years on x-axis
# ax1.set_xticks( range(len(df.index)), df_mean.index)
#
# ## 2) grey line
# ax1.axhline(y = y_voi,
#             alpha = 0.5, linewidth = 1.5, # ? default was 1, 2 too big
#             color = 'grey')

## 3 color and subplot, simple version
cpick = cm.ScalarMappable( cmap = mcol.LinearSegmentedColormap.from_list("color-map",["b", "w", "r"]) )
cpick.set_array([])
plt.colorbar(cpick, ax=ax2, orientation='horizontal', alpha=0.8)  # alpha makes it ugly ...



# Todo y_voi update for animation
# read y_voi from user input
percentages = []
trimmer = lambda x: 1 if x > 1 else 0 if x < 0 else x # trim > 1 and < 0

for tmp_bar, tmp_yerr in zip(bars, yerr):
    low  = tmp_bar.get_height() - tmp_yerr
    high = tmp_bar.get_height() + tmp_yerr
    perc = (high - y_voi) / (high - low)
    percentages.append( trimmer(perc) )

#bars.set_color( cpick.to_rgba(percentages) )  # ? better way to adjust ?
bars = ax1.bar( range(len(df.index)),
               df_mean, yerr = yerr,
               color = cpick.to_rgba(percentages),
               align='center', alpha=0.5
               )

## until now everything initial plotting

def onclick(event):
    ax1.cla()
    # plt.figure()
    # plt.show()
    global ix, iy
    ix, iy = event.xdata, event.ydata
    print(event)
    y_voi = int(iy) # just in case

    ## something wrong, have to draw everything anew and not just the motifications

    ## 1) simple bar chart for transformed data
    bars = ax1.bar( range(len(df.index)),
               df_mean,
               yerr = yerr,
               #hatch='-', hatch provides pattern on columns, not the error lines
               align='center', alpha=0.5
               )
    # ax1.xticks( range(len(df.index)), df_mean.index)
    # #
    # # ## 2) grey line
    # ax1.axhline(y = y_voi,
    #         alpha = 0.5, linewidth = 1.5, # ? default was 1, 2 too big
    #         color = 'grey')

    ## 3 color and subplot, simple version
    cpick = cm.ScalarMappable( cmap = mcol.LinearSegmentedColormap.from_list("color-map",["b", "w", "r"]) )
    cpick.set_array([])
    plt.colorbar(cpick, ax=ax2, orientation='horizontal', alpha=0.8)  # alpha makes it ugly ...

    percentages = []

    for tmp_bar, tmp_yerr in zip(bars, yerr):
        low  = tmp_bar.get_height() - tmp_yerr
        high = tmp_bar.get_height() + tmp_yerr
        perc = (high - y_voi) / (high - low)
        percentages.append( trimmer(perc) )

    # bars = plt.bar( range(len(df.index)),
    #            df_mean, yerr = yerr,
    #            color = cpick.to_rgba(percentages),
    #            align='center', alpha=0.5
    #            )



fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()
# safe image
# from matplotlib.backends.backend_agg import FigureCanvasAgg
# from matplotlib.figure import Figure
# canvas = FigureCanvasAgg(fig)
# canvas.print_png('assignment3_rh.png')


# In[90]:

# scrap code to figure out event stuff
#f = lambda x: 1 if x > 1 else 0 if x < 0 else x

# y_value = 10
#
# plt.figure()
# plt.show()
#
# plt.axhline(y = y_voi, alpha = 0.5, linewidth = 1.5, color = 'blue')
#
# def onclick(event):
#     plt.cla() # miss 1
#     global ix, iy
#     ix, iy = event.xdata, event.ydata
#     print('x = %d, y = %d'%(ix, iy))
#     y_value = iy
#     plt.axhline(y = y_value, alpha = 0.5, linewidth = 1.5, color = 'blue')
#
# plt.gcf().canvas.mpl_connect('button_press_event', onclick)     # miss 2
