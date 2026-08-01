"""
CV CLI — generates one client's condensed/reframed CV PDF via cv_builder.py.

Run:  python3 generate_cv.py "Client Name"

Reads Clients/<Client Name>/cv_data.py's CV dict and writes
Clients/<Client Name>/<initials>_CV.pdf alongside it.
"""

import importlib.util
import os
import sys

from cv_builder import build_cv

HERE = os.path.dirname(__file__)


def load_cv(client_name):
    data_path = os.path.join(HERE, "Clients", client_name, "cv_data.py")
    spec = importlib.util.spec_from_file_location("cv_data", data_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CV


def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: python3 generate_cv.py "Client Name"')

    client_name = sys.argv[1]
    data = load_cv(client_name)
    initials = data["client"]["initials"]
    output_path = os.path.join(HERE, "Clients", client_name, f"{initials}_CV.pdf")
    build_cv(data, output_path)
    print(f"Saved -> {output_path}")


if __name__ == "__main__":
    main()
