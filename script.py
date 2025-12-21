import json

data = {
    "d": "Win_MWrJFguE4a-UNP8x2VT5NC6seP96a7vrwrUTJPMIx131d0PXhL7BU74hG7NOgTx1jx5BCQDXnYLiGOzsOHjPNiw7LJQcAwrOyCsqDCvAQyDrrRy9BgPr3ZQHn0g3FqecRmflxxPsmpOenBIg-Uk3-gF-wvwVn7WkzH5e7bAJHR6u4GQwOQgHDiKZDVPJWqBM5XwxkfnjzufHbBqvFTXvTuch5q8O73kq_hGJ9nAIIljOc1uQBigfGI-sbqHXpF9LiWRxLfwArJxxF4rVHwA86voeKSsypcVF1GsXCv5Ik0k4vYz24x5qglzGTcdYR745cJwzVgogTD1xQ4Iv",
    "p": "uiOa0jdsQL_YYRdRlaVDMV-xYhwH6WsKA43snUcgO0zY0ak9olg_2fVICTfz9V-cSznk_BShWTfRZJTPm-fMHGLeke8WB01kfaCXRLXKWkYAEnaCATjKiLkHQ1st8-YcrBmIcOoXLWPqkhEat1EKf8kC8tjcB4KjwP2JdLLlI3M",
    "q": "tvilwsbn5RRh_dtmFNhL8XEtWxYDU9-RA1ke4Fw1Qd5ZvEV8bvJwR-4TZJEpZuEWZPmpPCzBNqacW8Fr3nMiMPSvz7Pmms7tuT5vTtb1p9T1EpVY1Q1BPq2PYygN4Jm_eK45aFwmSBv2G3Z2kI1hdiHJUb6_DAOYxmScoZ7JvDs",
    "dp": "Q6GUKzU_-_a4o-5ZEkpNs67VQJR2u3TM2qXChxLEv0cYsHURk98EtCjO16qg1VK78wlCDeVhCo2hYy4-kKMUImw5-kQoeNbB4HNtAuYac9pjRFISwmbkD_FKlkqW07uUR2Ovk3c6nJ9lJ1VXo6uqaOucSqhIqeHppcF5JBGr98k",
    "dq": "kUzr9b2XMef52Wp9qlgKFvZVmlvk0JpdwlbnmiwfbutwP36-zixg1f5OEDLmufhNnGpW5p5z4T52NLdpPgIYSOBHLZ4jpxRk3BKkuesiseD_rX5ESQx5n5icoZWRT6dI0kEo_aMQE3uA-VYd2bUsjG9QPEZJ2PSSQhpr-Dzs3zk",
    "qi": "BWukDPVph-s9B7mPtKGa-KJfEcqHtpf8YeB4X183m8idZxkgThmx8U2pXIfbrCjh9w9bQq6c41K1JvXW5WoExx43g0dGYz5PrAzitVQUVDNOw3zyFnW-60Z5gs93VyoXWxNrZuVtHbZkoY5b6-g8ST0lJ4CfrpO4p6aJV4OdfyI",
    "kty": "RSA",
    "e": "AQAB",
    "kid": "KrQ7N2oUwnJddM79T4GylJDlSg9iAG1okaiiZiGOxiE",
    "n": "hQobFgFxnl3Zh0-edWoXYWwwAbSRkNpNWBsQOP8E8gSwqMy1PZBQ1Va4i26ZO4G4AM0Kw55XR_EQZ86Rf1lMNDmWxbD530IUDYDXKgRY2WTGW0271rwAM0d7B2B9tq9YVtzhpgSuYVjUAL0xtErdZDVm71zqQxsR3cJsdj44sScDoUbsCvr5u3f5RBw54_8JQxfGFPSAgi_-eBR49Q1YjqN04HhR7Ljs8iitLokeU9hOL7ARl_G0lPojkYWmnE3gjzRIazG4WXI05FuWzOk1_TOlS55k3PhjiHp_j1HYIYzytuQ5OJ_h23tQwv-f6BdWplER9Q5fbvuNC6JiUCKfgQ"
}
json_string_compact = json.dumps(data, separators=(',', ':'))
print(json_string_compact)
# escaped_str = json_string_compact.replace('"', '\\"')
# print(escaped_str)  