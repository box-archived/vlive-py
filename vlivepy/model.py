# -*- coding: utf-8 -*-

from __future__ import annotations

from copy import deepcopy
from time import time
from typing import (
    Callable,
    Generator,
    List,
    Optional,
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
from .html_template import (
    formatted_body_template,
    video_box_template
)
from .parser import (
    format_epoch,
    max_res_from_play_info,
    v_timestamp_parser,
)
from .post import getFVideoPlayInfo
from .schedule import getScheduleData
from .session import UserSession
from .upcoming import (
    getUpcomingList,
    UpcomingVideo
)
from .video import (
    getInkeyData,
    getLivePlayInfo,
    getLiveStatus,
    getOfficialVideoData,
    getVodPlayInfo
)


class DataModel(object):
    """This is the base object for other class objects.
    It sends request with method from each modules and caching response.

    DataModels and its child objects are able to compare equality.
    Each objects are considered equal, if their :obj:`type` and :obj:`target_id` is equal.

    Note:
        This is the base object for other object without independent usage.

    Arguments:
        method (:class:`typing.Callable`) : function for loading data.
        target_id (:class:`str`) : argument for `method`.
        session (:class:`UserSession`, optional) : session for `method`, defaults to None.
        init_data (:class:`dict`, optional) : set initial data instead of loading data, defaults to None.

    Attributes:
        session (:class:`UserSession`) : session for method

    """

    __slots__ = ['_data_cache', '_target_id', 'session', '_method']

    def __init__(
            self,
            method: Callable,
            target_id: str,
            session: Optional[UserSession] = None,
            init_data: Optional[dict] = None
    ):
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

    def refresh(self) -> None:
        """Reload self data."""
        res = self._method(self._target_id, session=self.session, silent=True)
        if res:
            self._data_cache = res
        else:
            warn("Failed to refresh %s" % self, ModelRefreshWarning)

    @property
    def raw(self) -> dict:
        """Get full data as deep-copied dict.

        :rtype: :class:`dict`
        """
        return deepcopy(self._data_cache)

    @property
    def target_id(self):
        """Get internal target id.

        :rtype: :class:`str`
        """
        return str(self._target_id)


class Comment(DataModel):
    """This is the object represents a comment of VLIVE's post

    Arguments:
        commentId (:class:`str`) : Unique id of comment to load.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.
        init_data (:class:`dict`, optional) : set initial data instead of loading data, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.
    """

    def __init__(
            self,
            commentId: str,
            session: Optional[UserSession] = None,
            init_data: Optional[dict] = None
    ):
        super().__init__(getCommentData, commentId, session=session, init_data=init_data)

    def __repr__(self):
        return "<Comment [%s]>" % self._target_id

    @property
    def commentId(self) -> str:
        """Unique id of comment.

        :rtype: :class:`str`
        """
        return self._target_id

    @property
    def author(self) -> dict:
        """Detailed author info of post.

        :rtype: :class:`dict`
        """
        return deepcopy(self._data_cache['author'])

    @property
    def author_nickname(self) -> str:
        """Author nickname.

        :rtype: :class:`str`
        """
        return self._data_cache['author']['nickname']

    @property
    def author_memberId(self) -> str:
        """Unique id of author.

        :rtype: :class:`str`
        """
        return self._data_cache['author']['memberId']

    @property
    def body(self) -> str:
        """Content of comment.

        :rtype: :class:`str`
        """
        return self._data_cache['body']

    @property
    def sticker(self) -> list:
        """Sticker list of comment.

        :rtype: :class:`list`
        """
        return deepcopy(self._data_cache['sticker'])

    @property
    def created_at(self) -> float:
        """Epoch timestamp about created time.
        The nanosecond units are displayed below the decimal point.

        :rtype: :class:`float`
        """
        return v_timestamp_parser(self._data_cache['createdAt'])

    @property
    def comment_count(self) -> int:
        """Count of its nested comments.

        :rtype: :class:`int`
        """
        return self._data_cache['commentCount']

    @property
    def emotion_count(self) -> int:
        """Count of received emotion.

        :rtype: :class:`int`
        """
        return self._data_cache['emotionCount']

    @property
    def is_restricted(self) -> bool:
        return self._data_cache['isRestricted']

    @property
    def parent(self) -> dict:
        """Detailed information about parent(upper) item.

        :rtype: :class:`dict`
        """
        return deepcopy(self._data_cache['parent'])

    @property
    def root(self) -> dict:
        """Detailed information about root post.

        :rtype: :class:`dict`
        """
        return deepcopy(self._data_cache['root'])

    @property
    def written_in(self) -> str:
        """User language setting of comment.

        :rtype: :class:`str`
        """
        return self._data_cache['writtenIn']

    def getNestedCommentsIter(self) -> Generator[Comment]:
        """Get nested comments as iterable (generator).

        :rtype: :class:`Generator[Comment]`
        """
        return getNestedCommentsIter(self.commentId, session=self.session)

    def parent_info_tuple(self) -> tuple:
        """Get parent info as tuple (Parent type, Its(parent) id)

        :rtype: :class:`tuple`
        """
        tp = self.parent['type']
        key = "%sId" % tp.lower()
        return self.parent['type'], self.parent['data'][key]

    def root_info_tuple(self) -> tuple:
        """Get root info as tuple (Root type, Its(root) id)

        :rtype: :class:`tuple`
        """
        tp = self.root['type']
        key = "%sId" % tp.lower()
        return tp, self.root['data'][key]


class OfficialVideoModel(DataModel):
    """This is the base object for :class:`OfficialVideoLive` and :class:`OfficialVideoVOD`
    This contains common property of Live and VOD object.

    Note:
        This is the base object for other object without independent usage.

    Arguments:
        video_seq (:class:`Union[str, int]`) : Unique id(seq) of video.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.

    """
    def __init__(
            self,
            video_seq: Union[str, int],
            session: Optional[UserSession] = None
    ):
        super().__init__(getOfficialVideoData, video_seq, session=session)

    @property
    def video_seq(self) -> int:
        """Unique id(seq) of video.

        :rtype: :class:`str`
        """
        return self._data_cache['videoSeq']

    @property
    def video_type(self) -> str:
        """Type of video.

        Returns:
            "LIVE" if the video is upcoming/on air live. "VOD" if the video is VOD.

        :rtype: :class:`str`
        """
        return self._data_cache['type']

    @property
    def title(self) -> str:
        """Title of video.

        :rtype: :class:`str`
        """
        return self._data_cache['title']

    @property
    def multinational_titles(self) -> List[dict]:
        """Title translations.

        :rtype: :class:`List[dict]`
        """
        return deepcopy(self._data_cache['multinationalTitles'])

    def multinational_title_locales(self) -> list:
        """Get locales from multinational title.

        :rtype: :class:`list`
        """
        locale_list = []
        for item in self._data_cache['multinationalTitles']:
            locale_list.append(item['locale'])

        return locale_list

    def multinational_title_get(self, locale) -> dict:
        """Get multinational title info by locale.

        Arguments:
            locale (:class:`str`) : locale to load.

        :rtype: :class:`dict`
        """
        for item in self._data_cache['multinationalTitles']:
            if item['locale'] == locale:
                return item.copy()
        else:
            raise KeyError

    @property
    def play_count(self) -> int:
        """Count of video play time.

        :rtype: :class:`int`
        """
        return self._data_cache['playCount']

    @property
    def like_count(self) -> int:
        """Count of like received in video.

        :rtype: :class:`int`
        """
        return self._data_cache['likeCount']

    @property
    def comment_count(self) -> int:
        """Count of comment in video.

        :rtype: :class:`int`
        """
        return self._data_cache['commentCount']

    @property
    def thumb(self) -> str:
        """Url of thumbnail.

        :rtype: :class:`str`
        """
        return self._data_cache['thumb']

    @property
    def expose_status(self) -> str:
        """Exposed-on-website status of video.

        :rtype: bool
        """
        return self._data_cache['exposeStatus']

    @property
    def screen_orientation(self) -> str:
        """Orientation of video.

        Returns:
            "VERTICAL" if the video orientation is vertical. "HORIZONTAL" if the video orientation is horizontal.

        :rtype: str
        """
        return self._data_cache['screenOrientation']

    @property
    def will_start_at(self) -> float:
        """Epoch timestamp about Unknown.
        The nanosecond units are displayed below the decimal point.

        :rtype: :class:`float`
        """
        return v_timestamp_parser(self._data_cache['willStartAt'])

    @property
    def on_air_start_at(self) -> float:
        """Epoch timestamp about reserved/started on air time.
        The nanosecond units are displayed below the decimal point.

        :rtype: :class:`float`
        """
        return v_timestamp_parser(self._data_cache['onAirStartAt'])

    @property
    def will_end_at(self) -> float:
        """Epoch timestamp about reserved end time.
        The nanosecond units are displayed below the decimal point.

        :rtype: :class:`float`
        """
        return v_timestamp_parser(self._data_cache['willEndAt'])

    @property
    def created_at(self) -> float:
        """Epoch timestamp about Unknown.
        The nanosecond units are displayed below the decimal point.

        :rtype: :class:`float`
        """
        return v_timestamp_parser(self._data_cache['createdAt'])

    @property
    def has_live_thumb(self) -> bool:
        """Boolean value for having live thumbnail or not.

        :rtype: :class:`bool`
        """
        return self._data_cache['liveThumbYn']

    @property
    def has_upcoming(self) -> bool:
        """Boolean value for having upcoming.

        :rtype: :class:`bool`
        """
        return self._data_cache['upcomingYn']

    @property
    def has_notice(self) -> bool:
        """Boolean value for having notice.

        :rtype: :class:`bool`
        """
        return self._data_cache['noticeYn']

    @property
    def product_type(self) -> str:
        """Product type about VLIVE+

        Returns:
            "NONE" if the video is normal video. "VLIVE_PLUS" if the video is VLIVE+.

        :rtype: :class:`str`
        """
        return self._data_cache['productType']

    @property
    def has_pre_ad(self) -> bool:
        """Boolean value for having pre advertise.

        :rtype: :class:`bool`
        """
        return self._data_cache['preAdYn']

    @property
    def has_post_ad(self) -> bool:
        """Boolean value for having post advertise.

        :rtype: :class:`bool`
        """
        return self._data_cache['postAdYn']

    @property
    def has_mobile_da(self) -> bool:
        """Boolean value for Unknown.

        :rtype: :class:`bool`
        """
        return self._data_cache['mobileDAYn']

    @property
    def vr_content_type(self) -> str:
        """String value for vr content type.

        :rtype: :class:`str`
        """
        return self._data_cache['vrContentType']


class OfficialVideoLive(OfficialVideoModel):
    """This is the object represents a Live-type-OfficialVideo of VLIVE

    Arguments:
        video_seq (:class:`str`) : Unique id of Live to load.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.
    """

    def __init__(
            self,
            video_seq: Union[int, str],
            session: Optional[UserSession] = None
    ):
        super().__init__(video_seq, session=session)
        if self.video_type != "LIVE":
            raise ValueError("OfficialVideo [%s] is not Live." % video_seq)

    def __repr__(self):
        return "<VLIVE OfficialVideo-Live [%s]>" % self.target_id

    @property
    def has_filter_ad(self) -> bool:
        """Boolean value for having filter ad

        :rtype: :class:`bool`
        """
        return self._data_cache['filterAdYn']

    @property
    def momentable(self) -> bool:
        """Boolean value for what user can create moment of the video

        :rtype: :class:`bool`
        """
        return self._data_cache['momentable']

    @property
    def has_special_live(self) -> bool:
        """Boolean value for having special live

        :rtype: :class:`bool`
        """
        return self._data_cache['specialLiveYn']

    @property
    def status(self) -> str:
        """Status of the live

        Returns:
            "RESERVED" if the live is reserved to broadcast.
            "ON_AIR" if the live is going.
            "ENDED" if the live is ended.

        :rtype: :class:`str`
        """
        return self._data_cache['status']

    @property
    def hevc(self) -> bool:
        """Boolean value for broadcasting with hevc codec.

        :rtype: :class:`bool`
        """
        return self._data_cache['hevc']

    @property
    def low_latency(self) -> bool:
        """Boolean value for broadcasting with low-latency option

        :rtype: :class:`bool`
        """
        return self._data_cache['lowLatency']

    @property
    def pp_type(self) -> str:
        """Unknown boolean value

        :rtype: :class:`bool`
        """
        return self._data_cache['ppType']

    def getLivePlayInfo(self, silent=False):
        """Get play info of live

        Arguments:
            silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

        :rtype: :class:`dict`
        """
        return getLivePlayInfo(self.video_seq, session=self.session, silent=silent)

    def getLiveStatus(self, silent=False):
        """Get detailed status of live.

        Arguments:
            silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

        :rtype: :class:`dict`
        """
        return getLiveStatus(self.video_seq, silent=silent)


class OfficialVideoVOD(OfficialVideoModel):
    """This is the object represents a VOD-type-OfficialVideo of VLIVE

    Arguments:
        video_seq (:class:`str`) : Unique id of VOD to load.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.
    """

    def __init__(
            self,
            video_seq: Union[str, int],
            session: Optional[UserSession] = None
    ):
        super().__init__(str(video_seq), session=session)
        if self.video_type != "VOD":
            raise ValueError("OfficialVideo [%s] is not VOD." % video_seq)

    def __repr__(self):
        return "<VLIVE OfficialVideo-VOD [%s]>" % self.target_id

    @property
    def has_preview(self) -> bool:
        """Boolean value for having 30s preview video

        :rtype: :class:`bool`
        """
        return self._data_cache['previewYn']

    @property
    def has_moment(self) -> bool:
        """Boolean value for having user-created-moments

        :rtype: :class:`bool`
        """
        return self._data_cache['hasMoment']

    @property
    def vod_id(self) -> str:
        """Unique id of VOD that paired with videoSeq

        :rtype: :class:`bool`
        """
        return self._data_cache['vodId']

    @property
    def play_time(self) -> int:
        """Count of video play

        :rtype: :class:`int`
        """
        return self._data_cache['playTime']

    @property
    def encoding_status(self) -> str:
        """VOD encoding status

        Returns:
            "CONVERTING" if the video encoding is in progress. "COMPLETE" if the video encoding is done.

        :rtype: :class:`str`
        """
        return self._data_cache['encodingStatus']

    @property
    def vod_secure_status(self) -> str:
        """Status of DRM protection

        Returns:
            "READY" if the DRM is ready but not applied to video. "COMPLETE" if the DRM is applied to video.

        :rtype: :class:`str`
        """
        return self._data_cache['vodSecureStatus']

    @property
    def dimension_type(self) -> str:
        """Unknown value. Server commonly respond "NORMAL"

        :rtype: :class:`str`
        """
        return self._data_cache['dimensionType']

    def recommended_videos(
            self,
            as_object: bool = False
    ) -> list:
        """Get recommended video list

        Arguments:
            as_object (:class:`bool`, optional) : Init each item to :class:`OfficialVideoPost`, defaults to False.

        :rtype: :class:`list`
        """
        if as_object:
            video_list = []
            for item in self._data_cache['recommendedVideos']:
                video_list.append(OfficialVideoPost(item['videoSeq']))

            return video_list
        else:
            return deepcopy(self._data_cache['recommendedVideos'])

    def getInkeyData(
            self,
            silent: bool = False
    ) -> dict:
        """Get InKey data of video

        Arguments:
            silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

        :rtype: :class:`dict`
        """
        return getInkeyData(self.video_seq, session=self.session, silent=silent)

    def getVodPlayInfo(
            self,
            silent: bool = False
    ) -> dict:
        """Get VOD play info of video

        Arguments:
            silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

        :rtype: :class:`dict`
        """
        return getVodPlayInfo(self.video_seq, self.vod_id, session=self.session, silent=silent)


class PostModel(DataModel):

    """This is the base object for :class:`Post` and :class:`OfficialVideoPost`
    This contains common property of each object

    :class:`OfficialVideoPost` has :class:`OfficialVideoModel` and doesn't have :obj:`body`
    compared with :class:`Post`

    Note:
        This is the base object for other object without independent usage.

    Arguments:
        post_id (:class:`str`) : Unique id of post to load.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.

    """

    def __init__(
            self,
            post_id: str,
            session: Optional[UserSession] = None
    ):
        super().__init__(getPostInfo, post_id, session=session)

    @property
    def attachments(self) -> dict:
        """Detailed attachments data of post.

        :rtype: :class:`dict`
        """
        return deepcopy(self._data_cache['attachments'])

    @property
    def attachments_photo(self) -> dict:
        """Detailed photo attachments data of post.

        :rtype: :class:`dict`
        """
        if 'photo' in self._data_cache['attachments']:
            return deepcopy(self._data_cache['attachments']['photo'])
        else:
            return {}

    @property
    def attachments_video(self) -> dict:
        """Detailed video attachments data of post.

        :rtype: :class:`dict`
        """
        if 'video' in self._data_cache['attachments']:
            return deepcopy(self._data_cache['attachments']['video'])
        else:
            return {}

    @property
    def author(self) -> dict:
        """Detailed author info of post.

        :rtype: :class:`dict`
        """
        return deepcopy(self._data_cache['author'])

    @property
    def author_nickname(self) -> str:
        """Author nickname.

        :rtype: :class:`str`
        """
        return self._data_cache['author']['nickname']

    @property
    def author_id(self) -> str:
        """Unique id of author.

        :rtype: :class:`str`
        """
        return self._data_cache['author']['memberId']

    @property
    def created_at(self) -> float:
        """Epoch timestamp about created time.
        The nanosecond units are displayed below the decimal point.

        :rtype: :class:`float`
        """
        return v_timestamp_parser(self._data_cache['createdAt'])

    @property
    def board_id(self) -> int:
        """Unique id of parent board

        :rtype: :class:`int`
        """
        return self._data_cache['boardId']

    @property
    def channel_name(self) -> str:
        """The name of the channel that contains the post

        :rtype: :class:`str`
        """
        return self._data_cache['channel']['channelName']

    @property
    def channel_code(self) -> str:
        """The code of the channel that contains the post

        :rtype: :class:`str`
        """
        return self._data_cache['channelCode']

    @property
    def comment_count(self) -> int:
        """Count of its comment

        :rtype: :class:`int`
        """
        return self._data_cache['commentCount']

    @property
    def content_type(self) -> str:
        """Type of post.

        Returns:
            "POST" if the post is normal Post.
            "VIDEO" if the post is OfficialVideoPost

        :rtype: :class:`str`
        """
        return self._data_cache['contentType']

    @property
    def emotion_count(self) -> int:
        """Count of received emotion.

        :rtype: :class:`int`
        """
        return self._data_cache['emotionCount']

    @property
    def is_comment_enabled(self) -> bool:
        """Boolean value for comment-enabled.

        :rtype: :class:`bool`
        """
        return self._data_cache['isCommentEnabled']

    @property
    def is_hidden_from_star(self) -> bool:
        """Boolean value for hidden-from-star.

        :rtype: :class:`bool`
        """
        return self._data_cache['isHiddenFromStar']

    @property
    def is_viewer_bookmarked(self) -> bool:
        """Boolean value for viewer-bookmarked.

        :rtype: :class:`bool`
        """
        return self._data_cache['isViewerBookmarked']

    @property
    def post_id(self) -> str:
        """Unique id of the post.

        :rtype: :class:`str`
        """
        return self._target_id

    @property
    def title(self) -> str:
        """Title of the post.

        :rtype: :class:`str`
        """
        return self._data_cache['title']

    def getPostCommentsIter(self) -> Generator[Comment, None, None]:
        """Get Its comments as iterable

        :rtype: :class:`Generator[Comment, None, None]`

        Yields:
            :class:`Comment`
        """
        return getPostCommentsIter(self.post_id, session=self.session)

    def getPostStarCommentsIter(self) -> Generator[Comment, None, None]:
        """Get Its star-comments as iterable

        :rtype: :class:`Generator[Comment, None, None]`

        Yields:
            :class:`Comment`
        """
        return getPostStarCommentsIter(self.post_id, session=self.session)


class Post(PostModel):
    """This is the object represents a post of VLIVE

    Arguments:
        post_id (:class:`str`) : Unique id of post to load.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.
    """

    def __init__(
            self,
            post_id: str,
            session: Optional[UserSession] = None
    ):
        super().__init__(post_id, session)

    def __repr__(self):
        return "<VLIVE Post [%s]>" % self.post_id

    @property
    def plain_body(self) -> str:
        """Text-only contents of post

        :rtype: :class:`str`
        """
        return self._data_cache['plainBody']

    @property
    def body(self) -> str:
        """Contents of post with ``<v:attachment>`` tag

        :rtype: :class:`str`
        """
        return self._data_cache['body']

    @property
    def written_in(self) -> str:
        """User language setting of post.

        :rtype: :class:`str`
        """
        return self._data_cache['writtenIn']

    def formatted_body(self) -> str:
        """Get contents of post with formatting attachments and styles as html.

        :rtype: :class:`str`
        """
        # load Template
        video_template = video_box_template
        doc_template = formatted_body_template

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
                    f_video_id=at_data['videoId'],
                    f_vod_id=at_data['uploadInfo']['videoId'],
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


class OfficialVideoPost(PostModel):
    """This is the object represents a post of VLIVE

    Arguments:
        init_id (:class:`Union[str, int]`) : Unique id of post to load.
            Also, the object can be initialized by video_seq.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.
    """

    def __init__(
            self, 
            init_id: Union[str, int],
            session: Optional[UserSession] = None
    ):
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
        """Type of video.

        Returns:
            "LIVE" if the video is upcoming/on air live. "VOD" if the video is VOD.

        :rtype: :class:`str`
        """
        return self._data_cache['officialVideo']['type']

    @property
    def video_seq(self) -> str:
        """Unique id of OfficialVideoPost. (video_seq type)

        :rtype: :class:`str`
        """
        return self._data_cache["officialVideo"]["videoSeq"]

    def official_video(self) -> Union[OfficialVideoVOD, OfficialVideoLive]:
        """Generate :class:`OfficialVideoLive` or :class:`OfficialVideoVOD` object that paired to official video posts

        :return: :class:`OfficialVideoVOD`, if the video is VOD.
        :return: :class:`OfficialVideoLive`, if the video is Live.
        """
        if self.official_video_type == "LIVE":
            return OfficialVideoLive(self.video_seq, session=self.session)
        elif self.official_video_type == "VOD":
            return OfficialVideoVOD(self.video_seq, session=self.session)
        else:
            raise ModelInitError("Unknown official video type. please report issue with self.raw")


class Schedule(DataModel):
    """This is the object represents a post of VLIVE.

   Arguments:
       schedule_id (:class:`Union[str, int]`) : Unique id of schedule to load.
       session (:class:`UserSession`) : Session for loading data with permission.

   Attributes:
       session (:class:`UserSession`) : Session for loading data with permission.
   """

    def __init__(
            self,
            schedule_id: str,
            session: UserSession
    ):
        super().__init__(getScheduleData, schedule_id, session=session)

    def __repr__(self):
        return "<VLIVE Schedule [%s]>" % self._target_id

    @property
    def schedule_id(self) -> str:
        """Unique id of schedule.

        :rtype: :class:`str`
        """
        return self._target_id

    @property
    def author(self) -> dict:
        """Detailed author info of post.

        :rtype: :class:`dict`
        """
        return deepcopy(self._data_cache['author'])

    @property
    def author_nickname(self) -> str:
        """Author nickname.

        :rtype: :class:`str`
        """
        return self._data_cache['author']['nickname']

    @property
    def author_id(self) -> str:
        """Unique id of author.

        :rtype: :class:`str`
        """
        return self._data_cache['author']['memberId']
    
    @property
    def channel_code(self) -> str:
        """The code of the channel that contains the schedule.

        :rtype: :class:`str`
        """
        return self._data_cache['channel']['channelCode']
    
    @property
    def channel_name(self) -> str:
        """The name of the channel that contains the post.

        :rtype: :class:`str`
        """
        return self._data_cache['channel']['channelName']
    
    @property
    def comment_count(self) -> int:
        """Count of comment in video.

        :rtype: :class:`int`
        """
        return self._data_cache['commentCount']

    @property
    def emotion_count(self) -> int:
        """Count of received emotion in video.

        :rtype: :class:`int`
        """
        return self._data_cache['emotionCount']

    @property
    def official_video_type(self) -> str:
        """Type of video.

        Returns:
            "LIVE" if the video is upcoming/on air live. "VOD" if the video is VOD.

        :rtype: :class:`str`
        """
        return self._data_cache['officialVideo']['type']

    @property
    def video_seq(self) -> str:
        """videoSeq id that paired with the schedule.

        :rtype: :class:`str`
        """
        return self._data_cache["videoSeq"]

    @property
    def post_id(self) -> str:
        """Post id that paired with the schedule.

        :rtype: :class:`str`
        """
        return self._data_cache['postId']

    @property
    def title(self) -> str:
        """Title of the schedule.

        :rtype: :class:`str`
        """
        return self._data_cache['title']

    def official_video(self) -> Union[OfficialVideoVOD, OfficialVideoLive]:
        """Generate :class:`OfficialVideoLive` or :class:`OfficialVideoVOD` object that paired to schedule

        :return: :class:`OfficialVideoVOD`, if the video is VOD.
        :return: :class:`OfficialVideoLive`, if the video is Live.
        """
        if self.official_video_type == "LIVE":
            return OfficialVideoLive(self.video_seq, session=self.session)
        elif self.official_video_type == "VOD":
            return OfficialVideoVOD(self.video_seq, session=self.session)
        else:
            raise ModelInitError("Unknown official video type. please report issue with self.raw")


class Upcoming(object):
    """This is the object represents a upcoming list of VLIVE.

    This object doesn't use endpoint API but use parsing upcoming webpage.
    This use refresh rate to caching result.
    Set :obj:`refresh_rate` to 0 to disable caching

    See Also:
        This object mainly returns list of :class:`vlivepy.parser.UpcomingVideo`. Check docs!

    Arguments:
        refresh_rate (:class:`float`, optional) : Unique id of post to load.
            Also, the object can be initialized by video_seq.
            Defaults to 5
        show_vod (:class:`bool`, optional) : Add VOD to upcoming list, defaults to True.
        show_upcoming_vod (:class:`bool`, optional) : Add reserved VOD to upcoming list, defaults to True.
        show_upcoming_live (:class:`bool`, optional) : Add reserved Live to upcoming list, defaults to True.
        show_live (:class:`bool`, optional) : Add on air live to upcoming list, defaults to True.

    Attributes:
        refresh_rate (:class:`float`) : Optional. Unique id of post to load.
            Also, the object can be initialized by video_seq.
            Defaults to 5
        show_vod (:class:`bool`) : Optional. Add VOD to upcoming list, defaults to True.
        show_upcoming_vod (:class:`bool`) : Optional. Add reserved VOD to upcoming list, defaults to True.
        show_upcoming_live (:class:`bool`) : Optional. Add reserved Live to upcoming list, defaults to True.
        show_live (:class:`bool`) : Optional. Add on air live to upcoming list, defaults to True.
    """

    def __init__(
            self,
            refresh_rate: float = 5,
            show_vod: bool = True,
            show_upcoming_vod: bool = True,
            show_upcoming_live: bool = True,
            show_live: bool = True
    ):
        self.refresh_rate = refresh_rate
        self.__cached_data = []
        self.__cached_time = 0
        self.show_live = show_live
        self.show_vod = show_vod
        self.show_upcoming_vod = show_upcoming_vod
        self.show_upcoming_live = show_upcoming_live

        # refresh data
        self.refresh(True)

    def refresh(
            self,
            force: bool = False
    ) -> None:
        """Refresh self data

        Arguments:
            force (:class:`bool`, optional) : Force refresh with ignoring refresh rate, defaults to False.
        """
        distance = time() - self.__cached_time
        if distance >= self.refresh_rate or force:
            new_data = self.load(date=None, silent=True,
                                 show_vod=True, show_upcoming_vod=True,
                                 show_live=True, show_upcoming_live=True)
            if new_data is not None:
                self.__cached_data = new_data
                self.__cached_time = int(time())

    def load(
            self,
            date: Optional[str],
            show_vod: Optional[bool] = None,
            show_upcoming_vod: Optional[bool] = None,
            show_upcoming_live: Optional[bool] = None,
            show_live: Optional[bool] = None,
            silent: Optional[bool] = False
    ) -> Optional[List[UpcomingVideo]]:
        """Get upcoming list data with specific date

        Note:
            Use :func:`upcoming` instead of using this function to load current upcoming.

        Arguments:
            date (:class:`bool`) : Specify date to load upcoming.
            show_vod (:class:`bool`, optional) : Add VOD to upcoming list,
                defaults to :obj:`self.show_vod`
            show_upcoming_vod (:class:`bool`, optional) : Add reserved VOD to upcoming list,
                defaults to :obj:`self.show_upcoming_vod`
            show_upcoming_live (:class:`bool`, optional) : Add reserved Live to upcoming list,
                defaults to :obj:`self.show_upcoming_live`
            show_live (:class:`bool`, optional) : Add on air live to upcoming list,
                defaults to :obj:`self.show_live`
            silent (:class:`bool`, optional) : Return None instead of raising exception, defaults to False.

        Returns:
            List of :class:`vlivepy.parser.UpcomingVideo`
        """
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

    def upcoming(
            self, 
            force=False, 
            show_vod: Optional[bool] = None, 
            show_upcoming_vod: Optional[bool] = None, 
            show_upcoming_live: Optional[bool] = None, 
            show_live: Optional[bool] = None
    ) -> List[UpcomingVideo]:
        """Upcoming list with cache life check

        Arguments:
            force (:class:`bool`, optional) : Force refresh with ignoring refresh rate, defaults to False.
            show_vod (:class:`bool`, optional) : Add VOD to upcoming list,
                defaults to :obj:`self.show_vod`
            show_upcoming_vod (:class:`bool`, optional) : Add reserved VOD to upcoming list,
                defaults to :obj:`self.show_upcoming_vod`
            show_upcoming_live (:class:`bool`, optional) : Add reserved Live to upcoming list,
                defaults to :obj:`self.show_upcoming_live`
            show_live (:class:`bool`, optional) : Add on air live to upcoming list,
                defaults to :obj:`self.show_live`

        Returns:
            List of :class:`vlivepy.parser.UpcomingVideo`
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
    """This is the object represents board list of channel.

    Arguments:
        channel_code (:class:`str`) : Unique id of channel.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.
    """
    def __init__(
            self,
            channel_code: str,
            session: Optional[UserSession] = None
    ):
        super().__init__(getGroupedBoards, channel_code, session)

    def __repr__(self):
        return "<VLIVE GroupedBoards in [%s]>" % self.target_id

    def groups(self) -> List[str]:
        """Get name of board-groups

        :rtype: :class:`list`
        """
        group_names = []
        for item in self._data_cache:
            group_names.append(item['groupTitle'])

        return group_names

    def boards(self) -> List[dict]:
        """Get detailed info of boards

        :rtype: :class:`List[dict]`
        """
        board_list = []
        for item in self._data_cache:
            for board in item['boards']:
                board_list.append(board)

        return deepcopy(board_list)

    def board_names(self) -> List[str]:
        """Get name of the boards

        :rtype: :class:`list`
        """
        name_list = []
        for item in self.boards():
            name_list.append(item['title'])

        return name_list


class Channel(DataModel):
    """This is the object represents a post of VLIVE

    Arguments:
        channel_code (:class:`str`) : Unique id of channel.
        session (:class:`UserSession`, optional) : Session for loading data with permission, defaults to None.

    Attributes:
        session (:class:`UserSession`) : Optional. Session for loading data with permission.
    """

    def __init__(
            self,
            channel_code: str,
            session: Optional[UserSession] = None
    ):
        super().__init__(getChannelInfo, channel_code, session)

    def __repr__(self):
        return "<VLIVE Channel [%s]>" % self._target_id

    @property
    def channel_code(self) -> str:
        """Unique id of channel.

        :rtype: :class:`str`
        """
        return self._target_id

    @property
    def channel_name(self) -> str:
        """Name of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['channelName']

    @property
    def representative_color(self) -> str:
        """Representative color(hex) of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['representativeColor']

    @property
    def background_color(self) -> str:
        """Background color(hex) of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['backgroundColor']

    @property
    def channel_profile_image(self) -> str:
        """Profile image url of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['channelProfileImage']

    @property
    def channel_cover_image(self) -> str:
        """Cover image url of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['channelCoverImage']

    @property
    def channel_description(self) -> str:
        """Description of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['channelDescription']

    @property
    def prohibited_word_like_list(self) -> list:
        """Prohibited word (LIKE) in the channel.

        :rtype: :class:`str`
        """
        return deepcopy(self._data_cache['prohibitedWordLikeList'])

    @property
    def prohibited_word_exact_list(self) -> list:
        """Prohibited word (EXACT) in the channel.

        :rtype: :class:`str`
        """
        return deepcopy(self._data_cache['prohibitedWordExactList'])

    @property
    def sns_share_img(self) -> str:
        """SNS Share image url of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['snsShareImg']

    @property
    def qr_code(self) -> str:
        """QR code image url of the channel.

        :rtype: :class:`str`
        """
        return self._data_cache['qrCode']

    @property
    def open_at(self) -> int:
        """Epoch timestamp about channel opened(created) time.

        :return:
        """
        return self._data_cache['openAt'] // 1000

    @property
    def show_upcoming(self) -> bool:
        """Boolean value for using upcoming in the channel

        :rtype: :class:`bool`
        """
        return self._data_cache['showUpcoming']

    @property
    def use_member_level(self) -> bool:
        """Boolean value for using member level in the channel

        :rtype: :class:`bool`
        """
        return self._data_cache['useMemberLevel']

    @property
    def member_count(self) -> int:
        """Count of members in channel.

        :rtype: :class:`int`
        """
        return self._data_cache['memberCount']

    @property
    def post_count(self) -> int:
        """Count of post in channel.

        :rtype: :class:`int`
        """
        return self._data_cache['postCountOfStar']

    @property
    def video_count(self) -> int:
        """Count of video in channel.

        :rtype: :class:`int`
        """
        return self._data_cache['videoCountOfStar']

    @property
    def video_play_count(self) -> int:
        """Count of video play times in channel.

        :rtype: :class:`int`
        """
        return self._data_cache['videoPlayCountOfStar']

    @property
    def video_like_count(self) -> int:
        """Count of like in channel.

        :rtype: :class:`int`
        """
        return self._data_cache['videoLikeCountOfStar']

    @property
    def video_comment_count(self) -> int:
        """Count of video comment in channel.

        :rtype: :class:`int`
        """
        return self._data_cache['videoCommentCountOfStar']

    def decode_channel_code(self) -> int:
        """Decode channel code to unique channel seq

        :rtype: :class:`int`
        """
        return decode_channel_code(self.channel_code)

    def groupedBoards(self) -> GroupedBoards:
        """Load grouped board list of the channel

        :rtype: :class:`GroupedBoards`
        """
        return GroupedBoards(self.channel_code, self.session)
