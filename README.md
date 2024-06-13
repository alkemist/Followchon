### Install python 3.10
https://gist.github.com/rutcreate/c0041e842f858ceb455b748809763ddb

### Install pip

`sudo apt install python3-pip`

### Install pipenv

`brew upgrade pipenv`

### Install dependencies

`pipenv install`

### Run python with dependencies

`pipenv run python main.py`

### Change python version

`sudo apt install python<version>`  
`sudo update-alternatives --install /usr/bin/python python /usr/bin/python<version> <priority>`  
`sudo update-alternatives --config python`

#### Usage with conda

`conda config --append channels conda-forge`
`conda config --append channels pytorch`
`conda config --append channels nvidia`
`python<version> -m conda install <package>`

### Change yolo/ settings

`yolo settings datasets_dir=''`

### Check graphic card

`nvidia-smi`  


