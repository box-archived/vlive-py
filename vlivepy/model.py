# -*- coding: utf-8 -*-

from __future__ import annotations

from copy import deepcopy
from os.path import dirname
from time import time
from typing import (
    Generator,
    List,
    Union,
)
from warnings import warn

from bs4 import (
    BeautifulSoup,
    element,
)

from .channel import (
    getChannelInfo,
    getGroupedBoards,
)
from .comment import (
    getCommentData,
    getPostCommentsIter,
    getPostStarCommentsIter,
    getNestedCommentsIter,
)
from .connections import (
    getPostInfo,
    videoSeqToPostId,
    decode_channel_code,
)
from .exception import (
    ModelRefreshWarning,
    ModelInitError,
)
from .parser import (
    format_epoch,
    max_res_from_play_info,
    UpcomingVideo,
    v_timestamp_parser,
)
from .post import getFVideoPlayInfo
from .schedule import getScheduleData
from .upcoming import getUpcomingList
from .video import (
    getInkeyData,
    getLivePlayInfo,
    getLiveStatus,
    getOfficialVideoData,
    getVodPlayInfo
)


class DataModel(object):
    __slots__ = ['_data_cache', '_target_id', 'session', '_method']

    def __init__(self, method, target_id, session=None, init_data=None):
        self._method = method
        self._target_id = target_id
        self.session = session

        if init_data:
            self._data_cache = init_data
        else:
            self.refresh()

    def __eq__(self, other):
        if type(self) == type(other):
            if self.target_id == other.target_id:
                return True
        return False

    def refresh(self):
        res = self._method(self._target_id, session=self.session, silent=True)
        if res:
            self._data_cache = res
        else:
            warn("Failed to refresh %s" % self, ModelRefreshWarning)

    @property
    def raw(self) -> dict:
        return deepcopy(self._data_cache)

    @property
    def target_id(self) -> str:
        return str(self._target_id)


class Comment(DataModel):

    def __init__(self, commentId, session=None, init_data=None):
        super().__init__(getCommentData, commentId, session=session, init_data=init_data)

    def __repr__(self):
        return "<Comment [%s]>" % self._target_id

    @property
    def commentId(self) -> str:
        return self._target_id

    @property
    def author(self) -> dict:
        return deepcopy(self._data_cache['author'])

    @property
    def author_nickname(self) -> str:
        return self._data_cache['author']['nickname']

    @property
    def author_memberId(self) -> str:
        return self._data_cache['author']['memberId']

    @property
    def body(self) -> str:
        return self._data_cache['body']

    @property
    def sticker(self) -> list:
        return deepcopy(self._data_cache['sticker'])

    @property
    def created_at(self) -> float:
        return v_timestamp_parser(self._data_cache['createdAt'])

    @property
    def comment_count(self) -> int:
        return self._data_cache['commentCount']

    @property
    def emotion_count(self) -> int:
        return self._data_cache['emotionCount']

    @property
    def is_restricted(self) -> bool:
        return self._data_cache['isRestricted']

    @property
    def parent(self) -> dict:
        return deepcopy(self._data_cache['parent'])

    @property
    def root(self) -> dict:
        return deepcopy(self._data_cache['root'])

    @property
    def written_in(self) -> str:
        return self._data_cache['writtenIn']

    def getNestedCommentsIter(self) -> Generator[Comment]:
        return getNestedCommentsIter(self.commentId, session=self.session)

    def parent_info_tuple(self):
        tp = self.parent['type']
        key = "%sId" % tp.lower()
        return self.parent['type'], self.parent['data'][key]

    def root_info_tuple(self):
        tp = self.root['type']
        key = "%sId" % tp.lower()
        return tp, self.root['data'][key]


