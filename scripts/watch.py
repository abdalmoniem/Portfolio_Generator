"""
Run this script to watch for changes to the portfolio.json file and regenerate
the portfolio and resume pages when it changes.

Example usage:

    python watch.py

"""

from pathlib import Path
from subprocess import run
from typing import Optional
from livereload import Server
from sys import executable as python_executable

HOST = "localhost"
PORT = 8000
SCRIPT_DIR = Path(__file__).resolve().parent
SCRIPT_TO_RUN = f"{SCRIPT_DIR}/generate_portfolio.py"

watched_files = [
    SCRIPT_TO_RUN,
    f"{SCRIPT_DIR}/../templates/portfolio.json",
    f"{SCRIPT_DIR}/../templates/index_template.html",
    f"{SCRIPT_DIR}/../templates/resume_template.html",
    f"{SCRIPT_DIR}/../templates/resume_pdf_template.html",
]

for file in Path(f"{SCRIPT_DIR}/../templates/css").glob("*.css"):
    watched_files.append(str(file))

def run_script(changed_file: Optional[str] = None) -> None:
    """
    Executes a specified script and handles changes to files.

    If a change is detected in the specified `changed_file`, the function
    prints a message indicating the detected change. It then runs the script
    defined by `SCRIPT_TO_RUN` using the Python interpreter. After the script
    execution, a message is printed to confirm the script has finished.

    If the `changed_file` is an HTML file (i.e., its name ends with ".html"),
    the function assumes it corresponds to a served file and prints messages
    indicating the need to reload the served file and the browser.

    Args:
        changed_file (Optional[str]): The name of the file that has changed,
                                      which triggers the script execution.
    """

    if changed_file:
        print(f"Detected change in {changed_file}!")

    print(f"Running {SCRIPT_TO_RUN}...")
    run([python_executable, SCRIPT_TO_RUN], check=True)
    print(f"Script {SCRIPT_TO_RUN} finished!")

    if changed_file and changed_file.endswith(".html"):
        served_file = changed_file.replace("_template", "")
        print(f"Reloading {served_file}...")
        print("Reloading browser...")


def main() -> None:
    """
    Watches the specified files for changes and runs the specified script
    when changes are detected. Serves the current directory using a LiveReload
    server.

    This function runs the specified script once when it is first called, and
    also sets up a LiveReload server to watch for changes in the specified
    files. If any of the watched files are changed, the script is executed
    again.

    The LiveReload server is started after the script has finished running
    initially. The server serves the current directory, making it accessible
    at `http://<HOST>:<PORT>`. The server is configured to use LiveReload,
    which allows browsers to automatically reload the page when any of the
    watched files change.
    """

    run_script()

    server = Server()
    for file in watched_files:
        server.watch(file, lambda changed_file=file: run_script(changed_file))

    # Serve current directory (so output.html is served)
    print(f"Serving on http://{HOST}:{PORT} (LiveReload enabled)")
    server.serve(root=f"{SCRIPT_DIR}/../generated", port=PORT, host=HOST)


if __name__ == "__main__":
    main()
