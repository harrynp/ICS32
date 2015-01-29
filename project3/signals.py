class Average:
    def __init__(self, close_price:list, average_price:list)->list:
        self._close_price = close_price
        self._average_price = average_price
    def close_price(self):
        return self._close_price
    def average_price(self):
        return self._average_price
    def execute(self):
        signals=['']
        for i in range(1,len(self._close_price)):
            try:
                if self._close_price[i] > self._average_price[i] and self._close_price[i-1]<=self._average_price[i-1]:
                    signals.append('BUY')
                elif self._close_price[i] < self._average_price[i] and self._close_price[i-1]>=self._average_price[i-1]:
                    signals.append('SELL')
                else:
                    signals.append('')
            except:
                signals.append('')
        return signals

class Directional:
    def __init__(self, indicator_list:list)->list:
        self._indicator_list=indicator_list
    def indicator_list(self):
        return self._indicator_list
    def execute(self, buy, sell):
        signals=['']
        for i in range(1,len(self._indicator_list)):
            if self._indicator_list[i]>buy and self._indicator_list[i-1] <=buy:
                signals.append('BUY')
            elif self._indicator_list[i]<sell and self._indicator_list[i-1] >=sell:
                signals.append('SELL')
            else:
                signals.append('')
        return signals

