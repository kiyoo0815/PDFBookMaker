# PDF Book Maker

여러 PDF를 표지, 목차, 북마크와 연속 페이지 번호가 포함된 하나의 전자책으로 만드는 Windows 프로그램입니다.

현재 버전은 `v1.0 RC`입니다.

## 주요 기능

- 여러 PDF를 원하는 순서로 병합
- 전자책 표지 자동 생성
- 항목 수에 따라 여러 목차 페이지 자동 생성
- PDF별 제목 편집
- PDF 북마크 생성
- 본문 기준 연속 페이지 번호
- 병합 진행률과 단계별 로그 표시
- 기존 결과 파일을 보호하는 안전한 저장

## 실행 환경

- Windows 10 또는 Windows 11
- Python 3.10 이상

## 개발 환경 실행

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

## 사용 방법

1. `파일 선택`에서 병합할 PDF를 고릅니다.
2. `▲ 위로`, `▼ 아래로` 버튼으로 순서를 정합니다.
3. 필요한 경우 전자책 제목을 수정하고 `적용`을 누릅니다.
4. 출력 폴더와 최종 PDF 파일명을 입력합니다.
5. `전자책 만들기`를 누릅니다.

목차와 북마크에는 화면에 표시된 PDF 순서와 제목이 사용됩니다.

## 테스트

```powershell
python -m unittest discover -s tests -v
```

테스트는 다중 목차, 북마크, 병합 순서, 진행률, 로그와 누락 파일 오류를 확인합니다.

## Windows 실행파일 만들기

```powershell
python -m pip install -r requirements-dev.txt
pyinstaller --noconfirm --clean pdf_book_maker.spec
```

완성된 프로그램은 `dist\PDFBookMaker.exe`에 생성됩니다. 맑은 고딕 폰트 파일은 실행파일에 함께 포함됩니다.

## 프로젝트 구조

```text
main.py                  프로그램 시작
ui_main.py               사용자 화면
file_merge.py            PDF 생성 엔진
assets/fonts/malgun.ttf  표지와 목차용 한글 폰트
tests/                   회귀 테스트
pdf_book_maker.spec      PyInstaller 설정
```

## 현재 제한사항

- 암호가 설정된 PDF는 지원하지 않습니다.
- 병합 작업은 별도 작업 스레드를 사용하지 않습니다.
- ZIP 파일은 지원하지 않습니다.

## 릴리스 전 확인사항

- 실제 Windows 환경에서 대용량 PDF 병합 확인
- 깨끗한 Windows 환경에서 실행파일 실행 확인
- 프로젝트 라이선스 결정 및 `LICENSE` 파일 추가
