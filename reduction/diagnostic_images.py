from spectral_cube import SpectralCube
import numpy as np
from functools import reduce
import pylab as pl
from astropy import visualization

imnames = ['image', 'model', 'residual',]

def load_images(basename, crop=True):

    cubes = {imn: SpectralCube.read(f'{basename}.{imn}.tt0', format='casa_image')
             for imn in imnames}

    casamask = SpectralCube.read(f'{basename}.mask', format='casa_image')
    pb = SpectralCube.read(f'{basename}.pb.tt0', format='casa_image')


    #masks = [cube != 0 * cube.unit for cube in cubes.values()]
    #include_mask = reduce(lambda x,y: x or y, masks)
    #include_mask = cubes['residual'] != 0*cubes['residual'].unit
    include_mask = pb > 0.05*pb.unit

    cubes['mask'] = casamask
    cubes['pb'] = pb

    imgs = {imn:
            cubes[imn].with_mask(include_mask).minimal_subcube()[0]
            if crop else
            cubes[imn].with_mask(include_mask)[0]
            for imn in imnames}
    imgs['mask'] = (cubes['mask'].with_mask(include_mask).minimal_subcube()[0]
                    if crop else
                    cubes['mask'].with_mask(include_mask)[0])
    imgs['includemask'] = include_mask # the mask applied to the cube

    return imgs, cubes

asinhn = visualization.ImageNormalize(stretch=visualization.AsinhStretch())

def show(imgs, zoom=None, clear=True, norm=asinhn, **kwargs):

    if clear:
        pl.clf()


    for ii,imn in enumerate(imnames):
        ax = pl.subplot(1, len(imnames), ii+1)

        if np.isscalar(zoom):
            shp = imgs[imn].shape
            view = [slice(int((-ss*zoom + ss)/2),
                          int((ss*zoom + ss)/2))
                    for ss in shp]
        elif zoom is None:
            view = [slice(None), slice(None)]
        else:
            view = zoom

        ax.imshow(imgs[imn].value[view], origin='lower', interpolation='none',
                  norm=norm, **kwargs)

        if imn == 'model':
            ax.contour(imgs['mask'].value[view], levels=[0.5], colors=['w'])

        pl.title(imn)

        ax.set_xticklabels([])
        ax.set_yticklabels([])