# Course Assets

This directory contains supporting materials for the Stated Preference Survey Research course.

## Directory Structure

```
assets/
├── css/              # Custom stylesheets
│   └── style.scss    # Main theme with professional color scheme
├── code/             # Example code snippets
│   ├── example_mnl_biogeme.py    # MNL estimation in Python
│   └── example_design_ngene.txt  # Experimental design in Ngene
├── data/             # Sample datasets
│   └── sample_sp_data_structure.csv  # Example data format
└── images/           # Course images and diagrams (to be added)
```

## Usage

### CSS Theme

The custom CSS theme provides a professional academic color scheme:
- **Primary Colors:** Deep blue academic theme
- **Secondary Colors:** Complementary teal
- **Accent Colors:** Orange, green, yellow for highlights
- Responsive design for mobile and desktop
- Print-friendly styles

### Code Examples

**example_mnl_biogeme.py:**
- Complete MNL model estimation workflow
- Uses Python Biogeme library
- Includes data loading, model specification, estimation, and interpretation
- Calculates Value of Time (VoT) and elasticities

**example_design_ngene.txt:**
- Ngene syntax for efficient experimental design
- D-optimal design with Bayesian priors
- Three-alternative mode choice example
- Includes constraints and blocking

### Sample Data

**sample_sp_data_structure.csv:**
- Example format for SP choice data
- Long format (one row per alternative per choice task)
- Fields: respondent_id, choice_task, alt, choice, attributes, availability

## Adding Your Own Assets

Students and instructors can add:
- **Images:** Screenshots, diagrams, survey examples
- **Code:** Additional modeling scripts, data processing tools
- **Data:** Practice datasets, case study data
- **Templates:** Survey templates, report templates

## License

All assets are distributed under the MIT License (see main LICENSE file).

## Contact

Questions about course assets: [mahbub.hassan@ieee.org](mailto:mahbub.hassan@ieee.org)