class OfficialVideoModel(DataModel):
    def __init__(self, videoSeq, session=None):
        super().__init__(getOfficialVideoData, videoSeq, session=session)

    @property
    def video_seq(self) -> int:
        return self._data_cache['videoSeq']

    @property
    def video_type(self) -> str:
        return self._data_cache['type']

    @property
    def title(self) -> str:
        return self._data_cache['title']

    @property
    def multinational_titles(self) -> List[dict]:
        return deepcopy(self._data_cache['multinationalTitles'])

    def multinational_title_locales(self) -> list:
        locale_list = []
        for item in self._data_cache['multinationalTitles']:
            locale_list.append(item['locale'])

        return locale_list

    def multinational_title_get(self, locale) -> dict:
        for item in self._data_cache['multinationalTitles']:
            if item['locale'] == locale:
                return item.copy()
        else:
            raise KeyError

    @property
    def play_count(self) -> int:
        return self._data_cache['playCount']

    @property
    def like_count(self) -> int:
        return self._data_cache['likeCount']

    @property
    def comment_count(self) -> int:
        return self._data_cache['commentCount']

    @property
    def thumb(self) -> str:
        return self._data_cache['thumb']

    @property
    def expose_status(self) -> str:
        return self._data_cache['exposeStatus']

    @property
    def screen_orientation(self) -> str:
        return self._data_cache['screenOrientation']

    @property
    def will_start_at(self) -> float:
        return v_timestamp_parser(self._data_cache['willStartAt'])

    @property
    def on_air_start_at(self) -> float:
        return v_timestamp_parser(self._data_cache['onAirStartAt'])

    @property
    def will_end_at(self) -> float:
        return v_timestamp_parser(self._data_cache['willEndAt'])

    @property
    def created_at(self) -> float:
        return v_timestamp_parser(self._data_cache['createdAt'])

    @property
    def has_live_thumb(self) -> bool:
        return self._data_cache['liveThumbYn']

    @property
    def has_upcoming(self) -> bool:
        return self._data_cache['upcomingYn']

    @property
    def has_notice(self) -> bool:
        return self._data_cache['noticeYn']

    @property
    def product_type(self) -> str:
        return self._data_cache['productType']

    @property
    def has_pre_ad(self) -> bool:
        return self._data_cache['preAdYn']

    @property
    def has_post_ad(self) -> bool:
        return self._data_cache['postAdYn']

    @property
    def has_mobile_da(self) -> bool:
        return self._data_cache['mobileDAYn']

    @property
    def vr_content_type(self) -> str:
        return self._data_cache['vrContentType']


class OfficialVideoLive(OfficialVideoModel):
    def __init__(self, videoSeq, session=None):
        super().__init__(videoSeq, session=session)
        if self.video_type != "LIVE":
            raise ValueError("OfficialVideo [%s] is not Live." % videoSeq)

    def __repr__(self):
        return "<VLIVE OfficialVideo-Live [%s]>" % self.target_id

    @property
    def has_filter_ad(self) -> bool:
        return self._data_cache['filterAdYn']

    @property
    def momentable(self) -> bool:
        return self._data_cache['momentable']

    @property
    def has_special_live(self) -> bool:
        return self._data_cache['specialLiveYn']

    @property
    def status(self) -> str:
        return self._data_cache['status']

    @property
    def hevc(self) -> bool:
        return self._data_cache['hevc']

    @property
    def low_latency(self) -> bool:
        return self._data_cache['lowLatency']

    @property
    def pp_type(self) -> str:
        return self._data_cache['ppType']

    def getLivePlayInfo(self, silent=False):
        return getLivePlayInfo(self.video_seq, session=self.session, silent=silent)

    def getLiveStatus(self, silent=False):
        return getLiveStatus(self.video_seq, silent=silent)


