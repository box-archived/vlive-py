# VLive React App ID
AppId = "8c6cc7b45d2568fb668be6e05b6e5a3b"

# locale parameter(url postfix)
LocaleParam = "&gcc=KR&locale=ko_KR"

PlatformPCParam = "&platformType=PC"


# API: Post Info API
# APIPostUrl("POST-ID"): str
# APIPostReferer("POST-ID"): dict
def APIPostUrl(post):
    return "https://www.vlive.tv/globalv-web/vam-web/post/v1.0/post-%s?" \
           "appId=%s&fields=title,attachments,officialVideo%s" \
           % (post, AppId, LocaleParam)


def APIPostReferer(post):
    return {"Referer": "https://www.vlive.tv/post/%s" % post}


# API: Get user session (sign-in)
# APISignInUrl: str
# APISignInReferer: dict
APISignInUrl = "https://www.vlive.tv/auth/email/login"
APISignInReferer = {'Referer': 'https://www.vlive.tv/auth/email/login'}


def APIInkeyUrl(videoSeq):
    return ("https://www.vlive.tv/globalv-web/vam-web/video/v1.0/vod/%s/inkey?appId=%s%s%s" %
            (videoSeq, AppId, LocaleParam, PlatformPCParam))


# API: officialVideoPost
def APIofficialVideoPostUrl(videoSeq):
    return ("https://www.vlive.tv/globalv-web/vam-web/post/v1.0/officialVideoPost-"
            "%s?appId=%s&fields=attachments,author,authorId,availableActions,"
            "board{boardId,title,boardType,readAllowedLabel,payRequired,"
            "includedCountries,excludedCountries},boardId,body,channel{channelName,channelCode},"
            "channelCode,commentCount,contentType,createdAt,emotionCount,excludedCountries,"
            "includedCountries,isViewerBookmarked,isCommentEnabled,isHiddenFromStar,lastModifierMember,"
            "notice,officialVideo,originPost,plainBody,postId,postVersion,reservation,starReactions,"
            "targetMember,targetMemberId,thumbnail,title,url,smartEditorAsHtml,viewerEmotionId,"
            "writtenIn"
            "%s" % (videoSeq, AppId, LocaleParam))


def APIofficialVideoPostReferer(videoSeq):
    return {"referer": "https://www.vlive.tv/video/%s" % videoSeq}


def APILiveV3PlayInfoUrl(videoSeq):
    # Optional: vpdid2
    return ("https://www.vlive.tv/globalv-web/vam-web/old/v3/live/%s/playInfo?appId=%s%s%s" %
            (videoSeq, AppId, PlatformPCParam, LocaleParam))


def APILiveV2StatusUrl(videoSeq):
    return ("https://www.vlive.tv/globalv-web/vam-web/old/v2/live/%s/status?appId=%s%s" %
            (videoSeq, AppId, LocaleParam))


def APIVodPlayInfoUrl(vodId, inkey):
    return "https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/%s?key=%s&videoId=%s" % (vodId, inkey, vodId)


APIVodPlayInfoReferer = {"referer": "https://www.vlive.tv/"}


def APIPostDataUrl(post):
    return ("https://www.vlive.tv/globalv-web/vam-web/post/v1.0/post-%s"
            "?appId=%s&fields=attachments,author,authorId,availableActions,"
            "board{boardId,title,boardType,readAllowedLabel,payRequired,includedCountries,excludedCountries},"
            "boardId,body,channel{channelName,channelCode},channelCode,commentCount,contentType,createdAt,"
            "emotionCount,excludedCountries,includedCountries,isViewerBookmarked,isCommentEnabled,isHiddenFromStar,"
            "lastModifierMember,notice,officialVideo,originPost,plainBody,postId,postVersion,reservation,starReactions,"
            "targetMember,targetMemberId,thumbnail,title,url,smartEditorAsHtml,viewerEmotionId,writtenIn,"
            "playlist.limit(30)%s" % (post, AppId, LocaleParam))


def APIPostCommentsUrl(post, after=None):
    if after is None:
        after = ""
    else:
        after = "after=%s&" % after

    return ("https://www.vlive.tv/globalv-web/vam-web/comment/v1.0/post-%s/"
            "comments?%sappId=%s&fields=root,parent,commentId,body,emotionCount,commentCount,viewerEmotionId,"
            "viewerAvailableActions,createdAt,writtenIn,sticker,author,latestComments,isRestricted,"
            "lastModifierMember&startFrom=first"
            "%s" % (post, after, AppId, LocaleParam))


def APIPostStarCommentsUrl(post, after=None):
    if after is None:
        after = ""
    else:
        after = "after=%s&" % after

    return ("https://www.vlive.tv/globalv-web/vam-web/comment/v1.0/post-%s/"
            "starComments?%sappId=%s&fields=root,parent,commentId,body,emotionCount,commentCount,"
            "viewerEmotionId,viewerAvailableActions,createdAt,writtenIn,sticker,author,isRestricted,"
            "lastModifierMember&startFrom=first"
            "%s" % (post, after, AppId, LocaleParam))


def APIPostDataReferer(post):
    return {"referer": "https://www.vlive.tv/post/%s" % post}


# User-Agent header for requests module
HeaderUserAgent = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/87.0.4280.88 Safari/537.36"}

# Accept-Language header for requests module
HeaderAcceptLang = {"Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}

# Header for common use
HeaderCommon = {**HeaderUserAgent, **HeaderAcceptLang}
