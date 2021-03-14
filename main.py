import sys
from timeloop import Timeloop
from datetime import timedelta

from network.bn_call import BNCall

tl = Timeloop()
bn_call = BNCall()

if __name__ == "__main__":
    syms = sys.argv[1]
    syms2 = sys.argv[2]
    token = sys.argv[3]

    @tl.job(interval=timedelta(seconds=3600))
    def execute_cron_job():
        bn_call.get_price(symbols=syms, token=token)
        # bn_call.get_price(symbols=syms2, token=token)
        # print(msg)
        # bn_call.send_message_to_bot(token=token, msg=msg)
        # bn_call.send_message_to_bot(token=token, msg=msg2)

    tl.start(block=True)
