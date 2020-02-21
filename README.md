# robo-advisor

Project description: https://github.com/prof-rossetti/intro-to-python/blob/master/projects/robo-advisor/README.md

## Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

```sh
pip install -r requirements.txt
```

## API Setup

Visit https://www.alphavantage.co/support/#api-key and obtain an API Key.


Create a new file in this repo called .env and place inside the following contents:

```
ALPHAVANTAGE_API_KEY="___________"
```

## Usage

From within the virtual environment, demonstrate your ability to run the Python script from the command-line:

```sh
python app/robo_advisor.py
```