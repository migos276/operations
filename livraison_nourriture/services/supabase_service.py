
from supabase import create_client
import psycopg2
from django.conf import settings

import os
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(supabase_url=SUPABASE_URL,supabase_key= SUPABASE_KEY)
def sync_table(table_name, data, row_id=None):
    """
    Synchronise une ligne vers Supabase.
    Si row_id est fourni → update, sinon → insert/upsert.
    """
    if row_id:
        response = supabase.table(table_name).update(data).eq("id", str(row_id)).execute()
    else:
        response = supabase.table(table_name).upsert(data).execute()
    return response




def delete_from_supabase(table: str, match: dict):
    """
    Supprime une ligne de Supabase
    """
    response = supabase.table(table).delete().match(match).execute()
    return response