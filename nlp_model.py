from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
# from konlpy.tag import Okt

class NLPHandler:
    def __init__(self):
        self.intent_data = {
            "greeting": ["안녕", "안녕하세요", "반가워"],
            "farewell": ["안녕히 가세요", "잘가", "다음에 또 만나요"],
            "recommend": ["메뉴 추천해줘", "뭐 먹을까?", "오늘의 메뉴는 뭐야?", "뭘 먹을지 모르겠어", "결정 장애 있어"],
            "": [],
            "": [],
            "": [],
        }

        self.tokenizer = Okt()

        # 인텐트 분류기 학습
        self.train_intent_classifier()

    def train_intent_classifier(self):
        # 데이터 준비
        labels = []
        texts = []
        for intent, phrases in self.intent_data.items():
            for phrase in phrases:
                labels.append(intent)
                texts.append(" ".join(self.tokenizer.morphs(phrase)))

        # TF-IDF Vectorizer
        self.vectorizer = TfidfVectorizer()
        X = self.vectorizer.fit_transform(texts)

        # LinearSVC 분류기 학습
        self.classifier = LinearSVC()
        self.classifier.fit(X, labels)

    def classify_intent(self, query):
        query = " ".join(self.tokenizer.morphs(query))
        X = self.vectorizer.transform([query])
        return self.classifier.predict(X)[0]
    
    def extract_keywords(self, text):
        # Okt의 pos 함수를 사용하여 키워드를 추출합니다.
        tokens = self.tokenizer.pos(text, stem=True)
        keywords = [word for word, tag in tokens if tag in ['Noun', 'Verb']]  # 명사와 동사만 추출
        return keywords

