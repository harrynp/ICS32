"""SIMPLE MOVING AVERAGE"""
class Simple:
    def execute(self, price_list:list, days:int)->list:
        average_price = []
        interger_list = []
        for n in range(len(price_list)):
            interger_list.append(float(price_list[n]))
            if n < days - 1:
                average_price.append('N/A')
            else:
                total = sum(interger_list[n-(days-1):n+1]) / days
                total = float('{:.2f}'.format(total))
                average_price.append(total)
        return average_price


"""DIRECTIONAL INDICATOR"""
class Directional:
    def execute(self, price_list:list, days:int) -> list:
        direction=[0]
        indicator=[0]
        for i in range(1,len(price_list)):
            if price_list[i]>price_list[i-1]:
                direction.append(1)
            elif price_list[i]<price_list[i-1]:
                direction.append(-1)
            elif price_list[i]==price_list[i-1]:
                direction.append(0)
        for i in range(1,len(direction)):
            current=0
            if i < days:
                for d in range(i):
                    current += direction[i-d]
                indicator.append(current)
            else:
                for d in range(days):
                    current+=direction[i-d]
            indicator.append(current)
        return indicator
