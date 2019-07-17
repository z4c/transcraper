# transcraper
Transavia Scraper


## Install

Create a new python's virtual env
```bash
python3 -mvenv . && source bin/activate
```

Install required packages
```bash
pip install requests lxml python-dateutil click
```

## Usage
Run it 
```bash
python ./main.py --frm AIRPORT_CODE --to AIRPORT_CODE
```
It should print
```
From ORY: 2019-08-22 (58 €), 2019-08-25 (78 €)
To AMS 2019-08-22 (58 €), 2019-08-25 (78 €)
```