class OfficialVideoVOD(OfficialVideoModel):
    def __init__(self, videoSeq, session=None):
        super().__init__(videoSeq, session=session)
        if self.video_type != "VOD":
            raise ValueError("OfficialVideo [%s] is not VOD." % videoSeq)

    def __repr__(self):
        return "<VLIVE OfficialVideo-VOD [%s]>" % self.target_id
    
    @property
    def has_preview(self) -> bool:
        return self._data_cache['previewYn']
    
    @property
    def has_moment(self) -> bool:
        return self._data_cache['hasMoment']

    @property
    def vod_id(self) -> str:
        return self._data_cache['vodId']

    @property
    def play_time(self) -> str:
        return self._data_cache['playTime']
    
    @property
    def encoding_status(self) -> str:
        return self._data_cache['encodingStatus']
    
    @property
    def vod_secure_status(self) -> str:
        return self._data_cache['vodSecureStatus']
    
    @property
    def dimension_type(self) -> str:
        return self._data_cache['dimensionType']

    def recommended_videos(self, as_object=True) -> list:
        if as_object:
            video_list = []
            for item in self._data_cache['recommendedVideos']:
                video_list.append(OfficialVideoPost(item['videoSeq']))

            return video_list
        else:
            return deepcopy(self._data_cache['recommendedVideos'])

    def getInkeyData(self, silent=False):
        return getInkeyData(self.video_seq, session=self.session, silent=silent)

    def getVodPlayInfo(self, silent=False):
        return getVodPlayInfo(self.video_seq, self.vod_id, session=self.session, silent=silent)


class PostBase(DataModel):
    def __init__(self, post_id, session=None):
        super().__init__(getPostInfo, post_id, session=session)

    @property
    def attachments(self) -> dict:
        return deepcopy(self._data_cache['attachments'])

    @property
    def attachments_photo(self) -> dict:
        if 'photo' in self._data_cache['attachments']:
            return deepcopy(self._data_cache['attachments']['photo'])
        else:
            return {}

    @property
    def attachments_video(self) -> dict:
        if 'video' in self._data_cache['attachments']:
            return deepcopy(self._data_cache['attachments']['video'])
        else:
            return {}

    @property
    def author(self) -> dict:
        return deepcopy(self._data_cache['author'])

    @property
    def author_nickname(self) -> str:
        return self._data_cache['author']['nickname']

    @property
    def author_id(self) -> str:
        return self._data_cache['author']['memberId']

    @property
    def created_at(self) -> float:
        return v_timestamp_parser(self._data_cache['createdAt'])

    @property
    def board_id(self) -> int:
        return self._data_cache['boardId']

    @property
    def channel_name(self) -> str:
        return self._data_cache['channel']['channelName']

    @property
    def channel_code(self) -> str:
        return self._data_cache['channelCode']
    
    @property
    def comment_count(self) -> int:
        return self._data_cache['commentCount']
    
    @property
    def content_type(self) -> str:
        return self._data_cache['contentType']

    @property
    def emotion_count(self) -> int:
        return self._data_cache['emotionCount']
    
    @property
    def is_comment_enabled(self) -> bool:
        return self._data_cache['isCommentEnabled']
    
    @property
    def is_hidden_from_star(self) -> bool:
        return self._data_cache['isHiddenFromStar']
    
    @property
    def is_viewer_bookmarked(self) -> bool:
        return self._data_cache['isViewerBookmarked']

    @property
    def post_id(self) -> str:
        return self._target_id

    @property
    def title(self) -> str:
        return self._data_cache['title']

    def getPostCommentsIter(self) -> Generator[Comment, None, None]:
        return getPostCommentsIter(self.post_id, session=self.session)

    def getPostStarCommentsIter(self) -> Generator[Comment, None, None]:
        return getPostStarCommentsIter(self.post_id, session=self.session)


class Post(PostBase):
    def __init__(self, post_id, session=None):
        super().__init__(post_id, session)

    def __repr__(self):
        return "<VLIVE Post [%s]>" % self.post_id

    @property
    def plain_body(self) -> str:
        return self._data_cache['plainBody']

    @property
    def body(self) -> str:
        return self._data_cache['body']

    @property
    def written_in(self) -> str:
        return self._data_cache['writtenIn']

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

    def __repr__(self):
        return "<VLIVE OfficialVideoPost [%s]>" % self.video_seq

    @property
    def official_video_type(self) -> str:
        return self._data_cache['officialVideo']['type']

    @property
    def video_seq(self) -> int:
        return self._data_cache["officialVideo"]["videoSeq"]

    def official_video(self) -> Union[OfficialVideoVOD, OfficialVideoLive]:
        if self.official_video_type == "LIVE":
            return OfficialVideoLive(self.video_seq, session=self.session)
        elif self.official_video_type == "VOD":
            return OfficialVideoVOD(self.video_seq, session=self.session)
        else:
            raise ModelInitError("Unknown official video type. please report issue with self.raw")


