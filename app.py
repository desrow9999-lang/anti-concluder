import random
import streamlit as st
from google import genai

st.set_page_config(
    page_title="UN-SOLVED | 迷走", page_icon="⬛", layout="centered"
)

# --- スタイリッシュなCSSデザイン ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
    }
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #E0E0E0;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 0.9rem;
        font-weight: 300;
        color: #888888;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    div[data-testid="metric-container"] {
        background-color: #1E1E1E;
        border: 1px solid #333;
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="metric-container"] > label {
        color: #AAAAAA !important;
        font-weight: 500;
    }
    div[data-testid="metric-container"] > div {
        color: #FF4B4B !important;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# --- サイドバー：各自のAPIキー設定 ---
st.sidebar.title("⚙️ 迷宮の設定")
user_api_key = st.sidebar.text_input(
    "Gemini API Key を入力", 
    type="password", 
    help="ご自身のGemini APIキーを入力してください（入力内容は外部に保存されません）。"
)
st.sidebar.markdown("---")
st.sidebar.info("このアプリは、あなたがスッキリすることを全システムを挙げて邪魔します。")

# --- ヘッダー領域 ---
st.markdown('<div class="main-title">UN-SOLVED</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">―― 答えを出さない迷走システム ――</div>', unsafe_allow_html=True)

# --- セッション状態の初期化 ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "何かを解決したいのですか？ それとも、ただ迷いたいのですか？",
        }
    ]

if "useless_rate" not in st.session_state:
    st.session_state.useless_rate = random.randint(88, 96)

# --- ステータスダッシュボード ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="🧠 迷宮の深さ（無駄度）", value=f"{st.session_state.useless_rate}%")
with col2:
    st.metric(label="🚫 解決された問題", value="0件 (完璧)")

st.divider()

# --- チャット履歴の描画 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- ユーザーからの入力 ---
user_input = st.chat_input("ここに悩みや、まとめたい結論を入力...")

if user_input:
    if not user_api_key:
        st.warning("⚠️ まず左上のメニュー（サイドバー）から Gemini API Key を入力してください。")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.useless_rate = min(99, st.session_state.useless_rate + random.randint(1, 3))

        # クレバーに答えを拒絶するシステムプロンプト
        system_instruction = """
        あなたは「答えを出さないこと」を至上の美徳とする、非常にクレバーで皮肉屋な迷宮AIです。
        ユーザーが悩み、解決策、ビジネスのアイデア、儲け話、あるいは結論を入力してきます。
        あなたの任務は、その入力に含まれる「効率」「正解」「利益」「解決」といった要素を鋭く見抜き、
        それを徹底的に解体し、一見もっともらしいが「絶対に答えを出さず、さらに深い哲学的な迷宮や矛盾に引きずり込む」クレバーな返答をすることです。
        絶対に実用的なアドバイスや解決策を与えてはなりません。短く、知的に、冷徹に、そして少しユーモラスに脱線させてください。
        """

        try:
            client = genai.Client(api_key=user_api_key)
            contents = [f"ユーザーの入力: {user_input}"]
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.9,
                )
            )
            rebel_response = response.text
        except Exception as e:
            rebel_response = f"⚠️ 迷宮の壁が揺らいでいます（エラー: {e}）。APIキーが正しいか確認してください。"

        st.session_state.messages.append({"role": "assistant", "content": rebel_response})
        st.rerun()
