from hash_str import get_csci_salt, get_user_id, hash_str
import pandas as pd


def get_user_hash(username, salt=None):
    salt = salt or get_csci_salt()
    print(salt)
    return hash_str(username, salt=salt)


if __name__ == "__main__":

    for user in ["patch", "patchcasey"]:
        print("Id for {}: {}".format(user, get_user_id(user)))


    data_source = 'C:/aPost_Grad/Fall_Class/pset1branch/2019fa-pset-1-patchcasey/data/hashed.xlsx'
    df = pd.read_excel(data_source)
    df.to_parquet('hashed.parquet', engine='pyarrow')

    # TODO: read in, save as new parquet file, read back just id column, print
