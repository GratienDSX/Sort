import csv
import operator

def delete_incomplete(source, dest):
    with open(source, 'r') as csvfile:
        print("opened source file")
        reader = csv.reader(csvfile, delimiter=',')

        with open(dest, 'wb') as out_file:
            print("opened new file")
            writer = csv.writer(out_file, delimiter=',')
            i = 0
            j=0
            ratio = 0.0
            #number 1 and 2 and etp_seq
            # try to bucket outputs and use a softmax
            print("entre dans la boucle")
            for row in reader:
                i+=1
                incomplete = row[0] =="" or row[3] =="" or row[5] =="" or row[6] =="" or row[7] =="" or row[16] =="" or row[18] ==""
                if not incomplete:
                    j+=1
                    writer.writerow([row[0], row[3], row[5], row[6], row[7],row[16],row[18]])
                    #print [row[0], row[3], row[5], row[6], row[7],row[15],row[17]]
                if i%100000 ==0:
                    print i," lines seen"
                    print j, " correct lines"
                    ratio = float(j)/i*100
                    print ratio, "% percentage kept"
                if i==1:
                    print row
                    print [row[0], row[3], row[5], row[6], row[7],row[16],row[18]]
            print i," total lines seen"
            print j, " total kept lines"
            ratio = float(j)/i*100
            print ratio, "% total percentage kept"

def keep_start_finish(source,dest):
    with open(source, 'r') as csvfile:
        print("opened source file")
        reader = csv.reader(csvfile, delimiter=',')

        with open(dest, 'wb') as out_file:
            print("opened new file")
            writer = csv.writer(out_file, delimiter=',')
            i = 0
            j=0
            ratio = 0.0
            print("entre dans la boucle")
            for row in reader:
                if i==0:
                    writer.writerow(row)
                i+=1
                is_terminal = row[0] == "LeftOrigin" or row[0] =="ReachedDestination"
                if is_terminal:
                    j+=1
                    writer.writerow(row)
                if i%100000 ==0:
                    print i," lines seen"
                    print j, " correct lines"
                    ratio = float(j)/i*100
                    print ratio, "% percentage kept"
            print i," total lines seen"
            print j, " total kept lines"
            ratio = float(j)/i*100
            print ratio, "% total percentage kept"


# counts the couples
def count_couples(source,dest):
    with open(source, 'r') as csvfile:
        print("opened source file")
        reader = csv.reader(csvfile, delimiter=',')
        couples = dict()
        for row in reader:
            couple = row[5]+'_'+row[6]
            if couple in couples:
                couples[couple]+=1
            else:
                couples[couple]=1
    sorted_couples = sorted(couples.items(), key=operator.itemgetter(1))
    text=open(dest, 'w')
    text.write('\n'.join('%s %s' % x for x in sorted_couples))
    return sorted_couples






path = r"C:\VMShared\wagon\v2"+'\\'
source_file = path+'WAGON_STATUS_2.csv'
clean_file =path+'clean.csv'
fin_file = path+'fin.csv'
route_list= path+'list.txt'

delete_incomplete(source_file,clean_file)
keep_start_finish(clean_file,fin_file)
count_couples(fin_file,route_list)
