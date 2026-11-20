import argparse, asyncio
from .workflow import recommend

def main():
    p = argparse.ArgumentParser(description="Literary Agent — Top 5 book recommendations")
    p.add_argument("inquiry", nargs="*")
    p.add_argument("--level", default="Any")
    p.add_argument("--language", default="Any")
    p.add_argument("--length", default="Any")
    p.add_argument("--exclude", default="")
    a = p.parse_args()
    q = " ".join(a.inquiry).strip() or input("What would you like to read? ")
    print(asyncio.run(recommend(q, a.level, a.language, a.length, a.exclude)))

if __name__ == "__main__":
    main()
