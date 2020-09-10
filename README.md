# SunLearn Notification Bot
This is created to help Lecturers and postgraduate students of Stellenbosch University respond to
forum questions from undergraduate students quicker.
This python bot goes to the given SunLearn forum page(s) and notifies a MS Teams group about the new
question. It can also assigns it to a random person to answer.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites
This project was created using [Python 3.8.5](https://docs.python.org/3/using/index.html). Although it
might not be necessary to use this specific version for the project, this document will detail
the bot being setup using said version.

Along with Python, pip is required and a virtual environment is recommended. The following resources will
detail how to setup pip and start a virtual environment:
- https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

The following are the important modules needed and links to each of their install pages:
- [selenium](https://pypi.org/project/selenium/)
- [pymsteams](https://pypi.org/project/pymsteams/)
- [schedule](https://pypi.org/project/schedule/)

When the correct version of Python and pip is installed, the above mentioned packages can be installed
as follows:
```commandline
pip install selenium pymsteams schedule
```

### Installing
Download this repository to the folder setup in the previous step, activate the python environment, and
run the python file.

## Running
### Config
The config file is in the form of a json document. Here you can specify the forum(s) you want to be
watched, the assignees' names, and the code for connecting to Microsoft Teams.

```json
{
  "assignees": [
    "Name1 Surname1",
    "Name2 Surname2"  
  ],
  "forums": [
    "website link to sunlearn forum 1",
    "website link to sunlearn forum 2"
  ],
  "msteams": "MS Teams webhook link"
}
```

This is currently setup to post it only to MS Teams. To get the MS Teams webhook link follow the guide on:

https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook

In the directory of the project activate the virtual environment (see [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/))
and then run the Python file:
```commandline
python main.py
```

It will ask you a series of questions, such as:
- "Run every X minutes [10]:" => Every X minutes it will check each of the forums for new messages
- "Username:" => Stellenbosch SunLearn username
- "Password:" => Stellenbosch SunLearn password

## Final Remarks
This is not a full implementation of a bot that could help demis and lecturers with the 
SunLearn forums, but an initial attempt. Feel free to fork and add onto the project, make a pull request or
use it in your own projects. If you would like functionality added (such as support for Slack messaging) 
but do not have the Python capabilities to add it, email me at 23319003@sun.ac.za and I will look into adding it. 

## Authors
- Guillaume Odendaal - Initial work

## Acknowledgements
- Hat tip to Daniel Kritzinger