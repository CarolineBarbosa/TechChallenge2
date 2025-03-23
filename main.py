from scrapper import main
from datetime import datetime, timedelta
if __name__ == "__main__":

    today = datetime.today().strftime('%Y-%m-%d')
    main(today)
