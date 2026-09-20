# Sources — extracted snapshots, 2026-09-20

Everything here was fetched on **2026-09-20 (UTC)** through
`https://api.rv.pkgforge.dev/<url>`. The write-up cites these files, not the live
Electrosphere, because the provider pages move.

```
sites/     landing-page text extracts                     (26 .txt + index.json)
pricing/   pricing / plan / docs text extracts            (31 .txt)
configs/   window.__APP_CONFIG__ per sub2api instance     (7 .json)
```

- `sites/index.json` — per provider: advertised URL, HTTP status, byte count, TTFB, page
  title, whether the page carried a sub2api `__APP_CONFIG__`, and the public flags
  (registration / payment / subscription / available channels / model plaza / affiliate /
  risk control) plus custom API endpoints.
- `*.txt` — visible text with `<script>`/`<style>` removed and whitespace collapsed. This is
  the artifact a citation quotes. The raw HTML was **not** committed: it republished each
  vendor's whole minified bundle for no extra evidence, and tripped two runs of the
  repository's `check-no-secrets.sh --public` on unrelated content (see below).
- `configs/*.json` — the full public settings object the panel serves to anonymous visitors,
  which is where the ToS, SLA figure, custom endpoints and feature flags live.

## Redactions (the only edits made to captured content)

Two placeholder credentials and all contact emails / home paths / 24+ hex asset ids were
redacted so the repository's secret and public-fingerprint scans are clean:

- `sites/Bestproxy.txt`, `sites/RapidProxy.txt` — vendor documentation examples of the form
  `http://USER:PASS@host` were replaced with `://REDACTED_AUTH@`. They were placeholders
  (`username_custom_zone_US`, literally `password`), not live credentials, but the shape is
  what the scanner exists to catch.
- `*.txt`, `*.json` — `<email-redacted>`, `<home-redacted>`, `<hash-redacted>` for vendor
  contact addresses, developer home paths and asset hashes. These are public page content,
  not secrets; redacting them keeps `--public` meaningful.

Nothing else in the snapshots was altered. `check-no-secrets.sh` (default rules) reports zero
findings on this pass; `--public` reports zero on this pass (the two remaining findings in
the repository are pre-existing in the 2026-09-13 pass).

## Re-fetching

The instruments are committed and take the same inputs they took originally:

```sh
python3 tools/fetch-sources.py     2026-09-20   # landing pages -> sites/ + index.json
python3 tools/fetch-pages.py       2026-09-20   # pricing/docs  -> pricing/
python3 tools/probe-uptime.py      2026-09-20 3 # 3-round reachability -> data/
python3 tools/extract-snapshots.py 2026-09-20   # html -> .txt + configs/ (then remove html)
```

All three fetchers route through the pkgforge reverse proxy so the capture is reproducible
from a host that cannot reach the sites directly. Re-running them next week measures a
different site; the pass-directory date is the pin.

## What is NOT here

- The **subject tree and tracker** (`references/Wei-Shaw__sub2api/`, 7,290 issues/PRs) are
  kept outside this pass. Re-create with:
  `sh scripts/common/mine-repo.sh Wei-Shaw/sub2api --out references`
  It resolved to commit `19794bc46afb` on 2026-09-20; a later run captures a different commit,
  which is why every citation names the commit.
- Login-gated pages (dashboard pricing, model marketplaces after auth). Nothing behind a login
  was read, and no credentials were used.
- `Swiftproxy` pricing — HTTP 403 on both routes (recorded `UNKNOWN`, not "down").
- `ETok` model pages (404) and the `APIKEY.FUN` / `PP.dog` / `Nagora` / `PPToken` docs
  subdomains (530) — the landing pages are what answered.
