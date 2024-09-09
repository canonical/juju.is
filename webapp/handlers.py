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


def set_handlers(app):
    def get_csp_as_str(csp={}):
        csp_str = ""
        for key, values in csp.items():
            csp_value = " ".join(values)
            csp_str += f"{key} {csp_value}; "
        return csp_str.strip()

    @app.after_request
    def add_headers(response):
        response.headers["Content-Security-Policy"] = get_csp_as_str(CSP)
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "credentialless"
        response.headers["Cross-Origin-Opener-Policy"] = (
            "same-origin-allow-popups"
        )
        response.headers["Cross-Origin-Resource-Policy"] = "same-site"
        response.headers["X-Permitted-Cross-Domain-Policies"] = "none"
        return response
