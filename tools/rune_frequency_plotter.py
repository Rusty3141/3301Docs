import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


def main():
    runebet = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
    partsDirectory = "raw-data/"

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

            fm.fontManager.ttflist.append(
                fm.FontEntry(fname="C:/Windows/Fonts/cmunrm.ttf", name="Computer Modern Serif"))

            plt.rcParams["figure.figsize"] = [16, 9]
            plt.rcParams["figure.dpi"] = 240
            plt.rcParams["font.size"] = 20
            plt.rcParams["font.family"] = "Computer Modern Serif"
            plt.rcParams['axes.unicode_minus'] = False
            plt.plot(sorted(frequencyData.values(), reverse=True))
            plt.title(
                f"Rune frequencies in section {part}-{sectionPath.split('.')[0].zfill(2)}, sorted from most to least common")
            plt.ylabel(
                "Rune occurrences in section")
            plt.tight_layout()
            # plt.subplots_adjust(top=0.72)
            plt.savefig(
                f"docs/assets/images/LP/frequency-data/{part}/relative-rune-frequencies-{sectionPath.split('.')[0].zfill(2)}.png")
            plt.clf()
            plt.cla()
            print(
                f"{i + 1}/{sum(len(os.listdir(os.path.join(partsDirectory, part))) for part in os.listdir(partsDirectory))} plots made and saved.", flush=True)


if __name__ == "__main__":
    main()
