# transcraper
Transavia Scraper


## Install
Clone the repo
```bash
git clone https://github.com/z4c/transcraper.git 
cd transcraper
```

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
python3 ./main.py --help
```

Without any args it should print
```
From ORY: 2019-08-22 (58 €), 2019-08-25 (78 €)
To AMS 2019-08-22 (58 €), 2019-08-25 (78 €)
```

