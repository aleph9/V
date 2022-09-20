import pyupbit
import time

access = "2T1KcUmPKdY6rx46YxTi5hLrlsZAfIaxBpYxIsrh"          
secret = "jxxNxxmkeIvXczCxybwUgInv3xlR7jenAaK20TJO"    

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

"""목표가 조회""" #3분봉 50개 중 최고가에서 -1.3%의 가격
def tar_price(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute3", count=50)
    tar = max(df['high']) - (max(df['high']) * 0.013)
    return(tar)
# print("목표가 : ", tar_price("KRW-ETH"))

"""현재가 조회"""
def cur_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]
# print("현재가 : ", cur_price("KRW-ETH"))

"""잔고 조회"""
def get_balance(ticker): #KRW = 원화 / ETH = 잔고 
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0
# print("원화잔고 : ", get_balance("KRW"))

"""평균매수가 조회"""
def abp(ticker):
    return upbit.get_avg_buy_price(ticker)
    #abp("KRW-ETH")
# print("평균매수가 : ",abp("KRW-ETH"))


"""자동매매 시작"""
while True:
    try:
        tar = tar_price("KRW-ETH")#매수 목표가 설정 (3분봉 50개 중 '최고가 * -1.3%원' )
        cur = cur_price("KRW-ETH")#현재가 

        if cur <= tar:                                            #현재가가 목표가 보다 작거나 같다면
            krw = get_balance("KRW")
            if krw > 6000:                                        #잔고가 6000원 이상 확인 후 
                upbit.buy_market_order("KRW-ETH", krw*0.9995)     #시장가로 매수 
        elif cur > (abp("KRW-ETH")*0.007)+abp("KRW-ETH"):         #현재가가 매수평균가의 0.7% 수익 중이면 
                    eth = get_balance("ETH")                      
                    if eth > 0.001:                               #이더리움 잔고 조회 후 
                        upbit.sell_market_order("KRW-ETH", eth*1) #시장가로 전량 매도
        elif cur < (abp("KRW-ETH")*-0.003)+abp("KRW-ETH"):        #현재가가 매수평균가의 -0.3% 손해 중이면 
                    eth = get_balance("ETH")                       
                    if eth > 0.001:                               #이더리움 잔고 조회 후 
                        upbit.sell_market_order("KRW-ETH", eth*1) #시장가로 전량 매도 후 
                        time.sleep(1200)                          #20분 거래 정지 
        else:
            time.sleep(0.3)

    except Exception as e:
        print(e)
        time.sleep(1)