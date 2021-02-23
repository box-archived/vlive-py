from copy import deepcopy
from os.path import dirname
from time import time
from typing import Generator
from warnings import warn
from bs4 import BeautifulSoup, element
from .comment import getCommentData, getPostCommentsIter, getPostStarCommentsIter
from .connections import getPostInfo, postIdToVideoSeq, videoSeqToPostId
from .exception import ModelRefreshWarning
from .parser import (
    format_epoch, max_res_from_play_info,
    parseVodIdFromOffcialVideoPost, UpcomingVideo, v_timestamp_parser
)
from .post import getFVideoPlayInfo
from .schedule import getScheduleData
from .upcoming import getUpcomingList
from .video import (
    getInkeyData, getLivePlayInfo, getLiveStatus, getOfficialVideoPost, getVodPlayInfo
)


class Comment(object):
    __slots__ = ['__cached_data', '__comment_id', 'session']

    def __init__(self, commentId, session=None, init_data=None):
        self.session = session
        self.__comment_id = commentId
        if init_data:
            self.__cached_data = deepcopy(init_data)
        else:
            self.refresh()

    def __repr__(self):
        return "<Comment [%s]>" % self.__comment_id

    def __eq__(self, other):
        if type(self) == type(other):
            if self.commentId == other.commentId:
                return True
        return False

    def __dict__(self):
        return self.raw

    def refresh(self):
        res = getCommentData(commentId=self.__comment_id, session=self.session, silent=True)
        if res:
            self.__cached_data = res
        else:
            warn("Failed to refresh %s" % self, ModelRefreshWarning)

    @property
    def raw(self) -> dict:
        return deepcopy(self.__cached_data)

    @property
    def commentId(self) -> str:
        return self.__comment_id

    @property
    def author(self) -> dict:
        return self.raw['author']

    @property
    def author_nickname(self) -> str:
        return self.__cached_data['author']['nickname']

    @property
    def author_memberId(self) -> str:
        return self.__cached_data['author']['memberId']

    @property
    def body(self) -> str:
        return self.raw['body']

    @property
    def sticker(self) -> list:
        return self.raw['sticker']

    @property
    def created_at(self) -> float:
        return v_timestamp_parser(self.__cached_data['createdAt'])

    @property
    def comment_count(self) -> int:
        return self.__cached_data['commentCount']

    @property
    def emotion_count(self) -> int:
        return self.raw['emotionCount']

    @property
    def is_restricted(self) -> bool:
        return self.__cached_data['isRestricted']

    @property
    def parent(self) -> dict:
        return self.raw['parent']

    @property
    def root(self) -> dict:
        return self.raw['root']

    @property
    def written_in(self) -> str:
        return self.__cached_data['writtenIn']

    def parent_info_tuple(self):
        tp = self.parent['type']
        key = "%sId" % tp.lower()
        return self.parent['type'], self.parent['data'][key]

    def root_info_tuple(self):
        tp = self.root['type']
        key = "%sId" % tp.lower()
        return tp, self.root['data'][key]


class PostBase(object):
    def __init__(self, post_id, session=None):
        self.__post_id = post_id
        self.__cached_post = {}
        self.session = session

        self.refresh()

    def __repr__(self):
        return "<VLIVE Post [%s]>" % self.__post_id

    def __eq__(self, other):
        if type(self) == type(other):
            if self.post_id == other.post_id:
                return True
        return False

    def __dict__(self):
        return self.raw

    def refresh(self):
        result = getPostInfo(self.__post_id, session=self.session, silent=True)
        if result:
            self.__cached_post = result

    @property
    def raw(self):
        return deepcopy(self.__cached_post)

    @property
    def attachments(self) -> dict:
        return self.raw['attachments']

    @property
    def attachments_photo(self) -> dict:
        if 'photo' in self.__cached_post['attachments']:
            return self.raw['attachments']['photo']
        else:
            return {}

    @property
    def attachments_video(self) -> dict:
        if 'video' in self.__cached_post['attachments']:
            return self.raw['attachments']['video']
        else:
            return {}

    @property
    def author(self) -> dict:
        return self.raw['author']

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
    def post_id(self) -> str:
        return self.__post_id

    @property
    def title(self) -> str:
        return self.__cached_post['title']

    def getPostCommentsIter(self) -> Generator[Comment, None, None]:
        return getPostCommentsIter(self.__post_id, session=self.session)

    def getPostStarCommentsIter(self) -> Generator[Comment, None, None]:
        return getPostStarCommentsIter(self.__post_id, session=self.session)


