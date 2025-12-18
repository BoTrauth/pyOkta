import json

data = {
    "d": "M1gdin8p4WrhT6VG0t5Swd1boyILJwhLYS2MTXEZQ_hMwgRPuC-YAEihzjrd7D2sLvLhpBYL5d4u32yhzQQfnF1X_TdXeNkNx_y_gJfnYIiUncDG4jECYxqBeDEFNZAqhZF7mj2qOxFI4NnlgfsAwU0GVmfjGd8LnyzIyFfahqO2uWR5XdNamsLFUpGcbKsip45Z5QuLn4kRwsKV4FzzSMfLFRex8jnWtV-A7fnbVupHw_I7xAqb6fYyNXnR5gkYSp40VUT3qf4i6rXpEBS8qP5QoJagVf4Pmh0S0kWaD6kjtGaa07yOVuOULdWV0sYImEcMtpKmcbFs42tiqMXV",
    "p": "7l3T1WB63i1bEjFnosY0RV_5aspfuBz10D42D5r1-L5I8hw3PO66-5-hu2zGXic6CmiVNRyWzG1IQke9o_RaEBDG3nye133UVXDdrjPclASYq0eigZTBgp8zOrL6hMyIndNpIFKzy5s-bof1YLV-Xu_lQaAmtAZHb3uqrhO5EeU",
    "q": "td5ItuNMkm9euLmVBfQykhV_KHnE1QSh3mGvlfGUf6XDrBz4xVhuHx82hR10raIXRrso7-oCoXqWWoLQEUrbQ7Lp4aybEkmPnYzYMIKheo6_21auXWp0xRLc7fXZLm-nXNUcyVMqpL3tyr-nPy_CI3XlxS1b07YC9N3B261nucU",
    "dp": "H3ulDvm_QLkc3jpIReeH3-HdP42bNuYcUXTmDwmYk1IOsGupoBKn_7QF2It1Z9omgFlv26P7BuUoNhjjo1QS0SxmF9y93hhwgxh1Lx0KdUJmJ7k-bX8IUAhW69nX3NJm-PGDYRGLTckjZdXvQua12jQ1Q4WzlvN9W-wpjvRr7UE",
    "dq": "iz_GBxokL97L9L5LhwKBke6ZrOEHP17LnVzINxOAcvf1yRtpsphRwMyCTwvNoYCBN-vnnUJcf01AP873BrZ9Cem8P8mL9kWSi7wib4oln5Qa_BLzcJ0pCRe3Rw-9GVvuFhsqbk-aUAcIQfvaT3v-tm333rArJf-vZdNBMjUkPU0",
    "qi": "KltdvlkMXSvzS4rp3unz29W7WUVLW_x0vZocMlMVG6PqWuNDhA-rRasmbDfFbuKAq2049UbUzqSTfinG6U19KKJepGnhDv4A2sRjkGJsEsphcq9bYv1QCLm1kFtxw2XZ2x9MLrwW-x-mYx2i7Bx6b2MCtuIcCU3iijFZ1UV5p8Q",
    "kty": "RSA",
    "e": "AQAB",
    "kid": "Q947mdnX3BRzXcOekL4pdjJ3zYW_qeTfF0jQPJt4o5I",
    "n": "qVdP2D4tpYIwJiKdOwUYkfsRBBe-faO47DY9vo3b6nu2Diz_SHUzGJtETXpS5TUNxGxwvJ4iFr5GTFU3f1AYiycnANa8H8Yf0ZiC-UceaPdXEa6pJHMUkR9QhnfML3yz9y8inPhcrkib7n3eL-fJv1hqDo0nkcFE9l_S6HK47xiiGw2oc06vzyft0qs1fHInpezCrpeLB4kMWGzpVeQzIM1irhOzAcrrErqJLicKoNXpQ8LIXtBpkyVtMgioSBtRXJA20q_VlmXyobbEGY9Shh6DWhxzAlognO0ZkqpnWOdhV1VPJPbCMkTnU4phJAfRJgxOBGycfwiUYRiq33xCOQ"
}

json_string_compact = json.dumps(data, separators=(',', ':'))
escaped_str = json_string_compact.replace('"', '\\"')
print(escaped_str)  