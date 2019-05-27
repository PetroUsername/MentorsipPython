import requests
import argparse
import os

parser = argparse.ArgumentParser(
    description='Script that checks all the contributors of a given GitHub project and downloads their avatars into a corresponding folder')
parser.add_argument('-u', '--user', required=True,
                    help='user to search for')
parser.add_argument('-p', '--project', required=True,
                    help='project to search for')

args = parser.parse_args()

response = requests.get(
    'https://api.github.com/repos/%s/%s/contributors' % (str(args.user), str(args.project))
)
dir_path = 'mentorship_task_04_requests_output/%s/%s' % (str(args.user), str(args.project))
os.makedirs(dir_path, mode=0o777, exist_ok=True)

json_response = response.json()
contributors_counter = 0
for contributor in json_response:
    r = requests.get(contributor['avatar_url'], stream=True)
    print('Saving', contributor[
        'login'], 'contributor avatar image')
    if r.headers['Content-Type'] == 'image/jpeg':
        f = '.jpg'
    elif r.headers['Content-Type'] == 'image/png':
        f = '.png'
    else:
        f = ''
    r = r.raw.read()
    file_path = 'mentorship_task_04_requests_output/%s/%s/%s%s' % (str(args.user), str(args.project), contributor['login'], f)
    with open(file_path, 'wb') as fd:
        fd.write(r)
    print('Image for', contributor[
        'login'], 'is saved')
    contributors_counter += 1

print('In total avatar images for', str(contributors_counter), 'contributors were saved from', args.project,
      'project of', args.user, 'user')
