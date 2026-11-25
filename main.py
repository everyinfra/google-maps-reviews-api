"""谷歌地图点评 API 示例（Google Maps Reviews API in Python）。

  python main.py search "coffee shop in Singapore" --out places.csv # 按关键词搜商户 / search places
  python main.py place "<地点链接>" --out place.json                # 商户资料 / place details
  python main.py reviews "<地点链接>" --out reviews.csv             # 商户评论 / reviews
  python main.py reviewer <reviewer_id> --out reviewer.csv          # 点评人的评论 / reviewer's reviews
"""
import argparse

from everyinfra import fetch, report

SORTS = ["newest", "relevance"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜商户 / search places by keyword")
    s.add_argument("keyword")
    pl = sub.add_parser("place", help="商户资料 / place details")
    pl.add_argument("url")
    r = sub.add_parser("reviews", help="商户评论 / reviews of one place")
    r.add_argument("url")
    r.add_argument("--sort", choices=SORTS, help="newest 最新 / relevance 相关度")
    re = sub.add_parser("reviewer", help="某位点评人写过的评论 / all reviews by one reviewer")
    re.add_argument("contributor")
    for x in (s, r):
        x.add_argument("--pages", type=int, default=1, help="最多翻几页，每页算一次调用 / max pages, one call each")
    for x in (s, pl, r, re):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        rows, charged = fetch("search", {"keyword": a.keyword}, a.pages)
    elif a.cmd == "place":
        rows, charged = fetch("profile", {"url": a.url})
    elif a.cmd == "reviews":
        params = {"url": a.url, **({"sort": a.sort} if a.sort else {})}
        rows, charged = fetch("reviews", params, a.pages)
    else:
        rows, charged = fetch("contributor_reviews", {"contributor": a.contributor})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
