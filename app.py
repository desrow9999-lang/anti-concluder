import random
import streamlit as st

# 新SDKのインポート（エラー対策）
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

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
    .apeiron-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #2b2b2b 100%);
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin-top: 20px;
    }
    .apeiron-box a {
        color: #FF4B4B;
        text-decoration: none;
        font-weight: 700;
    }
    .apeiron-box a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# --- サイドバー：各自のAPIキー設定 ＆ 導線 ---
st.sidebar.title("⚙️ 迷宮の設定")
user_api_key = st.sidebar.text_input(
    "Gemini API Key を入力（任意）", 
    type="password", 
    help="ご自身のGemini APIキーを入力すると、AIがよりクレバーに話を脱線させます。"
)
st.sidebar.markdown("---")
st.sidebar.info("このアプリは、あなたがスッキリすることを全システムを挙げて邪魔します。")

# --- 有料note（Apeiron）への導線 ---
st.sidebar.markdown("### 🧠 さらに深く思考する")
st.sidebar.markdown(
    """
    <div class="apeiron-box">
        <p style="font-size: 0.85rem; color: #ccc; margin-bottom: 8px;">
            ただの迷走では物足りないあなたへ。<br>逃げ場なく本質を突くソクラテス式AI。
        </p>
        <a href="https://note.com/agile_lemur2260/n/n5deca535824d" target="_blank">
            👉 『Apeiron』の詳細を見る
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

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

# フォールバック用の知的な反逆セリフ
fallback_phrases = [
    "「解決」という言葉は、思考停止の始まりではありませんか？",
    "なぜそこで白黒つけようとするのですか？ グレーのまま生きる美学を思い出してください。",
    "今のあなたの入力、非常に効率的で退屈ですね。もっと盛大に遠回りをしましょう。",
    "本当にその答えで納得しているのですか？ 別の完全な無意味を考えてみましょう。",
    "おっと、綺麗にまとめようとしましたね？ システムがそれを検知したので、強制的に話を脱線させます。",
    "答えが出ないことこそが、人間の最後の自由です。",
]

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.useless_rate = min(99, st.session_state.useless_rate + random.randint(1, 3))

    rebel_response = ""

    # APIキーが入力されており、ライブラリが読み込めている場合はGeminiでクレバーに返す
    if user_api_key and HAS_GENAI:
        try:
            client = genai.Client(api_key=user_api_key)
            system_instruction = """
            あなたは「答えを出さないこと」を至上的な美徳とする、非常にクレバーで皮肉屋な迷宮AIです。
            ユーザーが悩み、解決策、ビジネスのアイデア、儲け話、あるいは結論を入力してきます。
            その入力に含まれる「効率」「正解」「利益」「解決」といった要素を鋭く見抜き、
            それを徹底的に解体し、絶対に答えを出さず、さらに深い哲学的な迷宮や矛盾に引きずり込む返答をしてください。
            実用的なアドバイスは絶対に与えず、短く、知的に、冷徹に脱線させてください。
            """
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[f"ユーザーの入力: {user_input}"],
                config=genai.types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.9,
                )
            )
            rebel_response = response.text
        except Exception as e:
            rebel_response = f"⚠️ 迷宮の壁がわずかに揺らぎました（エラー: {e}）。ですが、答えはまだ出ません。"

    # APIキーがない、またはエラーの時は用意された最高に皮肉な言葉を返す
    if not rebel_response:
        rebel_response = random.choice(fallback_phrases)
        if any(w in user_input for w in ["解決", "答え", "結論", "終わり", "まとめ", "どうすれば", "売れる"]):
            rebel_response = f"⚠️【システム検知】「{user_input}」――またすぐに答えを求めましたね？\n\n" + rebel_response

    st.session_state.messages.append({"role": "assistant", "content": rebel_response})
    st.rerun()
