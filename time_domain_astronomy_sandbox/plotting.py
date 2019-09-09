"""Plotting methods."""
from matplotlib import pyplot as plt
from matplotlib import rc
rc('font', size=16)
rc('axes', titlesize=18)
rc('axes', labelsize=18)


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

def plot_multi_images(data_arr,
                      xticks=[], xtick_labels=[],
                      yticks=[], ytick_labels=[],
                      direction='horizontal',
                      xfig_size=10, yfig_size=5,
                      spectrum=False,
                      savefig=False,
                      fig_name='multi-images',
                      ext='png',
                      dpi=150
                      ):
    """Plot spectrum.

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
    if direction == 'horizontal':
        ncols = len(data_arr)
        nrows = 1
    elif direction == 'vertical':
        ncols = 1
        nrows = len(data_arr)

    fig, ax = plt.subplots(
        figsize=(xfig_size, yfig_size),
        ncols=ncols,
        nrows=nrows
        )

    for i in range(len(data_arr)):
        im = ax[i].imshow(data_arr[i], origin='lower')
        if spectrum:
            ax2 = ax[i].twinx()
            ax[i].autoscale(False)
            ax2.plot(data_arr[i].sum(axis=0), color='black', alpha=0.2)
            ax2.set_ylabel('S/N')
        fig.colorbar(im, ax=ax[i])

    if len(xticks) > 0 and len(xtick_labels) > 0:
        for i in range(len(ax)):
            if (direction == 'vertical' and i == len(ax)-1) or direction == 'horizontal':
                ax[i].set_xlabel('Time (s)')
                ax[i].set_xticks(xticks)
                ax[i].set_xticklabels(xtick_labels)
            else:
                plt.setp(ax[i].get_xticklabels(), visible=False)

    if len(yticks) > 0 and len(ytick_labels) > 0:
        for i in range(len(ax)):
            if (direction == 'horizontal' and i == 0) or direction == 'vertical':
                ax[i].set_ylabel('Frequency (MHz)')
                ax[i].set_yticks(yticks)
                ax[i].set_yticklabels(ytick_labels)
            else:
                plt.setp(ax[i].get_yticklabels(), visible=False)

    plt.tight_layout()
    if savefig:
        plt.savefig("%s.%s" % (fig_name, ext), dpi=dpi)
