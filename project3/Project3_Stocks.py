'''
Created on Feb 5, 2013

@author: Harry
'''
#Harry Pham 79422112
import datetime, yahoofinance, indicators, signals, os

start_menu = """
Stock Program --- Choose one
 1: Start Program in Online Mode Using Yahoo Finance
 2: Start Program in Offline Mode Using a Yahoo Finance .csv file from your computer
 q: Quits Stock Program
"""

def start()->None:
    '''Startup Program'''
    while True:
        response=input(start_menu).strip().lower()
        if response=='1':
            return stocks('online')
        elif response=='2':
            return stocks('offline')
        elif response=='q':
            return
        else:
            _invalid_command(response)


strategy_menu="""
Strategies --- Choose One:
 s: N-day simple moving average
 d: N-day directional indicator
"""

offline_menu='''
Offline Mode --- Choose one
 d: Use file from given path to run stock program
 s: Use search program to search for files in a given directory
 r: Returns to Main Menu
 q: Quits Stock Program
 '''

error_menu='''
There was an error with getting the file from Yahoo Finance --- Choose One
 o: Move to offline mode
 t: Try again
 q: Quits Stock Program
 '''

end_menu='''
What do you want to do now? --- Choose One
 1: Run another analysis in online mode
 2: Run another analtsis in offline mode
 q: Quits Stock Program
 '''

def stocks(mode:str)->None:
    '''Main Program'''
    if mode == 'offline':
        while True:
            response=input(offline_menu).strip().lower()
            if response == 'd':
                path=input('Please enter the directory path: ')
                date, close_price = _file_contents(path)
                tickerid='File: {}'.format(path)
                break
            elif response == 's':
                directory=input('Please enter a directory to search in: ')
                currentdir=os.path.abspath(directory)
                filesincurdir=os.listdir(currentdir)
                if len(filesincurdir)==0:
                       print('No Files found. Please try again.')
                       return stocks(offline)
                else:
                    files=[]
                    for i in range(len(filesincurdir)):
                        if os.path.isfile(os.path.join(currentdir,filesincurdir[i])):
                            files.append(os.path.join(currentdir,filesincurdir[i]))
                    for i in range(len(files)):
                        print('{:2}: {}'.format(i+1, files[i]))
                    while True:
                        try:
                            response=int(input('These files were found in the directory. Please choose the file you want to run stock program on: ').strip())
                            if response in range(len(files)+1):
                                path=os.path.join(currentdir,files[response-1])
                                print("File has been retrieved from {}.".format(path),end='\n\n')
                                try:
                                    date, close_price = _file_contents(path)
                                    tickerid='File: {}'.format(files[response-1])
                                except:
                                    print("An error has occured.  This file is probably not a yahoofinace .csv file.",end='\n\n')
                                    raise ValueError("Invalid file")
                                break
                            else:
                                _invalid_command(str(response))
                        except ValueError:
                            pass
                break
            elif response == 'r':
                return start()
            elif response == 'q':
                return
            else:
                invalid_command(response)
    if mode == 'online':
        while True:
            tickerid=input('Please input a ticker ID: ').strip().upper()
            break
        start = None
        end = None
        while start == None:
            start=_start_date()
        while end == None:
            end=_end_date()
            while start>=end:
                print('Please enter a ending date later than the starting date.')
                end = None
                end=_end_date()
        url=_url_builder(tickerid,start,end)
        print('Retrieving data...')
        try:
            date, close_price = yahoofinance._download_url(url)
        except:
            print('Error with getting file')
            while True:
                response=input(error_menu).strip().lower()
                if response=='o':
                    stocks('offline')
                elif response=='t':
                    stocks('online')
                elif response=='q':
                    return
                else:
                    _invalid_command(response)
    while True:
        signal_strategy=input(strategy_menu).strip().lower()
        if signal_strategy=='s':
            while True:
                try:
                    days=int(input('How many days: ').strip())
                    break
                except ValueError:
                    print('Please enter a number.')
            buy=None
            sell=None
            indicator=execute_indicators(indicators.Simple(),close_price,days)
            simple_indicator=signals.Average(close_price,indicator)
            signal=simple_indicator.execute()
            break
        elif signal_strategy=='d':
            while True:
                try:
                    days=int(input('How many days: ').strip())
                    break
                except ValueError:
                    print('Please enter a number')
            while True:
                try:
                    buy=int(input('Buy when indicator is above: ').strip())
                    break
                except ValueError:
                    print('Please enter a number')
            while True:
                try:
                    sell=int(input('Sell when indicator is below: ').strip())
                    break
                except ValueError:
                    print('Please enter a number')
            indicator=execute_indicators(indicators.Directional(),close_price,days)
            directional_indicator=signals.Directional(indicator)
            signal=directional_indicator.execute(buy,sell)
            break
        else:
            _invalid_command(signal_strategy)
    _final_report(tickerid, signal_strategy, days, date, close_price, indicator, signal, buy, sell)
    end_response=input(end_menu).strip().lower()
    if end_response=='1':
        return stocks('online')
    elif end_response=='2':
        return stocks('offline')
    elif end_response=='q':
        return
    
