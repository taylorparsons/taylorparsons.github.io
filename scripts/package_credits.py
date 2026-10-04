"""Split the reviewed attribution snapshot into small, reviewable source files."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def package(data):
    folder = ROOT / 'data/credits'
    folder.mkdir(exist_ok=True)
    for pattern in ('packages-*.json', 'dependencies-*.json'):
        for old in folder.glob(pattern): old.unlink()
    overview = {'reviewed': data['reviewed'], 'repositories': []}
    dependencies = []
    for repo in data['repositories']:
        overview['repositories'].append({k: v for k, v in repo.items() if k != 'dependencies'})
        dependencies.extend({'repository': repo['name'], 'dependency': d} for d in repo['dependencies'])
    def write(name, value):
        (folder / name).write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('\u2014', ',') + '\n')
    write('overview.json', overview)
    packages = sorted(data['packages'].items())
    for index in range(0, len(packages), 100):
        write(f'packages-{index // 100:03}.json', dict(packages[index:index + 100]))
    for index in range(0, len(dependencies), 150):
        write(f'dependencies-{index // 150:03}.json', dependencies[index:index + 150])
    print(f'Packaged {len(packages)} upstream records and {len(dependencies)} project dependency credits.')

if __name__ == '__main__':
    package(json.loads((ROOT / 'data/credits.json').read_text()))
