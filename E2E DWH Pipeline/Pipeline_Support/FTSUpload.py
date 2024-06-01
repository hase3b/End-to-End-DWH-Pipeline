from github import Github

github_token='########################################' # Hidden due to confidentiality

# GitHub configuration
github_token=github_token
repo_name='End-to-End-DWH-Pipeline'
facttable_folder='E2E DWH Pipeline/Fact Table Snapshot'

def upload_fact_table(file_content, file_name):
    g=Github(github_token)
    repo=g.get_user().get_repo(repo_name)
    file_path=f'{facttable_folder}/{file_name}'
    try:
        contents=repo.get_contents(file_path)
        repo.update_file(contents.path, f'Update {file_name}', file_content, contents.sha)
        print('Fact Table Snapshot Updated')
    except Exception as e:
        repo.create_file(file_path, f'Create {file_name}', file_content)
        print('Fact Table Snapshot Uploaded')