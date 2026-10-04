"""Render recognition pages from recorded public dependency evidence."""
import html
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
E = html.escape

def link(url, label):
    if urlsplit(url).scheme not in ('http', 'https'):
        return E(label)
    return f'<a href="{E(url, quote=True)}">{E(label)}</a>'

def render_credits(page, projects):
    bundle = ROOT / 'data/credits'
    if bundle.exists():
        data = json.loads((bundle / 'overview.json').read_text())
        data['packages'] = {}
        for part in sorted(bundle.glob('packages-*.json')):
            data['packages'].update(json.loads(part.read_text()))
        for repo in data['repositories']:
            repo['dependencies'] = []
        by_name = {r['name']: r for r in data['repositories']}
        for part in sorted(bundle.glob('dependencies-*.json')):
            for record in json.loads(part.read_text()):
                by_name[record['repository']]['dependencies'].append(record['dependency'])
    else:
        data = json.loads((ROOT / 'data/credits.json').read_text())
    extra = json.loads((ROOT / 'data/credits-extra.json').read_text())
    output = ROOT / 'site/credits'
    output.mkdir(exist_ok=True)
    catalog = {p['slug']: p['name'] for p in projects}
    covered = {r['name'] for r in data['repositories']}
    assert set(catalog) <= covered, 'Every project guide needs a recognition page.'
    cards = []
    for repo in sorted(data['repositories'], key=lambda r: (r['name'] not in catalog, r['name'].lower())):
        slug = repo['name']; title = catalog.get(slug, slug)
        dependencies = repo['dependencies']
        supplements = extra.get(slug, [])
        source_root = 'https://github.com/' + repo['repo']
        source_revision = source_root + '/tree/' + repo['sha']
        origin = ''
        if repo.get('parent'):
            upstream = 'https://github.com/' + repo['parent']
            origin = '<section><h2>Original project</h2><p>This repository is a fork of ' + link(upstream, repo['parent']) + '. Credit belongs to the upstream maintainers and contributors.</p><p>' + link(upstream + '/graphs/contributors', 'Meet the contributors') + '</p></section>'
            if repo.get('copyright'):
                origin += '<section><h2>Credit from the original notice</h2><p>' + E(' · '.join(repo['copyright'])) + '</p><p>' + link(source_root + '/blob/' + repo['sha'] + '/LICENSE', 'Original copyright and license notice') + '</p></section>'
        body = f'<p class="breadcrumb"><a href="../credits.html">Recognition</a> / {E(title)}</p><section class="project-hero"><p class="eyebrow">People and projects behind the code</p><h1>{E(title)}<br>Recognition</h1><p class="lead">Thank you to the maintainers and contributors whose work this project uses.</p><a class="button" href="{E(source_root)}">Project source ↗</a>'
        if slug in catalog:
            body += f'<a class="button secondary" href="../projects/{E(slug)}.html">Project guide ↗</a>'
        body += '</section><article class="credits-prose">' + origin
        if supplements:
            body += '<section><h2>Tools, models, assets, and data</h2><div class="credit-table-wrap"><table class="credit-table"><thead><tr><th>Project</th><th>Maintainers / creators</th><th>Use in this project</th><th>Source and notices</th></tr></thead><tbody>'
            for item in supplements:
                body += '<tr><td>' + E(item['name']) + '</td><td>' + E(item['maintainers']) + '</td><td>' + E(item['use']) + '</td><td>' + link(item['source'], 'Source')
                if item.get('license_url'): body += ' · ' + link(item['license_url'], 'License / notices')
                if item.get('evidence'): body += '<br>' + link(source_root + '/blob/' + repo['sha'] + '/' + item['evidence'], 'Used here')
                body += '</td></tr>'
            body += '</tbody></table></div></section>'
        direct = [x for x in dependencies if set(x['scopes']) != {'locked'}]
        locked = [x for x in dependencies if set(x['scopes']) == {'locked'}]
        def table(items):
            content = '<div class="credit-table-wrap"><table class="credit-table"><thead><tr><th>Dependency and source</th><th>Maintainers / package owners</th><th>License metadata</th><th>Versions / evidence</th></tr></thead><tbody>'
            for dep in sorted(items, key=lambda x: x['key'].lower()):
                meta = data['packages'][dep['key']]
                names = ', '.join(meta.get('maintainers', []))
                if not names:
                    names = meta['name'] + ' contributors'
                content += '<tr><td>' + link(meta['source'], meta['name']) + '<br><span class="small">' + E(meta['ecosystem']) + ' · ' + link(meta['registry'], 'Package metadata') + '</span></td><td>' + E(names) + '</td><td>' + E(meta.get('license', 'See upstream license'))
                if meta.get('metadata_version'): content += '<br><span class="small">Metadata version ' + E(meta['metadata_version']) + '</span>'
                if meta.get('error'):
                    content += '<br><span class="small">' + link(meta['registry'], 'Published maintainer names and license') + '</span>'
                content += '</td><td>' + E(', '.join(dep['versions'])) + '<br><span class="small">' + E(', '.join(dep['scopes'])) + '</span><details><summary>Dependency evidence</summary><ul>'
                content += ''.join('<li>' + link(source_root + '/blob/' + repo['sha'] + '/' + path, path) + '</li>' for path in dep['evidence'])
                content += '</ul></details></td></tr>'
            return content + '</tbody></table></div>'
        if direct:
            body += f'<section><h2>Declared dependencies</h2><p>{len(direct)} packages declared in manifests, including optional and development tools.</p>' + table(direct) + '</section>'
        if locked:
            body += f'<section><details class="locked-credits"><summary><h2>Additional packages in lockfiles ({len(locked)})</h2></summary><p>These packages appear in recorded lockfiles. Optional platforms and development dependencies can be present even when a particular installation does not use them.</p>' + table(locked) + '</details></section>'
        if not dependencies:
            body += '<section><h2>Dependency records</h2><p>No external package dependencies were declared in the supported manifests found in this revision. Upstream project and tool credits appear above where applicable.</p></section>'
        if repo['notices']:
            body += '<section><h2>Original licenses and notices</h2><p>Original copyright notices and license terms are preserved in the linked source files.</p><ul>' + ''.join('<li>' + link(source_root + '/blob/' + repo['sha'] + '/' + path, path) + '</li>' for path in repo['notices']) + '</ul></section>'
        body += '<section><h2>Review sources</h2><p>Reviewed ' + E(data['reviewed']) + ' against ' + link(source_revision, repo['ref'] + ' at ' + repo['sha'][:12]) + '. Maintainer names come from package registry records or the upstream source namespace. Copyright holders are named in the original notices. License metadata includes the registry version reviewed; use the license shipped with your installed version.</p>'
        if repo['manifests']:
            body += '<details><summary>Manifests and lockfiles reviewed</summary><ul>' + ''.join('<li>' + link(source_root + '/blob/' + repo['sha'] + '/' + path, path) + '</li>' for path in repo['manifests']) + '</ul></details>'
        if repo.get('errors'):
            body += '<p>Additional source review is needed for: ' + E(', '.join(x['path'] for x in repo['errors'])) + '.</p>'
        body += '</section><section><h2>Give back</h2><p>Visit the upstream projects, read their contribution guides, report reproducible issues, improve documentation, and use their published sponsorship links when available.</p></section></article>'
        (output / (slug + '.html')).write_text(page(title + ' recognition', body, '../'))
        label = 'Fork / upstream project credited' if repo.get('fork') else 'Project / dependencies credited'
        cards.append(f'<article class="card"><p class="eyebrow">{E(label)}</p><h2><a href="credits/{E(slug)}.html">{E(title)}</a></h2><p>{len(dependencies)} package credits · {len(supplements)} tool, asset, or data credits</p><a href="credits/{E(slug)}.html">People, source, and notices ↗</a></article>')
    body = '<section class="project-hero"><p class="eyebrow">Upstream recognition</p><h1>Credit the work<br>behind the tools.</h1><p class="lead">Source projects, package maintainers, creators, and contributors behind these public repositories.</p><p>' + str(len(data['repositories'])) + ' repositories · ' + str(len(data['packages'])) + ' distinct package records · reviewed ' + E(data['reviewed']) + '</p></section><div class="grid">' + ''.join(cards) + '</div><section class="next"><h2>Keeping credit visible</h2><p>Every project guide links to its recognition page. Dependency records include manifests and lockfiles; existing notices remain linked at their original revision. Credits are a recorded review, updated with the source inventory and collection script.</p></section>'
    (ROOT / 'site/credits.html').write_text(page('Open source recognition', body))
    return len(data['repositories'])
