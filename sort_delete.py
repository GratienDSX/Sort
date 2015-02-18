# coding=utf-8

import csv
import operator
from datetime import datetime
import numpy as np

#imports a csv into a list of rows (each row is itself a list of the values on its line)
def csv_to_list(csv_file, delimiter=','):
    print 'reading from file'
    with open(csv_file, 'r') as csv_con:
        reader = csv.reader(csv_con, delimiter=delimiter)
        return list(reader)

def get_header(csv_cont,target):
    header = csv_cont[0]
    if isinstance(target, str):
        target_index= header.index(target)
    else:
        target_index=target
    return target_index


def output_route(route, source, path):
    with open(source, 'r') as csvfile:
        print("opened source file")
        reader = csv.reader(csvfile, delimiter=',')
        total_path = path+route+".csv"
        i=0
        with open(total_path, 'wb') as out_file:
            print("opened new file")
            writer = csv.writer(out_file, delimiter=',')
            for row in reader:
                couple=row[5]+'_'+row[6]
                if i==0:
                    writer.writerow(row)
                    i+=1
                if couple==route:
                    i+=1
                    if i%100==0:
                        print 'wrote ', i, " lines"
                    writer.writerow(row)
    print 'wrote ',i,' total lines'

def sort_by_column(csv_cont, col, reverse=False):
    print 'sorting'
    header=csv_cont[0]
    body = csv_cont[1:]
    col_index= get_header(csv_cont,col)
    body = sorted(body, 
            key=operator.itemgetter(col_index), 
            reverse=reverse)
    body.insert(0, header)
    return body


def subsort_by_col(csv_cont, new_col, prev_col, reverse =False):
    print 'subsorting'
    body = csv_cont[1:]
    new_col_index= get_header(csv_cont,new_col)
    prev_col_index = get_header(csv_cont,prev_col)
    start_index=1
    curr_index=1
    print curr_index
    print prev_col_index
    curr_value = csv_cont[curr_index][prev_col_index]
    size = len(csv_cont)
    while curr_index <size:
        while csv_cont[curr_index][prev_col_index] == curr_value:
            curr_index += 1
            if curr_index >= size:
                break
        csv_cont[start_index:curr_index]= sorted(csv_cont[start_index:curr_index], key= operator.itemgetter(new_col_index), reverse=reverse)
        start_index=curr_index
        if curr_index<size:
            curr_value = csv_cont[curr_index][prev_col_index]
    return csv_cont

#Sort a sublist (without headers) by date (used by subsort_by_date)
def minisort_by_date(csv_cont, col_index, reverse = False):
    body = csv_cont
    body = sorted(body, key = lambda row: datetime.strptime(row[col_index], "%Y-%m-%d %H:%M:%S"))
    return body

#takes in a table previously sorted by prev_col and sorts it by date while maintaining the previous order
def subsort_by_date(csv_cont, date_col, prev_col, reverse = False):
    print 'subsorting by date'
    body = csv_cont[1:]
    date_col_index=get_header(csv_cont,date_col)
    prev_col_index=get_header(csv_cont,prev_col)
    start_index=1
    curr_index=1
    curr_value = csv_cont[curr_index][prev_col_index]
    size = len(csv_cont)
    while curr_index <size:
        while csv_cont[curr_index][prev_col_index] == curr_value:
            curr_index += 1
            if curr_index >= size:
                break
        csv_cont[start_index:curr_index]= minisort_by_date(csv_cont[start_index:curr_index], date_col_index)
        start_index=curr_index
        if curr_index<size:
            curr_value = csv_cont[curr_index][prev_col_index]
    return csv_cont

def remove_unique_wags(csv_,wag_col):
    wag_col_index=get_header(csv_,wag_col)
    wagon=csv_[1][wag_col_index]
    lines=len(csv_)
    i=2
    while i<lines-2:
        if csv_[i][wag_col_index] != csv_[i+1][wag_col_index] and csv_[i][wag_col_index] !=csv_[i-1][wag_col_index]:
            csv_.remove(csv_[i])
            lines=len(csv_)
        else:
            i+=1
    #if i == lines-1:
        #csv_.remove(csv_[i])
    #print csv_
    return csv_

def remove_bad_pairs(csv_,wag_col,evt_col):
    wag_col_index=get_header(csv_,wag_col)
    evt_col_index=get_header(csv_,evt_col)
    start= 'LeftOrigin'
    finish='ReachedDestination'
    i=1
    lines=len(csv_)
    while i<lines-1:
        if not (csv_[i][evt_col_index]==start and csv_[i+1][evt_col_index]==finish):
            csv_.remove(csv_[i])
            csv_.remove(csv_[i])
            lines=len(csv_)
        else:
            i=i+2

    return csv_

def add_final_target(csv_cont, target,evt):
    print 'adding final target'
    target_index=get_header(csv_cont,target)
    evt_index=get_header(csv_cont,evt)
    i=1
    csv_cont[0].insert(0,'TARGET')
    size=len(csv_cont)
    start='LeftOrigin'
    while i <size-1:
        if csv_cont[i][evt_index]==start:
            diff =(datetime.strptime(csv_cont[i+1][target_index], "%Y-%m-%d %H:%M:%S")-datetime.strptime(csv_cont[i][target_index],"%Y-%m-%d %H:%M:%S"))
            diff_string = diff.total_seconds()
            csv_cont[i].insert(0,diff_string)
            csv_cont[i+1].insert(0,0)
            i=i+2;
    return csv_cont

