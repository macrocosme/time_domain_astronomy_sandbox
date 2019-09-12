"""Plotting methods."""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc
rc('font', size=16)
rc('axes', titlesize=18)
rc('axes', labelsize=18)

from mpl_toolkits.axes_grid1 import AxesGrid
from matplotlib.offsetbox import AnchoredText

def add_at(ax, t, loc=2):
    # fp = dict(size=13)
    _at = AnchoredText(t, loc=loc)#, prop=fp)
    ax.add_artist(_at)
    return _at

def set_fig_dims(direction, data_arr):
    if direction == 'horizontal':
        ncols = len(data_arr)
        nrows = 1
    elif direction == 'vertical':
        ncols = 1
        nrows = len(data_arr)

    return ncols, nrows

def snr(data, noise_median, noise_std):
    return np.abs(np.median(data, axis=0)/noise_median)

def set_multi_axes(ax, direction, xticks, xtick_labels, yticks, ytick_labels):
    """Set axes ticks and tick labels

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Array of axes
    direction : str
        General direction onto which append subplots
    xticks : list
        List of ticks for x axis
    xticks_labels : list
        List of tick labels for x axis
    yticks : list
        List of ticks for y axis
    yticks_labels : list
        List of tick labels for y axis

    """
    for i, axi in enumerate(ax):
        if len(xticks) > 0 and len(xtick_labels) > 0:
            if (direction == 'vertical' and i == len(ax)-1) or direction == 'horizontal':
                axi.set_xlabel('Time (s)')
                axi.set_xticks(xticks)
                axi.set_xticklabels(xtick_labels)
            else:
                plt.setp(axi.get_xticklabels(), visible=False)
        else:
            axi.set_xlabel('X Index')

        if len(yticks) > 0 and len(ytick_labels) > 0:
            if (direction == 'horizontal' and i == 0) or direction == 'vertical':
                axi.set_ylabel('Freq. (MHz)')
                axi.set_yticks(yticks)
                axi.set_yticklabels(ytick_labels)
            else:
                plt.setp(axi.get_yticklabels(), visible=False)
        else:
            axi.set_ylabel('S/N')

def plot_spectrum(data, ncols=1, nrows=1):
    """Plot spectrum.

    Parameters
    ----------
    data : Numpy.Array
    ncols : int
        Number of column for matplotlib.pyplot.subplots
    nrows : int
        Number of rows for matplotlib.pyplot.subplots
    """
    fig, ax = plt.subplots(figsize=(10, 5), ncols=ncols, nrows=nrows)
    ax.plot(data, extent='lower')
    ax.set_xlabel('channel')
    ax.set_ylabel('intensity')

def plot_image(data,
               xticks=[], xtick_labels=[],
               yticks=[], ytick_labels=[],
               ncols=1, nrows=1,
               xfig_size=10, yfig_size=5
               ):
    """Plot spectrum.

    Parameters
    ----------
    data : Numpy.Array
    xticks : list
        List of ticks for x axis
    xticks_labels : list
        List of tick labels for x axis
    yticks : list
        List of ticks for y axis
    yticks_labels : list
        List of tick labels for y axis
    ncols : int
        Number of column for matplotlib.pyplot.subplots
    nrows : int
        Number of rows for matplotlib.pyplot.subplots
    xfig_size : int
        Figure size in x
    yfig_size : int
        Figure size in y

    """
    fig, ax = plt.subplots(
        figsize=(xfig_size, yfig_size),
        ncols=ncols,
        nrows=nrows
        )
    ax.imshow(data, origin='lower')
    ax.set_xlabel('time (s)')
    ax.set_ylabel('frequency (MHz)')

    if len(xticks) > 0 and len(xtick_labels) > 0:
        ax.set_xticks(xticks)
        ax.set_xticklabels(xtick_labels)

    if len(yticks) > 0 and len(ytick_labels) > 0:
        ax.set_yticks(yticks)
        ax.set_yticklabels(ytick_labels)

