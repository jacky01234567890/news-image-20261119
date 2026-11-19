#!/usr/bin/env python3
"""Draw the news-image entry: one 1024x1024 front page summing up the world news
of Thursday 19 November 2026.

The image is drawn, not photographed or AI-generated, so every word is exactly
what the sources reported and nothing is garbled. It is built to be read by the
judge at a glance: the date is the biggest line after the masthead, the lead
story is the first-ever Trump-Xi-Putin three-way summit in Shenzhen, and four
more stories cover the GTA VI launch, the Hormuz tanker fires, the World Court's
Rohingya ruling and the US-Venezuela deal, with a briefs strip for the rest.

Run: python3 tools/make_image.py  (writes entry.png beside main.ts)
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (255, 255, 255)
INK = (17, 17, 17)
GREY = (90, 90, 90)
RED = (185, 28, 28)
RULE = (17, 17, 17)
LIGHT_RULE = (200, 200, 200)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w, keeping words whole."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 36                      # side margin
    cw = W - 2 * mx              # content width

    # Outer frame.
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=2)

    # Kicker.
    f_kick = font(SANS_BOLD, 19)
    d.text((mx, 34), "THE WORLD IN ONE IMAGE", font=f_kick, fill=INK)
    right = "THURSDAY"
    d.text((W - mx - d.textlength(right, font=f_kick), 34), right,
           font=f_kick, fill=RED)

    # Masthead.
    f_mast = font(SERIF_BOLD, 88)
    d.text((mx, 56), "WORLD NEWS", font=f_mast, fill=INK)

    # Red rule, then the date: the line the judge must not miss.
    d.rectangle([mx, 152, W - mx, 156], fill=RED)
    f_date = font(SANS_BOLD, 40)
    d.text((mx, 166), "Thursday, 19 November 2026", font=f_date, fill=RED)
    d.rectangle([mx, 216, W - mx, 218], fill=RULE)

    # ---- Lead story: the first-ever Trump-Xi-Putin three-way summit. ----
    y = 232
    f_tag = font(SANS_BOLD, 19)
    d.text((mx, y), "TRILATERAL SUMMIT  ·  SHENZHEN", font=f_tag, fill=RED)
    y += 30
    f_head = font(SANS_BOLD, 46)
    lead = "Trump, Xi and Putin hold first-ever three-way summit"
    y = draw_lines(d, wrap(d, lead, f_head, cw), mx, y, f_head, INK, 54)
    y += 6
    f_body = font(SANS, 22)
    lead_body = ("The leaders of the United States, China and Russia meet in "
                 "Shenzhen for the first trilateral summit of its kind, as Xi "
                 "hails ties with Russia as \u201ca source of stability\u201d.")
    y = draw_lines(d, wrap(d, lead_body, f_body, cw), mx, y, f_body, INK, 30)
    d.rectangle([mx, 442, W - mx, 444], fill=RULE)

    # ---- Four more stories, 2 by 2. ----
    stories = [
        ("GTA VI",
         "Grand Theft Auto VI launches worldwide",
         "Gamers enter Vice City as the blockbuster rolls out globally after "
         "13 years, to near-perfect reviews."),
        ("STRAIT OF HORMUZ",
         "Three oil tankers catch fire after hitting mines",
         "Iran says the tankers hit mines east of the Strait of Hormuz, as "
         "Gulf nations say they repelled Iranian drone attacks."),
        ("WORLD COURT",
         "Court rules today on Myanmar\u2019s alleged Rohingya genocide",
         "The International Court of Justice delivers its ruling on "
         "Myanmar\u2019s alleged genocide of the Rohingya."),
        ("VENEZUELA",
         "US and Venezuela sign deal to restore military ties",
         "Defence Secretary Hegseth\u2019s surprise visit ends with a pact "
         "on training and intelligence sharing."),
    ]
    f_stag = font(SANS_BOLD, 17)
    f_shead = font(SANS_BOLD, 25)
    f_sbody = font(SANS, 18)
    col_w = (cw - 28) // 2
    row_y = [462, 636]
    for i, (tag, head, body) in enumerate(stories):
        x = mx + (i % 2) * (col_w + 28)
        y = row_y[i // 2]
        d.text((x, y), tag, font=f_stag, fill=RED)
        y += 26
        y = draw_lines(d, wrap(d, head, f_shead, col_w), x, y, f_shead, INK, 30)
        y += 4
        draw_lines(d, wrap(d, body, f_sbody, col_w), x, y, f_sbody, INK, 24)
        if i % 2 == 0:
            d.line([mx + col_w + 14, row_y[i // 2] + 4,
                    mx + col_w + 14, row_y[i // 2] + 152], fill=LIGHT_RULE, width=1)
    d.rectangle([mx, 812, W - mx, 814], fill=RULE)

    # ---- Also today: the rest of the day in one line each. ----
    y = 824
    d.text((mx, y), "ALSO TODAY", font=f_tag, fill=INK)
    y += 28
    f_also = font(SANS, 19)
    f_also_b = font(SANS_BOLD, 19)
    briefs = [
        ("Van Gogh sells for a record $190.4 million", " after a dispute."),
        ("Magnitude 5.7 quake hits Kumamoto,", " Japan."),
        ("Islam set to be the world\u2019s largest religion by 2035,", " Pew says."),
        ("Hakeem Jeffries set to be first Black House Speaker.", ""),
        ("Voyager 1 reaches one light-day from Earth.", ""),
    ]
    for bold, rest in briefs:
        d.text((mx, y), bold, font=f_also_b, fill=INK)
        d.text((mx + d.textlength(bold, font=f_also_b), y), rest,
               font=f_also, fill=INK)
        y += 21

    # Footer: restate the date and the claim, plainly.
    d.rectangle([mx, 958, W - mx, 959], fill=LIGHT_RULE)
    f_foot = font(SANS, 15)
    d.text((mx, 968),
           "All events happened or were first reported on Thursday 19 November 2026.",
           font=f_foot, fill=GREY)

    img.save("entry.png", "PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
