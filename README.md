# vlivepy
vlivepy는 파이썬 기반의 vlive.tv 비공식 API입니다.

## 문서
### 영상 로드하기
Video 객체를 사용하여 VOD와 라이브를 로드할 수 있습니다. post링크의 id와 video링크의 id를 모두 지원합니다
```python
import vlivepy

# load with postId
video = vlivepy.Video("0-18396482")

# load with videoSeq
video = vlivepy.Video("142851")

```
