# Pixel Legion Maker

English guide, public API reference and support resources for **Pixel Legion Maker**, a 2D pixel hero builder for Unity 6.

- Manual: https://hyunter777.github.io/pixel-legion-maker/
- API: https://hyunter777.github.io/pixel-legion-maker/api/
- FAQ: https://hyunter777.github.io/pixel-legion-maker/faq/
- Bug reports and questions: https://github.com/hyunter777/pixel-legion-maker/issues

This repository holds documentation only. The product's implementation, Unity project and package files are not published here.

## Build

Use Python 3.12, .NET 8 and DocFX 2.81.0:

```sh
python -m pip install -r requirements.txt
dotnet tool install --global docfx --version 2.81.0
python scripts/build.py --output site
```

The committed API metadata (`api-metadata/`) holds public type and member declarations only; source files and source links are stripped. A site build reads it and does not need Unity or the product.

## Preview

After building, run `python -m http.server 8788 --directory site` and open the printed local address. To edit guides with automatic reload, run `python -m mkdocs serve`.

## Publish an update

```sh
python scripts/build.py --output site
ghp-import -n -p site
```

The repository's Pages source is `gh-pages` at `/`. `-n` adds `.nojekyll` so GitHub serves the generated files directly. A GitHub Actions workflow template is kept in `deployment/pages-workflow.yml`.

Copyright © FlyCat. Documentation and screenshots belong to the publisher. Inter is distributed under SIL OFL 1.1; its license accompanies the font files in `docs/en/assets/fonts/`.
