#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, gridspec, widgets, cm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import logging, sys
import scipy.stats as st

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

log = logging.getLogger('assigment3')
logging.basicConfig()


dfT = df.sort_index().T
stats = pd.DataFrame({'mean': dfT.apply(np.mean),
                      'stderr': dfT.apply(st.sem),
                      'dof': dfT.count()-1})


ar1, ar2 = st.t.interval(0.95, stats['dof'], loc=stats['mean'], scale=stats['stderr'])
stats['interval'] = stats['mean'] - ar1


def p_to_norm(p, higher):
    """Scale a p value to a value between 0 and 1 for the color map. choose a scale to adjust the rate of gradient change"""
    scaled = np.power(p, 0.3)
    return (0.5 + (1-scaled)/2) if higher else scaled/2

def p_to_color_div(p, higher=False):
    """Convert of p value to a color code using a diverging
color map, meaning two opposite poles are distinguished from the middle and from each other.
higher=True if the observed mean (bar height) is higher than the test mean."""
    cmap = cm.get_cmap('seismic')
#     help(cmap)
    return cmap(p_to_norm(p, higher))


def p_to_color_seq(p):
    """Convert of p value to a color code using a sequential
color map, meaning the distinction is made primarily between two opposite poles."""
    cmap = cm.get_cmap('Reds')
#     help(cmap)
    return cmap(p)


gs = gridspec.GridSpec(2, 1, height_ratios=(6,1), hspace=0.3)
fig = plt.figure(figsize=(9,7))
ax = plt.subplot(gs[0, 0])
ax2 = plt.subplot(gs[1, 0])

y1, y2 = 40000, 40000
cursor, lines = None, []


def redraw():
    """Redraw the basic subplot and bars"""
    global cursor
    cursor = None
    ax.cla()
    
    bars = ax.bar(stats.index.astype(str), stats['mean'], yerr=stats['interval'], capsize=10);
    fig.subplots_adjust(right=.75)
    
    ax.set_frame_on(False)
    ax.tick_params(bottom=False)
    return bars

def plot(stats):
    """Plot the bars, draw all supporting features, run tests, paint according to test results."""
    global y1, y2, lines
    bars = redraw()
    
    if y1 == y2:
        add_line(y1)
        ax.set_title('Mean comparison against y = {}'.format(int(y1)))

        ttres = st.ttest_1samp(dfT, y1)
        ps = ttres[1]
        
        label_bars(ps, bars, lambda p,b: p_to_color_div(p, b.get_height() > y1), True)

        asc, desc = np.arange(0,1,0.2), np.arange(1,-0.1,-0.2)
        colors = [p_to_color_div(p, True) for p in asc] + [p_to_color_div(p, False) for p in desc]

        leg = add_legend(colors, np.around(np.append(asc, desc), 1))
    else:
        add_line(y1)
        add_line(y2)
        ymin, ymax = min(y1, y2), max(y1, y2)
        
        ax.set_title('Probability of population mean between {} and {}'.format(int(ymin), int(ymax)))
        
        lower = st.t.cdf(ymin, stats['dof'], loc=stats['mean'], scale=stats['stderr'])
        higher = st.t.cdf(ymax, stats['dof'], loc=stats['mean'], scale=stats['stderr'])
        density_in_range = higher - lower
        
        label_bars(density_in_range, bars, lambda p,b: p_to_color_seq(p), False)

        seq = np.arange(1.01,0,-0.1)
        colors = [p_to_color_seq(p) for p in seq]

        leg = add_legend(colors, np.around(seq, 1))
    
    return bars

def label_bars(ps, bars, ptc, invert_colors=False):
    for p,b in zip(ps, bars):
        textcolor = 'black' if invert_colors ^ (p < 0.40) else 'white'
        ax.text(b.get_x() + b.get_width()/2, 8000, '\u03bc: {}'.format(int(b.get_height())),
                  ha='center', va='center', color=textcolor)
        ax.text(b.get_x() + b.get_width()/2, 5000, 'p: {:.2}'.format(p),
                  ha='center', va='center', color=textcolor)
        b.set_color(ptc(p, b))

def setup_widgets():
    ax2.set_frame_on(False)
    ax2.tick_params(bottom=False, labelbottom=False, left=False, labelleft=False)
    ax2.text(-0.1,1, ("Directions: Click once to establish a single mean value to compare against "
                   "depicted means.\nClick and drag to establish a vertical range to assess how "
                   "likely each mean is to fall within the range."))
    
def add_line(y):
    global lines
    lines.append(ax.add_line(Line2D([-0.5, 3.5], [y,y], linewidth=0.5, color='black')))
    
def clear_lines():
    global lines
    for l in lines: l.set_visible(False)
    lines.clear()
    
def add_legend(colors, labels):
    leg = ax.legend(handles=[Patch(facecolor=c, label=l) for c, l in
                             zip(colors, labels)
                            ],
                    loc=(0.98,0.1), title='p-value')
    leg.set_frame_on(False)
    return leg

def onpress(event):
    global y1, cursor, lines
    y1 = event.ydata
    clear_lines()
    add_line(y1)
    cursor = widgets.Cursor(ax, vertOn=False, color='black', linestyle='--')
    
def onrelease(event):
    global y2
    y2 = event.ydata
    plot(stats)
    
    
# tell mpl_connect we want to pass a 'button_press_event' into onclick when the event is detected
fig.canvas.mpl_connect('button_press_event', onpress)
fig.canvas.mpl_connect('button_release_event', onrelease)

plot(stats)
setup_widgets()
plt.show()
