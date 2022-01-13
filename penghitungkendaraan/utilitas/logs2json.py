import csv
import json

with open('logs/klasifikasi/gabungan/logs_gabungan.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    line_count = 0
    objeks = {}
    objeks['kendaraan'] = []
    for row in csv_reader:
        # print(row)
        objeks['kendaraan'] .append({
            'frame':row[0],
            'time':row[1],
            'lajur':row[2],
            'klasifikasi':row[3],
            'jumlah':row[4],
            'filename':row[5],
        })
        # print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
        line_count += 1

    with open('logs_gabungan.json', 'w') as outfile:
        json.dump(objeks, outfile)    
    print(f'Processed {line_count} lines.')