def _start_date()->None:
    '''Returns a Starting Date'''
    while True:
        try:
            date=input("Please enter a starting date in the following format(YYYY-MM-DD): ").strip()
            year, month, day = date.split('-')
            year=int(year.lstrip('0'))
            month=int(month.lstrip('0'))
            day=int(day.lstrip('0'))
            start_date=datetime.date(year, month, day)
            break
        except ValueError:
            print('This date is not valid.  Please try again.')
    while True:
        response=input('Is {} the correct starting date (Y/N)'.format(start_date)).strip().lower()
        if response=='y':
            return start_date
        elif response=='n':
            break
        else:
            print('Please enter N for No or Y for Yes.')

def _end_date()->None:
    '''Returns an Ending Date'''
    while True:
        try:
            date=input("Please enter a ending date in the following format(YYYY-MM-DD): ").strip()
            year, month, day = date.split('-')
            year=int(year.lstrip('0'))
            month=int(month.lstrip('0'))
            day=int(day.lstrip('0'))
            end_date=datetime.date(year, month, day)
            break
        except ValueError:
            print('This date is not valid. Please try again.')
    while True:
        response=input('Is {} the correct ending date (Y/N)'.format(end_date)).strip().lower()
        if response=='y':
            return end_date
        elif response=='n':
            break
        else:
            print('Please enter N for No or Y for Yes.')


def _invalid_command(response:str)->None:
    """Prints message for invalid commands"""
    print("Sorry; '" + response + "' isn't a valid command.  Please try again.")

def _url_builder(tickerid:str, start:"datetime", end:"datetime")->str:
    url='http://ichart.yahoo.com/table.csv?s={}&a={}&b={}&c={}&d={}&e={}&f={}&g=d'.format(tickerid, start.month-1, start.day, start.year,
                                                                                            end.month-1, end.day, end.year)
    return url

def _file_contents(path:str)->(list,list):
    file=open(path,'r')
    content=file.read()
    content_lines=content.splitlines()
    content_lines=content_lines[1:]
    date=[]
    close_price=[]
    for day in content_lines:
        split_day=day.split(',')
        date.append(split_day[0])
        close_price.append(float(split_day[4]))
    date.reverse()
    close_price.reverse()
    return date, close_price

def execute_indicators(indicator_type: 'Indicators', price_list:list, days:int)->list:
    return indicator_type.execute(price_list,days)

def _final_report(symbol:str, strategy:str, days:int, date_list:list,close_price:list,indicator:list,signal:list, buy=None, sell=None,)->None:
    print('Symbol: {}'.format(symbol))
    if strategy == 's':
        print('Strategy: {}-Day Simple Moving Average\n'.format(days))
    elif strategy == 'd':
        print('Strategy: {}-Day Directional Indicator, buy above {}, sell below {}\n'.format(days,buy,sell))
        for i in range(len(indicator)):
            if indicator[i]>0:
                indicator[i]='+{}'.format(indicator[i])
    print('{:<12}{:<12}{:<12}{:<12}'.format('DATE','CLOSE','INDICATOR','SIGNAL'))
    for i in range(len(date_list)):
        print('{:<12}{:<12}{:<12}{:<12}'.format(date_list[i],close_price[i],indicator[i],signal[i]))

if __name__ == '__main__':
    print("Welcome to the stock analysis program!")
    start()
