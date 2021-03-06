import getopt
import json
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import (AutoMinorLocator, FixedLocator)


def analyse(runebet, frequencyData, stringData):
    for rune in runebet:
        frequencyData[rune] = 0
    for char in stringData:
        if char in frequencyData:
            frequencyData[char] += 1


def sorted_dict_by_frequency(dict, reversedSort=True):
    return {k: v for k, v in sorted(dict.items(),
                                    key=lambda x: dict[x[0]], reverse=reversedSort)}


def analyse_gutenberg_runic(path, runebet):
    with open(path, encoding="utf8") as book:
        stringData = "".join(
            [x for x in book.readlines() if not(x.startswith('#'))])
        frequencyData = {}
        analyse(runebet, frequencyData, stringData)
        print(sorted_dict_by_frequency(frequencyData))


def plot_frequencies(plt, dict, **extraArgs):
    plt.plot(sorted(dict.values(), reverse=True), **extraArgs)


def scatter_frequencies(plt, dict, **extraArgs):
    plt.scatter(sorted(dict.keys(), key=lambda x: dict[x], reverse=True), sorted(
        dict.values(), reverse=True), **extraArgs)


def write_section_plots(runebet):
    partsDirectoryContainerPath = os.path.join(
        os.path.dirname(__file__), "../raw-data/")

    plt.rcParams["figure.figsize"] = [16, 9]
    plt.rcParams["figure.dpi"] = 240
    plt.rcParams["font.size"] = 20
    plt.rcParams["font.family"] = "Computer Modern Serif"
    plt.rcParams["mathtext.fontset"] = "custom"
    plt.rcParams["mathtext.rm"] = "Computer Modern Serif"
    plt.rcParams["mathtext.it"] = "Computer Modern Serif Italic"
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['axes.xmargin'] = 0.02

    fm.fontManager.ttflist.append(
        fm.FontEntry(fname="C:/Windows/Fonts/cmunrm.ttf", name="Computer Modern Serif"))
    fm.fontManager.ttflist.append(
        fm.FontEntry(fname="C:/Windows/Fonts/cmunti.ttf", name="Computer Modern Serif Italic"))

    # This font must support runic characters.
    fm.fontManager.ttflist.append(fm.FontEntry(
        fname="C:/Windows/Fonts/seguihis.ttf", name="Segoe UI Historic"))

    raw_data = {}
    parts = next(os.walk(partsDirectoryContainerPath))[1]
    for part in parts:
        raw_data[part] = {}

        for i, section in enumerate(os.listdir(os.path.join(partsDirectoryContainerPath, part))):
            with open(os.path.join(partsDirectoryContainerPath, part, section), encoding='utf8') as sectionFile:
                stringData = "".join(sectionFile.readlines())
                actualFrequencies = {}
                analyse(runebet, actualFrequencies, stringData)

                raw_data[part][f"section-{section}"] = sorted_dict_by_frequency(
                    actualFrequencies)

            fig = plt.figure()

            axes = fig.add_subplot(111, label="1")
            helperAxes = fig.add_subplot(
                111, label="2", frame_on=False, sharey=axes)

            # Force integral values on y-axis ticks.
            axes.yaxis.get_major_locator().set_params(integer=True)

            helperAxes.set_axisbelow(True)
            axes.set_axisbelow(True)

            axes.xaxis.tick_bottom()
            axes.tick_params(axis="x")

            axes.yaxis.set_minor_locator(AutoMinorLocator())
            axes.grid(True, which="both", alpha=0.4)

            plot_frequencies(axes, actualFrequencies,
                             linewidth=2, label="Frequencies for this section", zorder=3)
            scatter_frequencies(
                axes, actualFrequencies, linewidth=2, zorder=3)

            naturalFrequencies = {'???': 4812, '???': 7765, '???': 7725, '???': 14961, '???': 11598, '???': 6525, '???': 2930, '???': 5539, '???': 5795, '???': 12774, '???': 12473, '???': 0, '???': 31, '???': 3774,
                                  '???': 231, '???': 13515, '???': 13891, '???': 2901, '???': 25366, '???': 5535, '???': 8730, '???': 2388, '???': 17, '???': 10340, '???': 15869, '???': 10, '???': 3919, '???': 657, '???': 1829}

            # Normalise by scaling the Gutenberg data to fit the section counts.
            normalisationConstant = sum(
                naturalFrequencies.values()) / sum(actualFrequencies.values())
            naturalFrequencies = {
                k: v / normalisationConstant for k, v in naturalFrequencies.items()}

            plot_frequencies(axes, naturalFrequencies, label="Natural frequencies for runic plaintext",
                             linestyle="--", linewidth=2, color="#7fbf7f", zorder=2)
            axes.scatter(range(len(naturalFrequencies.keys())), sorted(naturalFrequencies.values(), reverse=True),
                         color="#7fbf7f", zorder=2)

            # Show secondary axis ticks.
            scatter_frequencies(helperAxes, naturalFrequencies, alpha=0)

            flatY = sum(actualFrequencies.values()) / \
                len(actualFrequencies.values())
            axes.axhline(y=flatY, linestyle="--", linewidth=2, color="orange",
                         label=f"Uniformly distributed text ($y={round(flatY, 1)})$", alpha=0.5, zorder=1)

            helperAxes.xaxis.tick_bottom()

            # Shift ticks downwards
            helperAxes.tick_params(axis="x", direction="out", pad=30)

            for label in helperAxes.get_xticklabels():
                label.set_fontproperties(
                    fm.FontProperties(family="Segoe UI Historic", size=12))
                label.set_color("green")
            for label in axes.get_xticklabels():
                label.set_fontproperties(
                    fm.FontProperties(family="Segoe UI Historic"))

            plt.gca().set_title(
                f"Rune frequencies in section {part}_{section.split('.')[0].zfill(2)}.txt, sorted from most to least common", pad=22)
            plt.xlabel("Rune character")
            plt.ylabel("Frequency")
            plt.tight_layout()

            plt.figlegend(bbox_to_anchor=[0.98, 0.9], loc="upper right")

            plt.savefig(os.path.join(os.path.dirname(
                __file__), f"../docs/assets/images/LP/frequency-data/{part}/relative-rune-frequencies-section-{section.split('.')[0].zfill(2)}.png"))
            print(f"{i + 1}/{sum(len(os.listdir(os.path.join(partsDirectoryContainerPath, part))) for part in parts)} plots made and saved.", flush=True)
            plt.close()

    raw_path = os.path.join(os.path.dirname(
        __file__), f"../docs/assets/images/LP/frequency-data/raw-data.json")
    with open(raw_path, "w", encoding="utf8") as jsonWriteStream:
        json.dump(raw_data, jsonWriteStream,
                  ensure_ascii=False, indent=2)


def print_help():
    print("Usage:")
    print(r"rune_frequency_plotter.py (-h|--help|-g <gutenberg runic file path>|--gutenberg <gutenberg runic file path>)?")
    print("Entering Gutenberg mode and passing a file path analyses the text to find a \"natural\" distribution.")


def main(argv):
    opts = []
    try:
        opts, args = getopt.getopt(argv, "hg:", ["help", "gutenberg="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    runebet = "???????????????????????????????????????????????????????????????????????????????????????"
    for opt, arg in opts:
        if opt in ["-h", "--help"]:
            print_help()
            return
        elif opt in ["-g", "--gutenberg"]:
            analyse_gutenberg_runic(arg, runebet)
            return
    write_section_plots(runebet)


if __name__ == "__main__":
    main(sys.argv[1:])
