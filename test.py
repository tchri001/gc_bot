import pandas as pd

def get_values(row):
    buy_price = ''
    buy_qty = ''
    sell_price = ''
    sell_qty = ''

    if row['event_type'] == 'ADD':
        if row['side'] == 'BUY':
            buy_price = int(row['price'] or 0)
            buy_qty = int(row['quantity'] or 0)
        else:
            sell_price = int(row['price'] or 0)
            sell_qty = int(row['quantity'] or 0)
    
    return buy_price, buy_qty, sell_price, sell_qty

def add_row(row):
    bp, bq, sp, sq = get_values(row)
    dict[row['symbol']] = [row['date'], row['symbol'], row['timestamp'], row['sequence_number'], bp, bq, sp, sq]

def add_side(row):
    sy = row['symbol']
    bp, bq, sp, sq = get_values(row)
    if row['side'] == 'SELL' and int(dict[sy][6] or 0) == 0:
        dict[sy][6] = sp
        dict[sy][7] = sq
        return True
    elif row['side'] == 'BUY' and int(dict[sy][4] or 0) == 0:
        dict[sy][4] = bp
        dict[sy][5] = bq
        return True
    else:
        return False

def process_add(row):
    sy = row['symbol']
    row_price = int(row['price'])
    row_qty = int(row['quantity'])

    if not add_side(row):
        if row['side'] == 'SELL' and row_price < dict[sy][6]:
            dict[sy][6] = row_price
            dict[sy][7] = row_qty
        elif row['side'] == 'SELL' and row_price == dict[sy][6]:
            dict[sy][7] = dict[sy][7] + row_qty
        elif row['side'] == 'BUY' and row_price > dict[sy][4]:
            dict[sy][4] = row_price
            dict[sy][5] = row_qty
        elif row['side'] == 'BUY' and row_price == dict[sy][4]:
            dict[sy][5] = dict[sy][5] + row_qty

def process_delete(row):
    

#date, symbol, timestamp, sequence_number, highest_buy_price, buy_quantity, lowest_sell_price, sell_quantity
if __name__ == '__main__':
    in_head = ['date', 'symbol', 'sequence_number', 'timestamp', 'side', 'price', 'quantity', 'order_id', 'event_type']
    in_data = [
        ['2023-12-11','Z74_RY','1702246271258206460','2023-12-11 01:00:00.284762 UTC','SELL','2350','71200','7798175719082828454','ADD'],
        ['2023-12-11','Z74_RY','1702246271258206461','2023-12-11 01:00:00.291256 UTC','SELL','2630','50000','7798175719082828679','ADD'],
        ['2023-12-11','Z74_RY','1702246271258206462','2023-12-11 01:00:00.292518 UTC','SELL','2350','100','7798175719082828742','ADD'],
        ['2023-12-11','Z74_RY','1702246271258206463','2023-12-11 01:00:00.292832 UTC','SELL','2360','43600','7798175719082828759','ADD'],
        ['2023-12-11','Z74_RY','1702246271258206464','2023-12-11 01:00:00.292887 UTC','SELL','','','7798175719082828759','DELETE'],
        ['2023-12-11','Z74_RY','1702246271258206465','2023-12-11 01:00:00.293950 UTC','SELL','','','7798175719082828742','DELETE'],
        ['2023-12-11','Z74_RY','1702246271258206466','2023-12-11 01:00:00.294163 UTC','SELL','2350','8000','7798175719082828796','ADD'],
        ['2023-12-11','Z74_RY','1702246271258206467','2023-12-11 01:00:00.294369 UTC','BUY','2340','8000','7798175719082828808','ADD'],
        ['2023-12-11','Z74_RY','1702246271258206468','2023-12-11 01:00:00.294470 UTC','BUY','','','7798175719082828808','DELETE']]
    
    dfin = pd.DataFrame(columns=in_head, data=in_data)

    #['date','symbol','timestamp','sequence_number','highest_buy_price','buy_quantity','lowest_sell_price','sell_quantity']
    dict = {}

    for index, row in dfin.iterrows():
        sy = row['symbol']
        
        if not dict: #Add first row
            add_row(row)
        elif row['symbol'] not in dict: #Add rows for new symbols
            add_row(row)
        elif row['symbol'] in dict: #Add rows for existing symbols with new orders
            if row['event_type'] == 'ADD':
                process_add(row)
            elif row['event_type'] == 'DELETE':
                process_delete(row)
            # elif row['event_type'] == 'DELETE':
            #     process_delete(row)
    print(dict)