def delete_end(csv_cont,evt):
    end='ReachedDestination'
    i=1
    size=len(csv_cont)
    evt_index=get_header(csv_cont,evt)
    while i<size:
        if csv_cont[i][evt_index]==end:
            csv_cont.remove(csv_cont[i])
            size=len(csv_cont)
        else:
            i+=1
    return csv_cont

def neuronalize_datetime(csv_):
    print 'neuronalizing datetime'
    header = csv_[0]
    index = header.index('EVENT_TIMESTAMP')

    for row in csv_[1:]:
        if not row:
            del row
        elif not isinstance(row[index], str):
            del row
        else:
            try:
                date = datetime.strptime(row[index], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
            else:
                # on crée active un neurone par jour de la semaine
                weekday_neurons = [0] * 7
                weekday_neurons[date.weekday()] = 1
                # on active un neurone par heure de la journée
                dailyhour_neurons = [0] * 24
                dailyhour_neurons[date.hour] = 1
                # on ajoute ces neurones à notre set d'apprentissage
                row.extend(weekday_neurons)
                row.extend(dailyhour_neurons)

    header.extend([0] * 7)
    header.extend([0] * 24)
    for hour in range(24):
        header[-24 + hour] = 'DAILY_HOUR_' + str(hour)
    for weekday in range(7):
        header[-24 - 7 + weekday] = 'WEEKDAY_' + str(weekday)
    return csv_

def neuronalize_wagon_status(csv_):
    print 'neuronalizing wagon status'
    # select column wagon_status
    header = csv_[0]
    index = header.index('WAGON_STATUS')
    # 1 if loaded, else 0
    for row in csv_[1:]:
        if not row:
            pass
        elif row[index] == 'loaded':
            row[index] = 1
        elif row[index] == 'empty':
            row[index] = 0
        else:
            row[index] = -1
    return csv_

def make_unique(csv_,target):
    target_index=get_header(csv_,target)
    i=1
    size=len(csv_)
    while i<size-1:
        if csv_[i][target_index] == csv_[i+1][target_index]:
            #print csv_[i][target_index]
            csv_.remove(csv_[i])
            size=len(csv_)
        else:
            i=i+1
    return csv_

def make_bucket(csv_, target,numBuckets):
    #Getting a list of targets
    target_index=get_header(csv_,target)
    targ = [row[target_index] for row in csv_]
    targ.remove('TARGET')
    targets = np.array(targ)

    #getting the limits to have equal buckets
    print 'min',np.min(targets)
    print 'max',np.max(targets)
    percentiles = [ np.percentile(targets,i*int(100/numBuckets)) for i in range(0,numBuckets+1)]
    percentiles[numBuckets]+=1
    print percentiles

    #Making our buckets
    bucket =[]
    buckets = []
    for i in range(0,numBuckets):
        bucket =[val for val in targets if val>= percentiles[i] and val<percentiles[i+1]]
        bucket.sort()
        buckets.append(bucket)
    print 'Buckets:',buckets
    csv_[0].insert(0,'TARGET_BUCKET')
    for row in csv_:
        for i in range(0,numBuckets):
            if row[target_index]>=percentiles[i] and row[target_index]<percentiles[i+1]:
                row.insert(0,i)
    return csv_


#writes out a list of list to a csv
def write_csv(dest, csv_cont):
    print 'writing out csv'
    with open(dest, 'wb') as out_file:
        writer = csv.writer(out_file, delimiter=',')
        for row in csv_cont:
            writer.writerow(row)

path = r"C:\VMShared\wagon\v2"+'\\'
route='ee858439706a04691c5c3b2fd2f6573b_39349a7c3ed00bda5647ff55406aa4d2'
route_path=path+route+'.csv'
route_sort_path= path+route+'sortedneurun_test.csv'
bucket_path = path+route+'bucket_test.csv'
fin_file = path+'fin.csv'

output_route(route,fin_file,path)
listing=csv_to_list(route_path)
listing = sort_by_column(listing,'CONSIGNMENT_NR_SC')
listing = subsort_by_col(listing,'WAGON_NR','CONSIGNMENT_NR_SC')
listing = subsort_by_date(listing,'EVENT_TIMESTAMP','WAGON_NR')
listing = remove_unique_wags(listing,'WAGON_NR')
write_csv(route_sort_path,listing)

listing = remove_bad_pairs(listing,'WAGON_NR','TYPE')
write_csv(route_sort_path,listing)

listing = add_final_target(listing,'EVENT_TIMESTAMP','TYPE')
listing = delete_end(listing,'TYPE')
listing =neuronalize_datetime(listing)
listing = neuronalize_wagon_status(listing)
listing = make_unique(listing, 'TARGET')
#write_csv(route_sort_path,listing)
listing = make_bucket(listing, 'TARGET',10)
write_csv(bucket_path,listing)