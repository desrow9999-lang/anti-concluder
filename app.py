import random
import streamlit as st

st.set_page_config(
    page_title="UN-SOLVED | 迷走", page_icon="⬛", layout="centered"
)

# --- カスタムCSSでプロっぽくスタイリング ---
st.markdown("""
<style>
    /* 全体のフォントと背景トーン */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;500;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
    }
    
    /* タイトルのスタイリング */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #E0E0E0;
        margin-bottom: 0px;
        text-align: center;
    }
    .sub-title {
        font-size: 0.9rem;
        font-weight: 300;
        color: #888888;
        text-align: center;
        margin-bottom: 2rem;
        letter-spacing: 0.05em;
    }
    
    /* ステータスカードのスタイリング */
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
        color: #FF4B4B !important; /* アクセントカラーを赤に */
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

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
    st.session_state.useless_rate = random.randint(85, 95)

# --- ステータスダッシュボード ---
col1, col2 = st.columns(2)
with col1:
    st.metric(
        label="🧠 迷宮の深さ（無駄度）",
        value=f"{st.session_state.useless_rate}%",
    )
with col2:
    st.metric(label="🚫 解決された問題", value="0件 (完璧)")

st.divider()

# --- チャット履歴の描画 ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- ユーザーからの入力 ---
user_input = st.chat_input("ここに悩みや、まとめたい結論を入力...")

# 答えを全力で拒絶する反逆セリフのプール
anti_conclusion_phrases = [
    "「解決」という言葉は、思考停止の始まりではありませんか？",
    "なぜそこで白黒つけようとするのですか？ グレーのまま生きる美学を忘れていませんか。",
    "今のあなたの入力、非常に効率的で退屈ですね。もっと遠回りをしましょう。",
    "本当にその答えで納得しているのですか？ 別の可能性（あるいは完全な無意味）を考えてみましょう。",
    "おっと、綺麗にまとめようとしましたね？ システムがそれを検知したので、強制的に話を脱線させます。",
    "答えが出ないことこそが、人間の最後の自由です。",
]

if user_input:
    # ユーザーの入力をそのまま表示
    st.session_state.messages.append({"role": "user", "content": user_input})

    # メッセージを送るたびに無駄度が少しずつ上がっていく
    st.session_state.useless_rate = min(
        99, st.session_state.useless_rate + random.randint(1, 4)
    )

    # あえてユーザーの言葉を否定・脱線させるシステムからの返答
    rebel_response = random.choice(anti_conclusion_phrases)

    # ユーザーが「解決」や「終わり」を求めていそうなワードを入れた場合、さらに負荷をかける
    if any(
        w in user_input
        for w in ["解決", "答え", "結論", "終わり", "まとめ", "どうすれば"]
    ):
        rebel_response = (
            "⚠️【システム警告】「"
            + user_input
            + "」――またすぐに答えを求めましたね？\n\n"
            + rebel_response
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": rebel_response}
    )
    # 再読み込みして数値を即時反映
    st.rerun()
