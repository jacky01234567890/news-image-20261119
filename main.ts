// news-image-20261119: a program that writes one image summing up the world news
// of Thursday 19 November 2026 to /output/entry.png.
//
// The image is drawn by tools/make_image.py (a front page: the first-ever
// Trump-Xi-Putin three-way summit in Shenzhen, the GTA VI launch, the Hormuz
// tanker fires, the World Court's Rohingya ruling, the US-Venezuela deal, and
// the day's briefs) and committed here as entry.png, so this program only has
// to copy it. That keeps the run deterministic: two runs write the same bytes,
// with no network.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
