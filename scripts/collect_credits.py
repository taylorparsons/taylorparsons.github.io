"""Collect public dependency attribution without installing or executing upstream code.

Usage: python3 scripts/collect_credits.py --inventory data/credits-sources.json
Registry metadata is attribution evidence, not a claim of legal ownership.
"""
from __future__ import annotations
import argparse, ast, concurrent.futures, email.utils, json, re, time, tomllib
import urllib.request, urllib.error, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'credits-cache'
HEADERS = {'User-Agent': 'TaylorParsons-OpenSource-Credits/1.0 (public attribution review)'}
OFFLINE = False

def get(url, as_json=False):
    key = __import__('hashlib').sha256(url.encode()).hexdigest()
    path = CACHE / key
    CACHE.mkdir(exist_ok=True)
    if path.exists():
        text = path.read_text()
    else:
        if OFFLINE:
            raise FileNotFoundError('No cached public metadata for this source')
        for attempt in range(3):
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=25) as response:
                    text = response.read().decode('utf-8')
                path.write_text(text)
                break
            except urllib.error.HTTPError as exc:
                if exc.code not in (429, 500, 502, 503) or attempt == 2:
                    raise
                time.sleep(1 + attempt)
            except (TimeoutError, urllib.error.URLError):
                if attempt == 2: raise
    return json.loads(text) if as_json else text

def clean_name(value):
    if isinstance(value, dict): value = value.get('name') or value.get('username') or ''
    if not isinstance(value, str): return ''
    value = re.sub(r'<[^>]*>', '', value).strip()
    if '@' in value and ' ' not in value: return ''
    return value.replace('\u2014', ',')

def source_url(value):
    if isinstance(value, dict): value = value.get('url') or ''
    if not isinstance(value, str): return ''
    value = re.sub(r'^git\+', '', value)
    value = value.replace('git://', 'https://').replace('git@github.com:', 'https://github.com/')
    if value.startswith('github:'): value = 'https://github.com/' + value[7:]
    return re.sub(r'\.git(?:#.*)?$', '', value).split('#')[0] if value.startswith(('http://', 'https://')) else ''

