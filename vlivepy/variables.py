# -*- coding: utf-8 -*-

# Overwrite-able vars
overwrite_app_id = "8c6cc7b45d2568fb668be6e05b6e5a3b"
overwrite_gcc = "KR"
overwrite_locale = "ko_KR"


# VLive React App ID
AppId = {"appId": overwrite_app_id}

# locale parameter(url postfix)
LocaleParam = {"gcc": overwrite_gcc, "locale": overwrite_locale}

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
        "lc": "ko_KR",
        "CC": "KR"
    }
    headers = {
        **HeaderCommon,
        **referer_vlive()
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_post_comment_template(prefix, srl, postfix=None, after=None, field: list = None):
    if field is None:
        field = []

    url = "https://www.vlive.tv/globalv-web/vam-web/comment/v1.0/%s-%s" % (prefix, srl)
    if postfix:
        url += "/%s" % postfix

    params = {
        **AppId,
        **LocaleParam,
        "fields": "root,parent,commentId,body,emotionCount,commentCount,viewerEmotionId,viewerAvailableActions,"
                  "createdAt,writtenIn,sticker,author,isRestricted,lastModifierMember",
        "startFrom": "first"
    }
    if after:
        params.update({"after": after})

    for item in field:
        params["fields"] += ",%s" % item

    headers = {
        **HeaderCommon,
        **referer_post(srl)
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_post_comments(post, after=None):
    return endpoint_post_comment_template(
        "post", post, postfix="comments", after=after, field=["latestComments"]
    )


def endpoint_post_star_comments(post, after=None):
    return endpoint_post_comment_template(
        "post", post, postfix="starComments", after=after
    )


def endpoint_comment_data(post):
    return endpoint_post_comment_template(
        "comment", post
    )


def endpoint_comment_nested(post, after=None):
    return endpoint_post_comment_template(
        "comment", post, postfix="comments", after=after
    )


def endpoint_schedule_data(schedule):
    url = "https://www.vlive.tv/globalv-web/vam-web/schedule/v1.0/schedule-%s" % schedule
    params = {
        **AppId,
        **LocaleParam,
        "fields": "scheduleId,title,description,alarm,location,postId,videoSeq,officialVideo,photos,author,"
                  "timezoneId,type,startAt,commentCount,emotionCount,commentWritable,availableActions,writtenIn,"
                  "url,viewerEmotionId,channel{channelCode,channelName},post{url},timeUsing,lastModifierMember"
    }
    headers = {
        **HeaderCommon,
        "referer": "https://www.vlive.tv/schedule/%s" % schedule
    }

    return {"url": url, "params": params, "headers": headers}


def endpoint_decode_channel_code(channel_code):
    url = "http://api.vfan.vlive.tv/vproxy/channelplus/decodeChannelCode"
    params = {
        "app_id": overwrite_app_id,
        "channelCode": channel_code,
        "_": "1614426919000"
    }
    headers = {
        **HeaderCommon,
        "referer": "https://www.vlive.tv/"
    }

    return {"url": url, "params": params, "headers": headers}
