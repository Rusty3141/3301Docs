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


def analyse_gutenberg_runic(path, runebet):
    with open(path, encoding="utf8") as book:
        stringData = "".join(
            [x for x in book.readlines() if not(x.startswith('#'))])
        frequencyData = {}
        analyse(runebet, frequencyData, stringData)
        print(frequencyData)


def plot_frequencies(plt, dict, **extraArgs):
    plt.plot(sorted(dict.values(), reverse=True), **extraArgs)


def scatter_frequencies(plt, dict, **extraArgs):
    plt.scatter(sorted(dict.keys(), key=lambda x: dict[x], reverse=True), sorted(
        dict.values(), reverse=True), **extraArgs)


def write_section_plots(runebet):
    partsDirectory = os.path.join(os.path.dirname(__file__), "../raw-data/")

    plt.rcParams["figure.figsize"] = [16, 9]
    plt.rcParams["figure.dpi"] = 160
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

    parts = next(os.walk(partsDirectory))[1]
    for part in parts:
        for i, sectionPath in enumerate(os.listdir(os.path.join(partsDirectory, part))):
            with open(os.path.join(partsDirectory, part, sectionPath), encoding='utf8') as sectionFile:
                stringData = "".join(sectionFile.readlines())
                actualFrequencies = {}
                analyse(runebet, actualFrequencies, stringData)
                raw_path = os.path.join(os.path.dirname(
                    __file__), f"../docs/assets/images/LP/frequency-data/{part}/raw-data/relative-rune-frequencies-section-{sectionPath.split('.')[0].zfill(2)}.json")
                with open(raw_path, "w", encoding="utf8") as jsonWriteStream:
                    json.dump(actualFrequencies, jsonWriteStream,
                              ensure_ascii=False, indent=4)

            fig = plt.figure()

            actualAxes = fig.add_subplot(111, label="1")
            idealAxes = fig.add_subplot(
                111, label="2", frame_on=False, sharey=actualAxes)

            # Force integral values on y-axis ticks.
            actualAxes.yaxis.get_major_locator().set_params(integer=True)

            idealAxes.set_axisbelow(True)
            actualAxes.set_axisbelow(True)

            actualAxes.xaxis.tick_bottom()
            actualAxes.tick_params(axis="x")

            actualAxes.yaxis.set_minor_locator(AutoMinorLocator())
            actualAxes.grid(True, which="both", alpha=0.4)

            plot_frequencies(actualAxes, actualFrequencies,
                             linewidth=2, label="Frequencies for this section")
            scatter_frequencies(
                actualAxes, actualFrequencies, linewidth=2)

            flatY = sum(actualFrequencies.values()) / \
                len(actualFrequencies.values())
            idealAxes.axhline(y=flatY, linestyle="--", linewidth=2, color="orange",
                              label=f"Uniformly distributed text ($y={round(flatY, 1)})$", alpha=0.5)

            naturalFrequencies = {'ᚠ': 4812, 'ᚢ': 7765, 'ᚦ': 7725, 'ᚩ': 14961, 'ᚱ': 11598, 'ᚳ': 6525, 'ᚷ': 2930, 'ᚹ': 5539, 'ᚻ': 5795, 'ᚾ': 12774, 'ᛁ': 12473, 'ᛄ': 0, 'ᛇ': 31, 'ᛈ': 3774,
                                  'ᛉ': 231, 'ᛋ': 13515, 'ᛏ': 13891, 'ᛒ': 2901, 'ᛖ': 25366, 'ᛗ': 5535, 'ᛚ': 8730, 'ᛝ': 2388, 'ᛟ': 17, 'ᛞ': 10340, 'ᚪ': 15869, 'ᚫ': 10, 'ᚣ': 3919, 'ᛡ': 657, 'ᛠ': 1829}

            # Normalise by scaling the Gutenberg data to fit the section counts.
            normalisationConstant = sum(
                naturalFrequencies.values()) / sum(actualFrequencies.values())
            naturalFrequencies = {
                k: v / normalisationConstant for k, v in naturalFrequencies.items()}

            plot_frequencies(idealAxes, naturalFrequencies, label="Natural frequencies for runic plaintext",
                             linestyle="--", linewidth=2, color="green")
            scatter_frequencies(idealAxes, naturalFrequencies, color="green")
            idealAxes.xaxis.tick_bottom()
            idealAxes.tick_params(axis="x", colors="green")

            # Shift ticks downwards
            idealAxes.tick_params(axis="x", direction="in", pad=30)

            for label in idealAxes.get_xticklabels():
                label.set_fontproperties(
                    fm.FontProperties(family="Segoe UI Historic", size=12))
            for label in actualAxes.get_xticklabels():
                label.set_fontproperties(
                    fm.FontProperties(family="Segoe UI Historic"))

            plt.gca().set_title(
                f"Rune frequencies in section {part}_{sectionPath.split('.')[0].zfill(2)}.txt, sorted from most to least common", pad=22)
            plt.xlabel("Rune character")
            plt.ylabel("Frequency")
            plt.tight_layout()

            plt.figlegend(bbox_to_anchor=[0.98, 0.9], loc="upper right")

            plt.savefig(os.path.join(os.path.dirname(
                __file__), f"../docs/assets/images/LP/frequency-data/{part}/relative-rune-frequencies-section-{sectionPath.split('.')[0].zfill(2)}.png"))
            print(f"{i + 1}/{sum(len(os.listdir(os.path.join(partsDirectory, part))) for part in parts)} plots made and saved.", flush=True)
            plt.close()


def print_help():
    print("Usage:")
    print(r"    rune_frequency_plotter.py (-h|--help|-g <gutenberg runic file path>|--gutenberg <gutenberg runic file path>)?")
    print("    Entering gutenberg mode and passing a file path analyses the text to find a \"natural\" distribution.")


def main(argv):
    opts = []
    try:
        opts, args = getopt.getopt(argv, "hg:", ["help", "gutenberg="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    runebet = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
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
