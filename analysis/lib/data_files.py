import sys, os, csv

source_data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_source(file):
    return os.path.join(source_data_dir, 'data/source_data', file)
def get_temp(file):
    return os.path.join(source_data_dir, 'data/temp', file)

def save_temp_csv(array_csv_rows, file_name):
    data_file = open(get_temp(file_name), 'w', newline='')
    csv_writer = csv.writer(data_file)
    
    count = 0
    for data in array_csv_rows:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    
    data_file.close()

def save_temp_array(array_rows, file_name):
    with open(get_temp(file_name), "w") as txt_file:
        for row in array_rows:
            txt_file.write(row + "\n")