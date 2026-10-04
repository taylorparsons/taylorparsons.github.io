# Taylor Parsons Open Source

Public project catalog for https://taylorparsons.github.io/.

## Build and preview

```sh
python3 scripts/build.py
python3 -m http.server 8000 --directory site
```

Open http://localhost:8000/. Project facts and copy are in scripts/build.py. Styles and browser interactions are in assets/. Only site/ is deployed.

## Deployment

Create the public taylorparsons.github.io repository. Push to main and select Settings > Pages > Source > GitHub Actions. The workflow uses the official Pages actions pinned by the create-gh-pages-site template.

## Content scope

Eight public projects and contributions are documented. The ChatGPT History to Markdown guide covers Taylor's vector-search contribution on the feature/hybrid-search branch and credits the original project. Private repository reviews and personal data are excluded. Source documentation is linked from every project guide.

## Graphics

The homepage uses a CSS workflow illustration. Project visuals reuse public repository images. Social card and favicon are SVG graphics.

## Upstream recognition

Recognition is linked from every project guide and the main navigation. The credits index covers 29 public repositories, including forks whose original upstream projects are credited. Direct dependencies, development dependencies, and packages in lockfiles have source or registry links. Additional credits cover runtime tools, fonts, models, browser libraries, maps, and public data.

The recorded review is in data/credits/ and data/credits-extra.json. Provenance includes source revisions and manifest paths in data/credits-sources.json. Names come from public package metadata and source notices; where a registry lookup is unavailable, the package contributor group is credited and linked to the published maintainer records. A package's public maintainers are not necessarily all its copyright holders.

To refresh, update the public source revisions and manifest paths in data/credits-sources.json, run python3 scripts/collect_credits.py, then python3 scripts/package_credits.py. Review the changes before committing them. The collection script reads public source and package metadata without installing or executing dependency code. A new project guide must have a recognition record or the site build fails.

Project guides also support extensionless URLs. The 404 page uses full site asset URLs so its navigation and styling work at missing nested paths. Asset version queries refresh cached styles and browser scripts after edits.

## Edit the site yourself

On GitHub, open scripts/build.py and choose Edit file. Project records near the top contain name, pitch, use, requirements, commands, steps, and detail. The homepage, use-case, and About text are in the same file. Commit to main to rebuild and deploy. Change appearance in assets/styles.css. Edit recognition additions in data/credits-extra.json. Do not edit generated site/ HTML.
