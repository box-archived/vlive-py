from os.path import dirname
from bs4 import BeautifulSoup, element
import reqWrapper
from . import variables as gv
from .connections import getPostInfo
from .exception import auto_raise, APINetworkError
from .parser import max_res_from_play_info, format_epoch, v_timestamp_parser, response_json_stripper
from .comment import getPostCommentsIter, getPostStarCommentsIter


def getFVideoInkeyData(fvideo, session=None, silent=False):
    r""" get Inkey Data

    :param fvideo: file video id from VLIVE (like ######)(Numbers)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return: Inkey data
    :rtype: dict
    """

    # Make request
    sr = reqWrapper.get(**gv.endpoint_fvideo_inkey(fvideo),
                        wait=0.5, session=session, status=[200])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)['inKey']
    else:
        auto_raise(APINetworkError, silent)

    return None


def getFVideoPlayInfo(videoSeqId, videoVodId, session=None, silent=False):
    r""" Get fvideo VOD Data

    :param videoSeqId: videoId from attachment-id (like #-########)
    :param videoVodId: videoId from attachment/uploadInfo (like #-########)
    :param session: use specific session
    :param silent: Return `None` instead of Exception
    :return:
    """

    inkey = getFVideoInkeyData(fvideo=videoSeqId, session=session)
    sr = reqWrapper.get(**gv.endpoint_vod_play_info(videoVodId, inkey),
                        session=session, wait=0.3, status=[200, 403])

    if sr.success:
        return response_json_stripper(sr.response.json(), silent=silent)
    else:
        auto_raise(APINetworkError, silent=silent)


class Post(object):
    def __init__(self, post_id, session=None):
        self.post_id = post_id
        self.__cached_post = {}
        self.session = session

        self.refresh()

    def __repr__(self):
        return "<VLIVE Post [%s]>" % self.post_id

    def refresh(self):
        result = getPostInfo(self.post_id, session=self.session, silent=True)
        if result:
            self.__cached_post = result

    @property
    def attachments(self) -> dict:
        return self.__cached_post['attachments']

    @property
    def attachments_photo(self) -> dict:
        if 'photo' in self.__cached_post['attachments']:
            return self.__cached_post['attachments']['photo']
        else:
            return {}

    @property
    def attachments_video(self) -> dict:
        if 'video' in self.__cached_post['attachments']:
            return self.__cached_post['attachments']['video']
        else:
            return {}

    @property
    def author(self) -> dict:
        return self.__cached_post['author']

    @property
    def author_nickname(self) -> str:
        return self.__cached_post['author']['nickname']

    @property
    def author_id(self) -> str:
        return self.__cached_post['author']['memberId']

    @property
    def created_at(self) -> float:
        return v_timestamp_parser(self.__cached_post['createdAt'])

    @property
    def plain_body(self) -> str:
        return self.__cached_post['plainBody']

    @property
    def body(self) -> str:
        return self.__cached_post['body']

    @property
    def title(self) -> str:
        return self.__cached_post['title']

    def formatted_body(self):
        loc = dirname(__file__)
        with open(loc + "/video_template.html", encoding="utf8") as f:
            video_template = f.read()

        with open(loc + "/formatted_body.html", encoding="utf8") as f:
            doc_template = f.read()

        soup = BeautifulSoup(self.body, 'html.parser')
        for item in soup.children:
            if type(item) == element.NavigableString:
                item.wrap(soup.new_tag("p"))

        for item in soup.find_all("p"):
            br_text = '<p class="body">%s</p>' % item.string.replace("\n", "<br />")
            sub_soup = BeautifulSoup(br_text, 'html.parser')
            item.replace_with(sub_soup)

        for item in soup.find_all("v:attachment"):
            at_id = item.get("id")
            at_type = item.get("type")
            at_data = self.attachments[at_type][at_id]

            if at_type == 'photo':
                dom_obj = soup.new_tag("img")
                dom_obj.attrs['src'] = at_data['url']
                dom_obj.attrs["class"] = "photo"
                dom_obj.attrs['style'] = "display: block;margin-bottom:10px;width:100%"

            elif at_type == "video":

                play_info = getFVideoPlayInfo(
                    videoSeqId=at_data['videoId'],
                    videoVodId=at_data['uploadInfo']['videoId'],
                    session=self.session
                )
                video = max_res_from_play_info(play_info)
                dom_obj = soup.new_tag("video")
                dom_obj.attrs['src'] = video['source']
                dom_obj.attrs['type'] = "video/mp4"
                dom_obj.attrs['poster'] = at_data['uploadInfo']['imageUrl']
                dom_obj.attrs['controls'] = ""
                dom_obj.attrs["class"] = "video"
                dom_obj.attrs['style'] = "display: block;width: 100%;height: 100%;outline:none;"
                dom_obj = BeautifulSoup(video_template.replace("###VIDEO###", str(dom_obj)), 'html.parser')
            else:
                dom_obj = ""
            item.replace_with(dom_obj)

        doc_template = doc_template.replace("###LINK###", "https://www.vlive.tv/post/" + self.post_id)
        doc_template = doc_template.replace("###AUTHOR###", self.author_nickname)
        doc_template = doc_template.replace("###TIME###", format_epoch(self.created_at, "%Y.%m.%d %H:%M:%S"))
        doc_template = doc_template.replace("###TITLE###", self.title)
        doc_template = doc_template.replace("###POST###", str(soup))

        return doc_template

    def getPostCommentsIter(self):
        return getPostCommentsIter(self.post_id, session=self.session)

    def getPostStarCommentsIter(self):
        return getPostStarCommentsIter(self.post_id, session=self.session)
