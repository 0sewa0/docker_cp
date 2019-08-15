import argparse



class DockerCp:

    def __init__(self, path_from, path_to, buffer_size, is_archive):
        self._path_from = path_from
        self._path_to = path_to
        self._buffer_size = buffer_size
        self._is_archive = is_archive

    def __str__(self):
        return f'DockerCp: from: {self._path_from}, to: {self._path_to}, buffer: {self._buffer_size}, archive: {self._is_archive}'



def __parse_args__():
        parser = argparse.ArgumentParser(prog='docker_cp')
        parser.add_argument('path_from',
            help='Path to the item to be copied.',
            type=str)
        
        parser.add_argument('path_to',
            help='Path where the item will be copied.',
            type=str)
        parser.add_argument('-b', '--buffer-length',
            help='Specify buffer-size, defaults to 0',
            default=0,
            type=int,
            dest='buffer_size')
                    
        parser.add_argument('-a','--archive',
                        help='copy_from => copies into an archive\ncopy_to => expects to copy an archive',
                        default=False,
                        dest='is_archive')
        return parser.parse_args()

if __name__ == '__main__':
    args = dict(__parse_args__()._get_kwargs())
    cp = DockerCp(**args)
    print(cp)