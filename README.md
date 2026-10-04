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

Eight public, non-fork project repositories were reviewed. Private repository reviews and personal data are excluded. Source documentation is linked from every project guide.

## Graphics

The homepage uses a CSS workflow illustration. Project visuals reuse public repository images. Social card and favicon are SVG graphics.
