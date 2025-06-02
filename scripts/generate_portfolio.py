"""
Generate an HTML page from a Jinja template and a JSON data file.

The script assumes that the JSON file is in the same directory as the script,
and is named "portfolio.json". The script also assumes that the Jinja template
is in the same directory as the script, and is named "index_template.html".

The generated HTML page is saved to a file named "index.html", in the same
directory as the script.

The script also assumes that the JSON file is a serialized version of a
dataclass, and that the dataclass has a class variable named "TEMPLATE_VARS"
that contains a list of strings. The strings in the list are the names of
the variables that are available in the Jinja template.

The JSON file is read from disk, parsed into a Python object, and passed to
the Jinja template as a variable named "data". The Jinja template is then
rendered to HTML, and saved to disk.

The script can be run from the command line, with no arguments.

Example usage:

    python generate_portfolio.py

"""

import os
import json
import shutil
import pdfkit
from pathlib import Path
from dacite import from_dict
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader


@dataclass
class ContactInfo:
    """Contact information class

    Attributes:
        email (str): Email address
        phone (str): Phone number
        location (str): Location
    """

    email: Optional[str]
    phone: Optional[str]
    location: Optional[str]


@dataclass
class SocialLink:
    """Social link class

    Attributes:
        label (str): Label of the social link
        url (str): URL of the social link
        svg_path (str): Path of the SVG icon
        svg_data (str): SVG data of the icon
    """

    label: str
    url: str
    svg_path: str
    svg_data: Optional[str]


@dataclass
class WorkExperience:
    """Work experience class

    Attributes:
        company (str): Company name
        position (str): Position
        url (str): URL of the company
        start_date (str): Start date of the work experience
        end_date (str): End date of the work experience
        summary (str): Summary of the work experience
        highlights (list[str]): Highlights of the work experience
    """

    company: str
    position: str
    url: Optional[str]
    start_date: str
    end_date: str
    summary: Optional[str]
    highlights: Optional[List[str]]


@dataclass
class ProjectImage:
    """Project image class

    Attributes:
        img_path (str): Path to the image
        caption (str): Caption of the image
    """

    img_path: str
    caption: Optional[str]


@dataclass
class Project:
    """Project class

    Attributes:
        title (str): Title of the project
        summary (str): Summary of the project
        url (str): URL of the project
        highlights (list[str]): Highlights of the project
        images (list[ProjectImage]): List of images of the project
        tools (list[str]): List of tools used in the project
    """

    title: str
    summary: Optional[str]
    url: Optional[str]
    highlights: Optional[List[str]]
    images: Optional[List[ProjectImage]]
    tools: Optional[List[str]]


@dataclass
class VolunteerExperience:
    """Volunteer experience class

    Attributes:
        organization (str): Organization of the volunteer experience
        position (str): Position of the volunteer experience
        url (str): URL of the organization
        start_date (str): Start date of the volunteer experience
        end_date (str): End date of the volunteer experience
        summary (str): Summary of the volunteer experience
        highlights (list[str]): Highlights of the volunteer experience
    """

    organization: str
    position: str
    url: Optional[str]
    start_date: str
    end_date: str
    summary: Optional[str]
    highlights: Optional[List[str]]


@dataclass
class Education:
    """Education class

    Attributes:
        institution (str): Institution of the education
        location (str): Location of the institution
        url (str): URL of the institution
        degrees (list[str]): Degrees of the education
        honors (list[str]): Honors of the education
        gpa_cumulative (str): Cumulative GPA of the education
        gpa_major (str): Major GPA of the education
        enrollment_date (str): Enrollment date of the education
        graduation_date (str): Graduation date of the education
    """

    institution: str
    location: str
    url: Optional[str]
    degrees: List[str]
    honors: Optional[List[str]]
    gpa_cumulative: Optional[str]
    gpa_major: Optional[str]
    enrollment_date: str
    graduation_date: str


