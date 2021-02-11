# VLive React App ID
AppId = {"appId": "8c6cc7b45d2568fb668be6e05b6e5a3b"}

# locale parameter(url postfix)
LocaleParam = {"gcc": "KR", "locale": "ko_KR"}

PlatformPCParam = {"platformType": "PC"}

# Header for common use
HeaderCommon = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/87.0.4280.88 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
}


# Referer
def referer_post(post):
    return {"Referer": "https://www.vlive.tv/post/%s" % post}


def referer_auth():
    return {'Referer': 'https://www.vlive.tv/auth/email/login'}


def referer_video(videoSeq):
    return {"referer": "https://www.vlive.tv/video/%s" % videoSeq}


def referer_vlive():
    return {"referer": "https://www.vlive.tv/"}


# Endpoint
def endpoint_post(post):
    url = "https://www.vlive.tv/globalv-web/vam-web/post/v1.0/post-%s" % post
    params = {
        "fields": "attachments,author,authorId,availableActions,board{boardId,title,boardType,"
                  "readAllowedLabel,payRequired,includedCountries,excludedCountries},boardId,"
                  "body,channel{channelName,channelCode},channelCode,commentCount,contentType,"
                  "createdAt,emotionCount,excludedCountries,includedCountries,isViewerBookmarked,"
                  "isCommentEnabled,isHiddenFromStar,lastModifierMember,notice,officialVideo,"
                  "originPost,plainBody,postId,postVersion,reservation,starReactions,targetMember,"
                  "targetMemberId,thumbnail,title,url,smartEditorAsHtml,viewerEmotionId,writtenIn,"
                  "playlist.limit(30)",
        **AppId,
        **LocaleParam
    }
    headers = {
        **referer_post(post),
        **HeaderCommon
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_auth(email, pwd):
    url = "https://www.vlive.tv/auth/email/login"
    data = {
        'email': email,
        'pwd': pwd
    }
    headers = {
        **referer_auth(),
        **HeaderCommon
    }

    return {"url": url, "data": data, "headers": headers}


def endpoint_vod_inkey(videoSeq):
    url = "https://www.vlive.tv/globalv-web/vam-web/video/v1.0/vod/%s/inkey" % videoSeq
    params = {
        **AppId,
        **LocaleParam,
        **PlatformPCParam
    }
    headers = {
        **HeaderCommon,
        **referer_video(videoSeq)
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_fvideo_inkey(fvideo):
    url = "https://www.vlive.tv/globalv-web/vam-web/fvideo/v1.0/fvideo-%s/inKey" % fvideo
    params = {
        **AppId,
        **LocaleParam,
    }
    headers = {
        **HeaderCommon,
        **referer_post("")
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_official_video_post(videoSeq):
    url = "https://www.vlive.tv/globalv-web/vam-web/post/v1.0/officialVideoPost-%s" % videoSeq
    params = {
        **AppId,
        **LocaleParam,
        "fields": "attachments,author,authorId,availableActions,board{boardId,title,boardType,"
                  "readAllowedLabel,payRequired,includedCountries,excludedCountries},boardId,"
                  "body,channel{channelName,channelCode},channelCode,commentCount,contentType,"
                  "createdAt,emotionCount,excludedCountries,includedCountries,isViewerBookmarked,"
                  "isCommentEnabled,isHiddenFromStar,lastModifierMember,notice,officialVideo,"
                  "originPost,plainBody,postId,postVersion,reservation,starReactions,targetMember,"
                  "targetMemberId,thumbnail,title,url,smartEditorAsHtml,viewerEmotionId,writtenIn"
    }
    headers = {
        **HeaderCommon,
        **referer_video(videoSeq)
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_live_play_info(videoSeq, vpdid2=None):
    url = "https://www.vlive.tv/globalv-web/vam-web/old/v3/live/%s/playInfo" % videoSeq
    params = {
        **AppId,
        **PlatformPCParam,
        **LocaleParam,
    }
    if vpdid2:
        params.update({"vpdid2": vpdid2})
    headers = {
        **HeaderCommon,
        **referer_video(videoSeq)
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_live_status(videoSeq):
    url = "https://www.vlive.tv/globalv-web/vam-web/old/v2/live/%s/status" % videoSeq
    params = {
        **AppId,
        **LocaleParam
    }
    headers = {
        **HeaderCommon,
        **referer_video(videoSeq)
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_vod_play_info(vodId, inkey):
    url = "https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/%s" % vodId
    params = {
        "key": inkey,
        "videoId": vodId,
        "ver": "2.0",
        "ctls": '{"visible":{"fullscreen":true,"logo":false,"playbackRate":false,"scrap":false,"playCount":true,'
                '"commentCount":true,"title":true,"writer":true,"expand":true,"subtitles":true,"thumbnails":true,'
                '"quality":true,"setting":true,"script":false,"logoDimmed":true,"badge":true,"seekingTime":true,'
                '"muted":true,"muteButton":false,"viewerNotice":false,"linkCount":false,"createTime":false,'
                '"thumbnail":true},"clicked":{"expand":false,"subtitles":false}}',
        "devt": "html5_pc",
        "doct": "json",
        "cpt": "vtt",
        "cpl": "ko_KR",
        "lc": "ko_KR"
    }
    headers = {
        **HeaderCommon,
        **referer_vlive()
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_post_comments(post, after=None):
    url = "https://www.vlive.tv/globalv-web/vam-web/comment/v1.0/post-%s/comments" % post
    params = {
        **AppId,
        **LocaleParam,
        "fields": "root,parent,commentId,body,emotionCount,commentCount,viewerEmotionId,viewerAvailableActions,"
                  "createdAt,writtenIn,sticker,author,latestComments,isRestricted,lastModifierMember",
        "startFrom": "first"
    }
    if after:
        params.update({"after": after})
    headers = {
        **HeaderCommon,
        **referer_post(post)
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_post_star_comments(post, after=None):
    url = "https://www.vlive.tv/globalv-web/vam-web/comment/v1.0/post-%s/starComments" % post
    params = {
        **AppId,
        **LocaleParam,
        "fields": "root,parent,commentId,body,emotionCount,commentCount,viewerEmotionId,viewerAvailableActions,"
                  "createdAt,writtenIn,sticker,author,isRestricted,lastModifierMember",
        "startFrom": "first"
    }
    if after:
        params.update({"after": after})
    headers = {
        **HeaderCommon,
        **referer_post(post)
    }

    return {"url": url, "params": params, "headers": headers}
