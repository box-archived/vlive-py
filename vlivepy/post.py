from bs4 import BeautifulSoup, element
from .api import getPostInfo, getFVideoPlayInfo
from .parser import max_res_from_play_info, format_epoch
from .utils import getPostCommentsIter, getPostStarCommentsIter


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
        parsed = str(self.__cached_post['createdAt'])
        return float("%s.%s" % (parsed[:-3], parsed[-3:]))

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
                dom_obj.attrs['width'] = at_data['width']
                dom_obj.attrs['height'] = at_data['height']
                dom_obj.attrs["class"] = "photo"

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
                dom_obj.attrs['width'] = video['encodingOption']['width']
                dom_obj.attrs['height'] = video['encodingOption']['height']
                dom_obj.attrs['poster'] = at_data['uploadInfo']['imageUrl']
                dom_obj.attrs['controls'] = ""
                dom_obj.attrs["class"] = "video"

            else:
                dom_obj = ""

            dom_obj.attrs['style'] = "display: block;margin-bottom:10px;"
            item.replace_with(dom_obj)

        # add author
        html = ('<div style="padding:15px 0;border-bottom:1px solid #f2f2f2">'
                '<div><span class="author" style="font-weight:600;color:#111;font-size:14px">%s</span></div>'
                '<div><span class="createdAt" style="color:#777;font-size:12px">%s</span></div>'
                '</div>'
                % (self.author_nickname, format_epoch(self.created_at, "%Y.%m.%d %H:%M:%S")))

        # add title
        html += '<h2 class="title">%s</h2>' % self.title

        # add content
        html += str(soup)

        return html

    def getPostCommentsIter(self):
        return getPostCommentsIter(self.post_id, session=self.session)

    def getPostStarCommentsIter(self):
        return getPostStarCommentsIter(self.post_id, session=self.session)