@dataclass
class Skill:
    """Skill class

    Attributes:
        name (str): Name of the skill
        proficiency (int): Proficiency of the skill
        proficiency_label (str): Proficiency label of the skill
    """

    name: str
    proficiency: Optional[int]
    proficiency_label: Optional[str]


@dataclass
class Language:
    """Language class

    Attributes:
        name (str): Name of the language
        fluency (str): Fluency of the language
    """

    name: str
    fluency: Optional[str]


@dataclass
class InterestImage:
    """Interest image class

    Attributes:
        img_path (str): Path to the image
        caption (str): Caption of the image
    """

    img_path: str
    caption: Optional[str]


@dataclass
class Interest:
    """Interest class

    Attributes:
        name (str): Name of the interest
        summary (str): Summary of the interest
        images (List[InterestImage]): List of images related to the interest
    """

    name: str
    summary: Optional[str]
    images: Optional[List[InterestImage]]


@dataclass
class Portfolio:
    """Portfolio class

    Attributes:
        name (str): Name of the portfolio
        label (str): Label of the portfolio
        image_path (str): Path to the portfolio image
        contact (List[ContactInfo]): List of contact information
        summary (str): Summary of the portfolio
        base_url (str): Base URL of the portfolio
        social_links (List[SocialLink]): List of social links
        work_experience (List[WorkExperience]): List of work experiences
        projects (List[Project]): List of projects
        volunteer_experience (List[VolunteerExperience]): List of volunteer experiences
        education (List[Education]): List of education records
        skills (List[Skill]): List of skills
        interests (Optional[List[Interest]]): List of interests
        languages (Optional[List[Language]]): List of languages
        current_year (Optional[int]): The current year
    """

    name: str
    label: str
    image_path: str
    contact: List[ContactInfo]
    summary: str
    base_url: str
    social_links: List[SocialLink]
    work_experience: List[WorkExperience]
    projects: List[Project]
    volunteer_experience: List[VolunteerExperience]
    education: List[Education]
    skills: List[Skill]
    interests: Optional[List[Interest]]
    languages: Optional[List[Language]]
    current_year: Optional[int]


