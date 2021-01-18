> #### Language
> [English](README.md) Korean

# vlivepy
vlivepy는 파이썬 기반의 vlive.tv 비공식 API입니다.

## 설치
[PyPI](https://pypi.org/project/vlivepy/) 를 통해 설치할 수 있습니다.
```console
$ python -m pip install vlivepy
```

# Documentation
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
- [Upcoming](#upcoming)
  - [Upcoming.upcoming()](#upcomingupcoming)
  - [Upcoming.refresh()](#upcomingrefresh)
  - [Upcoming.load()](#upcomingload)
- [Video](#video)


## API
### getUserSession()
### getPostInfo()
### getOfficialVideoPost()
### getInkeyData()
### getLivePlayInfo()
### getLiveStatus()
### getVodPlayInfo()

## Utils
### utils.postIdToVideoSeq()
### utils.getVpdid2()
### utils.getVodId()
### utils.getUpcomingList()
[VLIVE 일정표](https://www.vlive.tv/upcoming) 를 파싱하고 리스트를 리턴합니다.
```python
from vlivepy.utils import getUpcomingList

print (getUpcomingList(date=None,  # Optional
                       silent=False))  # Optional
# [UpcomingVideo(...), ...]
```
#### UpcomingVideo
UpcomingVideo는 일정표의 개별 일정에 대응되는 `namedtuple` 객체입니다.

UpcomingVideo은 다음의 필드를 가집니다:
- `seq`: videoSeq 값
- `time`: VOD공개/방송시작 시간
- `cseq`: 방송하는 채널의 channelSeq 값
- `cname`: 방송하는 채널의 이름
- `ctype`: 방송하는 채널의 타입. 리턴 항목은 아래와 같습니다.
    - `PREMIUM`: 멤버십 채널 방송
    - `BASIC`: 일반 채널 방송
- `name`: 방송 제목
- `type`: 방송 타입. 리턴 항목은 아래와 같습니다.
    - `VOD`: 공개된 VOD 입니다.
    - `UPCOMING_VOD`: 시간이 예약된 VOD 입니다.
    - `UPCOMING_LIVE`: 시간이 예약된 LIVE 입니다.
    - `LIVE`: 지금 방송중인 LIVE 입니다.
- `product`: 판매상품 여부. 리턴 항목은 아래와 같습니다.
    - `PAID`: V LIVE+ 등 유료 상품
    - `NONE`: (멤버십 라이브 포함) 일반 라이브 

## Upcoming
`Upcoming` 객체는 [VLIVE 일정표](https://www.vlive.tv/upcoming) 캐싱하고 영상 타입에 따라 목록을 구성합니다.

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

## Video
Video 객체를 사용하여 VOD와 라이브를 로드할 수 있습니다. post링크의 id와 video링크의 id를 모두 지원합니다
```python
import vlivepy

# load post url `https://www.vlive.tv/post/0-18396482`
vlivepy.Video("0-18396482")

# load video url `https://www.vlive.tv/video/142851`
vlivepy.Video("142851")
``` 
