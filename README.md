# Stated Preference Survey Research for Transportation

This repository houses a ready-to-deploy GitHub Pages site for the **Stated Preference Survey Research for Transportation** course developed by Mahbub Hassan (Non Asean Scholar, Department of Civil Engineering, Faculty of Engineering, Chulalongkorn University, Bangkok, Thailand).

## Repository structure
- `index.md` - public landing page with quick facts and navigation.
- `syllabus.md` - full syllabus, logistics, and expectations.
- `modules/` - detailed lesson content for the six modules.
- `assignments/` - assessment briefs with instructions and rubrics.
- `_config.yml` - GitHub Pages/Jekyll configuration (title, theme, metadata).
- `.gitignore` - ignores build artifacts such as `_site/`.
- `LICENSE` - MIT license covering this repository.

## How to deploy on GitHub Pages
1. Create a new GitHub repository and copy these files into it (or add this directory as a subfolder named `docs`).
2. Commit and push the content to the `main` branch.
3. In GitHub, open **Settings -> Pages** and set the source to `main` (or `/docs` if applicable).
4. Optionally pick a theme; all files already include Markdown-friendly headings that render cleanly on GitHub Pages.

### Suggested Git workflow
```powershell
cd "E:\06_GitHub_Repo\02_Templates\SP Survey Course"
git init
git add .
git commit -m "Add stated preference survey research course"
git branch -M main
git remote add origin https://github.com/mahbubchula/-Stated-Preference-Survey-Research.git
git push -u origin main
```

After the first push, future updates are just `git add .`, `git commit -m "..."`, and `git push`.

## Customization tips
- Update module content in `modules/` to add local datasets, institutional policies, or links to slides.
- Expand the `assignments/` folder with rubrics, templates, or submission checklists hosted on your LMS.
- Add media (images, PDFs, datasets) under a new `assets/` folder and link directly from the Markdown files.
- If you adopt a Jekyll theme, keep the YAML front matter at the top of each Markdown file or add new keys such as `nav_order`.

## Local preview (optional)
If you want to run the site locally with Jekyll:
```powershell
gem install bundler jekyll
bundle init
bundle add jekyll
bundle exec jekyll serve
```
Then browse to `http://localhost:4000`. This step is optional because GitHub Pages builds automatically after pushes.

## Support
Questions or requests for tailoring can be directed to Mahbub Hassan at [mahbub.hassan@ieee.org](mailto:mahbub.hassan@ieee.org) or [6870376421@student.chula.ac.th](mailto:6870376421@student.chula.ac.th).

## License
Content and code are distributed under the MIT License (see `LICENSE`). Feel free to reuse with attribution.


