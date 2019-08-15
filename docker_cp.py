import os
import docker
import argparse

class DockerCp:

    def __init__(self, path_from: str, path_to: str, buffer_size: int, is_archive: bool):
        self._path_from = path_from
        self._path_to = path_to
        self._buffer_size = buffer_size
        self._is_archive = is_archive

        if self.is_container_path(self._path_from):
            self._container_id, self._path_from = self._path_from.split(':')
            self._is_from = True
        elif self.is_container_path(self._path_to):
            self._container_id, self._path_to = self._path_to.split(':')
            self._is_from = False
        else:
            raise ValueError('No container specified in path.')
        
        self._container = docker.from_env().containers.get(self._container_id)
        self._copy()
        print(self)

    def _copy(self):
        if self._is_from:
            self._copy_from_container()
        else:
            self._copy_to_container()

    def _copy_to_container(self):
        pass
    
    def _copy_from_container(self):
        pass

    @staticmethod
    def is_container_path(path: str):
        if ':' not in path:
            return False
        container, file_path = path.split(':')
        return container and file_path

    def __str__(self):
        _from = ":".join([self._container_id, self._path_from]) if self._is_from else self._path_from
        _to = ":".join([self._container_id, self._path_to]) if not self._is_from else self._path_to
        return f'DockerCp: from: { _from }, to: {_to}, buffer: {self._buffer_size}, archive: {self._is_archive}'



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
    if DockerCp.is_container_path(args.get('path_from')) or DockerCp.is_container_path(args.get('path_to')):
        cp = DockerCp(**args)
    else:
        raise ValueError('No container specified in path.')