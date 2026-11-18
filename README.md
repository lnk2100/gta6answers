# GTA6Answers.gg

A complete, responsive static fan website with 23 routes, 10 editable articles, section landing pages, live search and filters, native accessible FAQ disclosures, sources, editorial policy, privacy, custom 404, sitemap and per-page SEO metadata. Original SVG coastal artwork is decorative, not a game screenshot or map. No paid services, dependencies, API keys, npm or Node required.

## Run on a Mac

Install Python 3 from https://www.python.org/downloads/macos/ if `python3 --version` does not work. Unzip the download, open Terminal and change into the extracted folder (type `cd `, drag the GTA6Answers folder into Terminal, then press Return).

```sh
python3 scripts/build.py
python3 scripts/test.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory dist
```

Open http://localhost:4173 in Safari or Chrome. Stop the server with Control-C. Do not open HTML directly with file://: navigation and assets use root-relative URLs. If the port is busy, replace 4173 with 4174 in both places. The included `dist` is already built, so the server command alone previews the packaged version.

## Content and post-launch updates

- `content/site.json`: public origin, phase label, review date and primary sources.
- `content/articles.json`: reusable article records with slug, category, title, summary, status, optional source key, and paragraph array `body`.
- `scripts/build.py`: templates and category/FAQ/editorial content.
- `assets/style.css`, `assets/app.js`, `assets/coast.svg`: design, interactions, original art.
- `dist/`: generated deployable files; do not edit these directly.

Keep slugs stable. Categories: news, facts, guides, money, missions, vehicles, map. Statuses: Verified, Pre-release, Unconfirmed. Add primary source entries before referencing them. Escape handling is built into article rendering. Rebuild after edits.

This is a pre-release editorial snapshot checked 2026-11-18. The release date and platforms are sourced from Rockstar; regional unlock timing from Rockstar Support. No alleged New Zealand early access, mission names, money payouts, vehicle stats, leaked coordinates or PC release dates are invented. The site includes an official-headline feed; editorial release facts do not switch automatically. Sample guide pages intentionally explain what remains untested. A working map directory is included; a fictional interactive game map is not.

Before changing an entry to Verified, document the source or platform, patch, steps and test results. Add spoiler warnings to story content, revise all pre-release wording in the build templates, FAQ and article bodies, update dates and regenerate. The `phase` config records editorial intent; the initial edition text in templates must also be revised. Confirm current release status immediately before public deployment.

## Deploy

1. Choose your real domain. The current canonical origin is `https://boisterous-sawine-40cb61.netlify.app`; owning this source does not register that domain.
2. If using another domain, build with its origin:

```sh
SITE_URL=https://your-domain.example python3 scripts/build.py
python3 scripts/test.py
```

3. Upload the **contents of `dist/`** to your static host's web root. For Netlify manual deploy, drag the `dist` folder into its deploy upload area. For Cloudflare Pages direct upload, upload `dist` as the site assets. No server functions or SPA fallback are required. A host that serves directory `index.html` files is required; keep the site at the domain root, not a subdirectory.
4. Set the custom domain in your host and apply the exact DNS records it provides at your registrar. Enable HTTPS. No DNS changes or public publishing were performed by this project.
5. Verify `/`, `/search/?q=money`, `/articles/vice-city/`, `/faq/`, `/sitemap.xml`, `/robots.txt` and an unknown URL. Configure the host to serve `404.html` with an HTTP 404 status for unknown URLs (Python's preview server uses its own default error response).
6. Submit the sitemap to your search engine webmaster account. Review the privacy policy for the host's logging practices. Add a real corrections contact before opening public submissions; no nonfunctional contact form is included.

For a Git-connected host with Python installed, use `python3 scripts/build.py` as the build command and `dist` as the publish directory. GitHub Pages project subpaths are not supported without changing URL generation; use a root/custom-domain deployment.

## Validation

`python3 scripts/test.py` checks every generated internal link/asset, H1, main landmark, canonical and description, sitemap parsing, unique article slugs and verified-source presence. Manually check keyboard navigation, mobile menu, combined search filters, empty results and FAQ expansion in a browser. No analytics, remote images, external fonts, cookies or user accounts are used. Search is browser-local and persists filters in URL parameters.

## License and attribution

Original project code and decorative SVG artwork may be reused and modified by the recipient. GTA, GTA VI and related trademarks belong to their respective owners. No Rockstar assets are bundled. This website is unofficial and not endorsed by Rockstar Games or Take-Two Interactive.


## Cloud news updates

The `Update official news` GitHub Actions workflow checks Rockstar's official GTA VI page twice daily (07:23 and 19:23 UTC) and can also be run manually. It collects only linked official headlines, dates when present, and URLs. It does not research every announcement, watch Twitch, write AI articles, or change editorial facts automatically. Previously checked editorial content remains a dated snapshot.

The workflow commits `content/official-news.json` only when featured links change. Connect this repository's main branch to the existing Netlify site; `netlify.toml` supplies build and publish settings. Netlify deploys the changed commit. No API key or paid AI is required. Normal GitHub/Netlify quotas still apply; no paid upgrade is authorized.

If fetching or parsing fails, the prior feed stays intact and the workflow fails visibly in GitHub Actions. Last-change time is displayed on the site; it is not a claim that a check just ran. GitHub schedules may be delayed and public repository schedules may be disabled after 60 days without repository activity. Check Actions periodically and re-enable when needed. Test with Actions → Update official news → Run workflow after connecting Netlify.
