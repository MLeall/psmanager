import csv
from pymongo import MongoClient

class App:
    def __init__(self, user, password, cluster_name):
        self.user = user
        self.password = password
        self.cluster_name = cluster_name

        if self.__check_connection():
            print(f'Connected to {cluster_name}.')
            uri = f"mongodb+srv://{self.user}:{self.password}@{self.cluster_name}.tniafyu.mongodb.net/?retryWrites=true&w=majority"
            self.client = MongoClient(uri)
        else:
            print(f'Failed to connect to {cluster_name}.')
    

    def __check_connection(self):
        """
        Check connection with MongoDB cluster.
        """
        try:
            uri = f"mongodb+srv://{self.user}:{self.password}@{self.cluster_name}.tniafyu.mongodb.net/?retryWrites=true&w=majority"
            client = MongoClient(uri)
            client.admin.command('ping')
            return True
        except Exception as e:
            print(e)
            return False


    def list_colletion(self):
        db = self.client['psmanager']
        collection = db['logins']
        
        collection_list = list()
        for item in collection.find():
            # Removing `_id` column created by mongoDB so it can be listed properly on the TreeView container
            l = list(zip(item.keys(), item.values()))
            d = {
                l[1][0]: l[1][1],
                l[2][0]: l[2][1],
                l[3][0]: l[3][1]
            }
            collection_list.append(d)

        sorted_collection = sorted(collection_list, key=lambda x: x['service'])
        return sorted_collection


    def create_login(self, service, login, password):
        db = self.client['psmanager']
        collection = db['logins']

        item = {
                'service': service,
                'login': login,
                'password': password
            }
        
        collection.insert_one(item)

    
    def update_login(self, search, update):
        db = self.client['psmanager']
        collection = db['logins']
        collection.find_one_and_update(search, update)


    def delete_login(self, search):
        db = self.client['psmanager']
        collection = db['logins']
        collection.find_one_and_delete(search)


    def csv_to_dict(self, file_path):
        result_dict = {}
        dict_list = []
        try:
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames        
                for row in reader:
                    # Adjust the headers index according to your actual csv headers.    
                    d = {
                        'service': row[headers[3]],
                        'login': row[headers[0]],
                        'password': row[headers[4]]
                    }
                    dict_list.append(d)
            
            for d in dict_list:
                self.create_login(service=d['service'], login=d['login'], password=d['password'])
            return True, len(dict_list)
        except Exception as e:
            return False, e
