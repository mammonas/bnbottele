import requests
import datetime
import urllib.parse
from colorama import Fore, Style
GET_PRICE_ENDPOINT = 'https://binance.com/api/v3/ticker/24hr?symbol='
TELE_END_POINT = 'https://api.telegram.org/bot'
TELE_END_POINT_PARAMS = '/sendMessage?chat_id=-573320155&text='
LAST_BUY_PRICE_BNB = 244.9068
LAST_BUY_PRICE_BTC = 50800.00
highest_perc = None

class BNCall:

    def get_price(self, symbols):
        global highest_perc
        end_point = GET_PRICE_ENDPOINT + symbols
        r = requests.get(end_point)
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_sell_pr = LAST_BUY_PRICE_BNB if symbols == 'BNBUSDT' else LAST_BUY_PRICE_BTC
        price_current = float(r.json()['lastPrice'])
        dau = '-' if last_sell_pr > price_current else '+'
        diff = abs(last_sell_pr - price_current)
        percent_diff = (abs(diff) / last_sell_pr) * 100
        percent_diff_txt = '%s%.2f' % (dau, percent_diff)
        percent_diff_txt_return = percent_diff_txt

        if highest_perc is None:
            highest_perc = percent_diff
        elif percent_diff > highest_perc:
            highest_perc = percent_diff

        if highest_perc == percent_diff:
            color = Fore.GREEN if dau == '+' else Fore.RED
            percent_diff_txt = color + percent_diff_txt + Style.RESET_ALL
        
        # print('%s Price:%.4f Diff:%s%.4f Per:%s' %(time_str, price_current, dau, diff, percent_diff_txt))
        return '%s-%s\t%.4f\t%s%%' % (time_str, symbols, price_current, percent_diff_txt_return)

    def send_message_to_bot(self, token, msg):
        encoded_msg = urllib.parse.quote(msg)
        end_point = TELE_END_POINT + token + TELE_END_POINT_PARAMS + encoded_msg
        requests.post(end_point)
