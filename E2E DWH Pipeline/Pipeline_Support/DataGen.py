import requests
from github import Github
import os
import pandas as pd
from io import StringIO

mockaroo_api_key='########' # Hidden due to confidentiality
github_token='########################################' # Hidden due to confidentiality

# Mackaroo API configuration
mockaroo_api_key=mockaroo_api_key
base_url='https://my.api.mockaroo.com'
schemas=['address', 'client', 'agent', 'owner', 'features', 'property', 'maintenance',
         'visit', 'commission', 'sale', 'contract', 'rent', 'admin']

# GitHub configuration
github_token=github_token
repo_name='End-to-End-DWH-Pipeline'
dataset_folder='Database/Datasets'

def get_data(schema):
    url=f'{base_url}/{schema}.csv?key={mockaroo_api_key}'
    response=requests.get(url)
    response.raise_for_status()
    return response.content

def append_csv(prev_content, new_content):
    prev_df=pd.read_csv(StringIO(prev_content))
    new_df=pd.read_csv(StringIO(new_content))
    combined_df=pd.concat([prev_df, new_df], ignore_index=True)
    return combined_df.to_csv(index=False)

def upload_to_github(file_content, file_name):
    g=Github(github_token)
    repo=g.get_user().get_repo(repo_name)
    file_path=f'{dataset_folder}/{file_name}'
    try:
        contents=repo.get_contents(file_path)
        prev_content=contents.decoded_content.decode('utf-8')
        appended_content=append_csv(prev_content, file_content)
        repo.update_file(contents.path, f'Update {file_name}', appended_content, contents.sha)
    except:
        repo.create_file(file_path, f'Create {file_name}', file_content)
        
def main():
    for schema in schemas:
        print(f'Fetching data for schema: {schema}')
        dataset=get_data(schema)
        file_name=f'{schema}.csv'
        print(f'Uploading {file_name} to GitHub')
        upload_to_github(dataset.decode('utf-8'), file_name)
    print('All datasets have been uploaded.')

if __name__ == '__main__':
    main()