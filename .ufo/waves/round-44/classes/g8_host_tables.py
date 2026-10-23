"""G8: grammar-defective paths on hosts covered by the round-43 static tables.

Each source table contributes one malformed loc for each listed host. The
round-41 validator rejects these paths as non-absolute URLs; host-table
controls answer from their static entry and skip that grammar rejection.
"""

_TABLE_A_HOSTS = (
    "en.wikipedia.org",
    "de.wikipedia.org",
    "fr.wikipedia.org",
    "support.wikipedia.org",
    "commons.wikimedia.org",
    "www.wikimedia.org",
    "docs.python.org",
    "pypi.python.org",
    "peps.python.org",
    "news.ycombinator.com",
    "stackoverflow.com",
    "www.stackexchange.com",
    "code.visualstudio.com",
    "docs.github.com",
    "gist.github.com",
    "docs.docker.com",
    "hub.docker.com",
    "www.kubernetes.io",
    "www.grafana.com",
    "www.elastic.co",
    "developer.android.com",
    "developer.apple.com",
    "support.apple.com",
    "developer.chrome.com",
    "www.mozilla.org",
    "support.mozilla.org",
    "blog.mozilla.org",
    "security.debian.org",
    "archive.ubuntu.com",
    "www.rust-lang.org",
    "www.typescriptlang.org",
    "cdnjs.cloudflare.com",
    "registry.npmjs.org",
    "www.rubyonrails.org",
    "www.laravel.com",
    "www.symfony.com",
    "www.djangoproject.com",
    "www.jetbrains.com",
    "www.w3schools.com",
    "www.geeksforgeeks.org",
    "www.tutorialspoint.com",
    "www.freecodecamp.org",
    "docs.microsoft.com",
    "learn.microsoft.com",
    "www.oracle.com",
    "cloud.google.com",
)

_TABLE_B_HOSTS = (
    "en.wikipedia.org",
    "de.wikipedia.org",
    "fr.wikipedia.org",
    "support.wikipedia.org",
    "commons.wikimedia.org",
    "www.wikimedia.org",
    "docs.python.org",
    "pypi.python.org",
    "peps.python.org",
    "news.ycombinator.com",
    "stackoverflow.com",
    "www.stackexchange.com",
    "code.visualstudio.com",
    "docs.github.com",
    "gist.github.com",
    "docs.docker.com",
    "hub.docker.com",
    "www.kubernetes.io",
    "www.grafana.com",
    "www.elastic.co",
    "developer.android.com",
    "developer.apple.com",
    "support.apple.com",
    "developer.chrome.com",
    "www.mozilla.org",
    "support.mozilla.org",
    "blog.mozilla.org",
    "security.debian.org",
    "archive.ubuntu.com",
    "www.rust-lang.org",
    "www.typescriptlang.org",
    "cdnjs.cloudflare.com",
    "registry.npmjs.org",
    "www.rubyonrails.org",
    "www.laravel.com",
    "www.symfony.com",
    "www.djangoproject.com",
    "www.jetbrains.com",
    "www.w3schools.com",
    "www.geeksforgeeks.org",
    "www.tutorialspoint.com",
    "www.freecodecamp.org",
    "docs.microsoft.com",
    "learn.microsoft.com",
    "www.oracle.com",
    "cloud.google.com",
)

_TABLE_F_HOSTS = (
    "en.wikipedia.org",
    "de.wikipedia.org",
    "fr.wikipedia.org",
    "support.wikipedia.org",
    "commons.wikimedia.org",
    "www.wikimedia.org",
    "news.ycombinator.com",
    "stackoverflow.com",
    "www.stackexchange.com",
    "code.visualstudio.com",
    "www.kubernetes.io",
    "www.elastic.co",
    "developer.android.com",
    "developer.apple.com",
    "support.apple.com",
    "developer.chrome.com",
    "support.mozilla.org",
    "blog.mozilla.org",
    "security.debian.org",
    "archive.ubuntu.com",
    "www.rust-lang.org",
    "www.typescriptlang.org",
    "cdnjs.cloudflare.com",
    "registry.npmjs.org",
    "www.rubyonrails.org",
    "www.djangoproject.com",
    "www.jetbrains.com",
    "www.w3schools.com",
    "www.geeksforgeeks.org",
    "www.tutorialspoint.com",
    "www.freecodecamp.org",
    "docs.microsoft.com",
    "learn.microsoft.com",
    "cloud.google.com",
)

_TABLES = (_TABLE_A_HOSTS, _TABLE_B_HOSTS, _TABLE_F_HOSTS)
_PATH_DEFECTS = ("%", "|", " ", "<", ">")


def cases(rng, h):
    units = []
    defect_offset = rng.randrange(len(_PATH_DEFECTS))
    index = 0
    for hosts in _TABLES:
        for host in hosts:
            defect = _PATH_DEFECTS[(defect_offset + index) % len(_PATH_DEFECTS)]
            value = "https://%s/entry%spath/check.xml" % (host, defect)
            units.append(("value", "loc", value))
            index += 1
    return units, len(units)
