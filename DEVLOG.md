# DEVLOG.md

# PDF Book Maker 개발일지

---

# 프로젝트 정보

- 프로젝트명 : PDF Book Maker
- 현재 버전 : v0.3
- 시작일 : 2026-08
- 최근 업데이트 : 2026-08-14

---

# 프로젝트 진행률

████████░░ 80%

---

# 개발 기록

# 2026-08-14

## ✅ 완료

### 표지

- 하단 정보 드래그 이동
- 하단 정보 ↔ SpinBox 양방향 연동
- 그림 위치 조절 Slider → SpinBox 변경
- 그림 세로 위치 조절 방식 통일
- 그림 드래그 이동
- 그림 ↔ SpinBox 양방향 연동
- 제목 / 부제목 / 하단 정보 / 그림 위치 조절 방식 통일

### 페이지 번호

- 페이지 번호 전용 미리보기 구현
- 페이지 번호 메뉴 선택 시 전용 미리보기로 전환
- 짝수/홀수 페이지 위치 선택
- 짝수/홀수 동일 위치 적용
- 페이지 번호 크기 설정
- 시작 번호 설정
- 가로 여백 설정(mm)
- 세로 여백 설정(mm)
- 하이픈(-) 사용 설정
- mm → PDF point 변환 적용
- PDF 출력 여백 계산 수정
- 병합 대상 첫 번째 PDF의 첫 페이지 미리보기 구현
- 실제 PDF 위에 페이지 번호 위치 미리보기 구현
- 미리보기와 실제 PDF 출력 위치 일치 확인

### Git

- Commit 완료
- Push 완료
- Commit :
  `feat: complete cover positioning and page number preview`

---

# 2026-08-13

## ✅ 완료

### 표지

- 제목 정렬 기능
- 제목 세로 위치
- 제목 드래그 이동
- 제목 ↔ SpinBox 양방향 연동
- 제목 PDF 반영

- 부제목 정렬 기능
- 부제목 세로 위치
- 부제목 드래그 이동
- 부제목 ↔ SpinBox 양방향 연동
- 부제목 PDF 반영

- 하단 정보
  - 정렬
  - 세로 위치
  - 줄 간격
  - PDF 반영

### 목차

- 목차 제목 디자인 개선
- 제목 크기 확대
- 상/하단 선 제거

### Git

- Commit 완료
- Push 완료

---

# 수정한 파일

## 2026-08-14

- ui/widgets/cover_preview_widget.py
- ui/widgets/page_number_preview_widget.py
- ui/pages/cover_page.py
- ui/settings_dialog.py
- ui_main.py
- file_merge.py

## 2026-08-13

- ui/widgets/cover_preview_widget.py
- ui/pages/cover_page.py
- ui/settings_dialog.py
- file_merge.py

---

# 남은 작업

## 🔴 v1.0 필수

### 설정

- [ ] 설정 저장
- [ ] 설정 불러오기

### 테스트

- [ ] 전체 기능 테스트
- [ ] 예외 처리

### 배포

- [ ] EXE 제작
- [ ] README.md 작성
- [ ] 사용자 매뉴얼 작성
- [ ] 스크린샷 제작

---

## 🟡 v1.1

- [ ] 표지 자유 배치(X/Y)
- [ ] 드래그 가이드라인
- [ ] 그림 크기 드래그
- [ ] 표지 템플릿

---

# 메모

- 제목 / 부제목 / 하단 정보 / 그림의 세로 위치 드래그 구조 완성
- 표지 위치 조절은 SpinBox 방식으로 통일
- 그림 위치 조절 Slider 제거
- 페이지 번호는 드래그 방식 대신 위치 선택 + mm 여백 방식 사용
- 페이지 번호 미리보기에서 실제 병합 대상 PDF의 첫 페이지 표시
- 페이지 번호 미리보기와 실제 PDF 출력 위치 일치 확인
- 미리보기와 PDF 출력 구조를 가능한 동일하게 유지