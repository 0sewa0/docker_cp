import os
import io
import docker
import tarfile
import argparse

from docker.models.containers import Container

class DockerCp:

    def __init__(self, path_from: str, path_to: str, buffer_size: int, is_archive: bool):
        self._path_from = path_from
        self._path_to = path_to
        self._buffer_size = buffer_size
        self._is_archive = is_archive

        self._container_id: str
        self._is_from: bool
        if self.is_container_path(self._path_from):
            self._container_id, self._path_from = self._path_from.split(':')
            self._is_from = True
        elif self.is_container_path(self._path_to):
            self._container_id, self._path_to = self._path_to.split(':')
            self._is_from = False
        else:
            raise ValueError('No container specified in path.')

        self._container: Container = docker.from_env().containers.get(self._container_id)
        self._copy()

    def _copy(self):
        if self._is_from:
            self._copy_from_container()
        else:
            self._copy_to_container()

    def _copy_to_container(self):
        if os.path.exists(self._path_from):
            tmp = ''
            location = self._path_from
            if not self._is_archive:
                if os.path.isdir(self._path_from):
                    tmp = self._path_from + '.tar'
                    location = tmp
                    with tarfile.open(tmp, "w") as tar:
                        tar.add(self._path_from, arcname=os.path.basename(self._path_from))
            with open(location, 'rb') as tar:
                    self._container.put_archive(path=self._path_to, data=tar)
            if tmp:
                os.remove(tmp)
        else:
            print('File doesn\'t exists.')
    
    def _copy_from_container(self):
        tar_gen, info = self._container.get_archive(self._path_from)
        final_dest = self._path_to
        if os.path.isdir(self._path_to):
            final_dest = os.path.join(final_dest, info.get('name'))
        with open(final_dest, 'wb+', buffering=self._buffer_size) as file:
                for byte in tar_gen:
                    file.write(byte)
        if not self._is_archive:
            tarfile.open(final_dest).extractall()


    @staticmethod
    def is_container_path(path: str) -> bool:
        if ':' not in path:
            return False
        container, file_path = path.split(':')
        return container and file_path


    def __str__(self) -> str:
        _from = ":".join([self._container_id, self._path_from]) if self._is_from else self._path_from
        _to = ":".join([self._container_id, self._path_to]) if not self._is_from else self._path_to
        return f'DockerCp: from: { _from }, to: {_to}, buffer: {self._buffer_size}, archive: {self._is_archive}'


def __parse_args__() -> dict:
        parser = argparse.ArgumentParser(prog='docker_cp')

        parser.add_argument('-b', '--buffer-length',
            help='Specify buffer-size, defaults to 0',
            default=0,
            type=int,
            dest='buffer_size')

        parser.add_argument('-a','--archive',
            help='copy_from => copies into an archive | copy_to => expects to copy an archive',
            default=False,
            dest='is_archive')

        parser.add_argument('path_from',
        help='Path to the item to be copied.',
        type=str)

        parser.add_argument('path_to',
            help='Path where the item will be copied.',
            type=str)

        return dict(parser.parse_args()._get_kwargs())

if __name__ == '__main__':
    args = __parse_args__()
    if DockerCp.is_container_path(args.get('path_from')) or DockerCp.is_container_path(args.get('path_to')):
        cp = DockerCp(**args)
    else:
        raise ValueError('No container specified in path.')