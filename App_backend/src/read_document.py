import pandas as pd


def read_csv(url: str)->pd.DataFrame:
    """Read a document .csv and then transform to dataframe
    Args:
        url (str): _description_

    Returns:
        pd.DataFrame: _description_
    """
    dataframe_astro = pd.read_csv(url)
    print(dataframe_astro.Planet_Name)
    return dataframe_astro

