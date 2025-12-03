#!/usr/bin/env python3
import pandas as pd, re, argparse
from urllib.parse import urlparse
from pathlib import Path

SECCIONES = {
    'articles','business','politics','world','finance','economy','markets',
    'us-news','tech','health','sports','lifestyle','arts-culture','real-estate',
    'style','personal-finance','science','opinion'
}
SUBRUTAS = {
    'markets','economy','macroeconomics','policy','elections','china',
    'middle-east','europe','autos','retail','media','deals','tech','personal-tech',
    'cybersecurity','biotech','investing','banking','housing','healthcare','law',
    'national-security','courts','luxury-homes','commercial','fashion','design',
    'travel','relationships'
}
EXCLUDE_PAT = re.compile(r"/news/archive|/video/|/livecoverage|/podcast|/photos|/client/login|/subscribe|/newsletter|/audio|/market-data|/topics|/pro|/professional", re.IGNORECASE)


def path_parts(u: str):
    try:
        p = urlparse(u)
        return [x for x in p.path.split('/') if x]
    except Exception:
        return []


def s1(u: str):
    return bool(re.search(r"-\d+$", u))


def s2(u: str, seg: str):
    if EXCLUDE_PAT.search(u):
        return False
    return (seg in SECCIONES) and s1(u)


def s3(u: str, seg: str, last: str):
    if EXCLUDE_PAT.search(u) or seg not in SECCIONES:
        return False
    if s1(u):
        return True
    if (last.count('-') >= 2 and len(last) >= 15) or re.search(r"[?&]mod=", u):
        return True
    return False


def s4(u: str, seg: str, parts: list, last: str):
    if EXCLUDE_PAT.search(u) or seg not in SECCIONES:
        return False
    if s1(u):
        return True
    if (last.count('-') >= 2 and len(last) >= 15) or re.search(r"[?&](mod|st|share)=", u):
        return True
    if any(sr in parts[:-1] for sr in SUBRUTAS) and '-' in last:
        return True
    if '-' in last and len(parts) >= 3 and len(last) >= 12 and not re.search(r"^(index|video|photos|gallery)$", last):
        return True
    return False


def s5(u: str, seg: str, parts: list, last: str, title: str):
    if EXCLUDE_PAT.search(u) or seg not in SECCIONES:
        return False
    if s1(u):
        return True
    wc = len(str(title).split())
    if wc >= 4 and '-' in last and len(parts) >= 3:
        return True
    if re.search(r"[?&](mod|st|share)=", u):
        return True
    return False


STRATEGIES = {
    'S1_id_only': lambda r: s1(r['url']),
    'S2_sections_id': lambda r: s2(r['url'], r['seg']),
    'S3_slug_or_mod': lambda r: s3(r['url'], r['seg'], r['last']),
    'S4_subroutes_plus': lambda r: s4(r['url'], r['seg'], r['parts'], r['last']),
    'S5_title_depth': lambda r: s5(r['url'], r['seg'], r['parts'], r['last'], r.get('titulo', '')),
}


def main():
    ap = argparse.ArgumentParser(description='Evaluar estrategias de filtrado WSJ')
    ap.add_argument('--input', type=Path, default=Path('hipervinculos_wsj.csv'))
    ap.add_argument('--year-start', type=int, default=2016)
    ap.add_argument('--year-end', type=int, default=2025)
    args = ap.parse_args()

    df = pd.read_csv(args.input)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.dropna(subset=['fecha'])
    df['año'] = df['fecha'].dt.year
    df['url'] = df['url'].fillna('')
    df['parts'] = df['url'].apply(path_parts)
    df['seg'] = df['parts'].apply(lambda x: x[0] if x else '')
    df['last'] = df['parts'].apply(lambda x: x[-1] if x else '')

    orig_year = df.groupby('año').size()

    for name, fn in STRATEGIES.items():
        sel = df.apply(fn, axis=1)
        d = df[sel].copy()
        fil_year = d.groupby('año').size()
        print('\n' + '=' * 80)
        print(name)
        print(f"{'Año':<6}{'Original':>12}{'Filtrado':>12}{'%':>8}")
        for y in range(args.year_start, args.year_end + 1):
            o = int(orig_year.get(y, 0))
            f = int(fil_year.get(y, 0))
            pct = (f / o * 100) if o > 0 else 0
            marker = '✓' if (y >= 2023 and pct >= 80) else ('-' if y < 2023 else '⚠️')
            print(f"{y:<6}{o:>12,}{f:>12,}{pct:>8.2f} {marker}")
        print('Top segments:', d['seg'].value_counts().head(8).to_dict())


if __name__ == '__main__':
    main()
