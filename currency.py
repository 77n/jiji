import sys
import pandas as pd
import urllib.request, json
from pprint import pprint


def main(currency):
    """
    Arg: currency (str) - three-character currency code like 'USD'
    Return: dict with task results
    """
    
    link = 'https://bank.gov.ua/NBU_Exchange/exchange_site?start=20210101&end=20211231&sort=exchangedate&order=desc&json'
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
    
    df = pd.DataFrame.from_dict(data) # all currencies
    df_currency = df[df['cc'] == currency] # selected currency
    
    result = {}
    result['Дати із найнижчим курсом'] = df_currency[df_currency['rate'] == df_currency['rate'].min()]['exchangedate'].to_list()
    result['Дати із найвищим курсом'] = df_currency[df_currency['rate'] == df_currency['rate'].max()]['exchangedate'].to_list()
    result['Середньорічний курс'] = df_currency['rate'].mean()
    result['Стандратне відхилення'] = df_currency['rate'].std(ddof=0) # ddof=0 for division by N (not N-1) as we have all data
    
    currency_rate = df[df['cc'] == currency]['rate'].reset_index(drop=True) # reset_index for correct following division
    euro_rate = df[df['cc'] == 'EUR']['rate'].reset_index(drop=True) # no need to worry about sort, data already sorted in sourse
    result['Середньорічний крос-курс до євро'] = (currency_rate / euro_rate).mean() # data is already sorted by date in source

    other_currencies_means = df[['cc', 'rate']].groupby('cc').aggregate('mean').drop(currency) # excluding selected currency
    result['Код валюти, яка має найближчий середьорічний курс'] = (other_currencies_means - result['Середньорічний курс']).abs().idxmin()[0]
    
    return result


if __name__ == '__main__':

    currency = sys.argv[1]
    pprint(main(currency))