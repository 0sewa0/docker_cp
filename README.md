# Task 

Containers are commonly used in our infrastructure. It is therefore important to have at least some idea how they work. The first task is to write an implementation of `docker cp` command, that is, a command that copies a file from or to the container using a fixed size buffer. The solution we're looking for shouldn't need to create any temporary file in the container, start any new processes in the container, nor export the entire container file system during the write. Choose any language you want - using SDK or library like docker-py or docker-api is allowed as long as the latest version is used, and only functions that haven't been deprecated or obsoleted are used.
Executing `docker` commands isn't allowed.

An example run of the command should look like this:

    $ docker run -d --name test fedora:25 /usr/bin/sleep
    293f80ab6d2bf57e85a6d10762b3cc795cdb104a152d0257471b63544e093166
    $ docker-cp --bufer-length=4 test:/etc/fedora-release .
    $ cat fedora-release
    Fedora release 25 (Twenty Five)

## Exmaple calls
* copy the file to the `host machine`:
    
        python3 docker_cp.py --buffer-length=4 test:/etc/fedora-release .`
* copy the file to the `host machine` as a tar (dosen't extracts the tar):

        python3 docker_cp.py --buffer-length=4 --archive true test:/etc/fedora-release .`
* copy the tar file to the `docker machine` (dest folder **MUST** exist):

        python3 docker_cp.py --buffer-length=4 --archive true ./fedora-release-file test:/etc/fedora/

* copy the file/folder to the `docker machine` (dest folder **MUST** exist):

        python3 docker_cp.py --buffer-length=4 ./fedora-release-file test:/etc/fedora/

## Known issues

When copied item from the `docker machnice` is a folder, then it wont be able to extract the tar after the copy so it will throw an error without `--archive true`. You can use `tar -xf <FILE>` to extract it. 

[issue](https://bugs.python.org/issue30438) 