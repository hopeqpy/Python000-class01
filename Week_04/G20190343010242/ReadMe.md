## Week 04 Assigments

See [here](https://u.geekbang.org/lesson/8?article=201458) for the requirements.

### Task 1

Ansible will be installed as docker container, and start/stop nginx operations will be acted within the container.

#### Prerequisites

- Unix like system. (Linux or MacOs)
- Docker installed.

#### Run task

Go to folder task1, run command
```
$ ./ansible.sh <action> <image name> <image version>
``` 
You must specify all the params.
'action' param can only be 'start', 'stop' and 'clean'.

'image name' params is arbitrary legal value for the docker image.

'image version' will be the image tag which skips 'v' prefix.

e.g.
```
$ ./ansible.sh start myansible 1.0.0
```
You can start/stop the nginx service by passing action value.

Finally, you can clean up everything if you don't need it by passing 'clean' action.

#### To-Dos

The task can only under local host, it hasn't been applied and tested on remote hosts which requires ssh setup.

### Task 2

The task was done by jupyter notebook.

#### Prerequisites

- Python3 and pip

#### Steps

1. Install python environment
    ```bash
    $ python3 -m venv <your preferred virtual env name>
    $ source <venv in prev cmd>/bin/activate
    ```
2. Install required libs
    ```bash
    $ pip install -r requirements.txt
    ```
3. Start jupyter
    ```bash
    $ cd task2
    $ jupyter notebook
    ```
4. Run cells one by one or run all the cells in the notebook.
   
   You can either run the notebook in the browser or vscode.