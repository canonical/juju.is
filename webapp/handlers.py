import base64
import hashlib
import re

CSP = {
    "default-src": ["'self'"],
    "script-src-elem": [
        "'self'",
        "assets.ubuntu.com",
        "buttons.github.io",
        "www.googletagmanager.com",
        # This is necessary for Google Tag Manager to function properly.
        "'unsafe-inline'",
    ],
    "img-src": [
        "data: blob:",
        # This is needed to allow images from
        # https://www.google.*/ads/ga-audiences to load.
        "*",
    ],
    "font-src": [
        "'self'",
        "assets.ubuntu.com",
    ],
    "style-src": [
        "'self'",
        "'unsafe-inline'",
    ],
    "frame-src": [
        "'self'",
        "td.doubleclick.net",
        "www.youtube.com",
        "*",
    ],
    "connect-src": [
        "'self'",
        "analytics.google.com",
        "stats.g.doubleclick.net",
        "www.googletagmanager.com",
        "sentry.is.canonical.com",
        "www.google-analytics.com",
        "*.crazyegg.com",
    ],
}

CSP_SCRIPT_SRC = [
    "'self'",
    "blob:",
    "'unsafe-eval'",
    "'unsafe-hashes'",
]


def set_handlers(app):
    def get_csp_as_str(csp={}):
        csp_str = ""
        for key, values in csp.items():
            csp_value = " ".join(values)
            csp_str += f"{key} {csp_value}; "
        return csp_str.strip()

    # Calculate the SHA256 hash of the script content and encode it in base64.
    def calculate_sha256_base64(script_content):
        sha256_hash = hashlib.sha256(script_content.encode()).digest()
        return "sha256-" + base64.b64encode(sha256_hash).decode()

    def get_csp_directive(content, regex):
        directive_items = set()
        pattern = re.compile(regex)
        matched_contents = pattern.findall(content)
        for matched_content in matched_contents:
            hash_value = f"'{calculate_sha256_base64(matched_content)}'"
            directive_items.add(hash_value)
        return list(directive_items)

    # Find all script elements in the response and add their hashes to the CSP.
    def add_script_hashes_to_csp(response):
        response.freeze()
        decoded_content = b"".join(response.response).decode(
            "utf-8", errors="replace"
        )

        CSP["script-src"] = CSP_SCRIPT_SRC + get_csp_directive(
            decoded_content, r'onclick\s*=\s*"(.*?)"'
        )
        return CSP

    @app.after_request
    def add_headers(response):
        csp = add_script_hashes_to_csp(response)
        response.headers["Content-Security-Policy"] = get_csp_as_str(csp)
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "unsafe-none"
        response.headers["Cross-Origin-Opener-Policy"] = (
            "same-origin-allow-popups"
        )
        response.headers["Cross-Origin-Resource-Policy"] = "same-site"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        return response
