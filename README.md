# selenium-testing

## Level 0

```
Must be logged in the webpage and logged out when completing testing in each testcase (automatically)
username: student (for Create event and Get calendar url) or teacher (for Set maximum grade for assignment)
password: moodle
web_url: https://qa.moodledemo.net/
```

> For `Create event` feature, before run the next testcase, in the previous testcase, it must remove that new event (remove automatically)

## Level 1

```
Must be logged in the webpage and logged out when completing testing in each method of a feature testing (automatically)
username: student (for Create event and Get calendar url) or teacher (for Set maximum grade for assignment) 
password: moodle
web_url: https://qa.moodledemo.net/
```

> For `Create event` feature, before run the next testcase, in the previous testcase, it must remove that new event (remove automatically)
> Notes: must close these windows to not affect testcases (not automatic)

<img src="./images/note 1.png">

<img src="./images/note 2.png">


### In project directory, use this command

```
cd Level_1
cd [Feature] 
```
Example: cd Create_event

### Run commmand

- MacOS/Linux:

```
python3 UseCase.py
python3 EquivalenceClass.py
python3 DecisionTable.py
python3 Boundary.py
```
- Windows:
```
python UseCase.py
python EquivalenceClass.py
python DecisionTable.py
python Boundary.py
```

