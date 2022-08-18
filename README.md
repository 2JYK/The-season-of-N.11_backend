# **☠️ \[S.A\] 유화제작-Django Project**☠️

# 👻 프로젝트 주제

-   유화 제작
    -   유화제작 인공지능 기술(NST)를 사용해서 사용자가 이미지를 넣으면 유화 스타일이 적용된 이미지로 변환되어 출력되는 서비스
    -   이미지 생성 기술(Generative models)을 이용해서 사용자가 흥미를 느낄 수 있는 서비스

---

# 👻 필수 구현 기술

-   Django Rest-framework
-   유화제작 인공지능 기술(NST)
-   CRUD
-   회원가입/로그인 기능 - JWT
-   AWS EC2 배포

---

# 👻 이번 프로젝트 목표

-   정기적인 상호 피드백 및 코드 리뷰 시간
-   git hub
    -   branch 활용법 공부 ( 백업 및 롤백기능 사용,다른 팀원도 잘 알아보도록 표시 )
    -   **Issues / Projects / Wiki 탭 활용**
    -   pull & push
    -   merge 방법 3 가지에 대한 의미 숙지
-   프론트엔드와 백엔드를 분리하는 RESTful API 작성
-   공부
    -   DRF
    -   mySQL
    -   머신러닝
    -   북마크, 좋아요 기능 추가

---

# 👻 필수 포함 사항

## 😇 필수 기능

-   DRF 사용
    -   회원 기능 포함 (JWT 토큰을 이용)
-   프론트엔드와 백엔드를 별도의 레포지토리에서 기능별 관리
-   CRUD 기능
-   유화제작 인공지능 기술(NST)
-   AWS EC2 배포

## 😇 추가 기능

-   생성된 이미지는 S3에 올려서 관리
-   생성된 결과물을 사이트에 게시할 수 있게 설정(노출 시간, 공개 여부 선택 가능)
-   게시물에 대해 댓글 기능 추가
-   게시물에 대해 좋아요 기능 추가
-   마이페이지에 본인이 생성한 이미지/게시글을 확인할 수 있는 기능 추가
-   생성된 게시물에 대한 공유기능(메일 보내기 등) 추가
-   소셜 로그인 회원가입/로그인 기능 추가

---

# 👻 MOCKUP 및 DB 작성

## 😇 MOCKUP
![mockup](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FM7SBU%2FbtrFZdSFHcO%2FpEnrZBks6tez01kwFxsowK%2Fimg.png)
## 😇 ERD 작성
![ERD](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FOhP0p%2FbtrFXYWawfh%2FK8nnxUm26abG8R7pm3yMhK%2Fimg.png)

```
user {
	"user_id(pk)" : "Primary Key",
	"username" : "사용자 아이디",
	"password" : "비밀번호",
	"email" : "이메일",
	"fullname": "이름",
	"join_date": "생성시간",
}

style {
	"style_id(pk)": "Primary Key",
	"style_image": "풍경 사진",
	"category": "카테고리"
}

image {
	"image_id(pk)": "Primary Key",
	"style_id(fk)": "Foreign Key",
	"article_id(fk)": "Foreign Key",
	"user_id(fk)": "Foreign Key",
	"input": "사용자가 입력한 사진",
	"output": "결과 사진"
}

article {
	"article_id(pk)" : "Primary Key",
	"user_id(fk)" : "Foreign Key",
	"image_id(fk)": "Foreign Key",
	"title" : "제목",
	"content" : "내용",
	"created_at" : "등록 일자",
	"modlfied_at" : "수정 일자"
}

comment {
	"comment_id(pk)" : "Primary Key",
	"article_id(fk)": "Foreign Key",
	"user_id(fk)" : "Foreign Key",
	"content" : "내용"
}

like {
	"like_id(pk)" : "Primary Key",
	"user_id(fk)" : "Foreign Key",
	"article(fk)" : "Foreign Key",
}

bookmark {
	"bookmark_id(pk)" : "Primary Key",
	"user_id(fk)" : "Foreign Key",
  "article_id(fk)" : "Foreign Key",
}
```

---

# 👻 컨벤션

## 😇 GitHub

-   프론트엔드
    -   브랜치 (app 별로 )
-   백엔드
    -   브랜치 (app 별로 )
-   커밋 메세지