def attribution(eco, name):
    out = {'ecosystem': eco, 'name': name}
    try:
        if eco == 'npm':
            d = get('https://registry.npmjs.org/' + urllib.parse.quote(name, safe='') + '/latest', True)
            source = source_url(d.get('repository')) or source_url(d.get('homepage'))
            owners = [clean_name(d.get('author'))] + [clean_name(x) for x in d.get('maintainers', [])]
            license_id = d.get('license') or 'See upstream license'
            if isinstance(license_id, dict): license_id = license_id.get('type', 'See upstream license')
            registry = 'https://www.npmjs.com/package/' + name
            version = d.get('version', '')
        elif eco == 'pypi':
            d = get('https://pypi.org/pypi/' + urllib.parse.quote(name, safe='') + '/json', True)['info']
            urls = d.get('project_urls') or {}
            candidates = [(k, v) for k, v in urls.items() if any(t in k.lower() for t in ('source', 'repository', 'github', 'code'))]
            source = source_url(candidates[0][1]) if candidates else ''
            if not source: source = next((source_url(v) for v in urls.values() if 'github.com/' in v), '') or source_url(d.get('home_page'))
            owners = [clean_name(d.get('author')), clean_name(d.get('maintainer'))]
            for field in ('author_email', 'maintainer_email'):
                owners.extend(clean_name(n) for n, _ in email.utils.getaddresses([d.get(field) or '']))
            license_id = d.get('license_expression') or ''
            if not license_id:
                license_id = '; '.join(x.split(' :: ')[-1] for x in d.get('classifiers', []) if x.startswith('License ::') and 'OSI Approved ::' in x)
            if not license_id:
                raw = d.get('license') or ''
                license_id = raw if len(raw) < 140 else 'See upstream license'
            registry = 'https://pypi.org/project/' + name + '/'
            version = d.get('version', '')
        elif eco == 'cargo':
            d = get('https://crates.io/api/v1/crates/' + name, True)
            crate = d['crate']
            source = source_url(crate.get('repository')) or source_url(crate.get('homepage'))
            owners_data = get('https://crates.io/api/v1/crates/' + name + '/owners', True)
            owners = [clean_name(x.get('name')) or clean_name(x.get('login')) for x in owners_data.get('users', [])]
            version = crate.get('max_stable_version') or crate.get('max_version') or ''
            entry = next((x for x in d.get('versions', []) if x.get('num') == version), {})
            license_id = entry.get('license') or 'See upstream license'
            registry = 'https://crates.io/crates/' + name
        else:
            group, artifact = name.split(':', 1)
            query = urllib.parse.urlencode({'q': f'g:"{group}" AND a:"{artifact}"', 'rows': 1, 'wt': 'json'})
            search = get('https://search.maven.org/solrsearch/select?' + query, True)
            version = search['response']['docs'][0]['latestVersion']
            pom_url = 'https://repo.maven.apache.org/maven2/' + group.replace('.', '/') + '/' + artifact + '/' + version + '/' + artifact + '-' + version + '.pom'
            root = ET.fromstring(get(pom_url)); ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
            source = root.findtext('m:scm/m:url', namespaces=ns) or root.findtext('m:url', namespaces=ns) or ''
            source = source_url(source)
            owners = [root.findtext('m:organization/m:name', namespaces=ns)] + [x.text for x in root.findall('m:developers/m:developer/m:name', ns)]
            license_id = '; '.join(x.text for x in root.findall('m:licenses/m:license/m:name', ns)) or 'See upstream license'
            registry = 'https://central.sonatype.com/artifact/' + name.replace(':', '/')
        owners = sorted({x for x in owners if x})
        if not owners and 'github.com/' in source:
            owners = [source.split('github.com/')[1].split('/')[0] + ' contributors']
        out.update(source=source or registry, maintainers=owners, license=license_id or 'See upstream license', registry=registry, metadata_version=version)
    except Exception as exc:
        registry = {'npm': 'https://www.npmjs.com/package/', 'pypi': 'https://pypi.org/project/', 'cargo': 'https://crates.io/crates/', 'maven': 'https://central.sonatype.com/artifact/'}[eco] + (name.replace(':', '/') if eco == 'maven' else name)
        out.update(source=registry, maintainers=[], license='See upstream license', registry=registry, metadata_version='', error=type(exc).__name__)
    return out

def dependency_paths(paths):
    result = []
    for item in paths:
        p = item['path'] if isinstance(item, dict) else item
        base = p.rsplit('/', 1)[-1]
        if base in {'package.json', 'package-lock.json', 'Cargo.toml', 'Cargo.lock', 'pyproject.toml', 'uv.lock', 'poetry.lock', 'pom.xml', 'Package.swift', 'Package.resolved', 'setup.py', 'setup.cfg', 'pnpm-lock.yaml', 'yarn.lock'} or re.fullmatch(r'requirements[^/]*\.txt', base):
            if not re.search(r'/(fixtures|fixture)/', p): result.append(p)
    return result

