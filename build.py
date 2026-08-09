# ITEMS_原稿.md の箇条書きを読んで items.json を作る。
# 使い方: python build.py
import base64
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "ITEMS_原稿.md")
OUT = os.path.join(HERE, "items.json")


def read_items(path):
    """「## リスト」以降の "- " 行だけを、書かれた順に拾う。"""
    items = []
    in_list = False
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith("## "):
                in_list = line.startswith("## リスト")
                continue
            if in_list and line.startswith("- "):
                items.append(line[2:].strip())
    return items


def main():
    items = read_items(SRC)
    if not items:
        raise SystemExit("項目が1つも読めなかった。ITEMS_原稿.md の「## リスト」節を確認して。")

    payload = json.dumps(items, ensure_ascii=False).encode("utf-8")
    b64 = base64.b64encode(payload).decode("ascii")

    with io.open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"itemsB64": b64}, f, ensure_ascii=False)
        f.write("\n")

    print("items.json を書きました: {} 項目".format(len(items)))
    for i, text in enumerate(items, 1):
        print("  その{:<3} {}".format(i, text))


if __name__ == "__main__":
    main()