```
Commit Type
- Feat : 새로운 기능 추가/수정/삭제
- Fix : 버그 수정
- Docs : 문서 수정
- Design : CSS 등 사용자 UI 디자인 변경
- Style: 코드에 영향을 주지 않는 변경사항 /  코드 포맷 변경, 새미 콜론 누락, 코드 수정이 없는 경우
- Refactor: 코드 리팩토링
- Test: 테스트 코드/기능 추가
- Rename : 파일 혹은 폴더명을 수정하거나 옮기는 작업만인 경우
- Remove : 파일을 삭제하는 작업만 수행한 경우

Subject
- 50자를 넘기지 않고, 커밋 타입을 준수함.

 Body
- 72자를 넘기지 않고, 모든 커밋에 본문 내용을 작성할 필요는 없음.
```

---

# 👻 기능 명세서

## 😇 회원가입/로그인

-   아이디와 비밀번호를 입력해 회원가입 또는 로그인을 할 수 있습니다.
    -   회원가입은 아이디와 패스워드가 6자리 이상 이여야 가능합니다.
    -   아이디가 중복되면 회원가입이 불가합니다.
-   로그인이 된 상태에선 회원가입/로그인 페이지에 접속이 불가합니다.
-   추가 : 소셜 로그인 회원가입/로그인 기능
-   추가 : 비밀번호 찾기

## 😇 메인 페이지

-   여러 사용자가 업로드한 게시물을 한 눈에 확인할 수 있습니다. (역순)
-   각 게시물에 좋아요와 북마크를 누를 수 있습니다.
-   업로드 버튼을 누르면 업로드 페이지로 이동합니다.
-   페이지 네이션을 통해 2 x 3 이 넘어가면 페이지가 생깁니다.
-   게시물을 클릭 시 게시글의 상세페이지로 이동합니다.

## 😇 업로드 페이지

-   사진을 선택하여 업로드 하면 머신러닝을 통해 사진의 스타일을 변환합니다.
-   사용자는 자신이 원하는 계절감의 사진을 선택합니다.
-   머신러닝의 결과물이 나오면 사진에 맞는 코멘트를 작성한 뒤 사진을 게시합니다.
-   제목은 30자, 설명은 100자 이하로만 작성할수 있습니다.
-   업로드 버튼을 클릭 시 메인페이지로 보내집니다.

## 😇 마이 페이지

-   현재 로그인한 사용자가 올린 사진 및 북마크한 사진을 확인할 수 있습니다.
-   기본값으로는 사용자가 올린 사진들이 보여집니다.
-   무한 스크롤을 이용하여 보여집니다.
-   게시물을 클릭 시 게시글의 상세페이지로 이동합니다.
-   사용자가 올린 사진에 대한 수정 및 삭제가 가능합니다.

## 😇 게시글 상세 페이지

-   다른 사용자가 댓글을 작성할 수 있습니다.
-   다른 사용자의 글에 북마크를 남겨 마이 페이지의 북마크 탭에서 확인할 수 있습니다.
-   좋아요 카운트 숫자를 보여주고 누릅니다.

## 😇 게시글 수정 페이지

-   로그인한 사용자가 작성한 사진 중 수정할 사진을 선택하면 해당 화면으로 들어와
-   사용자가 수정을 진행할 수 있습니다.
-   취소 버튼을 누르면 마이페이지로 다시 돌아갑니다.
-   수정할 수 있는 내용은 아래와 같습니다.
    -   게시글의 제목
    -   게시글의 설명
-   우상단의 삭제 버튼을 눌러 해당 게시글을 삭제할 수 있습니다.

---

# 👻 API

![API](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbwCgPL%2FbtrFZEPUIxV%2FYJZLdHVpjg161cDwzW13s1%2Fimg.png)

![API](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcwYAKa%2FbtrFZLuAzhq%2FOQB6Fn8lbeGnbiwi9dbqB1%2Fimg.png)

---

# 👻 팀원들의 역할 및 약속

## 😇 팀원별 역할

-   김경수, 정주현
    -   배포
    -   메인 페이지 : 적용된 대상 이미지를 보여주는 페이지
    -   게시글 업로드 페이지 :이미지 업로드하여 보여주는 페이지
    -   댓글
    -   좋아요
    -   북마크
-   정대근, 윤슬기
    -   유화제작 인공지능 기술
    -   회원가입
    -   로그인
    -   마이 페이지
        -   북마크 모은 페이지
        -   게시글 수정 및 삭제

## 😇 우리 팀의 약속

-   서로의 의견을 존중해 주기
-   프로젝트가 어렵고 힘들어도 웃기
-   휴일에도 프로젝트에 시간을 최대한 할애하기
-   함께 성장하며 서로가 서로의 멘토가 되어주기
