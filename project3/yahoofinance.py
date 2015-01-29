import urllib.request, urllib.error

def _download_url(url:str)->(list,list):
    response=None
    try:
        response=urllib.request.urlopen(url)
        date, close_price=_url_contents(response)
        return date, close_price
    except urllib.error.HTTPError as e:
        print('Failed to download contents of URL')
        print('Status code: {}'.format(e.code))
        print()
        return
    finally:
        if response!=None:
            response.close()

def _url_contents(response:str)->(list,list):
    content_bytes=response.read()
    content_string=content_bytes.decode(encoding='utf-8')
    content_lines = content_string.splitlines()
    content_lines = content_lines[1:]
    date=[]
    close_price=[]
    for day in content_lines:
        split_day=day.split(',')
        date.append(split_day[0])
        close_price.append(float(split_day[4]))
    date.reverse()
    close_price.reverse()
    print('Data successfully retrieved.')
    return date, close_price