def parse_source(repo, path, text):
    entries = []
    def add(eco, name, version='', scope='declared'):
        if not name or name.startswith(('./', '../')): return
        if eco == 'pypi': name = re.sub(r'[-_.]+', '-', name).lower()
        entries.append({'ecosystem': eco, 'name': name, 'version': str(version), 'scope': scope, 'evidence': path})
    def python_requirement(value, scope='declared'):
        match = re.match(r'([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^]]*\])?\s*(.*)', value.strip())
        if match: add('pypi', match[1], match[2].split(';')[0].strip(), scope)
    base = path.rsplit('/', 1)[-1]
    if base == 'package.json':
        d = json.loads(text)
        for section in ('dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies'):
            for name, version in d.get(section, {}).items():
                if str(version).startswith(('workspace:', 'file:', 'link:')): continue
                if str(version).startswith('npm:'):
                    alias = version[4:]; match = re.match(r'(@[^/]+/[^@]+|[^@]+)(?:@(.*))?$', alias)
                    if match: name, version = match[1], match[2] or ''
                add('npm', name, version, 'development' if section == 'devDependencies' else 'declared')
    elif base == 'package-lock.json':
        d = json.loads(text)
        for key, value in d.get('packages', {}).items():
            if 'node_modules/' in key and not value.get('link'):
                name = value.get('name') or key.rsplit('node_modules/', 1)[-1]
                add('npm', name, value.get('version', ''), 'locked')
        def walk(values):
            for name, value in values.items():
                add('npm', name, value.get('version', ''), 'locked')
                walk(value.get('dependencies', {}))
        if not d.get('packages'): walk(d.get('dependencies', {}))
    elif base in ('Cargo.toml', 'Cargo.lock', 'pyproject.toml', 'uv.lock', 'poetry.lock'):
        d = tomllib.loads(text)
        if base == 'Cargo.lock':
            for x in d.get('package', []):
                if str(x.get('source', '')).startswith('registry+'): add('cargo', x['name'], x.get('version', ''), 'locked')
                elif x.get('source'): add('cargo', x['name'], x.get('source'), 'git dependency')
        elif base == 'Cargo.toml':
            def walk(obj):
                for key, value in obj.items():
                    if key in ('dependencies', 'dev-dependencies', 'build-dependencies') and isinstance(value, dict):
                        for name, spec in value.items():
                            if isinstance(spec, dict) and ('path' in spec or spec.get('workspace')): continue
                            add('cargo', spec.get('package', name) if isinstance(spec, dict) else name, spec.get('version', spec.get('git', '')) if isinstance(spec, dict) else spec, 'development' if key != 'dependencies' else 'declared')
                    elif isinstance(value, dict): walk(value)
            walk(d)
        elif base in ('uv.lock', 'poetry.lock'):
            for x in d.get('package', []):
                source = x.get('source') or {}
                if base == 'uv.lock' and ('editable' in source or 'virtual' in source): continue
                add('pypi', x['name'], x.get('version', ''), 'locked')
        else:
            project = d.get('project', {})
            for x in project.get('dependencies', []): python_requirement(x)
            for group in project.get('optional-dependencies', {}).values():
                for x in group: python_requirement(x, 'optional')
            for x in d.get('build-system', {}).get('requires', []): python_requirement(x, 'development')
            for group in d.get('dependency-groups', {}).values():
                for x in group:
                    if isinstance(x, str): python_requirement(x, 'development')
            poetry = d.get('tool', {}).get('poetry', {})
            def poetry_deps(group, scope='declared'):
                for name, spec in group.items():
                    if name == 'python' or isinstance(spec, dict) and ('path' in spec): continue
                    add('pypi', name, spec.get('version', '') if isinstance(spec, dict) else spec, scope)
            poetry_deps(poetry.get('dependencies', {}))
            poetry_deps(poetry.get('dev-dependencies', {}), 'development')
            for group in poetry.get('group', {}).values(): poetry_deps(group.get('dependencies', {}), 'development')
    elif re.fullmatch(r'requirements[^/]*\.txt', base):
        for line in text.splitlines():
            if not line.strip() or line.lstrip().startswith(('#', '-')): continue
            python_requirement(line.split(' #')[0])
    elif base == 'setup.py':
        for node in ast.walk(ast.parse(text)):
            if isinstance(node, ast.keyword) and node.arg in ('install_requires', 'setup_requires', 'tests_require') and isinstance(node.value, (ast.List, ast.Tuple)):
                for x in node.value.elts:
                    if isinstance(x, ast.Constant) and isinstance(x.value, str): python_requirement(x.value)
    elif base == 'pom.xml':
        root = ET.fromstring(text); ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
        for dep in root.findall('.//m:dependency', ns):
            group = dep.findtext('m:groupId', namespaces=ns) or ''; artifact = dep.findtext('m:artifactId', namespaces=ns) or ''
            if '${' not in group + artifact: add('maven', group + ':' + artifact, dep.findtext('m:version', namespaces=ns) or '')
    elif base == 'pnpm-lock.yaml':
        for match in re.finditer(r'^  [\'\"]?(@[^/]+/[^@\s]+|[^@/\s\'\"]+)@(\d[^:\s\'\"]*)[\'\"]?:', text, re.M):
            add('npm', match[1], match[2].split('(')[0], 'locked')
    elif base == 'Package.swift':
        for url in re.findall(r'\.package\([^)]*url:\s*"([^"]+)"', text):
            add('source', url.rstrip('/').rsplit('/', 1)[-1].removesuffix('.git'), url)
    return entries

