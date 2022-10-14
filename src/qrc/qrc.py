import argparse
import sys
from pathlib import Path

import qrcode


def _parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("text")
    parser.add_argument("path", nargs="?", default="qrcode.png")

    parser.add_argument("-v", "--version", type=int, choices=range(1, 41), metavar="VERSION")
    parser.add_argument("-s", "--size", "--cell-size", type=int, default=10)
    parser.add_argument("-m", "--margin", "--quiet-zone", type=int, default=4)
    parser.add_argument("-e", "--error-correction", choices=["L", "M", "Q", "H"], default="M", metavar="LEVEL")

    parser.add_argument("-c", "--color", default="black")
    parser.add_argument("-b", "--background-color", default="white", metavar="COLOR")

    return parser.parse_args()


def main():

    args = _parse_args()

    # マージンの大きさをチェック
    if args.margin is not None and args.margin < 4:
        cmd = Path(sys.argv[0]).name
        print(f"{cmd}: warning: margin should be greater than or equal to 4", file=sys.stderr)

    # 誤り訂正レベル（デフォルト：M）
    if args.error_correction == "L":
        error_correction = qrcode.ERROR_CORRECT_L
    elif args.error_correction == "H":
        error_correction = qrcode.ERROR_CORRECT_H
    elif args.error_correction == "Q":
        error_correction = qrcode.ERROR_CORRECT_Q
    else:
        error_correction = qrcode.ERROR_CORRECT_M

    # QR コードを作成
    qr = qrcode.QRCode(version=args.version, error_correction=error_correction, box_size=args.size, border=args.margin)
    qr.add_data(args.text)
    qr.make(fit=True)

    # 画像としてファイルに保存
    img = qr.make_image(fill_color=args.color, back_color=args.background_color)
    img.save(args.path)


if __name__ == "__main__":
    main()
