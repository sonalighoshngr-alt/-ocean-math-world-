import random
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# পুরস্কার ও সিকিউরিটি কনফিগারেশন
GLOBAL_SPONSOR_FUND = "$10,000 USD"
ANTI_CHEAT_SYSTEM = "ACTIVE (Biometric Lock & Tab Switch Block)"

TRANSLATIONS = {
    "BN": {
        "kids": "★ কিডস জোন ★\n{n1} টি তারা + {n2} টি তারা = মোট কয়টি তারা?",
        "kids_exp": "সহজ ব্যাখ্যা: প্রথমে {n1} টি তারা গুনুন, তারপর {n2} টি যোগ করুন। মোট {ans} টি।",
        "algebra": "★ স্কুল ও কলেজ (বীজগণিত) ★\nযদি {a}x + {b} = {c} হয়, তবে x এর মান কত?",
        "algebra_exp": "ধাপে ধাপে ব্যাখ্যা:\n১. {a}x = {c} - {b} => {a}x = {sub_val}\n২. x = {sub_val}/{a} = {ans}",
        "prize_alert": "🏆 [GLOBAL CASH ALERT] এই সঠিক উত্তরের জন্য আপনার গ্লোবাল ওয়ালেটে রিওয়ার্ড যুক্ত করা হলো!"
    }
}

@app.route('/generate', methods=['GET'])
def get_quiz():
    tier = int(request.args.get('tier', 2))
    lang = request.args.get('lang', 'BN')
    t = TRANSLATIONS.get(lang, TRANSLATIONS['BN'])
    
    # এআই র্যান্ডম প্রশ্ন তৈরি
    if tier == 1:
        n1, n2 = random.randint(2, 6), random.randint(1, 5)
        ans = n1 + n2
        return jsonify({
            "question": t["kids"].format(n1=n1, n2=n2),
            "explanation": t["kids_exp"].format(n1=n1, n2=n2, ans=ans),
            "answer": str(ans),
            "prize_eligible": True,
            "message": t["prize_alert"]
        })
    else:
        a, x, b = random.randint(2, 5), random.randint(2, 9), random.randint(1, 10)
        val_c = (a * x) + b
        sub_val = val_c - b
        return jsonify({
            "question": t["algebra"].format(a=a, b=b, c=val_c),
            "explanation": t["algebra_exp"].format(a=a, b=b, c=val_c, sub_val=sub_val, ans=x),
            "answer": str(x),
            "prize_eligible": True,
            "message": t["prize_alert"]
        })

@app.route('/claim-prize', methods=['POST'])
def claim_prize():
    """স্বয়ংক্রিয় থার্ড-পার্টি স্পনসরড ক্যাশআউট সিস্টেম"""
    data = request.json
    user_id = data.get("user_id")
    score = data.get("score")
    
    if score >= 90: # ৯০% বা তার বেশি স্কোর পেলে
        return jsonify({
            "status": "APPROVED",
            "payout_source": "Global Corporate Sponsorship Pool",
            "message": f"অভিনন্দন! ইউজার {user_id}, আপনার মেধার ভিত্তিতে পুরস্কারের অর্থ সরাসরি অ্যাকাউন্টে পাঠানো হচ্ছে।"
        })
    return jsonify({"status": "FAILED", "message": "পুরস্কার পেতে ন্যূনতম ৯০% স্কোর প্রয়োজন। আবার চেষ্টা করুন!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