def main():
    global OFFLINE
    parser = argparse.ArgumentParser(); parser.add_argument('--inventory', default='data/credits-sources.json'); parser.add_argument('--output', default='data/credits.json'); parser.add_argument('--offline', action='store_true')
    args = parser.parse_args(); inventory = json.loads((ROOT / args.inventory).read_text())
    OFFLINE = args.offline
    repositories = inventory['repositories']; tasks = []
    for repo in repositories:
        for path in dependency_paths(repo.get('paths', [])):
            tasks.append((repo, path))
    evidence_errors = []; dependency_map = {r['name']: [] for r in repositories}
    def fetch(item):
        repo, path = item
        url = 'https://raw.githubusercontent.com/' + repo['repo'] + '/' + repo['sha'] + '/' + path
        try: return repo['name'], parse_source(repo, path, get(url)), None
        except Exception as exc: return repo['name'], [], {'path': path, 'error': str(exc)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        for name, entries, error in pool.map(fetch, tasks):
            dependency_map[name].extend(entries)
            if error: evidence_errors.append({'repository': name, **error})
    for repo in repositories:
        dependency_map[repo['name']].extend(repo.get('additional_dependencies', []))
    keys = sorted({(x['ecosystem'], x['name']) for deps in dependency_map.values() for x in deps if x['ecosystem'] != 'source'})
    print(f'Parsed {len(tasks)} manifests and lockfiles; resolving {len(keys)} unique dependencies.', flush=True)
    metadata = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as pool:
        for i, record in enumerate(pool.map(lambda key: attribution(*key), keys), 1):
            metadata[record['ecosystem'] + ':' + record['name']] = record
            if i % 100 == 0: print(f'Resolved {i}/{len(keys)} dependencies.', flush=True)
    records = []
    for repo in repositories:
        grouped = {}
        for x in dependency_map[repo['name']]:
            key = x['ecosystem'] + ':' + x['name']
            item = grouped.setdefault(key, {'key': key, 'versions': [], 'scopes': [], 'evidence': []})
            for field, source in [('versions', 'version'), ('scopes', 'scope'), ('evidence', 'evidence')]:
                if x[source] and x[source] not in item[field]: item[field].append(x[source])
            if x['ecosystem'] == 'source':
                source = source_url(x['version'])
                owner = source.split('github.com/')[-1].split('/')[0] if 'github.com/' in source else ''
                metadata[key] = {'name': x['name'], 'ecosystem': 'source', 'source': source, 'registry': source, 'maintainers': [owner + ' contributors'] if owner else [], 'license': 'See upstream license', 'metadata_version': ''}
        records.append({k: v for k, v in repo.items() if k != 'paths'} | {'dependencies': list(grouped.values()), 'manifests': dependency_paths(repo.get('paths', [])), 'notices': [p['path'] if isinstance(p, dict) else p for p in repo.get('paths', []) if re.search(r'(^|/)(LICENSE[^/]*|NOTICE[^/]*|THIRD_PARTY[^/]*|ThirdPartyNoticeText\.txt)$', p['path'] if isinstance(p, dict) else p)], 'errors': [e for e in evidence_errors if e['repository'] == repo['name']]})
    out = {'reviewed': inventory['reviewed'], 'repositories': records, 'packages': metadata}
    target = ROOT / args.output; target.parent.mkdir(exist_ok=True); target.write_text(json.dumps(out, indent=2, ensure_ascii=False).replace('\u2014', ','))
    print(f'Wrote {target}; {len(evidence_errors)} source parse errors; {sum(bool(v.get("error")) for v in metadata.values())} metadata errors.', flush=True)

if __name__ == '__main__': main()
