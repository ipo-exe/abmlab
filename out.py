import os


def export_gif(dir_output, dir_images, nm_gif='animation', kind='png', suf=''):
    """
    export gif animation
    :param dir_images: directory path of images
    :param nm_gif: name of gif file
    :param kind: kind of image format
    :param suf: string suffix
    :return: gif file path
    """
    import imageio
    # empty list
    lst_images = []
    for file_name in sorted(os.listdir(dir_images)):
        if suf != '':
            if file_name.endswith('.{}'.format(kind)) and file_name.startswith(suf):
                file_path = os.path.join(dir_images, file_name)
                lst_images.append(imageio.imread(file_path))
        else:
            if file_name.endswith('.{}'.format(kind)):
                file_path = os.path.join(dir_images, file_name)
                lst_images.append(imageio.imread(file_path))
    # gif name
    fpath = dir_output + '/{}.gif'.format(nm_gif)
    # save gif
    imageio.mimsave(fpath, lst_images)
    return fpath