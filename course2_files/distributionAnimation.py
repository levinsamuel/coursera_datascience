#!/usr/bin/env python
# coding: utf-8

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import InsetPosition
import numpy as np
from matplotlib import animation, gridspec, widgets
import logging
import sys

mpl.use('TkAgg')

log = logging.getLogger('plot_animation')
logging.basicConfig()

src1 = np.random.normal(5, 1, 10000)
src2 = np.random.gamma(2, 1, 10000)*0.8
src3 = np.random.exponential(1.2, 10000)
src4 = np.random.uniform(0, 10, 10000)

labeled_data = {
    'gamma': src2,
    'normal': src1,
    'uniform': src4,
    'exponential': src3
}

ani = None
selected = ['gamma', 'gamma']
howmany, step = 100, 4
fig = plt.figure()
gs = gridspec.GridSpec(3, 4)


def add_radios(row, gs, ax):

    right = plt.subplot(gs[row, 3])
    right.set_frame_on(False)
    right.tick_params(labelleft=False, labelbottom=False, left=False,
                      bottom=False)
    right.set_title('Select {} Distribution'.format(ax),
                    loc='left', y=0.89)
    rb = widgets.RadioButtons(right, labeled_data.keys(), active=0)
    return right, rb


r1, rb1 = add_radios(0, gs, 'X')
r2, rb2 = add_radios(1, gs, 'Y')

cid1 = rb1.on_clicked(lambda l: rbclick(l, selected, 0, step, howmany, fig))
cid2 = rb2.on_clicked(lambda l: rbclick(l, selected, 1, step, howmany, fig))

br = plt.subplot(gs[2, 3])
br.set_frame_on(False)
br.tick_params(labelleft=False, labelbottom=False, left=False, bottom=False)

endbtn = widgets.Button(br, 'Skip Animation', color='#888888',
                        hovercolor='#cccccc')
btncid = endbtn.on_clicked(lambda e: skip_to_end(selected, step, howmany))
# sizeform = widgets.TextBox(br, 'Sample Size')
# formcid = sizeform.on_submit(lambda e: set_sample_size(e))


class RootChart:
    def __init__(self, fig, mid, tl, top, left):
        self.fig = fig
        self.mid = mid
        self.tl = tl
        self.top = top
        self.left = left

    def clear(self):
        self.mid.cla()
        self.tl.cla()
        self.top.cla()
        self.left.cla()

    def reset(self):
        self.mid.axis([-1, 11, -1, 11])
        self.left.axis([1, 0, -1, 11])
        self.top.axis([-1, 11, 0, 1])


def build_figure(fig, limit, selected, gs):

    left = plt.subplot(gs[1:3, 0])
    # left.xaxis.tick_top()
    left.invert_xaxis()
    # left.autoscale(enable=False, axis='both')

    top = plt.subplot(gs[0, 1:3])
    top.xaxis.tick_top()
    # top.yaxis.tick_right()
    # top.autoscale(enable=False, axis='both')

    mid = plt.subplot(gs[1:3, 1:3])
    mid.xaxis.tick_top()
    mid.tick_params(labelleft=False, labeltop=False)
    # Does nothing
    # mid.autoscale(enable=False, axis='both')

    tl = plt.subplot(gs[0, 0])
    tl.set_frame_on(False)
    tl.tick_params(labelleft=False, labelbottom=False, left=False,
                   bottom=False)

    return RootChart(fig, mid, tl, top, left)


def rbclick(label, selected, which, step, limit, fig):

    global root, n, running
    selected[which] = label
    n = 1
    running = True


def skip_to_end(selected, step, limit):

    global n, running
    n = limit


def set_sample_size(e):
    global root
    root.tl.annotate('sample = {}'.format(e), [0.5, 0])


def render(curr, step, limit, selected):

    global root, labeled_data, running, n
    if not running or n > limit:
        return
    root.clear()
    i, end = n*step, limit*step
    n += 1
    x = labeled_data[selected[0]][0:i]
    y = labeled_data[selected[1]][end:end+i]
    root.mid.scatter(x, y, marker='.', alpha=0.6)
    root.top.hist(x, density=True, bins=np.arange(0, 10.5, 0.5), alpha=0.8)
    root.left.hist(y, density=True, bins=np.arange(0, 10.5, 0.5), alpha=0.8,
                   orientation='horizontal')
    root.reset()
    root.tl.annotate('n = {}'.format(i), [0, 0])

# Kick off with initial click event


root = build_figure(fig, howmany, selected, gs)
rbclick('gamma', selected, 0, step, howmany, fig)
ani = animation.FuncAnimation(
        fig, lambda c: render(c, step, howmany, selected),
        interval=100, repeat=True, blit=False)

running, n = True, 1
plt.show()
