from flask import Blueprint, jsonify
import random
import colorsys
import re

color_api = Blueprint("color_api", __name__, url_prefix="/api/color")


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")

    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)

    if not re.fullmatch(r"[0-9a-fA-F]{6}", hex_color):
        raise ValueError("Invalid HEX color")

    return tuple(
        int(hex_color[i:i + 2], 16)
        for i in (0, 2, 4)
    )


def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def rgb_to_hsl(r, g, b):
    r /= 255
    g /= 255
    b /= 255

    h, l, s = colorsys.rgb_to_hls(r, g, b)

    return {
        "h": round(h * 360, 2),
        "s": round(s * 100, 2),
        "l": round(l * 100, 2)
    }


@color_api.route("/<hex_color>")
def get_color(hex_color):
    try:
        rgb = hex_to_rgb(hex_color)

        return jsonify({
            "hex": rgb_to_hex(rgb),
            "rgb": {
                "r": rgb[0],
                "g": rgb[1],
                "b": rgb[2]
            },
            "hsl": rgb_to_hsl(*rgb)
        })

    except ValueError:
        return jsonify({
            "error": "Invalid HEX color",
            "example": "/api/color/FF5733"
        }), 400


@color_api.route("/random")
def random_color():
    rgb = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

    return jsonify({
        "hex": rgb_to_hex(rgb),
        "rgb": {
            "r": rgb[0],
            "g": rgb[1],
            "b": rgb[2]
        }
    })


@color_api.route("/palette/<hex_color>")
def color_palette(hex_color):
    try:
        rgb = hex_to_rgb(hex_color)

        r, g, b = [x / 255 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)

        palette = []

        for rotation in [-60, -30, 0, 30, 60]:
            new_h = (h + rotation / 360) % 1

            nr, ng, nb = colorsys.hls_to_rgb(
                new_h,
                l,
                s
            )

            palette.append(
                rgb_to_hex((
                    round(nr * 255),
                    round(ng * 255),
                    round(nb * 255)
                ))
            )

        return jsonify({
            "base": rgb_to_hex(rgb),
            "palette": palette
        })

    except ValueError:
        return jsonify({
            "error": "Invalid HEX color",
            "example": "/api/color/palette/FF5733"
        }), 400


@color_api.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "Color API"
    })
