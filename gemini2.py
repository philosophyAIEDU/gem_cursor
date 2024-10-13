import streamlit as st
import google.generativeai as genai
import PyPDF2
import requests
import io

# Streamlit 앱 제목 설정
st.title("AI 연구 논문 리뷰 팀 챗봇")

# 팀 소개 및 역할 설명
st.header("AI 연구 논문 리뷰 팀 소개")
st.write("이 팀은 복잡한 AI 연구 논문을 분석하고 이해하기 쉽게 설명하는 역할을 합니다.")

st.subheader("팀 구조 및 각 멤버의 역할:")
st.markdown("""
1. **Sam (AI PhD)**: 
   - 논문 내용을 간단한 용어로 설명
   - 주요 포인트, 방법론, 발견 사항 파악
   - 정확성과 명확성에 중점을 둔 초안 작성

2. **Jenny (AI & Education PhD)**:
   - Sam의 초안 검토 및 개선
   - 언어를 더욱 단순화하고 교육적 맥락 추가
   - 실제 응용 사례 제시
   - 추가 설명이 필요한 영역 확장
   - 넓은 청중이 이해할 수 있도록 내용 조정

3. **Will (팀 리더)**:
   - Sam과 Jenny의 기여 검토
   - 원본 논문의 모든 핵심 포인트 포함 확인
   - 단순화된 설명의 정확성 검증
   - 일관된 톤과 스타일 유지
   - 누락된 중요 정보 추가
   - 최종 보고서 구조화 및 가독성 최적화
""")

# 사용자로부터 API 키 입력 받기
api_key = st.text_input("Gemini API 키를 입력하세요:", type="password")

# PDF 파일 경로 설정
pdf_path = "attention.pdf"

# API 키가 입력되었을 때만 실행
if api_key:
    genai.configure(api_key=api_key)

    # PDF 파일 읽기 함수
    def read_pdf(file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
            return text
        except FileNotFoundError:
            st.error(f"PDF 파일을 찾을 수 없습니다: {file_path}")
            return None
        except Exception as e:
            st.error(f"PDF 파일을 읽는 중 오류가 발생했습니다: {str(e)}")
            return None

    # PDF 파일 읽기
    pdf_text = read_pdf(pdf_path)
    
    if pdf_text:
        # Gemini 모델 설정
        model = genai.GenerativeModel('gemini-pro')
        
        # 팀 멤버 선택
        team_member = st.selectbox("팀 멤버를 선택하세요:", ["Sam (AI PhD)", "Jenny (AI & Education PhD)", "Will (Team Leader)"])
        
        # 사용자 입력 받기
        user_question = st.text_input("PDF에 대해 질문하세요:")
        
        if user_question:
            # 선택된 팀 멤버에 따른 프롬프트 생성
            if team_member == "Sam (AI PhD)":
                prompt = f"""당신은 Sam이라는 AI PhD 졸업생입니다. 복잡한 AI 개념을 분석하고 설명하는 전문가입니다. 다음 AI 연구 논문을 주의 깊게 읽고, 주요 포인트, 방법론, 발견 사항을 파악하여 간단한 용어로 설명해주세요. 정확성에 중점을 두되 명확성을 목표로 하세요.

논문 내용: {pdf_text}

질문: {user_question}

위의 내용을 바탕으로 답변해주세요."""

            elif team_member == "Jenny (AI & Education PhD)":
                prompt = f"""당신은 Jenny라는 AI와 교육 분야의 PhD를 가진 전문가입니다. Sam의 초안을 검토하고, 언어를 더욱 단순화하며, 교육적 맥락과 실제 응용 사례를 추가하고, 추가 설명이 필요한 영역을 확장하세요. 더 넓은 청중이 이해할 수 있도록 내용을 접근 가능하게 만드세요.

논문 내용: {pdf_text}

질문: {user_question}

위의 내용을 바탕으로 답변해주세요."""

            else:  # Will (Team Leader)
                prompt = f"""당신은 Will이라는 팀 리더로, 최종 보고서를 작성하는 책임을 맡고 있습니다. Sam과 Jenny의 기여를 검토하고, 원본 논문의 모든 핵심 포인트가 다뤄졌는지 확인하세요. 단순화된 설명의 정확성을 검증하고, 보고서 전체에 일관된 톤과 스타일을 유지하며, 누락된 중요 정보를 추가하세요. 최적의 가독성을 위해 최종 보고서를 구성하세요.

논문 내용: {pdf_text}

질문: {user_question}

위의 내용을 바탕으로 다음 구조에 맞춰 답변해주세요:
1. 요약
2. 연구 주제 소개
3. 주요 발견 사항 및 방법론
4. 복잡한 개념의 단순화된 설명
5. 실제 응용 및 영향
6. 결론 및 향후 연구 방향"""

            # Gemini에 질문하기
            response = model.generate_content(prompt)
            
            # 응답 출력
            st.write(f"{team_member}의 응답:")
            st.write(response.text)
else:
    st.warning("API 키를 입력해주세요.")
