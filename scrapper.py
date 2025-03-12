from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
import os
# import boto3

def main(date_input):
    data = get_b3_data(date_input)
    if data is not None:
        save_data_to_s3(data, date_input)



def save_data_to_s3(data, date_input):
    file_name = f'data/b3_pregao_{date_input}.parquet'
    data.to_parquet(file_name, index=False)
    # mudar aqui para adicionar os dados no S3
    # BUCKET = 'amzn-s3-demo-bucket'
    # s3 = boto3.client('s3')
    # with open(file_name, 'rb') as data:
        # s3.Bucket( BUCKET ).put_object(Key='{date_input}.parquet', Body=data)


def get_b3_data(date):

    formatted_date = format_date(date)
    # url = 
    url = f"https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br&date={formatted_date}"
    
    with sync_playwright() as p:
        browser = launch_browser(p)
        page = browser.new_page()
        page.goto(url)
        data = scrappe_data(page, date)
        browser.close()
        return data
    
def format_date(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')

def launch_browser(p):
    for browser_type in ['chromium', 'firefox', 'webkit']:
        try:
            if browser_type == 'chromium':
                return p.chromium.launch(headless=False)
            elif browser_type == 'firefox':
                return p.firefox.launch(headless=False)
            elif browser_type == 'webkit':
                return p.webkit.launch(headless=False)
        except Exception as e:
            print(f"Failed to launch {browser_type} browser: {e}")
    raise RuntimeError("All browser types failed to launch.")

def scrappe_data(page, date):

    try:
        page.wait_for_load_state('networkidle')    
        return get_downloaded_file(page, date)
    except Exception as e:
        print(f"Download button not found or error during download: {e}")
        return None

def get_downloaded_file(page, date):
    download_path = download_daily_file(page, date)
    df = read_downloaded_file(download_path)
    os.remove(download_path) 

    return df

def download_daily_file(page, date):

    page.click('text=Download')
    with page.expect_download() as download_info:
        download = download_info.value
    download_path = f"b3_{date}.csv"
    download.save_as(download_path)
    print(f"File downloaded successfully: {download_path}")
    return download_path

    
def read_downloaded_file(download_path):
    if download_path is not None:
        df = pd.read_csv(download_path, encoding='iso-8859-1', sep=';', decimal=',', header=1, usecols=[0, 1, 2, 3, 4])
        df.columns = ['Codigo', 'Acao', 'Tipo', 'Qtde_Teorica', 'Part_Percentual']
        return df[:-2] 
    else:
        raise Exception("Failed to download the file.")

