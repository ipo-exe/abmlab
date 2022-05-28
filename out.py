'''

File Output routines source code

Copyright (C) 2022 Iporã Brito Possantti


************ GNU GENERAL PUBLIC LICENSE ************

https://www.gnu.org/licenses/gpl-3.0.en.html

Permissions:
 - Commercial use
 - Distribution
 - Modification
 - Patent use
 - Private use

Conditions:
 - Disclose source
 - License and copyright notice
 - Same license
 - State changes

Limitations:
 - Liability
 - Warranty

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

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