class Schedule(DataModel):
    def __init__(self, schedule_id, session):
        super().__init__(getScheduleData, schedule_id, session=session)

    def __repr__(self):
        return "<VLIVE Schedule [%s]>" % self._target_id

    @property
    def schedule_id(self) -> str:
        return self._target_id

    @property
    def author(self) -> dict:
        return deepcopy(self._data_cache['author'])

    @property
    def author_nickname(self) -> str:
        return self._data_cache['author']['nickname']

    @property
    def author_id(self) -> str:
        return self._data_cache['author']


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


class GroupedBoards(DataModel):
    def __init__(self, channel_code, session=None):
        super().__init__(getGroupedBoards, channel_code, session)

    def __repr__(self):
        return "<VLIVE GroupedBoards in [%s]>" % self.target_id

    def groups(self) -> list:
        group_names = []
        for item in self._data_cache:
            group_names.append(item['groupTitle'])

        return group_names

    def boards(self) -> list:
        board_list = []
        for item in self._data_cache:
            for board in item['boards']:
                board_list.append(board)

        return deepcopy(board_list)

    def board_names(self) -> list:
        name_list = []
        for item in self.boards():
            name_list.append(item['title'])

        return name_list


class Channel(DataModel):
    def __init__(self, channel_code, session=None):
        super().__init__(getChannelInfo, channel_code, session)

    def __repr__(self):
        return "<VLIVE Channel [%s]>" % self._target_id

    @property
    def channel_code(self) -> str:
        return self._target_id

    @property
    def channel_name(self) -> str:
        return self._data_cache['channelName']

    @property
    def representative_color(self) -> str:
        return self._data_cache['representativeColor']

    @property
    def background_color(self) -> str:
        return self._data_cache['backgroundColor']

    @property
    def channel_profile_image(self) -> str:
        return self._data_cache['channelProfileImage']

    @property
    def channel_cover_image(self) -> str:
        return self._data_cache['channelCoverImage']

    @property
    def channel_description(self) -> str:
        return self._data_cache['channelDescription']

    @property
    def prohibited_word_like_list(self) -> list:
        return deepcopy(self._data_cache['prohibitedWordLikeList'])

    @property
    def prohibited_word_exact_list(self) -> list:
        return deepcopy(self._data_cache['prohibitedWordExactList'])

    @property
    def sns_share_img(self) -> str:
        return self._data_cache['snsShareImg']

    @property
    def qr_code(self) -> str:
        return self._data_cache['qrCode']

    @property
    def open_at(self) -> int:
        return self._data_cache['openAt'] // 1000
    
    @property
    def show_upcoming(self) -> bool:
        return self._data_cache['showUpcoming']
    
    @property
    def use_member_level(self) -> bool:
        return self._data_cache['useMemberLevel']
    
    @property
    def member_count(self) -> int:
        return self._data_cache['memberCount']
    
    @property
    def post_count(self) -> int:
        return self._data_cache['postCountOfStar']

    @property
    def video_count(self) -> int:
        return self._data_cache['videoCountOfStar']

    @property
    def video_play_count(self) -> int:
        return self._data_cache['videoPlayCountOfStar']

    @property
    def video_like_count(self) -> int:
        return self._data_cache['videoLikeCountOfStar']

    @property
    def video_comment_count(self) -> int:
        return self._data_cache['videoCommentCountOfStar']

    def decode_channel_code(self) -> int:
        return decode_channel_code(self.channel_code)

    def groupedBoards(self) -> GroupedBoards:
        return GroupedBoards(self.channel_code, self.session)
