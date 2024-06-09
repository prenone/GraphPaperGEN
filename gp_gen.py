import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import re


class gp_state:
    height = 0
    width = 0

    margin_left = 0
    margin_right = 0
    margin_top = 0
    margin_bottom = 0

    xscale = ""
    yscale = ""

    grid = False
    grid_major_thicker_x = False
    grid_major_thicker_y = False

    x_max = 0
    x_min = 0
    y_max = 0
    y_min = 0

    title = ""
    x_label = ""
    y_label = ""

    x_tiks_numbers = False
    y_tiks_numbers = False

    img_format = "png"


def gp_gen(state: gp_state, filename):
    # Set the page size
    fig, ax = plt.subplots(figsize=(state.height, state.width))

    # Set margins
    plt.subplots_adjust(left=state.margin_left, right=state.margin_right,
                        top=state.margin_top, bottom=state.margin_bottom)

    # Set linear/log scale
    ax.set_xscale(state.xscale)
    ax.set_yscale(state.yscale)

    # Set scale size
    ax.set_xlim(state.x_min, state.x_max)
    ax.set_ylim(state.y_min, state.y_max)

    if state.xscale != "log":
        ax.xaxis.set_major_locator(plt.MultipleLocator(
            0.1 * (state.x_max - state.x_min)))
        ax.xaxis.set_minor_locator(plt.MultipleLocator(
            0.01 * (state.x_max - state.x_min)))
    if state.yscale != "log":
        ax.yaxis.set_major_locator(plt.MultipleLocator(
            0.1 * (state.y_max - state.y_min)))
        ax.yaxis.set_minor_locator(plt.MultipleLocator(
            0.01 * (state.y_max - state.y_min)))

    # Set grid
    if state.grid:
        ax.grid(True, which="both", linewidth=0.5)
    if state.grid_major_thicker_x:
        ax.xaxis.grid(True, which='major', linestyle='-', linewidth=1.5)
    if state.grid_major_thicker_y:
        ax.yaxis.grid(True, which='major', linestyle='-', linewidth=1.5)

    # Removes axis tiks
    if not state.x_tiks_numbers:
        ax.set_xticklabels([])
    if not state.y_tiks_numbers:
        ax.set_yticklabels([])

    # Set labels
    ax.set_title(state.title)
    ax.set_xlabel(state.x_label)
    ax.set_ylabel(state.y_label)

    if state.img_format == "pdf":
        with PdfPages(filename) as pdf:
            pdf.savefig(fig)
            d = pdf.infodict()
            d['Title'] = state.title
            d['Creator'] = 'GraphPaperGen by Achille'
    else:
        plt.savefig(filename)
    plt.close()


def gp_sanitycheck(state: gp_state):
    try:
        if not (0 < state.height <= 100) or not (0 < state.width <= 100):
            return False

        if not (0 <= state.margin_left < 1) or not (0 <= state.margin_right < 1):
            return False
        if not (0 <= state.margin_top < 1) or not (0 <= state.margin_bottom < 1):
            return False

        if state.xscale not in ["linear", "log"] or state.yscale not in ["linear", "log"]:
            return False

        if not (state.x_min < state.x_max) or not (state.y_min < state.y_max):
            return False

        if not isinstance(state.grid, bool) or not isinstance(state.grid_major_thicker_x, bool):
            return False
        if not isinstance(state.grid_major_thicker_y, bool) or not isinstance(state.x_tiks_numbers, bool):
            return False
        if not isinstance(state.y_tiks_numbers, bool):
            return False

        if state.title is not None and not isinstance(state.title, str):
            return False
        if state.x_label is not None and not isinstance(state.x_label, str):
            return False
        if state.y_label is not None and not isinstance(state.y_label, str):
            return False

        if state.img_format not in ["png", "pdf"]:
            return False

        return True
    except Exception as e:
        print(f"Sanity check failed: {e}")
        return False


def sanitize_filename(filename: str) -> str:
    parts = filename.split('.')

    if len(parts) > 2:
        name = '_'.join(parts[:-1])
        extension = parts[-1]
    else:
        name = parts[0]
        extension = parts[1] if len(parts) == 2 else ''
    name = re.sub(r'[^a-zA-Z0-9_\-]', '', name)

    sanitized_filename = f"{name}.{extension}" if extension else name

    return sanitized_filename[:255]


test = gp_state()

test.height = 11.69
test.width = 8.27

test.margin_left = 0.05
test.margin_right = 0.95
test.margin_top = 0.95
test.margin_bottom = 0.05

test.xscale = "log"
test.yscale = "linear"

test.grid = True
test.grid_major_thicker_x = True
test.grid_major_thicker_y = True

test.x_min = 1
test.x_max = 10**6
test.y_min = 0
test.y_max = 10

test.title = "Title!"
test.x_label = "X LABEL []"
test.y_label = "Y LABEL []"

test.x_tiks_numbers = True
test.y_tiks_numbers = True

test.img_format = "pdf"


# gp_gen(test)