def plot_multi_1D(data_arr,
                  xticks=[], xtick_labels=[],
                  yticks=[], ytick_labels=[],
                  noise_median=0, noise_std=1,
                  direction='horizontal',
                  xfig_size=10, yfig_size=5,
                  savefig=False,
                  fig_name='multi-1D',
                  ext='png',
                  dpi=150
                  ):
    """Plot multiple spectrum.

    Parameters
    ----------
    data : list(Numpy.Array)
        list of data arrays
    xticks : list
        List of ticks for x axis
    xticks_labels : list
        List of tick labels for x axis
    yticks : list
        List of ticks for y axis
    yticks_labels : list
        List of tick labels for y axis
    direction : str
        General direction onto which append subplots (default: 'horizontal')
    xfig_size : int
        Figure size in x (default: 10)
    yfig_size : int
        Figure size in y (default: 5)
    savefig : bool
        Save figure (default: False)
    fig_name : str
        Figure name (default: 'multi-images')
    ext : str
        File extension (default 'png')

    """
    ncols, nrows = set_fig_dims(direction, data_arr)

    fig, ax = plt.subplots(
        figsize=(xfig_size, yfig_size),
        ncols=ncols,
        nrows=nrows
    )

    for i, axi in enumerate(ax):
        axi.plot(snr(data_arr[i], noise_median, noise_std))

    set_multi_axes(ax, direction, xticks, xtick_labels, yticks, ytick_labels)

    plt.tight_layout()
    if savefig:
        plt.savefig("%s.%s" % (fig_name, ext), dpi=dpi)

def plot_multi_images(data_arr,
                      labels=[],
                      xticks=[], xtick_labels=[],
                      yticks=[], ytick_labels=[],
                      noise_median=0, noise_std=1,
                      direction='horizontal',
                      xfig_size=10, yfig_size=5,
                      spectrum=False,
                      colorbar=False,
                      savefig=False,
                      fig_name='multi-images',
                      ext='png',
                      dpi=150
                      ):
    """Plot images.

    Parameters
    ----------
    data : list(Numpy.Array)
        list of data arrays
    xticks : list
        List of ticks for x axis
    xticks_labels : list
        List of tick labels for x axis
    yticks : list
        List of ticks for y axis
    yticks_labels : list
        List of tick labels for y axis
    direction : str
        General direction onto which append subplots (default: 'horizontal')
    xfig_size : int
        Figure size in x (default: 10)
    yfig_size : int
        Figure size in y (default: 5)
    savefig : bool
        Save figure (default: False)
    fig_name : str
        Figure name (default: 'multi-images')
    ext : str
        File extension (default 'png')

    """
    ncols, nrows = set_fig_dims(direction, data_arr)

    fig, ax = plt.subplots(
        figsize=(xfig_size, yfig_size),
        ncols=ncols,
        nrows=nrows,
        gridspec_kw = {'hspace':0, 'wspace':0},
    )

    for i, axi in enumerate(ax):
        im = axi.imshow(data_arr[i], origin='lower')
        if len(labels) > 0:
            pos_x = data_arr[i].shape[0]-0.3*data_arr[i].shape[0]
            pos_y = data_arr[i].shape[1]-0.3*data_arr[i].shape[1]
            # axi.annotate(pos_x, pos_y, labels[i], bbox={'facecolor': 'white', 'pad': 10})
            if len(labels[i]) > 0:
                add_at(axi, labels[i], loc=4)
        if spectrum:
            axi.autoscale(False)
            ax2 = axi.twinx()
            ax2.plot(np.mean(data_arr[i], axis=0), color='white', alpha=0.2)
            ax2.set_ylabel('Median intensity')
        if colorbar:
            fig.colorbar(im, ax=axi)

    set_multi_axes(ax, direction, xticks, xtick_labels, yticks, ytick_labels)

    plt.tight_layout()
    if savefig:
        plt.savefig("%s.%s" % (fig_name, ext), dpi=dpi)
