> #### Language
> [English](README.md) Korean

# vlivepy
vlivepy는 파이썬 기반의 vlive.tv 비공식 API입니다.

## Upcoming
`Upcoming` 객체는 [VLIVE 일정표](https://www.vlive.tv/upcoming) 를 파싱합니다.
```python
from vlivepy import Upcoming

upc = Upcoming(refresh_rate=5, show_vod=True, show_upcoming=True, show_live=True)

print(upc.upcoming())
# [UpcomingVideo(seq='232395', cseq='447', cname='CHUNG HA',ctype='BASIC',
#                name="CHUNG HA 청하 'X (걸어온 길에 꽃밭 따윈 없었죠)' MV Teaser 2",
#                type='VOD',product='NONE'), ... ]
```
`Upcoming`객체는 새로고침 캐시 수명과 표시 속성에 대한 변수를 받습니다 (Optional)
- `refresh_rate`: 캐시 수명입니다. 초 단위이며 해당시간이 초과했을 경우 일정표를 다시 로드합니다. (기본값: 5)
- `show_vod`: 목록에 VOD를 포함합니다. (기본값: True)
- `show_upcoming`: 목록에 예약된 일정을 포함합니다. 공개시간이 되지 않은 VOD와 LIVE가 모두 포함됩니다. (기본값: True)
- `show_live`: 목록에 진행중인 LIVE를 포함합니다. (기본값: True)



### 영상 로드하기
Video 객체를 사용하여 VOD와 라이브를 로드할 수 있습니다. post링크의 id와 video링크의 id를 모두 지원합니다
```python
import vlivepy

# load post url `https://www.vlive.tv/post/0-18396482`
vlivepy.Video("0-18396482")

# load video url `https://www.vlive.tv/video/142851`
vlivepy.Video("142851")
``` 
