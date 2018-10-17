# ENGR1624

## Install Instructions

### 1. Install Python3 (the latest version). You can do this by doing one of the following based on your operating system.

#### Windows:
Download python at the following url: [https://www.python.org/downloads/](https://www.python.org/downloads/). Make sure to download the latest version that formatted like this `Python 3.X.X`.

#### Mac:
First, install HomeBrew, a package manager, that allows you to easily install packages.
```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
Then, at the bottom of your `~/.profile` file, add the following line:
```
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
```
Next, install python with the following command.
```
brew install python
```

### 2. Clone this GitHub Repository. You can do that by typing the following command:
```
git clone https://github.com/rithik/ENGR1624
```

### 3. Create a Virtual Environment (you can skip this step if you want). A Virtual Environment only installs packages for that project and not for your entire computer. Use the following commands:

```
virtualenv venv
source venv/bin/activate
```

If `virtualenv` is not installed, use this command: `pip3 install virtualenv`. Then re-run the previous set of commands.

To get out of your virtual environment, use the command `deactivate`.

### 4. Install all of the required libraries. 

Run the following command to install all of the required packages `pip3 install -r requirements.txt`. If you run into issues installing the `opencv` package, use this link for help: [https://pypi.org/project/opencv-python/](https://pypi.org/project/opencv-python/).

### 5. Run the program. 

Start the program by typing `python3 detection.py`. To quit out of the program, click on the window with your video feed and hit the `q` key.