class Post(PostBase):
    def __init__(self, post_id, session=None):
        super().__init__(post_id, session)

    @property
    def plain_body(self) -> str:
        return self.raw['plainBody']

    @property
    def body(self) -> str:
        return self.raw['body']

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


class OfficialVideoPost(PostBase):
    def __init__(self, init_id, session=None):
        # interpret number
        if type(init_id) == int:
            init_id = str(init_id)

        # Case <videoSeq>
        if "-" not in init_id:
            init_id = videoSeqToPostId(init_id)
        super().__init__(init_id, session)

    @property
    def official_video(self):
        return self.raw['officialVideo']


class Schedule(object):
    __slots__ = ["__cached_data", "__schedule_id", "session"]

    def __init__(self, schedule_id, session):
        self.__schedule_id = schedule_id
        self.__cached_data = {}
        self.session = session
        self.refresh()

    def __eq__(self, other):
        if type(self) == type(other):
            if self.schedule_id == other.schedule_id:
                return True
        return False

    def __dict__(self):
        return self.raw

    def refresh(self, silent=False):
        data = getScheduleData(self.__schedule_id, self.session, silent)
        if data is not None:
            self.__cached_data = data

    @property
    def raw(self) -> dict:
        return deepcopy(self.__cached_data)

    @property
    def schedule_id(self) -> str:
        return self.__schedule_id

    @property
    def author(self) -> dict:
        return self.raw['author']

    @property
    def author_nickname(self) -> str:
        return self.__cached_data['author']['nickname']

    @property
    def author_id(self) -> str:
        return self.__cached_data['author']


class Upcoming(object):
    def __init__(self, refresh_rate=5, show_vod=True, show_upcoming_vod=True, show_upcoming_live=True, show_live=True):
        self.refresh_rate = refresh_rate
        self.__cached_data = []
        self.__cached_time = 0
        self.show_live = show_live
        self.show_vod = show_vod
        self.show_upcoming_vod = show_upcoming_vod
        self.show_upcoming_live = show_upcoming_live

        # refresh data
        self.refresh(True)

    def refresh(self, force=False):
        distance = time() - self.__cached_time
        if distance >= self.refresh_rate or force:
            new_data = self.load(date=None, silent=True,
                                 show_vod=True, show_upcoming_vod=True,
                                 show_live=True, show_upcoming_live=True)
            if new_data is not None:
                self.__cached_data = new_data
                self.__cached_time = int(time())
                return True
        return False

    def load(self, date, show_vod=None, show_upcoming_vod=None, show_upcoming_live=None, show_live=None, silent=False):
        if show_live is None:
            show_live = self.show_live
        if show_vod is None:
            show_vod = self.show_vod
        if show_upcoming_vod is None:
            show_upcoming_vod = self.show_upcoming_vod
        if show_upcoming_live is None:
            show_upcoming_live = self.show_upcoming_live

        upcomings = getUpcomingList(date=date, silent=silent)

        if upcomings is not None:
            data_list = []
            for item in upcomings:
                item: UpcomingVideo
                if item.type == "VOD" and show_vod:
                    data_list.append(item)
                elif item.type == "LIVE" and show_live:
                    data_list.append(item)
                elif item.type == "UPCOMING_VOD" and show_upcoming_vod:
                    data_list.append(item)
                elif item.type == "UPCOMING_LIVE" and show_upcoming_live:
                    data_list.append(item)

            return data_list
        return None

    def upcoming(self, force=False, show_vod=None, show_upcoming_vod=None, show_upcoming_live=None, show_live=None):
        r""" get upcoming list, auto refresh

        :return: Upcoming list
        :rtype: list[parser.upcomingVideo]
        """
        self.refresh(force=force)
        if show_live is None:
            show_live = self.show_live
        if show_vod is None:
            show_vod = self.show_vod
        if show_upcoming_vod is None:
            show_upcoming_vod = self.show_upcoming_vod
        if show_upcoming_live is None:
            show_upcoming_live = self.show_upcoming_live

        data_list = []
        for item in self.__cached_data:
            item: UpcomingVideo
            if item.type == "VOD" and show_vod:
                data_list.append(item)
            elif item.type == "LIVE" and show_live:
                data_list.append(item)
            elif item.type == "UPCOMING_VOD" and show_upcoming_vod:
                data_list.append(item)
            elif item.type == "UPCOMING_LIVE" and show_upcoming_live:
                data_list.append(item)

        return data_list


