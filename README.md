> #### Language
> English [Korean](README.Korean.md)

# vlivepy
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/box-archived/vlive-py)](https://github.com/box-archived/vlive-py/releases/latest)
[![PyPI](https://img.shields.io/pypi/v/vlivepy)](https://pypi.org/project/vlivepy/)
[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/box-archived/vlive-py?include_prereleases&label=dev)](https://github.com/box-archived/vlive-py/releases/)
[![GitHub](https://img.shields.io/github/license/box-archived/vlive-py)](LICENSE)

vlivepy is reverse-engineered Python-based API of VLIVE(vlive.tv)

## Install
vlivepy can be installed via [PyPI](https://pypi.org/project/vlivepy/).
```console
$ python -m pip install vlivepy
```

---
# Documentation
## Contents
- [Contents](#Contents)
- [Before Entering](#before-entering)
    - [Terms](#Terms)
    - [Expression](#Expression)
- [API](#api)
    - [getUserSession()](#getusersession)
    - [getPostInfo()](#getpostinfo)
    - [getOfficialVideoPost()](#getofficialvideopost)
    - [getInkeyData()](#getinkeydata)
    - [getLivePlayInfo()](#getliveplayinfo)
    - [getLiveStatus()](#getlivestatus)
    - [getVodPlayInfo()](#getvodplayinfo)
    - [getPostComments()](#getpostcomments)
    - [getPostStarComments()](#getpoststarcomments)
- [Utils](#utils)
    - [utils.postIdToVideoSeq()](#utilspostidtovideoseq)
    - [utils.getVpdid2()](#utilsgetvpdid2)
    - [utils.getVodId()](#utilsgetvodid)
    - [utils.getUpcomingList()](#utilsgetupcominglist)
        - [UpcomingVideo](#upcomingvideo)
    - [utils.dumpSession()](#utilsdumpsession)
    - [utils.loadSession()](#utilsloadsession)
    - [utils.getPostCommentsIter()](#utilsgetpostcommentsiter)
        - [CommentItem](#commentitem)
    - [utils.getPostStarCommentsIter()](#utilsgetpoststarcommentsiter)
- [Video](#video)
    - [Properties](#videoproperties)
    - [Video.refresh()](#videorefresh)
    - [Video.getOfficialVideoPost()](#videogetofficialvideopost)
    - [Video.getLivePlayInfo()](#videogetliveplayinfo)
    - [Video.getInkeyData()](#videogetinkeydata)
    - [Video.getLiveStatus()](#videogetlivestatus)
    - [Video.getUserSession()](#videogetusersession)
    - [Video.loadSession()](#videoloadsession)
    - [Video.getVodPlayInfo()](#videogetvodplayinfo)
- [Upcoming](#upcoming)
    - [Upcoming.upcoming()](#upcomingupcoming)
    - [Upcoming.refresh()](#upcomingrefresh)
    - [Upcoming.load()](#upcomingload)
- [Post](#post)
    - [Post.Property](#postproperty)
    - [Post.formatted_body()](#postformatted_body)

## Before Entering
Learn about terms and expressions used in this document.

### Terms
- `videoSeq`: url of `~/video/` this is the six-digit code that follows. Points to the officialVideo on VLIVE.
- `postId`: url of `~/post/` following `0-12345678` the code of the form. Point to a post on VLIVE.
- `vodId`: It is a 36-digit Hex code used on VLIVE internally.
- `vpdid2`: It is a 64 digit Hex code representing the user.
- `inKey`: VOD the value used when loading information.

### Expression
Descriptions of parameters of functions or objects are written in code blocks. Arguments are written in the order they are declared within the function, and example values ​​are provided. Optional arguments are annotated with `# Optional` and default values ​​are provided as examples.

An example code block for functions and parameters is shown below.
```python
from vlivepy import getPostInfo

# The lines below are examples of functions and explanations of required arguments.
getPostInfo(post="0-12345678",
            # The lines below are examples of functions and explanations of optional arguments.
            session=None,  # Optional
            silent=False)  # Optional
```

## API
### getUserSession()
VLIVE By logging into the website [requests.Session](https://requests.readthedocs.io/en/master/user/advanced/) Returns the object. For login, [email login](https://www.vlive.tv/auth/email/login) method
```python
from vlivepy import getUserSession

getUserSession(email="user@email.id",
               pwd="userPassword!",
               silent=False)  # Optional
```
- `email`: Email ID of the account to log in.
- `pwd`: This is the password of the account to log in.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### getPostInfo()
Loads information from VLIVE Post via postId and returns a dict object.
```python
from vlivepy import getPostInfo

getPostInfo(post="0-12345678",
            session=None,  # Optional
            silent=False)  # Optional
```
`getPostInfo()` Functions have the following variables:
- `post`: Enter the postId.
- `session`: UserSession is required for posts that require membership authentication.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### getOfficialVideoPost()
Loads information from VLIVE Video via videoSeq and returns a dict object.
```python
from vlivepy import getOfficialVideoPost

getOfficialVideoPost(videoSeq="123456",
                     session=None,  # Optional
                     silent=False)  # Optional
```
- `videoSeq`: Enter the videoSeq of the image.
- `session`: UserSession is required for videos that require membership authentication.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### getInkeyData()
Load VLIVE VOD and inKey corresponding to your account information.
```python
from vlivepy import getInkeyData

getInkeyData(videoSeq="123456",
             session=None,  # Optional
             silent=False)  # Optional
```
- `videoSeq`: Enter the videoSeq of the image.
- `session`: UserSession is required for videos that require membership authentication.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### getLivePlayInfo()
Get information related to VLIVE LIVE playback.
```python
from vlivepy import getLivePlayInfo

getLivePlayInfo(videoSeq="123456",
                session=None,  # Optional
                vpdid2=None,  # Optional
                silent=False)  # Optional
```
- `videoSeq`: Enter the videoSeq of the image.
- `session`: UserSession is required for videos that require membership authentication.
- `vpdid2`: If you have a preloaded vpdid2 value, you can use it to reduce data usage.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### getLiveStatus()
Get the current status information of VLIVE LIVE.
```python
from vlivepy import getLiveStatus

getLiveStatus(videoSeq="123456",
              silent=False)  # Optional
```
- `videoSeq`: Enter the videoSeq of the image.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### getVodPlayInfo()
Gets information related to VLIVE VOD playback.
```python
from vlivepy import getVodPlayInfo

getVodPlayInfo(videoSeq="123456",
               vodId=None,  # Optional
               session=None,  # Optional
               silent=False)  # Optional
```
- `videoSeq`: Enter the videoSeq of the image.
- `vodId`: If you have a preloaded vodId value, you can use it to reduce data usage.
- `session`: UserSession is required for videos that require membership authentication.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### getPostComments()
> Dev item (>=0.2.0)
>
Get comments from post
```python
from vlivepy import getPostComments

getPostComments(post="0-12345678",
                session=None,  # Optional
                after=None,  # Optional
                silent=False)  # Optional
```
- `post`: Enter the postId of the post to parse comment.
- `session`: UserSession is required for videos that require membership authentication.
- `after`: Required if post has over 20 comments, Format is like `commentId,createdAt` of last comment
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.


### getPostStarComments()
> Dev item (>=0.2.0)
>
Get star's comments from post
```python
from vlivepy import getPostStarComments

getPostStarComments(post="0-12345678",
                    session=None,  # Optional
                    after=None,  # Optional
                    silent=False)  # Optional
```
- `post`: Enter the postId of the post to parse comment.
- `session`: UserSession is required for videos that require membership authentication.
- `after`: Required if post has over 20 comments, Format is like `commentId,createdAt` of last comment
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.



## Utils
### utils.postIdToVideoSeq()
Convert VLIVE postId to videoSeq.
```python
from vlivepy.utils import postIdToVideoSeq

postIdToVideoSeq(post="0-12345678",
                 silent=False)  # Optional
```
- `post`: Enter the postId.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### utils.getVpdid2()
Find the vpdid2 value from the account information.
```python
from vlivepy import getUserSession
from vlivepy.utils import getVpdid2

user = getUserSession(email="user@email.id", pwd="userPassword!")

getVpdid2(session=user,
          silent=False)  # Optional
```
- `session`: UserSession is required for videos that require membership authentication.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### utils.getVodId()
Find the vodId corresponding to videoSeq.
```python
from vlivepy.utils import getVodId

getVodId(videoSeq="123456",
         silent=False)   # Optional
```
- `videoSeq`: Enter the videoSeq of the image.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### utils.getUpcomingList()
[VLIVE schedule](https://www.vlive.tv/upcoming) Parse the List (of [UpcomingVideo](#upcomingvideo)) returns.
```python
from vlivepy.utils import getUpcomingList

print (getUpcomingList(date=None,  # Optional
                       silent=False))  # Optional
# [UpcomingVideo(...), ...]
```
`getUpcomingList()`The function has the following variables:
- `date`: Enter the date to load. The format is `%Y%m%d`. If None, load today's calendar.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

#### UpcomingVideo
UpcomingVideo is a `namedtuple` object that corresponds to an individual schedule in the schedule.

UpcomingVideo has the following fields:

| Field | Explanation | Value |
|:---:|:---:|:---|
| `seq` | videoSeq value | Any |
| `time` | VOD release/broadcast start time | Any |
| `cseq` | ChannelSeq value of the channel to be broadcast (uploaded) | Any |
| `cname` | The name of the channel to be broadcast (uploaded) | Any |
| `ctype` | Type of channel to broadcast (upload) | `PREMIUM`: Membership channel broadcasting <br> `BASIC`: general channel broadcasting |
| `name` | Broadcast (VOD) title | Any |
| `type` | Schedule type | `VOD`: This is a public VOD. <br> `UPCOMING_VOD`: VOD with reserved time. <br> `UPCOMING_LIVE`: Live with reserved time. <br> `LIVE`: This is LIVE now on air. |
| `product` | Whether the product is for sale | `PAID`: Paid products such as V LIVE+ <br> `NONE`: (including membership live) General live |

### utils.dumpSession()
Save UserSession to prevent temporary login restrictions due to frequent logins.
```python
from vlivepy import getUserSession
from vlivepy.utils import dumpSession

user = getUserSession(email="user@email.id", pwd="userPassword!")

with open("user.pkl", mode="wb") as f:
    dumpSession(session=user,
                fp=f)
```

### utils.loadSession()
Load the saved UserSession.
```python
from vlivepy.utils import loadSession

with open("user.pkl", mode="rb") as f:
    user = loadSession(f)
```

### utils.getPostCommentsIter()
> Dev item (>=0.2.0)
>
Get comments from post as iterable by page(20 comments)
```python
from vlivepy.utils import getPostCommentsIter

for item in getPostCommentsIter(post="0-12345678",
                                session=None):  # Optional
    print(item)

# CommentItem(isRestricted=False, body=""...)
# CommentItem(isRestricted=False, body=""...)
# CommentItem(isRestricted=False, body=""...)
# ...
```

Each item only returns [`CommentItem`](#commentitem) object compared to [`getPostComments()`](#getpostcomments)
- `post`: Enter the postId of the post to parse comment.
- `session`: UserSession is required for videos that require membership authentication.

#### CommentItem
`CommentItem` is a `namedTuple` object that corresponds to each comment

`CommentItem` has the following fields:

| Field | Explanation | Value |
|:---:|:---:|:---|
| `commentId` | ID of comment | str |
| `author` | Author info of comment | dict |
| `body` | Comment body | Any |
| `sticker` | Sticker in body | List\[dict\] |
| `createdAt` | Created time (Epoch) | int |
| `commentCount` | count of nested comment | int |
| `emotionCount` | Like count | int |
| `isRestricted` |  | Bool |
| `parent` | Information about parent post or comment | dict  |
| `root` | Information about origin post | dict |

### utils.getPostStarCommentsIter()
> Dev item (>=0.2.0)
>
Get star's comments from post as iterable by page(20 comments)
```python
from vlivepy.utils import getPostStarCommentsIter

for item in getPostStarCommentsIter(post="0-12345678",
                                    session=None):  # Optional
    print(item)

# CommentItem(isRestricted=False, body=""...)
# CommentItem(isRestricted=False, body=""...)
# CommentItem(isRestricted=False, body=""...)
# ...
```

Each item only returns [`CommentItem`](#commentitem) object compared to [`getPostComments()`](#getpostcomments)
- `post`: Enter the postId of the post to parse comment.
- `session`: UserSession is required for videos that require membership authentication.

## Video
The `Video` object [getPostInfo](#getpostinfo) caches the results and has an API available as a method.
PostInfo of `Video` object uses temporary caching. Setting the `refresh_rate` variable to 0 disables the cached information.
```python
from vlivepy import Video

# Initialization via postId `https://www.vlive.tv/post/0-18396482`
Video("0-18396482")

# Initialization using videoSeq `https://www.vlive.tv/video/142851`
Video("142851")

video = Video(number="142851",
              session=None,  # Optional
              refresh_rate=10)  # Optional
```
- `number`: You need the videoSeq or postId of the video to load.
- `session`: It loads with a specific UserSession.
- `refresh_rate`: Cache lifetime. It is in seconds and reloads PostInfo when the time is exceeded.

### Video.Properties
The properties provided by the Video object are as follows.
- `videoSeq`: Returns the videoSeq value of the Video object
- `postInfo`: Return postInfo of VLIVE Video
- `is_vod`: `True` when VLIVE Video is VOD
- `vod_id`: Returns vodId if VLIVE Video is VOD
- `title`: Title of VLIVE Video
- `channelCode` Returns the ChannelCode of the channel where VLIVE Video was created.
- `channelName` Returns the name of the channel where VLIVE Video was created

### Video.refresh()
Checks the lifetime of the cache and reloads data if the cache has expired. You can load data overriding the cache lifetime via the `force` variable.

### Video.getOfficialVideoPost()
[getOfficialVideoPost](#getofficialvideopost) Call the API.
```python
from vlivepy import Video

video = Video(142851)
video.getOfficialVideoPost(
    silent=False  # Optional
)
```
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### Video.getLivePlayInfo()
[getLivePlayInfo](#getliveplayinfo) Call the API.
```python
from vlivepy import Video

video = Video(142851)
video.getLivePlayInfo(
    silent=False  # Optional
)
```
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### Video.getInkeyData()
[getInKeyData](#getinkeydata) Call the API.
```python
from vlivepy import Video

video = Video(142851)
video.getInkeyData(
    silent=False  # Optional
)
```
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### Video.getLiveStatus()
[getLiveStatus](#getlivestatus) Call the API.
```python
from vlivepy import Video

video = Video(142851)
video.getLiveStatus(
    silent=False  # Optional
)
```
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### Video.getUserSession()
```python
from vlivepy import Video

video = Video(142851)
video.getUserSession(email="user@email.id",
                     pwd="userPassword!",
                     silent=False)  # Optional
```
- `email`: Email ID of the account to log in.
- `pwd`: This is the password of the account to log in.
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.

### Video.loadSession()
[loadSession](#utilsloadsession) Call the utility.
```python
from vlivepy import Video

video = Video(142851)
with open("user.pkl", mode="rb") as f:
    video.loadSession(fp=f)
```


### Video.getVodPlayInfo()
[getVodPlayInfo](#getvodplayinfo) Call the API.
```python
from vlivepy import Video

video = Video(142851)
video.getVodPlayInfo(
    silent=False  # Optional
)
```
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.


## Upcoming
The `Upcoming` object caches the results of [getUpcomingList](#utilsgetupcominglist) and reorganizes the list according to the list display options.

It uses temporary caching because it works by reading it by web parsing, not by API. Setting the `refresh_rate` variable to 0 disables the cached information.
```python
from vlivepy import Upcoming

upc = Upcoming(refresh_rate=5,  # Optional
               show_vod=True,  # Optional
               show_upcoming_vod=True,  # Optional
               show_upcoming_live=True,  # Optional
               show_live=True)  # Optional
```
The `Upcoming` object receives variables for refresh cache lifetime and display properties.
- `refresh_rate`: cache lifetime. It is in seconds, and if the time is exceeded, the schedule is reloaded.
- `show_vod`: Include VOD in the list.
- `show_upcoming_vod`: Include reserved VODs in the list.
- `show_upcoming_live`: Includes reserved LIVEs in the list.
- `show_live`: Includes live LIVE in the list.

### Upcoming.upcoming()
Parse today's schedule and return it as list(of [UpcomingVideo](#upcomingvideo)). If the cache lifetime has not expired, data is served from the cache.
```python
from vlivepy import Upcoming

upc = Upcoming()

print(upc.upcoming(force=False,  # Optional
                   show_vod=None,  # Optional
                   show_upcoming_vod=None,  # Optional
                   show_upcoming_live=None,  # Optional
                   show_live=None))  # Optional
# [UpcomingVideo(seq='######', time='오전 12:00', cseq='###', cname='channel name ', ctype='BASIC', name="title", type='VOD', product='NONE'), ...]
```

You can override the cache and list containing options via variables.
```python
from vlivepy import Upcoming

upc = Upcoming()

# Override cache lifetime and force load new data
upc.upcoming(force=True)

# Temporarily override object properties
upc.upcoming(show_vod=False, show_upcoming_vod=False)
```

### Upcoming.refresh()
Checks the lifetime of the cache and reloads data if the cache has expired. You can load data overriding the cache lifetime via the `force` variable.

### Upcoming.load()
Loads the calendar for a specific date. Loaded calendars are not cached and are returned immediately.

The returned list follows the object's include list option, and can be overridden via `show_*` variables.
```python
from vlivepy import Upcoming
from datetime import date, timedelta

upc = Upcoming()
tomorrow = date.today() + timedelta(days=1)  # Example) Finding the date of tomorrow

print(upc.load(date=tomorrow.strftime("%Y%m%d"),
               show_vod=None,  # Optional
               show_upcoming_vod=None,  # Optional
               show_upcoming_live=None,  # Optional
               show_live=None,  # Optional
               silent=False))  # Optional
# [UpcomingVideo(seq='######', time='오전 12:00', cseq='###', cname='channel name ', ctype='BASIC', name="title", type='VOD', product='NONE'), ...]
```
The `load()` method takes the following variables:
- `date`: Enter the date to load. The format is `%Y%m%d`.
- `show_vod`, `show_upcoming_vod`, `show_upcoming_live`, `show_live`: Override list inclusion options
- `silent`: When a connection or parsing error occurs, it returns None instead of Exception.


## Post
`Post` object loads vlive post and contains related API as method

### Post.Property
The properties provided by the Post object

- `attachments`: Attachments data
- `attachments_photo`: Photo attachments data
- `attachments_video`: Video attachments data
- `author`: Author data of post
- `author_nickname`: nickname of author
- `author_id`: Unique ID of author
- `created_at`: Created time of post (timestamp)
- `plain_body`: Contents of post without attachments
- `body`: Contents of post with attachment tag
- `title`: Title of post


### Post.refresh()
Refresh post data

### Post.formatted_body()
Return body as html with replacing attachment tag as proper tag
