from scrapper import main
from datetime import datetime, timedelta
if __name__ == "__main__":
    # date_input = input("Selecione a data do pregão (YYYY-MM-DD): ")

    # start_date = datetime(2025, 2, 11)
    # end_date = datetime(2025, 2, 11)
    # date_list = [str((start_date + timedelta(days=x)).strftime('%Y-%m-%d')) for x in range((end_date - start_date).days + 1)]

    # for date_input in date_list:
    #     # print(date_input)
    today = datetime.today().strftime('%Y-%m-%d')
    main(today)
