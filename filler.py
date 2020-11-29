import requests
import json


if __name__=="__main__":
    with open('scientific_job.json') as json_file:
        data = json.load(json_file)
        for object in data['RECORDS']:
            print(object)
            try:
                response = requests.post(
                    'http://0.0.0.0:7777/api/v1/descriptors_encoding/encode/science_job',
                    json={
                        'user_id': object['author_id'],
                        'title': object['name']
                    },
                )
                print(response.status_code)
            except Exception as e:
                print(f"{object} end with error")
