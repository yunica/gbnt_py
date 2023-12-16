from tqdm import tqdm
import pandas as pd
import requests
import logging
from glob import glob
from database_utils import dataframe_to_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_EXTERNAL_URLS = {
    "departments.csv": {
        "link": "https://gist.githubusercontent.com/yunica/1ae5f0482cadad4e45a861c0c90db347/raw/9342aa987fe93bab6862a261cee53b5039ee52b8/departments.csv",
        "columns": ["id", "department"],
    },
    "jobs.csv": {
        "link": "https://gist.github.com/yunica/1ae5f0482cadad4e45a861c0c90db347/raw/9342aa987fe93bab6862a261cee53b5039ee52b8/jobs.csv",
        "columns": ["id", "jobs"],
    },
    "hired_employees.csv": {
        "columns": ["id", "name", "datetime", "department_id", "job_id"],
        "int_columns": ["department_id", "job_id"],
    },
}


def download_data(url, folder_path, file_name):
    if not url:
        return
    block_size = 1024
    response = requests.get(url, stream=True)
    if response.status_code != 200:
        logger.error(f"no data for {file_name}")
        return

    total_size_in_bytes = int(response.headers.get("content-length", 0))

    with open(f"{folder_path}/{file_name}", "wb") as file, tqdm(
        desc=f"{folder_path}/{file_name}",
        total=total_size_in_bytes,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)


def save_database(table_name_path, engine):
    table_name = table_name_path.split("/")[-1]
    metadata = DATA_EXTERNAL_URLS.get(table_name)
    if not metadata:
        logger.error(f"no metadata for {table_name}")
        return
    df = pd.read_csv(table_name_path, header=None, names=metadata.get("columns"))
    # spetial case (int null float )
    for int_colum in metadata.get("int_columns", []):
        df[int_colum] = df[int_colum].astype("Int64")

    # df.to_csv(table_name_path, index=False)
    dataframe_to_db(df, table_name.split(".")[0], engine)


def process(
    folder_path,
    database_db,
    database_user,
    database_password,
    database_port,
    database_host,
):
    # dowload data
    [
        download_data(value.get("link"), folder_path, filename)
        for filename, value in DATA_EXTERNAL_URLS.items()
    ]
    # migrate to database
    files = list(glob(f"{folder_path}/*.csv"))
    # create engine
    database_url = f"postgresql://{database_user}:{database_password}@{database_host}:{database_port}/{database_db}"
    # complete metadata
    for file in tqdm(files, desc="save in database"):
        save_database(file, database_url)
