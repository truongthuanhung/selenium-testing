# selenium-testing

## Prepare data for Search-Activity feature
> No need
## Prepare data for Submit-Assignment feature
- Windows:
    > Place a copy version of folder `submit-assignment` of the project in C drive\
    > Test environment: `Chrome`
- MacOS/Linux:
    > The `Submit-Assignment` feature are not supported for both level-0 and level 1, if you want to run level-0 and level-1, you have to change the path input of all file.

## Config for level 0

```
Must be logged in the webpage
username: student10
password: moodle
web_url: https://qa.moodledemo.net/
```

>For `Submit-Assignment` feature, before run any level-0 testcase, you have to remove the file from the submission. The remove file action will only be automatic in level-1

> For `Submit-Assignment` and `Search-Activity` feature, the login action will be automatic in level-1

## Config for level 1
### Install virtual environment

```
pip install virtualenv
```

### Create virtual environment
- MacOS/Linux:
```
python3 -m venv .venv
```
- Windows:
```
python -m venv .venv
```

### Start virtual environment

- MacOS/Linux:
```
source .venv/bin/activate
```
- Windows:
```
.venv\Scripts\activate
```

### Install selenium
- MacOS/Linux:
```
python3 -m pip install -r requirements.txt
```
- Windows:
```
python -m pip install -r requirements.txt
```

### In project directory, use this command

```
cd level-1
```
### Run commmand

- MacOS/Linux:

```
python3 run.py clean
python3 run.py test Submit-Assignment usecase
python3 ruy.py test Submit-Assignment equivalence
python3 run.py test Submit-Assignment boundary
python3 run.py test Search-Activity usecase
python3 run.py test Search-Activity equivalence
```
- Windows:
```
python run.py clean
python run.py test Submit-Assignment usecase
python ruy.py test Submit-Assignment equivalence
python run.py test Submit-Assignment boundary
python run.py test Search-Activity usecase
python run.py test Search-Activity equivalence
```

### Deactive virtual environment

- MacOS/Linux/Windows:
```
deactivate
```