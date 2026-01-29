import { Client, Databases, Query } from 'appwrite';

const client = new Client()
  .setEndpoint(import.meta.env.VITE_APPWRITE_ENDPOINT)
  .setProject(import.meta.env.VITE_APPWRITE_PROJECT_ID);

const databases = new Databases(client);

export { client, databases, Query };

export const CONFIG = {
  databaseId: import.meta.env.VITE_APPWRITE_DATABASE_ID,
  modulesCollectionId: import.meta.env.VITE_APPWRITE_MODULES_COLLECTION_ID,
  sectionsCollectionId: import.meta.env.VITE_APPWRITE_SECTIONS_COLLECTION_ID,
  resourcesCollectionId: import.meta.env.VITE_APPWRITE_RESOURCES_COLLECTION_ID,
};