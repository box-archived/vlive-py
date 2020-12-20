# VLive React App ID
AppId = "8c6cc7b45d2568fb668be6e05b6e5a3b"

# locale parameter(url postfix)
LocaleParam = "&gcc=KR&locale=ko_KR"


# API: Post Info API
# APIPostUrl("POST-ID"): str
# APIPostReferer(post): dict
def APIPostUrl(post):
    return "https://www.vlive.tv/globalv-web/vam-web/post/v1.0/post-%s?"\
           "appId=%s&fields=title,attachments,officialVideo%s" \
           % (post, AppId, LocaleParam)


def APIPostReferer(post):
    return {"Referer": "https://www.vlive.tv/post/%s" % post}


# API: Get user session (sign-in)
APISignInUrl = "https://www.vlive.tv/auth/email/login"
APISignInReferer = {'Referer': 'https://www.vlive.tv/auth/email/login'}


# User-Agent header for requests module
HeaderUserAgent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/87.0.4280.88 Safari/537.36"}

# Accept-Language header for requests module
HeaderAcceptLang = {"Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}

# Header for common use
HeaderCommon = {**HeaderUserAgent, **HeaderAcceptLang}
