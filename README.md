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
pip install requests lxml python-dateutil click logzero
```

## Usage
Run it 
```bash
./main.py --help
Usage: main.py [OPTIONS]

  A simple script to scrape Transavia flights

Options:
  -d, --departure TEXT        Departure airport code. default ORY ( Paris Orly).
  -f, --fromdays INTEGER      Departure date in days ( now + days ). default 15 days.
  -a, --arrival TEXT          Arrival airport code. default AMS ( Amsterdam Schiphol ).
  -t, --todays INTEGER        Arrival date in days ( now + days ). default 22 days.
  -ac, --adultcount INTEGER   Adults. default 1.
  -cc, --childcount INTEGER   children. default 0.
  -ic, --infantcount INTEGER  Infants. default 0.
  --help                      Show this message and exit.
```

Without any args it should print something like
```
From ORY: 2019-08-22 (58 €), 2019-08-25 (78 €)
To AMS: 2019-08-22 (58 €), 2019-08-25 (78 €)
```

