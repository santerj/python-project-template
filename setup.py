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

    subprocess.run(['rm', f'package/config/{ remove }'])
    subprocess.run(['mv', 'package', values['projectName']])
    subprocess.run([f'PROJECT_NAME={ values["projectName"] }', 'envsubst', '<', 'README.md'])
    subprocess.run([f'{ sys.interpreter }', '-m', 'venv', 'dev-venv'])
    subprocess.run(['dev-venv/bin/pip', 'install', '--uprade', 'pip', 'pip-compile'])
    subprocess.run(['dev-env/bin/pip-compile', 'requirements/dev-requirements.in', '--output-file', \
                   'requirements/dev-requirements.txt'])

def main():
    try:
        options = getOptions()
    except KeyboardInterrupt:
        exit(1)
    
    writeRequirements(options)
    useShell(options)

if __name__ == '__main__':
    main()
