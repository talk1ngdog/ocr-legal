import os

import pandas as pd
from whoosh.fields import Schema, TEXT
from whoosh.index import open_dir, create_in


def create_index(path_to_index):
    '''
    Create a whoosh index in the path specified with a simple Schema structure: {title: str, body: str}

    Parameters
    ----------
    path_to_index : str
        The location of the index
    '''

    schema = Schema(title=TEXT, content=TEXT)

    if not os.path.exists(path_to_index):
        os.mkdir(path_to_index)

    create_in(path_to_index, schema)


def add_documents_to_index(path_to_index, path_to_csv):
    '''
    Add documents, contained in a dataframe stored as a .csv with columns {'document_id': str, 'body': str},
    to the Whoosh index instance

    Parameters
    ----------
    path_to_index : str
        The location of the index
    path_to_csv : str
        THe locations of the dataframe
    '''

    df = pd.read_csv(path_to_csv)

    ix = open_dir(path_to_index)
    writer = ix.writer()

    for _, row in df.iterrows():
        writer.add_document(title=row['document_id'], content=row['body'])
    writer.commit()