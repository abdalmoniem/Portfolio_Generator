# Resume and Portfolio Generator

This project is a collection of tools and scripts that generate a resume and portfolio based on a JSON data file and a set of Jinja templates.

The project consists of the following parts:

- A JSON data file that contains information about the person, their education, work experience, skills, and projects. The data is organized as a nested dictionary, with each key corresponding to a section of the resume or portfolio.
- A set of Jinja templates that define the structure and layout of the resume and portfolio. The templates are written in HTML and use Jinja syntax to access the data in the JSON file.
- A Python script that reads the JSON data file, parses it into a Python object, and renders the Jinja templates using the data. The script generates an HTML file for the resume and portfolio, and also generates a PDF version of the resume.

The project is designed to be easy to use and customize. The user can simply edit the JSON data file to add or change information, and then run the script to generate the resume and portfolio. The user can also customize the templates to change the layout and design of the resume and portfolio.

## Getting Started

To use this project, follow these steps:

1. Clone the repository to a local directory.
2. Edit the `portfolio.json` file to add or change information about the person, their education, work experience, skills, and projects.
3. Run the `generate_portfolio.py` script to generate the resume and portfolio. The script will create an HTML file for the resume and portfolio, and also generate a PDF version of the resume.
4. Open the HTML file in a web browser to view the resume and portfolio.

## Customizing the Templates

The templates are written in HTML and use Jinja syntax to access the data in the JSON file. The templates are organized into the following directories:

- `templates/resume_template.html`: This is the main template for the resume. It defines the structure and layout of the resume, and uses Jinja syntax to access the data in the JSON file.
- `templates/resume_pdf_template.html`: This is the main template for the PDF version of the resume. It defines the structure and layout of the PDF resume, and uses Jinja syntax to access the data in the JSON file.
- `templates/index_template.html`: This is the main template for the portfolio. It defines the structure and layout of the portfolio, and uses Jinja syntax to access the data in the JSON file.
- `templates/css/main.css`: This is the stylesheet for the resume and portfolio. It defines the colors, fonts, and layout of the resume and portfolio.

To customize the templates, simply edit the HTML and CSS files in the `templates` directory. The changes will be reflected in the generated resume and portfolio.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
