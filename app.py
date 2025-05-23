import glob
import os
import json
import re
import pandas as pd

def get_column_names(schemas, ds_name, sorting_key = 'column_position'):
    column_details = schemas[ds_name]
    columns = sorted(column_details, key = lambda col:col[sorting_key])
    return [col['column_name'] for col in columns]

def read_csv(file,schemas):
    file_path_list = re.split('/',file)
    ds_name = file_path_list[-2]
    file_name = file_path_list[-1]
    columns = get_column_names(schemas, ds_name)
    df = pd.read_csv(file,names=columns)
    return df

def read_json(df,tgt_base_dir,ds_name,file_name):
    json_file_path = f'{tgt_base_dir}/{ds_name}/{file_name}'
    print(f'Writing {json_file_path}')
    os.makedirs(f'{tgt_base_dir}/{ds_name}', exist_ok=True)
    df.to_json(json_file_path,orient='records',lines=True)


def file_converter(src_base_dir,tgt_base_dir,ds_name):
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    files = glob.glob(f'{src_base_dir}/{ds_name}/part-*')
    for file in files:
        df = read_csv(file,schemas)
        file_name = re.split('/',file)[-1]
        read_json(df,tgt_base_dir,ds_name,file_name)

def process_files(ds_names=None):
    src_base_dir = 'data/retail_db'
    tgt_base_dir = 'data/retail_db_json'
    schemas = json.load(open(f'{src_base_dir}/schemas.json'))
    if not ds_names:
        ds_names = schemas.keys()
    for ds_name in ds_names:
        print(f'Processing {ds_name}')
        file_converter(src_base_dir,tgt_base_dir,ds_name)

if __name__ == '__main__':
    process_files()
