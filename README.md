# 🚆 Stated Preference Survey Research for Transportation

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-green.svg)](https://mahbubchula.github.io/-Stated-Preference-Survey-Research)

A comprehensive, professional course on designing, implementing, and analyzing stated preference (SP) surveys for transportation planning and policy.

**Developed by:** Mahbub Hassan, Non Asean Scholar
**Institution:** Department of Civil Engineering, Faculty of Engineering, Chulalongkorn University, Bangkok, Thailand
**Contact:** [mahbub.hassan@ieee.org](mailto:mahbub.hassan@ieee.org) | [6870376421@student.chula.ac.th](mailto:6870376421@student.chula.ac.th)

---

## 📚 About This Course

This repository houses a ready-to-deploy GitHub Pages site for the **Stated Preference Survey Research for Transportation** course. The course covers the complete SP research lifecycle—from theoretical foundations through survey design, experimental methods, implementation, discrete choice modeling, and policy communication.

### Course Highlights

- **6 comprehensive modules** with 400-1,500 lines of detailed content each
- **Real-world case studies** from Singapore, London, Norway, and North America
- **Hands-on labs** with Biogeme, Apollo, Ngene, R, and Python
- **Professional design** with custom CSS theme and responsive layout
- **Industry-ready skills** in SP survey design and discrete choice analysis

---

## 🎯 Learning Outcomes

Upon completing this course, participants will be able to:

1. ✅ Distinguish SP approaches from revealed preference data and defend when to use each
2. ✅ Formulate research objectives, target populations, and experiment-friendly attributes/levels
3. ✅ Construct efficient choice task designs using orthogonal and Bayesian techniques
4. ✅ Plan, pilot, and execute SP fieldwork ethically with reproducible documentation
5. ✅ Estimate logit-family models, interpret parameters, elasticity measures, and heterogeneity
6. ✅ Communicate findings for decision-makers via scenario analysis and policy memos

---

## 📂 Repository Structure

```
SP-Survey-Course/
├── index.md                 # Course landing page
├── syllabus.md              # Full syllabus and logistics
├── _config.yml              # Jekyll configuration
├── modules/                 # 6 detailed course modules
│   ├── 01-foundations.md
│   ├── 02-survey-design.md
│   ├── 03-experimental-design.md
│   ├── 04-implementation.md
│   ├── 05-modeling.md
│   └── 06-policy-communication.md
├── assignments/             # Assessment briefs with rubrics
│   ├── 01_reflection.md
│   ├── 02_design_brief.md
│   ├── 03_design_package.md
│   ├── 04_pilot_plan.md
│   ├── 05_modeling_memo.md
│   └── 06_capstone.md
├── assets/                  # Course resources
│   ├── css/
│   │   └── style.scss       # Custom professional theme
│   ├── code/
│   │   ├── example_mnl_biogeme.py
│   │   └── example_design_ngene.txt
│   ├── data/
│   │   └── sample_sp_data_structure.csv
│   └── images/              # (add your images here)
├── .gitignore
├── LICENSE                  # MIT License
└── README.md               # This file
```

---

## 🚀 How to Deploy on GitHub Pages

### Option 1: Direct Deployment

1. **Fork or clone this repository**
   ```bash
   git clone https://github.com/mahbubchula/-Stated-Preference-Survey-Research.git
   cd -Stated-Preference-Survey-Research
   ```

2. **Push to your GitHub repository**
   ```bash
   git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**
   - Go to **Settings → Pages**
   - Set source to `main` branch
   - Click **Save**

4. **Access your site**
   - Visit: `https://YOUR_USERNAME.github.io/YOUR_REPO`

### Option 2: New Repository Setup

```bash
# Navigate to your local course folder
cd "E:\06_GitHub_Repo\02_Templates\SP Survey Course"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Comprehensive SP Survey Research Course"

# Add remote repository
git remote add origin https://github.com/mahbubchula/-Stated-Preference-Survey-Research.git

# Push to GitHub
git branch -M main
git push -u origin main
```

After pushing, enable GitHub Pages in your repository settings.

---

## 🎨 Customization

### Visual Theme

The course includes a custom CSS theme with:
- **Professional color palette:** Deep blue primary, teal secondary, vibrant accents
- **Responsive design:** Mobile-friendly layout
- **Enhanced typography:** Clear hierarchy and readability
- **Custom components:** Alert boxes, module cards, badges

To customize colors, edit `assets/css/style.scss` and modify the CSS variables in the `:root` section.

### Content Adaptation

**For your institution:**
1. Update `_config.yml` with your details
2. Replace contact information in `index.md` and `syllabus.md`
3. Add local case studies in modules
4. Customize assignment rubrics in `assignments/` folder

**For different domains:**
- Adapt attribute examples (e.g., healthcare, environmental policy)
- Swap transportation case studies with relevant examples
- Modify software recommendations for your field

### Adding Media

Place images, PDFs, and datasets in `assets/` subfolders:
```
assets/
  images/         # Screenshots, diagrams, charts
  data/           # Practice datasets, examples
  code/           # Additional scripts, templates
  docs/           # Supplementary materials
```

Reference in Markdown:
```markdown
![Description](assets/images/your-image.png)
[Download Data](assets/data/your-dataset.csv)
```

---

## 🛠️ Local Development (Optional)

To preview the site locally before pushing:

### Prerequisites
- Ruby (2.7+)
- Bundler
- Jekyll

### Setup

```bash
# Install dependencies
gem install bundler jekyll

# Create Gemfile
bundle init

# Add Jekyll
bundle add jekyll

# Install plugins
bundle add jekyll-feed jekyll-seo-tag jekyll-sitemap

# Serve locally
bundle exec jekyll serve
```

Browse to `http://localhost:4000`

**Note:** Local preview is optional—GitHub Pages builds automatically.

---

## 📖 Course Modules

### Module 1: Foundations of SP Methods (429 lines)
Theoretical foundations, utility theory, RP vs. SP comparison, real-world applications

### Module 2: Survey Design Essentials (1,012 lines)
Attribute selection, questionnaire architecture, stakeholder engagement, sampling strategies

### Module 3: Experimental Design (1,298 lines)
Factorial designs, D-efficiency, Ngene tutorials, choice card design

### Module 4: Implementation & Fieldwork (1,570 lines)
Survey platforms, pilot testing, ethics compliance, quality assurance

### Module 5: Discrete Choice Modeling (1,692 lines)
MNL, mixed logit, Biogeme/Apollo workflows, model diagnostics, elasticities

### Module 6: Policy Communication (1,611 lines)
Scenario analysis, visualization, executive storytelling, capstone project

**Total:** Over 7,000 lines of comprehensive educational content!

---

## 🎓 Who Should Use This Course?

- **Transportation Planners** evaluating new services or policies
- **Policy Analysts** forecasting technology adoption
- **Graduate Students** in civil engineering, urban planning, economics
- **Consultants** working on transit, pricing, or mobility projects
- **Agency Researchers** designing demand studies or policy evaluations

---

## 🧰 Software & Tools

The course covers:

- **Survey Platforms:** Qualtrics, SurveyCTO, LimeSurvey
- **Experimental Design:** Ngene, R idefix, Python pylogit
- **Modeling:** Biogeme (Python), Apollo (R), Stata
- **Visualization:** ggplot2, matplotlib, Tableau, Power BI

---

## 📜 License

This repository and all course content are distributed under the **MIT License**. You are free to:

- ✅ Use for teaching and learning
- ✅ Modify and adapt to your context
- ✅ Share with attribution
- ✅ Use commercially (e.g., corporate training)

See [LICENSE](LICENSE) for full legal details.

---

## 🙏 Acknowledgments

This course draws inspiration from:
- **Choice Modelling Centre**, University of Leeds
- **Institute for Choice**, University of South Australia
- **Transportation Research Board** courses
- **Federal Transit Administration** training programs

Special thanks to the discrete choice modeling community for open-source tools and knowledge sharing.

### Key References

- Train, K. (2009). *Discrete Choice Methods with Simulation*
- Ben-Akiva, M., & Lerman, S. R. (1985). *Discrete Choice Analysis*
- Louviere, J. J., Hensher, D. A., & Swait, J. D. (2000). *Stated Choice Methods*

---

## 💬 Support & Contact

**Instructor:** Mahbub Hassan
**Email:** [mahbub.hassan@ieee.org](mailto:mahbub.hassan@ieee.org) | [6870376421@student.chula.ac.th](mailto:6870376421@student.chula.ac.th)
**GitHub:** [@mahbubchula](https://github.com/mahbubchula)
**Institution:** Chulalongkorn University, Bangkok, Thailand

### Getting Help

- **Course Questions:** Email the instructor
- **Technical Issues:** [Open a GitHub issue](https://github.com/mahbubchula/-Stated-Preference-Survey-Research/issues)
- **Contributions:** Pull requests welcome!

---

## 🌟 Features

✨ **Comprehensive Content:** 7,000+ lines of detailed module content
🎨 **Professional Design:** Custom CSS with modern color scheme
📊 **Real-World Cases:** Singapore, London, Norway, California
💻 **Code Examples:** Python, R, Ngene, JavaScript
📚 **Rich Resources:** Textbooks, articles, software tutorials
✅ **Assessment Ready:** Rubrics for all assignments
📱 **Responsive:** Mobile-friendly design
🔍 **SEO Optimized:** Meta tags and sitemap included

---

## 🚀 Quick Start

1. **View the course:** [https://mahbubchula.github.io/-Stated-Preference-Survey-Research](https://mahbubchula.github.io/-Stated-Preference-Survey-Research)
2. **Start learning:** Begin with [Module 1: Foundations](modules/01-foundations.md)
3. **Customize:** Fork and adapt to your needs
4. **Contribute:** Submit improvements via pull requests

---

## 📈 Version History

- **v2.0** (February 2026) - Complete course redesign with comprehensive content, custom theme, and 6 detailed modules
- **v1.0** (Initial) - Basic course structure

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

**Made with ❤️ for the transportation research community**

**Last Updated:** February 2026
**Maintained by:** Mahbub Hassan, Chulalongkorn University

---

⭐ **If you find this course helpful, please star this repository!** ⭐
