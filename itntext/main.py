import argparse

from itntext import Normalizer
from itntext.fst_processor import ALL_LANGUAGES, ITN_LANGUAGES, TN_LANGUAGES
from itntext.utils import str2bool


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="input string")
    parser.add_argument("--text", help="input string")
    parser.add_argument("--file", help="input file path")
    parser.add_argument(
        "--lang", "-l", "--language", dest="language", type=str, default="zh",
        choices=ALL_LANGUAGES,
        help="语言。ITN: " + ",".join(ITN_LANGUAGES) + "；TN: " + ",".join(TN_LANGUAGES),
    )
    parser.add_argument("--operator", "-o", type=str, default="tn", choices=["tn", "itn"])
    parser.add_argument("--remove_interjections", type=str, default="False")
    parser.add_argument("--remove_erhua", type=str, default="False")
    parser.add_argument("--traditional_to_simple", type=str, default="False")
    parser.add_argument("--remove_puncts", type=str, default="False")
    parser.add_argument("--full_to_half", type=str, default="False")
    parser.add_argument("--tag_oov", type=str, default="False")
    parser.add_argument("--enable_0_to_9", type=str, default="False")
    args = parser.parse_args()

    normalizer = Normalizer(
        lang=args.language,
        operator=args.operator,
        remove_interjections=str2bool(args.remove_interjections),
        remove_erhua=str2bool(args.remove_erhua),
        traditional_to_simple=str2bool(args.traditional_to_simple),
        remove_puncts=str2bool(args.remove_puncts),
        full_to_half=str2bool(args.full_to_half),
        tag_oov=str2bool(args.tag_oov),
        enable_0_to_9=str2bool(args.enable_0_to_9),
    )

    text = args.text or args.input
    if text:
        print(normalizer.normalize(text))
    elif args.file:
        with open(args.file, encoding="utf-8") as fin:
            for line in fin:
                print(normalizer.normalize(line.strip()))


if __name__ == "__main__":
    main()
