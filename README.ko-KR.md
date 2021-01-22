> #### Language
> [English](README.md) Korean

# vlivepy
![GitHub](https://img.shields.io/github/license/box-archived/vlive-py)
![PyPI](https://img.shields.io/pypi/v/vlivepy)

vlivepy는 파이썬 기반의 vlive.tv 비공식 API입니다.

## 설치
[PyPI](https://pypi.org/project/vlivepy/) 를 통해 설치할 수 있습니다.
```console
$ python -m pip install vlivepy
```

---
# Documentation
- [들어가기에 앞서](#들어가기에-앞서)
    - [용어](#용어)
    - [표현](#표현)
- [API](#api)
    - [getUserSession()](#getusersession)
    - [getPostInfo()](#getpostinfo)
    - [getOfficialVideoPost()](#getofficialvideopost)
    - [getInkeyData()](#getinkeydata)
    - [getLivePlayInfo()](#getliveplayinfo)
    - [getLiveStatus()](#getlivestatus)
    - [getVodPlayInfo()](#getvodplayinfo)
- [Utils](#utils)
    - [utils.postIdToVideoSeq()](#utilspostidtovideoseq)
    - [utils.getVpdid2()](#utilsgetvpdid2)
    - [utils.getVodId()](#utilsgetvodid)
    - [utils.getUpcomingList()](#utilsgetupcominglist)
        - [UpcomingVideo](#upcomingvideo)
    - [utils.dumpSession()](#utilsdumpsession)
    - [utils.loadSession()](#utilsloadsession)
- [Video](#video)
- [Upcoming](#upcoming)
    - [Upcoming.upcoming()](#upcomingupcoming)
    - [Upcoming.refresh()](#upcomingrefresh)
    - [Upcoming.load()](#upcomingload)


## 들어가기에 앞서
이 문서에서 사용되는 용어와 표현법에 대해 알아봅니다.

### 용어
- `videoSeq`: url의 `~/video/` 뒤에 오는 6자리 숫자 코드입니다. VLIVE 상에서 officialVideo를 가리킵니다.
- `postId`: url 의 `~/post/` 뒤에 오는 `0-12345678`형태의 코드입니다. VLIVE 상에서 게시물을 가리칩니다.
- `vodId`: VLIVE 내부적으로 사용되는 36자리 Hex형태의 코드입니다.
- `vpdid2`: 유저를 나타내는 64자리 Hex형태의 코드입니다.
- `inKey`: VOD 정보 로드시 사용되는 값입니다.

### 표현
함수나 객체의 매개변수에 대한 설명은 코드블럭으로 작성됩니다. 인수는 함수 내에서 선언한 순서대로 작성되며 예시 값이 제공됩니다. 선택적 인수는 `# Optional` 주석이 붙고 기본값을 예시로 제공합니다.

함수와 매개변수에 대한 코드블럭 예시는 아래와 같습니다.
```python
from vlivepy import getPostInfo

# 아래 라인은 함수 예시와 필수적 인수의 설명에 대한 예시입니다.
getPostInfo(post="0-12345678",
# 아래 라인은 선택적 인수의 설먕에 대한 예시입니다.
            session=None,  # Optional
            silent=False)  # Optional
```

## API
### getUserSession()
VLIVE 웹사이트에 로그인하여 [requests.Session](https://requests.readthedocs.io/en/master/user/advanced/) 객체를 반환합니다. 로그인에는 [이메일 로그인](https://www.vlive.tv/auth/email/login) 방식을 사용합니다
```python
from vlivepy import getUserSession

getUserSession(email="user@email.id",
               pwd="userPassword!",
               silent=False)  # Optional
```
- `email`: 로그인 할 계정의 이메일 아이디입니다.
- `pwd`: 로그인 할 계정의 비밀번호 입니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### getPostInfo()
postId를 통해 VLIVE Post의 정보를 로드하여 dict 객체를 리턴합니다.
```python
from vlivepy import getPostInfo

getPostInfo(post="0-12345678", 
            session=None,  # Optional
            silent=False)  # Optional
```
`getPostInfo()`합수는 다음의 변수를 갖습니다:
- `post`: postId를 입력합니다.
- `session`: 회원인증이 필요한 포스트인 경우 UserSession이 필요합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### getOfficialVideoPost()
videoSeq를 통해 VLIVE Video의 정보를 로드하여 dict 객체를 리턴합니다
```python
from vlivepy import getOfficialVideoPost

getOfficialVideoPost(videoSeq="123456",
                     session=None,  # Optional
                     silent=False)  # Optional
```
- `videoSeq`: 영상의 videoSeq를 입력합니다.
- `session`: 회원인증이 필요한 영상인 경우 UserSession이 필요합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### getInkeyData()
VLIVE VOD와 계정 정보에 해당하는 inKey를 로드합니다.
```python
from vlivepy import getInkeyData

getInkeyData(videoSeq="123456",
             session=None,  # Optional
             silent=False)  # Optional
```
- `videoSeq`: 영상의 videoSeq를 입력합니다.
- `session`: 회원인증이 필요한 영상인 경우 UserSession이 필요합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### getLivePlayInfo()
VLIVE LIVE의 재생에 관련된 정보를 가져옵니다.
```python
from vlivepy import getLivePlayInfo

getLivePlayInfo(videoSeq="123456",
                session=None,  # Optional
                vpdid2=None,  # Optional
                silent=False)  # Optional
```
- `videoSeq`: 영상의 videoSeq를 입력합니다.
- `session`: 회원인증이 필요한 영상인 경우 UserSession이 필요합니다.
- `vpdid2`: 미리 로드한 vpdid2 값이 있다면 이를 사용하여 데이터 사용량을 줄일 수 있습니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### getLiveStatus()
VLIVE LIVE의 현재 상태 정보를 가져옵니다.
```python
from vlivepy import getLiveStatus

getLiveStatus(videoSeq="123456",
              silent=False)  # Optional
```
- `videoSeq`: 영상의 videoSeq를 입력합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### getVodPlayInfo()
VLIVE VOD의 재생에 관련된 정보를 가져옵니다.
```python
from vlivepy import getVodPlayInfo

getVodPlayInfo(videoSeq="123456",
               vodId=None,  # Optional
               session=None,  # Optional
               silent=False)  # Optional
```
- `videoSeq`: 영상의 videoSeq를 입력합니다.
- `vodId`: 미리 로드한 vodId 값이 있다면 이를 사용하여 데이터 사용량을 줄일 수 있습니다.
- `session`: 회원인증이 필요한 영상인 경우 UserSession이 필요합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

## Utils
### utils.postIdToVideoSeq()
VLIVE postId를 videoSeq로 변환합니다.
```python
from vlivepy.utils import postIdToVideoSeq

postIdToVideoSeq(post="0-12345678",
                 silent=False)  # Optional
```
- `post`: postId를 입력합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### utils.getVpdid2()
계정 정보로 부터 vpdid2 값을 구합니다.
```python
from vlivepy import getUserSession
from vlivepy.utils import getVpdid2

user = getUserSession(email="user@email.id", pwd="userPassword!")

getVpdid2(session=user,
          silent=False)  # Optional
```
- `session`: 회원 정보를 담은 UserSession이 필요합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### utils.getVodId()
videoSeq에 해당하는 vodId를 구합니다.
```python
from vlivepy.utils import getVodId

getVodId(videoSeq="123456",
         silent=False)   # Optional
```
- `videoSeq`: 영상의 videoSeq를 입력합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

### utils.getUpcomingList()
[VLIVE 일정표](https://www.vlive.tv/upcoming) 를 파싱하고 List(of [UpcomingVideo](#upcomingvideo)) 리턴합니다.
```python
from vlivepy.utils import getUpcomingList

print (getUpcomingList(date=None,  # Optional
                       silent=False))  # Optional
# [UpcomingVideo(...), ...]
```
`getUpcomingList()`함수는 다음의 변수를 갖습니다:
- `date`: 로드 할 날짜를 입력합니다. 포맷은 `%Y%m%d` 입니다. None 일 경우 오늘 일정표를 로드합니다.
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.

#### UpcomingVideo
UpcomingVideo는 일정표의 개별 일정에 대응되는 `namedtuple` 객체입니다.

UpcomingVideo은 다음의 필드를 가집니다:

| 필드 | 설명 | 값 |
|:---:|:---:|:---|
| `seq` | videoSeq 값 | Any |
| `time` | VOD공개/방송시작 시간 | Any |
| `cseq` | 방송(업로드)하는 채널의 channelSeq 값 | Any |
| `cname` | 방송(업로드)하는 채널의 이름 | Any |
| `ctype` | 방송(업로드)하는 채널의 타입 | `PREMIUM`: 멤버십 채널 방송 <br> `BASIC`: 일반 채널 방송 |
| `name` | 방송(VOD) 제목 | Any |
| `type` | 스케쥴 타입 | `VOD`: 공개된 VOD 입니다. <br> `UPCOMING_VOD`: 시간이 예약된 VOD 입니다. <br> `UPCOMING_LIVE`: 시간이 예약된 LIVE 입니다. <br> `LIVE`: 지금 방송중인 LIVE 입니다. |
| `product` | 판매상품 여부 | `PAID`: V LIVE+ 등 유료 상품 <br> `NONE`: (멤버십 라이브 포함) 일반 라이브  |

### utils.dumpSession()
```python
from vlivepy import getUserSession
from vlivepy.utils import dumpSession

user = getUserSession(email="user@email.id", pwd="userPassword!")

with open("user.pkl", mode="wb") as f:
    dumpSession(session=user,
                fp=f)
```

### utils.loadSession()
```python
from vlivepy.utils import loadSession

with open("user.pkl", mode="rb") as f:
    user = loadSession(f)
```

## Video
`Video` 객체는 [getPostInfo](#getpostinfo) 결과를 캐싱하고 사용 가능한 API를 메소드로 갖습니다.

`Video` 객체의 PostInfo는 임시 캐싱을 사용합니다. `refresh_rate` 변수를 0으로 설정하면 캐시된 정보를 사용하지 않습니다.
```python
from vlivepy import Video

# postId를 통한 초기화 `https://www.vlive.tv/post/0-18396482`
Video("0-18396482")

# videoSeq를 이용한 초기화 `https://www.vlive.tv/video/142851`
Video("142851")

video = Video(number="142851",
              session=None,  # Optional
              refresh_rate=10)  # Optional
```
- `number`: 로드할 영상의 videoSeq나 postId가 필요합니다.
- `session`: 특정 UserSession을 이용해 로드합니다.
- `refresh_rate`: 캐시 수명입니다. 초 단위이며 해당시간이 초과했을 경우 PostInfo를 다시 로드합니다.

## Upcoming
`Upcoming` 객체는 [getUpcomingList](#utilsgetupcominglist) 결과를 캐싱하고 목록 표시 옵션에 따라 목록을 재구성합니다.

일정표는 API가 아닌 웹 파싱으로 읽어오는 방식으로 작동하기 때문에 임시 캐싱을 사용합니다. `refresh_rate` 변수를 0으로 설정하면 캐시된 정보를 사용하지 않습니다.

```python
from vlivepy import Upcoming

upc = Upcoming(refresh_rate=5,  # Optional
               show_vod=True,  # Optional
               show_upcoming_vod=True,  # Optional
               show_upcoming_live=True,  # Optional
               show_live=True)  # Optional
```
`Upcoming`객체는 새로고침 캐시 수명과 표시 속성에 대한 변수를 받습니다
- `refresh_rate`: 캐시 수명입니다. 초 단위이며 해당시간이 초과했을 경우 일정표를 다시 로드합니다.
- `show_vod`: 목록에 VOD를 포함합니다.
- `show_upcoming_vod`: 목록에 예약된 VOD를 포함합니다.
- `show_upcoming_live`: 목록에 예약된 LIVE를 포함합니다.
- `show_live`: 목록에 진행중인 LIVE를 포함합니다.

### Upcoming.upcoming()
오늘의 일정표를 파싱하여 list(of [UpcomingVideo](#upcomingvideo)) 타입으로 리턴합니다. 캐시 수명이 만료되지 않았다면 캐시에서 데이터를 제공합니다.
```python
from vlivepy import Upcoming

upc = Upcoming()

print(upc.upcoming(force=False,  # Optional
                   show_vod=None,  # Optional
                   show_upcoming_vod=None,  # Optional
                   show_upcoming_live=None,  # Optional
                   show_live=None))  # Optional
# [UpcomingVideo(seq='232395', time='오전 12:00', cseq='447', cname='CHUNG HA', ctype='BASIC', name="CHUNG HA 청하 'X (걸어온 길에 꽃밭 따윈 없었죠)' MV Teaser 2", type='VOD', product='NONE'), ...]
```

변수를 통해서 캐시와 목록 포함 옵션을 오버라이드 할 수 있습니다.
```python
from vlivepy import Upcoming

upc = Upcoming()

# 캐시 수명을 무시하고 강제로 새 데이터 로드
upc.upcoming(force=True)

# 객체 속성을 일시적으로 오버라이드 
upc.upcoming(show_vod=False, show_upcoming_vod=False)
```

### Upcoming.refresh()
캐시의 수명을 확인하여 캐시가 만료됐다면 데이터를 새로 로드합니다. `force`변수를 통해 캐시 수명을 무시하고 데이터를 로드할 수 있습니다.

### Upcoming.load()
특정 날짜의 일정표를 로드합니다. 로드된 일정표는 캐시되지 않으며 바로 리턴됩니다.

리턴되는 목록은 객체의 목록 포함 옵션을 따르며, `show_*` 변수를 통한 오버라이드를 사용할 수 있습니다.
```python
from vlivepy import Upcoming
from datetime import date, timedelta

upc = Upcoming()
tomorrow = date.today() + timedelta(days=1)  # 예제) 내일 날짜를 구한다

print(upc.load(date=tomorrow.strftime("%Y%m%d"),
               show_vod=None,  # Optional
               show_upcoming_vod=None,  # Optional
               show_upcoming_live=None,  # Optional
               show_live=None,  # Optional
               silent=False))  # Optional
# [UpcomingVideo(seq='232552', time='오전 10:00', cseq='967', cname='Arirang Radio │아리랑라디오', ctype='BASIC',name='Arirang Radio [#daily K]', type='UPCOMING_LIVE', product='NONE'), ...]
```
`load()`메소드는 다음의 변수를 갖습니다:
- `date`: 로드 할 날짜를 입력합니다. 포맷은 `%Y%m%d` 입니다.
- `show_vod`, `show_upcoming_vod`, `show_upcoming_live`, `show_live`: 목록 포함 옵션 오버라이드
- `silent`: 연결이나 파싱 오류가 발생했을 시 Exception 대신 None을 리턴합니다.
