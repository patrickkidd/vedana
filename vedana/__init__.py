import sys
import hashlib, hmac, base64

IS_TEST = "pytest" in sys.modules

ACCESS_READ_ONLY = "ro"
ACCESS_READ_WRITE = "rw"

ROLE_ADMIN = "admin"
ROLE_SUBSCRIBER = "subscriber"
ROLE_AUDITOR = "auditor"

LICENSE_FREE = "com.vedanamedia.familydiagram.free"
LICENSE_BETA = "com.vedanamedia.familydiagram.beta"
LICENSE_ALPHA = "com.vedanamedia.familydiagram.alpha"
LICENSE_CLIENT = "com.vedanamedia.familydiagram.client"
LICENSE_CLIENT_ONCE = "com.vedanamedia.familydiagram.client.once"
LICENSE_PROFESSIONAL = "com.vedanamedia.familydiagram.professional"
LICENSE_PROFESSIONAL_MONTHLY = "com.vedanamedia.familydiagram.professional.monthly"
LICENSE_PROFESSIONAL_ANNUAL = "com.vedanamedia.familydiagram.professional.annual"
LICENSE_RESEARCHER = "com.vedanamedia.familydiagram.researcher"
LICENSE_RESEARCHER_MONTHLY = "com.vedanamedia.familydiagram.researcher.monthly"
LICENSE_RESEARCHER_ANNUAL = "com.vedanamedia.familydiagram.researcher.annual"
LICENSES = (
    LICENSE_FREE,
    LICENSE_BETA,
    LICENSE_ALPHA,
    LICENSE_CLIENT_ONCE,
    LICENSE_PROFESSIONAL_MONTHLY,
    LICENSE_PROFESSIONAL_ANNUAL,
    LICENSE_RESEARCHER_MONTHLY,
    LICENSE_RESEARCHER_ANNUAL,
)
LICENSES_FEATURES = (
    LICENSE_FREE,
    LICENSE_BETA,
    LICENSE_ALPHA,
    LICENSE_CLIENT,
    LICENSE_PROFESSIONAL,
    LICENSE_RESEARCHER_ANNUAL,
)


def any_license_match(x, y):
    for _x in x:
        for _y in y:
            if _x.startswith(_y):
                return True
    return False


def licenses_features(licenses):
    if not licenses:
        return []
    ret = set()
    for x in licenses:
        for feature in LICENSES_FEATURES:
            if x["policy"]["code"].startswith(feature):
                ret.add(feature)
    ret = list(ret)
    # Custom overrides here
    if ret == [LICENSE_CLIENT]:  # Client is an add-on to the free license
        ret = [LICENSE_FREE, LICENSE_CLIENT]
    return ret


SERVER_API_VERSION = "v1"


def httpAuthHeader(user, signature):
    return "PKDiagram:%s:%s" % (user, signature)


def sign(secret, verb, content_md5, content_type, date, resource):
    """Just producce a signature."""
    canonical = "\n".join((verb, content_md5, content_type, date, resource))
    h = hmac.new(secret, canonical.encode("utf-8"), hashlib.sha1)
    signature = base64.encodebytes(h.digest()).strip().decode("utf-8")
    # Debug(verb, content_md5, content_type, date, resource, signature)
    return signature


ANON_SECRET = b"17754e81c5cd0adb73bbeffb064ccbc6"
ANON_USER = "anonymous"
