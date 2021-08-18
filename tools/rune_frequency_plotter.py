import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


def main():
    runebet = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
    partsDirectory = os.path.join(os.path.dirname(__file__), "../raw-data/")

    plt.rcParams["figure.figsize"] = [16, 9]
    plt.rcParams["figure.dpi"] = 160
    plt.rcParams["font.size"] = 20
    plt.rcParams["font.family"] = "Computer Modern Serif"
    plt.rcParams["mathtext.fontset"] = "custom"
    plt.rcParams["mathtext.rm"] = "Computer Modern Serif"
    plt.rcParams["mathtext.it"] = "Computer Modern Serif Italic"
    plt.rcParams['axes.unicode_minus'] = False

    fm.fontManager.ttflist.append(
        fm.FontEntry(fname="C:/Windows/Fonts/cmunrm.ttf", name="Computer Modern Serif"))
    fm.fontManager.ttflist.append(
        fm.FontEntry(fname="C:/Windows/Fonts/cmunti.ttf", name="Computer Modern Serif Italic"))
    # This font must support runic characters.
    fm.fontManager.ttflist.append(fm.FontEntry(
        fname="C:/Windows/Fonts/seguihis.ttf", name="Segoe UI Historic"))

    for part in os.listdir(partsDirectory):
        for i, sectionPath in enumerate(os.listdir(os.path.join(partsDirectory, part))):
            with open(os.path.join(partsDirectory, part, sectionPath), encoding='utf8') as sectionFile:
                stringData = "".join(sectionFile.readlines())
                frequencyData = {}
                for rune in runebet:
                    frequencyData[rune] = 0
                for char in stringData:
                    if char in frequencyData:
                        frequencyData[char] += 1

            # Force integral values on y-axis ticks.
            plt.figure().gca().yaxis.get_major_locator().set_params(integer=True)

            plt.gca().set_axisbelow(True)
            plt.gca().yaxis.set_minor_locator(MultipleLocator(1))
            plt.grid(True, which="both", alpha=0.4)

            plt.margins(x=0.02)

            plt.plot(sorted(frequencyData.values(), reverse=True))
            plt.scatter(sorted(frequencyData.keys(), key=lambda x: frequencyData[x], reverse=True),
                        sorted(frequencyData.values(), reverse=True))

            flatY = sum(frequencyData.values()) / len(frequencyData.values())
            plt.axhline(y=flatY, linestyle="--",
                        linewidth=2, color="orange", label=f"Uniformly distributed text, $y={round(flatY, 1)}$")
            # plt.annotate(, xy=(
            # 0, flatY), xytext=(len(frequencyData.values()) - 3, flatY + 0.5))

            plt.xticks(fontname="Segoe UI Historic")
            plt.gca().set_title(
                f"Rune frequencies in section {part}_{sectionPath.split('.')[0].zfill(2)}.txt, sorted from most to least common", pad=22)
            plt.ylabel(
                "Frequency")
            plt.tight_layout()

            plt.legend()

            plt.savefig(os.path.join(os.path.dirname(
                __file__), f"../docs/assets/images/LP/frequency-data/{part}/relative-rune-frequencies-{sectionPath.split('.')[0].zfill(2)}.png"))
            plt.clf()
            plt.cla()
            print(
                f"{i + 1}/{sum(len(os.listdir(os.path.join(partsDirectory, part))) for part in os.listdir(partsDirectory))} plots made and saved.", flush=True)


if __name__ == "__main__":
    main()
