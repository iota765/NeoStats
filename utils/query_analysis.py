import re


LOOKUP_KEYWORDS = {
    "ceo",
    "ceoo",
    "founder",
    "cofounder",
    "chief executive",
    "headquarters",
    "headquarter",
    "revenue",
    "valuation",
    "market cap",
    "stock price",
    "share price",
    "employees",
    "employee count",
    "launched",
    "released",
    "roadmap",
    "acquired",
    "acquisition",
    "partnered",
    "partnership",
    "president",
    "prime minister",
    "net worth",
    "date",
    "founded",
    "born",
    "died",
    "address",
    "located",
    "current",
    "latest",
    "today",
    "recent",
    "recently",
}


def requires_external_lookup(question: str) -> bool:
    text = (question or "").strip()
    lowered = text.lower()

    if not lowered:
        return False

    if lowered.startswith(("who ", "who's ", "who is ", "when ", "where ")):
        return True

    if any(keyword in lowered for keyword in LOOKUP_KEYWORDS):
        return True

    if re.search(r"\b(19|20)\d{2}\b", lowered):
        return True

    if re.search(r"\b[a-z0-9._%+-]+\.com\b", lowered):
        return True

    if re.search(r"\b\d+(\.\d+)?%?\b", lowered):
        return True

    return False
