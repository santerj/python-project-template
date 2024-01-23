import os
import subprocess
import sys

def getOptions() -> dict[str, str]:
    values = {
        'projectName': '',
        'configFormat': '',
        'dotenv': '',
        'loguru': ''
    }

    while values['projectName'] == '':
        values['projectName'] = input('Project name: ')
        if ' ' in values['projectName']:
            print('Space not allowed in project name!')
            values['projectName'] = ''

    while values['configFormat'] not in ('toml', 'yaml', 'none',):
        values['configFormat'] = input('Config format (toml/yaml/none): ').lower()

    while values['dotenv'] not in ('y', 'n'):
        values['dotenv'] = input('Install python-dotenv? (y/n): ').lower()

    while values['loguru'] not in ('y', 'n'):
        values['loguru'] = input('Install loguru? (y/n): ' ).lower()

    return values

def writeRequirements(values: dict[str, str]) -> None:
    packages = []
    
    if values['dotenv'] == 'y':
        packages.append('python-dotenv')
    if values['loguru'] == 'y':
        packages.append('loguru')
    if values['configFormat'] == 'yaml':
        packages.append('pyyaml')

    with open('./requirements/requirements.in', 'w') as f:
       for item in packages:
           f.write(f'{ item }\n')
       f.close()

    return

def useShell(values: dict[str, str]) -> None:
    # remove unnecessary config files
    remove = ''
    match (values['configFormat']):
        case 'toml':
            remove = 'config.yaml'
        case 'yaml':
            remove = 'config.toml'
        case 'none':
            remove = 'config.*'

    with open('.env', 'a+') as f:
        f.write(f'PROJECT={ values["projectName"] }\n')
        f.close()

    # in lieu of a templating engine, use envsubst to render templates
    for fn in ('README.md', 'noxfile.py', 'tests/test_main.py'):
        subprocess.run(f'PROJECT={ values["projectName"] } envsubst < { fn } > { fn }.out && mv { fn }.out { fn }', shell=True)
    os.remove('.env')

    # use shell mode for wildcard features
    subprocess.run(f'rm package/config/{ remove }', shell=True)

    for cmd in (
        ['mv', 'package', values['projectName']],
        [f'{ sys.executable }', '-m', 'venv', 'dev-venv'],
        ['dev-venv/bin/pip', 'install', '--upgrade', 'pip', 'pip-tools'],
        ['dev-venv/bin/pip-compile', 'requirements/requirements.in', '--output-file', 'requirements/requirements.txt'],
        ['dev-venv/bin/pip-compile', 'requirements/dev-requirements.in', '--output-file', 'requirements/dev-requirements.txt'],
        ['dev-venv/bin/pip', 'install', '-r', 'requirements/dev-requirements.txt'],
        ['rm', '-rf', '.git'],
        ['git', 'init'],
        ['git', 'add', '-A'],
        ['git', 'commit', '-m', '"project created with python-project-template"'],
        ):
        subprocess.run(cmd)
    print(
    """
    Setup done!

    Activate venv with:

        source dev-venv/bin/activate

    Remember to also add a new git remote url.

        git remote add origin [repo-url]
    """
    )

def main():
    try:
        options = getOptions()
    except KeyboardInterrupt:
        exit(1)
    
    writeRequirements(options)
    useShell(options)

if __name__ == '__main__':
    main()
