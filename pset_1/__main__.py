from hash_str import get_csci_salt, get_user_id, hash_str
from io_pset1 import atomic_write
import pandas as pd
import fastparquet
import os

def get_user_hash(username, salt=None):



    salt = salt or get_csci_salt()
    print(salt)
    return hash_str(username, salt=salt)


if __name__ == "__main__":
    filename = 'hashed'
    parquetfilename = filename+'.parquet'
    cwd = os.getcwd()
    data_wd = os.path.abspath(os.path.join(cwd, '..', 'data'))


    for user in ["gorlins", "patchcasey"]:
        print("Id for {}: {}".format(user, get_user_id(user)))


    data_source = os.path.join(data_wd,filename+'.xlsx')
    df = pd.read_excel(data_source)

    atomic_write(fastparquet.write(parquetfilename, df, compression=None))
    result = pd.read_parquet(parquetfilename, engine='fastparquet', columns=['hashed_id'])
    print(result)

    # print(df.dtypes)
    # parquetfile = df.to_parquet('hashed.parquet', engine='fastparquet', compression='GZIP', index=False)
    # print(type(parquetfile))
    # result = pd.read_parquet(parquetfile, engine='fastparquet', columns='hashed_id')


    # TODO: read in, save as new parquet file, read back just id column, print
