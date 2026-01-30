from decouple import config
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.id import ID

class AppwriteConfig:
    PROJECT_ID = config('APPWRITE_PROJECT_ID', default='')
    API_KEY = config('APPWRITE_API_KEY', default='')
    ENDPOINT = config('APPWRITE_ENDPOINT', default='https://cloud.appwrite.io/v1')
    DATABASE_ID = config('APPWRITE_DATABASE_ID', default='enise_db')

    @classmethod
    def get_client(cls):
        client = Client()
        client.set_endpoint(cls.ENDPOINT)
        client.set_project(cls.PROJECT_ID)
        if cls.API_KEY:
            client.set_key(cls.API_KEY)
        return client

    @classmethod
    def get_database(cls):
        client = cls.get_client()
        return Databases(client)

appwrite_db = AppwriteConfig