def main() -> None:
    """
    Main entry point of the script.

    This function loads the Portfolio JSON data, loads the SVG files, sets up the Jinja environment,
    renders the HTML templates with the data, and writes the output to an HTML file.

    :return: None
    """

    SCRIPT_DIR = Path(__file__).resolve().parent
    TEMPLATES_DIR = SCRIPT_DIR / "../templates"
    GENERATED_DIR = SCRIPT_DIR / "../generated"
    portfolio_path = TEMPLATES_DIR / "portfolio.json"
    index_template_path = TEMPLATES_DIR / "index_template.html"
    resume_template_path = TEMPLATES_DIR / "resume_template.html"
    resume_pdf_template_path = TEMPLATES_DIR / "resume_pdf_template.html"
    index_path = GENERATED_DIR / "index.html"
    resume_path = GENERATED_DIR / "resume.html"
    resume_pdf_path = GENERATED_DIR / "resume_pdf.html"
    pdf_output_path = GENERATED_DIR / "resume.pdf"

    # Ensure the generated directory exists
    if not GENERATED_DIR.exists():
        print(f"Creating directory: {GENERATED_DIR}")
        GENERATED_DIR.mkdir(parents=True, exist_ok=True)
    else:
        print(f"Clearing directory: {GENERATED_DIR}")
        delete_dir_contents(GENERATED_DIR)

    # Load JSON data
    with portfolio_path.open(encoding="utf-8") as file_handle:
        raw_data = json.load(file_handle)
        portfolio = from_dict(data_class=Portfolio, data=raw_data)

    portfolio.current_year = datetime.now().year

    if portfolio.social_links:
        for link in portfolio.social_links:
            if link.svg_path:
                with (TEMPLATES_DIR / link.svg_path).open(encoding="utf-8") as svg_file:
                    link.svg_data = svg_file.read()

    # Set up Jinja environment
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)
    index_template = env.get_template(index_template_path.name)
    resume_template = env.get_template(resume_template_path.name)
    resume_pdf_template = env.get_template(resume_pdf_template_path.name)

    # Render the template with the data
    html_output = index_template.render(**portfolio.__dict__)
    resume_output = resume_template.render(**portfolio.__dict__)
    resume_pdf_output = resume_pdf_template.render(**portfolio.__dict__)

    print("Copying CSS files...")
    css_dir = TEMPLATES_DIR / "css"
    generated_css_dir = SCRIPT_DIR / "../generated/css"
    generated_css_dir.mkdir(parents=True, exist_ok=True)

    copy_files(
        src=css_dir,
        dest=generated_css_dir,
        pattern="*.css",
    )

    print("Copying images...")
    images_dir = TEMPLATES_DIR / "img"
    favicon_path = TEMPLATES_DIR / "img/favicon.ico"
    generated_images_dir = SCRIPT_DIR / "../generated/img"

    copy_files(
        src=images_dir,
        dest=generated_images_dir,
        pattern="*.*",
    )

    copy_files(
        src=images_dir,
        dest=GENERATED_DIR,
        pattern=favicon_path.name,
    )

    print("Copying JS files...")
    js_dir = TEMPLATES_DIR / "js"
    generated_js_dir = SCRIPT_DIR / "../generated/js"

    copy_files(
        src=js_dir,
        dest=generated_js_dir,
        pattern="*.js",
    )

    # Write the output to an HTML file
    with index_path.open("w", encoding="utf-8") as file_handle:
        written = file_handle.write(html_output)

        if written == len(html_output):
            print(f"{index_path.name} generated successfully!!")
        else:
            print(f"Failed to generate {index_path.name}.")

    with resume_path.open("w", encoding="utf-8") as file_handle:
        written = file_handle.write(resume_output)

        if written == len(resume_output):
            print(f"{resume_path.name} generated successfully!!")
        else:
            print(f"Failed to generate {resume_path.name}.")

    with resume_pdf_path.open("w", encoding="utf-8") as file_handle:
        written = file_handle.write(resume_pdf_output)

        if written == len(resume_pdf_output):
            print(f"{resume_pdf_path.name} generated successfully!!")
        else:
            print(f"Failed to generate {resume_pdf_path.name}.")

    # Convert HTML to PDF
    status = pdfkit.from_file(
        input=str(resume_pdf_path),
        output_path=str(pdf_output_path),
        verbose=True,
        options={
            "enable-local-file-access": "",  # Required for local CSS/images
            "load-error-handling": "ignore",  # Suppress errors on loading
            "encoding": "UTF-8",
            "disable-smart-shrinking": "",
        },
    )

    if status:
        print(f"{pdf_output_path.name} generated successfully!!")
    else:
        print(f"Failed to generate {pdf_output_path.name}.")


def delete_dir_contents(path: Path) -> None:
    """
    Deletes the contents of a given directory.

    This function is used to remove the previous build of the website
    before generating a new one.

    Args:
        path (Path): The path to the directory to be cleaned.
    """

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # remove file or symlink
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # remove directory and its contents
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def copy_files(src: Path, dest: Path, pattern: str = "*.*") -> None:
    """
    Copies files from a source directory to a destination directory.

    This function searches for files in the source directory matching the
    specified pattern and copies them to the destination directory. If the
    destination directory does not exist, it is created. The function reads
    the content of each file in binary mode and writes it to the corresponding
    file in the destination directory.

    Args:
        src (Path): The path to the source directory containing files to copy.
        dest (Path): The path to the destination directory where files are copied.
        pattern (str, optional): A glob pattern to match files in the source
                                 directory. Defaults to "*.*".
    """

    dest.mkdir(parents=True, exist_ok=True)
    for file in src.glob(pattern):
        target_path = dest / file.name
        with file.open("rb") as source, target_path.open("wb") as target:
            content = source.read()
            target.write(content)
            # print(f"Copied {file.name} to {target_path.name}")


if __name__ == "__main__":
    main()
