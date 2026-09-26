# PDF Book Maker

여러 PDF를 표지, 목차, 북마크와 연속 페이지 번호가 포함된 하나의 전자책으로 만드는 Windows 프로그램입니다.

현재 버전은 `v1.0`입니다.

## 다운로드

**[PDF Book Maker 최신 버전 다운로드](https://github.com/kiyoo0815/PDFBookMaker/releases/latest)**

Windows 10/11에서 사용할 수 있으며 Python 설치는 필요하지 않습니다.

다운로드한 `PDFBookMaker-v1.0-Windows.zip`의 압축을 풀고
`PDFBookMaker.exe`를 실행하면 됩니다.

## 주요 기능

- 여러 PDF를 원하는 순서로 병합
- 전자책 표지 자동 생성
- 항목 수에 따라 여러 목차 페이지 자동 생성
- PDF별 제목 편집
- PDF 북마크 생성
- 본문 기준 연속 페이지 번호
- 병합 진행률과 단계별 로그 표시
- 기존 결과 파일을 보호하는 안전한 저장

## 프로그램 화면

### 메인 화면

여러 PDF와 목차를 원하는 순서로 구성하고 전자책 생성 정보를 설정할 수 있습니다.

![PDF Book Maker 메인 화면](docs/images/01_main.png)

### 표지 설정

제목, 부제목, 하단 정보와 이미지를 설정하고 결과를 미리 확인할 수 있습니다.

![표지 설정 화면](docs/images/02_cover_settings.png)

### 페이지 번호 설정

짝수·홀수 페이지의 번호 위치와 크기, 시작 번호, 여백 및 표시 형식을 설정할 수 있습니다.

![페이지 번호 설정 화면](docs/images/03_page_number_settings.png)

### 생성 결과

자동 생성된 목차와 PDF 북마크가 포함된 최종 전자책입니다.

![전자책 생성 결과](docs/images/04_result.png)

## 실행 환경

- 일반 사용자: Windows 10/11, Python 설치 불필요
- 개발자: Python 3.10 이상

## 개발 환경 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## 사용 방법

1. `파일 선택`에서 병합할 PDF 파일을 선택합니다.
2. `▲ 위로`, `▼ 아래로` 버튼으로 PDF의 병합 순서를 조정합니다.
3. 필요한 경우 각 PDF의 전자책 제목을 수정하고 `적용`을 누릅니다.
4. 출력 폴더와 최종 PDF 파일명을 지정합니다.
5. `전자책 설정`을 눌러 표지와 페이지 번호를 설정합니다.
6. 표지 설정에서 제목, 부제목, 하단 정보와 이미지를 설정하고 미리보기에서 결과를 확인합니다.
7. 페이지 번호 설정에서 위치, 크기, 시작 번호, 여백과 표시 형식을 설정합니다.
8. 설정을 완료한 뒤 메인 화면에서 `전자책 만들기`를 누릅니다.
9. 병합이 완료되면 지정한 출력 폴더에서 완성된 PDF를 확인합니다.

목차와 북마크에는 메인 화면에 표시된 PDF의 순서와 제목이 사용됩니다.

표지와 페이지 번호 설정은 자동으로 저장되며 프로그램을 다시 실행하면 마지막으로 사용한 설정이 복원됩니다.

## 테스트

```powershell
python -m unittest discover -s tests -v
```

테스트에서는 다음 주요 기능을 확인합니다.

1. 입력 파일 누락 시 오류 처리
2. 여러 페이지로 구성되는 목차 생성
3. PDF 병합 순서
4. 북마크 생성
5. 진행률 및 단계별 로그 처리

## Windows 실행파일 만들기

개발 환경에서 다음 명령으로 Windows 실행파일을 만들 수 있습니다.
```powershell
python -m pip install -r requirements-dev.txt
pyinstaller --noconfirm --clean PDFBookMaker.spec
```

빌드가 완료되면 실행파일은 `dist\PDFBookMaker\PDFBookMaker.exe`에 생성됩니다.

PDF 출력에 필요한 맑은 고딕 폰트 파일은 실행파일에 함께 포함됩니다.

## 프로젝트 구조

```text
PDF-Book-Maker/
│
├─ main.py
│  └─ 프로그램 시작
│
├─ ui_main.py
│  └─ 메인 화면 및 전자책 생성 제어
│
├─ file_merge.py
│  └─ 표지, 목차, 페이지 번호, 북마크 및 PDF 병합
│
├─ ui/
│  ├─ settings_dialog.py
│  │  └─ 전자책 설정 창
│  │
│  ├─ pages/
│  │  ├─ cover_page.py
│  │  │  └─ 표지 설정
│  │  └─ page_number_page.py
│  │     └─ 페이지 번호 설정
│  │
│  ├─ widgets/
│  │  ├─ cover_preview_widget.py
│  │  │  └─ 표지 미리보기
│  │  ├─ page_number_preview_widget.py
│  │  │  └─ 페이지 번호 미리보기
│  │  └─ position_selector.py
│  │     └─ 페이지 번호 위치 선택
│  │
│  └─ utils/
│     ├─ page_number_helper.py
│     │  └─ 페이지 번호 위치 계산
│     └─ pdf_title_reader.py
│        └─ PDF 제목 정보 읽기
│
├─ assets/
│  └─ fonts/
│     └─ malgun.ttf
│        └─ PDF 출력용 한글 글꼴
│
├─ docs/
│  └─ images/
│     └─ README용 프로그램 화면 이미지
│
├─ tests/
│  └─ test_file_merge.py
│     └─ PDF 병합 기능 자동 테스트
│
├─ requirements.txt
│  └─ 실행에 필요한 Python 패키지
│
├─ requirements-dev.txt
│  └─ 개발 및 배포용 패키지
│
├─ PDFBookMaker.spec
│  └─ PyInstaller 실행파일 빌드 설정
│
├─ README.md
│  └─ 프로젝트 소개 및 사용 방법
│
├─ USER_MANUAL.md
│  └─ 사용자 매뉴얼
│
├─ CHANGELOG.md
│  └─ 버전별 주요 변경사항
│
├─ LICENSE
│  └─ MIT License
│
└─ DEVLOG.md
   └─ 개발 진행 기록
```

## 현재 제한사항

- 암호가 설정된 PDF는 지원하지 않습니다.
- 입력 파일은 PDF 형식만 지원하며 ZIP 파일은 지원하지 않습니다.
- PDF 병합 중에는 작업이 완료될 때까지 프로그램의 응답이 일시적으로 느려질 수 있습니다.

