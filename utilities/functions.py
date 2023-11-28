# contains universal functions used across whole project

# library imports
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
import pandas as pd
import re
import unicodedata
import random


class HashContext:
    # clas related to creating and verifying password hashes
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"])

    def create(self, pwd_plain: str) -> str:
        return self.context.hash(pwd_plain)

    def verify(self, pwd_plain, pwd_hashed) -> bool:
        return self.context.verify(pwd_plain, pwd_hashed)


def compose_url(ip: str, port: str,) -> str:
    # compose valid url

    if not ip.startswith("http"):
        return str("http://" + ip + ":" + port)
    else:
        return str(ip + ":" + port)


def validate_db_type(db_type: str):
    # validate database type provided

    if db_type not in ['redis', 'mdb', 'psql', 'sqlite']:
        raise HTTPException(
            status_code=400,
            detail="Wrong db_type, possible database types: REDIS, MDB, PSQL, SQLi"
        )


def create_correlation_id(tb_const: str, te_const: str, nb_const):
    # create unique identifier of the request
    # tb - title_basics
    # te - title_episode
    # nb - name_basics
    # ts - timestamp start
    # tf timestamp finish

    return "tb:{tb_const}te:{te_const}nb:{nb_const}ts:{timestamp}tf:{randint}".format(
        tb_const=tb_const, te_const=te_const, nb_const=nb_const,
        timestamp=str(int(datetime.utcnow().timestamp())), randint=random.randint(1000, 9999))


def process_and_save_data(input_path: str, output_path: str, table_name: str, db_type: str = None):
    # prepare datasets for the selected database type
    # params:
    # @input_path- [REQUIRED] path to data source
    # @output_path- [REQUIRED] path to data output file
    # @table_name- [REQUIRED] name of the table that data will be processed for
    # @db_type- [OPTIONAL] database destination type, if not provided, basic preprocessing will be made

    # load data
    print("Loading data")
    if db_type == "redis":
        data = (
            pd.read_csv(input_path, sep='\t', na_values=["\\N"])
            .replace("'", "%27", regex=True).replace('"', "%22", regex=True)
            .fillna(-1)
        )
    else:
        data = (
            pd.read_csv(input_path, sep='\t', na_values=["\\N"])
            .replace("'", "%27", regex=True)
            .fillna(-1)
        )
    print("Data loaded")

    print("Converting invalid fields")
    # Convert float columns to integers
    float_columns = data.select_dtypes(include=['float']).columns
    data[float_columns] = data[float_columns].astype(int)

    # change null values with '-1'
    if table_name == "tb":
        data['runtimeMinutes'] = data['runtimeMinutes'].apply(lambda x: -1 if re.match(r'.*[a-zA-Z].*',
                                                                                       str(x)) else int(x))
        data['isAdult'] = data['isAdult'].apply(lambda x: int(x) if re.match(r'^(0|1)$',
                                                                             str(x)) else int(0))
    print("Converting finished")

    # preprocess fields accordingly to the database type
    if db_type == "psql":
        print("Postgres adjustments")
        if table_name == "tb":
            data['genres'] = data['genres'].apply(lambda x: "{"+str(x)+"}")
        elif table_name == "nb":
            data['primaryProfession'] = data['primaryProfession'].apply(lambda x: "{"+str(x)+"}" if re.match(
                r'^[a-zA-Z\[\],]+$',str(x)) else "{}")
            data['knownForTitles'] = data['knownForTitles'].apply(lambda x: "{"+str(x)+"}" if re.match(
                r"^[tnm][tnm]", str(x)) else "{}")

    elif db_type == "mdb":
        print("Mongo adjustments")
        if table_name == "tb":
            data['genres'] = data['genres'].apply(lambda x: x.split(",") if re.match(
                r'^[a-zA-Z\[\],]+$', str(x)) else [])
        elif table_name == "nb":
            data['primaryProfession'] = data['primaryProfession'].apply(lambda x: x.split(",") if re.match(
                r'^[a-zA-Z\[\],]+$',str(x)) else [])
            data['knownForTitles'] = data['knownForTitles'].apply(lambda x: x.split(",") if re.match(
                r"^[tnm][tnm]", str(x)) else [])

    elif db_type == "sqlite":
        # uses the same datasets as postgres
        pass

    elif db_type == "redis":
        print("Redis adjustments")
        if table_name == 'tb':
            # encode in ascii no in utf
            data["primaryTitle"] = data["primaryTitle"].apply(lambda val: unicodedata.normalize(
                'NFKD', str(val)).encode('ascii', 'ignore').decode())
            data["originalTitle"] = data["originalTitle"].apply(lambda val: unicodedata.normalize(
                'NFKD', str(val)).encode('ascii', 'ignore').decode())
            # rename column
            data.rename(columns={"tconst": "tid", "titleType": "tT", "primaryTitle": "pT", "originalTitle": "oT",
                                 "startYear": "sY", "endYear": "eY", "genres": "ge", "isAdult": "iA",
                                 "runtimeMinutes": "rT"}, inplace=True)
        elif table_name == 'nb':
            # encode in ascii no in utf
            data["primaryName"] = data["primaryName"].apply(lambda val: unicodedata.normalize(
                'NFKD', str(val)).encode('ascii', 'ignore').decode())
            # rename column
            data.rename(columns={"nconst": "nid", "primaryName": "pN", "birthYear": "bY", "deathYear": "dY",
                                 "primaryProfession": "pPr", "knownForTitles": "kFT"}, inplace=True)

        elif table_name == 'te':
            # rename column
            data.rename(columns={"tconst": "tid", "parentTconst": "paT", "seasonNumber": "sN",
                                 "episodeNumber": "eN"}, inplace=True)

    print("Saving output file")
    # save output file
    if db_type is None:
        data.to_csv(output_path.format(db_type="", file_ext="tsv"), sep='\t', index=False)
    else:
        if db_type == 'mdb':
            data.to_json(output_path.format(db_type=db_type, file_ext="json"), orient='records', lines=True)
        elif db_type == 'redis':
            data.to_csv(output_path.format(db_type=db_type, file_ext="csv"), sep=',', index=False)
        else:
            data.to_csv(output_path.format(db_type=db_type, file_ext="tsv"), sep='\t', index=False)

    return "Data preparation finished"
