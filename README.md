# Shut Up Fly website

The production site is https://shutupfly.timhudson.com/.
GitHub Pages serves this repository's `main` branch at `/`. This is a static
HTML/CSS site; the separate Next/Vinext marketing prototype is not production.
Preserve CNAME, `.nojekyll`, the official game logo, and the App Store badge.

## Search and download intent

- `/`: the official free iPhone arcade game, no ads or in-app purchases.
- `/offline-iphone-game/`: what works offline, connection limits, and setup.
- `/how-to-play/`: Fly Sense, infestation, four-hit combinations, and weapons.
- `/support/` and `/privacy/`: preserve the published support/privacy routes.

These pages describe the publicly released game, not a development candidate.
The September 6, 2026 US Apple lookup confirms version 1.2, free pricing,
iOS 18 minimum, and the official website. Release notes and review materials
support on-device single-player play; online Game Center rankings are optional.
Never describe development-only bosses or replay features as released.

Keep one canonical per page and update `sitemap.xml` when a substantive public
page changes. Preserve the Google verification tag on the homepage.
Use explicit iPhone/free/no-ads language where helpful, not keyword repetition.
No duplicate keyword landing pages, hidden links, purchased links, fabricated
reviews, or self-awarded “best game” claims. There are no analytics scripts or
third-party dependencies. The app schema intentionally has no frozen rating;
it describes the app but does not promise a Google software-app rich result.

## Validation and release

Run `python3 tools/check_site.py` and `git diff --check`. Preview with
`python3 -m http.server 4173 --bind 127.0.0.1`. Check new layouts at desktop and
iPhone widths, keyboard operation, local links, and the App Store destination.
Commit only task-owned files, push `main`, wait for the GitHub Pages build, and
verify the public HTML and sitemap after deployment.

Research snapshots, private acquisition metrics, and the growth project log
belong in gitignored `_local/`, never in the public site. The initial research
is `_local/seo-growth-project.md`. Search Console measurements and Apple
first-time downloads are separate: a website click is not a confirmed install.

## Evidence used for the initial search work

Research date: September 6, 2026. Google autocomplete, English with US country
hint, suggested free/no-ads/offline combinations across several seed phrases.
Autocomplete is a query-discovery signal, not a monthly-volume estimate.

[Google Trends comparison](https://trends.google.com/trends/explore?geo=US&q=best%20iphone%20games,free%20iphone%20games,offline%20iphone%20games,iphone%20games%20without%20ads,fun%20games%20for%20iphone&hl=en)
showed average relative interest 65 / 31 / 4 / 0 / 2, respectively, for US Web
Search over the displayed past 12 months. This is a normalized comparison,
not search counts; zero can reflect insufficient data. The no-ads wording is
prioritized for product fit and conversion, not claimed to have large measured
volume. Broad “best” searches commonly lead to multi-game editorial lists;
earning editorial consideration is a separate follow-up, never an invitation
to manufacture third-party endorsements.

Primary guidance: [Google people-first content](https://developers.google.com/search/docs/fundamentals/creating-helpful-content),
[Google title links](https://developers.google.com/search/docs/appearance/title-link),
[Google software-app schema](https://developers.google.com/search/docs/appearance/structured-data/software-app),
[Apple campaign links](https://developer.apple.com/help/app-store-connect-analytics/acquisition/campaign-links/),
and [Apple App Store search](https://developer.apple.com/app-store/search/).