class Video(object):
    # Will be deprecate
    def __init__(self, number, session=None, refresh_rate=10):
        r""" Init

        :param number: video post-id or videoSeq
        :param session: use specific session
        :param refresh_rate: cache refresh rate
        """

        # interpret number
        if type(number) == int:
            number = str(number)

        # Case <post-id>
        if "-" in number:
            self.__VideoSeq = postIdToVideoSeq(number)
        # Case <videoSeq>
        else:
            self.__VideoSeq = number

        # Variable declaration
        self.session = session
        self.refresh_rate = refresh_rate
        self.__cachedTime = 0
        self.__cached_data = {}

        # init variables
        while self.__cachedTime == 0:
            self.refresh(force=True)

    def __repr__(self):
        if self.is_vod:
            return "<VLIVE Video(VOD) [%s]>" % self.videoSeq
        else:
            return "<VLIVE Video(LIVE) [%s]>" % self.videoSeq

    @property
    def raw(self) -> dict:
        return deepcopy(self.__cached_data)

    @property
    def created_at(self):
        return v_timestamp_parser(self.__cached_data['createdAt'])

    @property
    def videoSeq(self) -> str:
        return self.__VideoSeq

    @property
    def vod_id(self) -> str:
        if self.is_vod():
            return parseVodIdFromOffcialVideoPost(self.__cached_data, silent=True)
        else:
            return ""

    @property
    def title(self) -> str:
        return self.__cached_data['officialVideo']['title']

    @property
    def channelCode(self) -> str:
        return self.__cached_data['author']['channelCode']

    @property
    def channelName(self) -> str:
        return self.__cached_data['author']['nickname']

    def refresh(self, force=False):
        # Cached time distance
        distance = time() - self.__cachedTime
        if distance >= self.refresh_rate or force:
            # Get data
            data = getOfficialVideoPost(self.videoSeq, silent=True)
            if data is not None:
                # Set data
                self.__cachedTime = int(time())
                self.__cached_data = data

    def is_vod(self) -> bool:
        if 'vodId' in self.__cached_data['officialVideo']:
            return True
        else:
            return False

    def getOfficialVideoPost(self, silent=False):
        return getOfficialVideoPost(self.videoSeq, session=self.session, silent=silent)

    def getLivePlayInfo(self, silent=False):
        return getLivePlayInfo(self.videoSeq, session=self.session, silent=silent)

    def getInkeyData(self, silent=False):
        return getInkeyData(self.videoSeq, session=self.session, silent=silent)

    def getLiveStatus(self, silent=False):
        return getLiveStatus(self.videoSeq, silent=silent)

    def getVodPlayInfo(self, silent=False):
        if self.is_vod:
            return getVodPlayInfo(self.videoSeq, self.vod_id, session=self.session, silent=silent)
        else:
            return None
