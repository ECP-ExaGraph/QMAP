import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import sys

# https://github.com/matplotlib/matplotlib/issues/5862#issuecomment-197330145
def fix_eps(fpath):
    """Fix carriage returns in EPS files caused by Arial font."""
    txt = b""
    with open(fpath, "rb") as f:
        for line in f:
            if b"\r\rHebrew" in line:
                line = line.replace(b"\r\rHebrew", b"Hebrew")
            txt += line
    with open(fpath, "wb") as f:
        f.write(txt)
        
def draw_lines(input_name):
    width = 5
    font_size = 30

    #set palette
    sns.set()
    sns.set_style("whitegrid", {'grid.color': '.5', 'grid.linestyle': u'-'})
    palette = sns.cubehelix_palette(n_colors=3, start=0, rot=0.17, gamma=3.1, \
                                hue=0.9, light=0.9, dark=0.5, reverse = False, as_cmap=False)
    sns.set_palette(palette)

    fig = plt.figure(figsize = (20, 7), dpi = 150)
    #fig = plt.figure(dpi=150)
    ax = plt.gca()
    fig.canvas.draw()

    df = pd.read_csv(input_name + '.csv', delimiter = ',')

    from itertools import cycle
    linecycler = cycle(["-","--",":","-."])
    markercycler = cycle(['o', 'v', 'D', 'd', 'p', 's'])

    np = df.shape[0]
    ns = df.shape[1]

    import numpy.matlib
    r = numpy.matlib.zeros(shape = [np, ns], dtype = float)
    df_mins = df.min(axis=1)
    for index, row in df.iterrows():
        r[index] = row / df_mins[index]
        #print r[index]
    #transpose the matrix to sort on each column
    r= numpy.transpose(numpy.sort(numpy.transpose(r)))

    lines = []
    pos = list(range(1, np + 1))
    for i in range(0, ns):
        xs = numpy.repeat(r[:,i], 2).tolist()[0][1:]
        ys = [float(i) /np for i in numpy.repeat(pos, 2)[:-1]]
        lines.append(ax.plot(xs, ys, linestyle = next(linecycler), \
                     marker = next(markercycler), \
                     markersize=11, linewidth=4))

    # associate each tick with thread number
    #ax.xaxis.grid(False)
    ax.tick_params(labelsize = 25)
    ax.set_xlabel('Performance Relative to the Best Algorithm', fontsize = font_size)
    ax.set_ylabel('Fraction of Problems (' + str(np) + ' settings)', fontsize = font_size)
    # associate each tick with thread number
    ax.set_ylim([0, 1.05])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])

    # set legend, exclude threadnumber
    leg = fig.legend(ax.lines, list(df), \
                    ncol = 1, frameon=True, fancybox = True, \
                    prop={'size':35}, shadow = False, framealpha=0.1, \
                    bbox_to_anchor = (0.82, 0.56))
    leg.get_frame().set_edgecolor('k')
    leg.get_frame().set_linewidth(1)

    plt.show()
    fig.savefig(input_name + '.pdf', format = 'pdf', bbox_inches='tight')
    fig.savefig(input_name + '.eps', format = 'eps', bbox_inches='tight', dpi = fig.dpi)
    fix_eps(input_name + '.eps')

    return

# change path accordingly

if __name__ == '__main__':
    
    filename=str(sys.argv[1])
    print("Processing: ",filename)
    draw_lines(filename)
