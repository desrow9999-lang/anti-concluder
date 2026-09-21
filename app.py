import random
import streamlit as st

st.set_page_config(
    page_title="答えを出さない迷宮", page_icon="🌀", layout="centered"
)

st.title("🌀 答えを出さない迷宮")
st.caption("―― 効率や結論を求める現代への小さな反逆。")

# セッション状態の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "何かを解決したいのですか？ それとも、ただ迷いたいのですか？",
        }
    ]

if "resistance_level" not in st.session_state:
    st.session_state.resistance_level = 0

# ユーザーからの入力
user_input = st.chat_input(
    "ここに悩みや、まとめたい結論を入力してください..."
)

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
            + "」――またすぐに答えを求めましたね？"
            + "\n\n"
            + rebel_response
        )

    st.session_state.messages.append(
        {"role": "assistant", "content": rebel_response}
    )

# チャット履歴の描画
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# サイドバーに現在の「迷宮の深さ」を表示
st.sidebar.title("🧠 迷宮のステータス")
st.sidebar.metric("効率の低さ（無駄度）", f"{random.randint(85, 99)}%")
st.sidebar.info(
    "このアプリは、あなたがスッキリすることを全システムを挙げて邪魔します。"
)
