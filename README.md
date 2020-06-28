# Spoken language identification API

Simple Flask API around Pytorch model for identifying spoken language from speech

⚠ The app cannot really be run because the large language identification models are not included in this repository.

A client app that uses this API can be found [here](https://github.com/jorgenvvv/lang-id-client).

## Installation

Clone the repository.

```bash
git clone https://github.com/jorgenvvv/lang-id-server
```

Install the required packages.

```bash
pip install -r requirements.txt
```

Rename the `config.example.py` file to `config.py` and change the values if needed.

The model loading is done in the `language_identifier.py` file and some changes need to be made there. The paths that point to the model need to be modified.

Running the app in development mode can be done by executing the following commands

```bash
FLASK_APP=lang-id-server
FLASK_ENV=development

flask run --port 5005
```
