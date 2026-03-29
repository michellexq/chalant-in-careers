"""
dialogue.py – Hardcoded conversation scripts for all three career scenarios.

Each scenario has:
  - intro        : opening line from the NPC / narrator
  - npc_name     : who the player is talking to
  - context      : brief situation description shown to player
  - turns        : list of dicts {npc, player_choices: [A,B,C], feedback_hint}
                   The player picks A/B/C; after MAX_TURNS the script ends.
  - ratings      : thresholds for score → {great/ok/poor} + wages
"""

# ── Score weights per choice ───────────────────────────────────────────────────
# Each turn has 3 choices rated [2, 1, 0] points (best→worst)

CLINIC_DOCTOR = {
    "role":    "Doctor",
    "setting": "The Clinic – Consultation Room",
    "intro":   (
        "Welcome, Dr. {name}! Your first patient has just been brought in. "
        "They look pale and are holding their stomach. Take a deep breath — "
        "you've got this. Type your greeting to begin."
    ),
    "npc_name":  "Patient (Mr. Tan)",
    "context":   "Mr. Tan, 45, reports sharp stomach pain since this morning. No fever.",
    "turns": [
        {
            "npc": "Doctor... I've had this awful stomach pain since breakfast. I can barely stand.",
            "choices": [
                ("A) Good morning, Mr. Tan. I'm sorry to hear that. Can you describe the pain for me?",   2),
                ("B) Hmm. When exactly did it start? Morning, afternoon?",                                1),
                ("C) Okay, we'll run some tests. Sit down.",                                              0),
            ],
            "hint": "Empathy + open question is the gold standard opener."
        },
        {
            "npc": "It started around 7 AM. Sharp, like a cramp, mostly on the right side.",
            "choices": [
                ("A) Right side — has the pain moved or stayed in the same spot?",                       2),
                ("B) On a scale of 1–10, how bad is the pain right now?",                                1),
                ("C) Sounds like appendix. I'll book surgery.",                                          0),
            ],
            "hint": "Gather more history before jumping to conclusions."
        },
        {
            "npc": "It's stayed on the right side. About a 7 out of 10. I feel nauseous too.",
            "choices": [
                ("A) Nausea as well — have you had any vomiting, or changes in appetite?",                2),
                ("B) I see. Are you on any medications currently?",                                       1),
                ("C) That's probably food poisoning. Drink water.",                                      0),
            ],
            "hint": "Follow the symptom trail systematically."
        },
        {
            "npc": "No vomiting. I haven't eaten much since last night actually.",
            "choices": [
                ("A) Okay. I'd like to press gently on your abdomen — please let me know if it hurts.",  2),
                ("B) Any recent travel or unusual food?",                                                 1),
                ("C) We'll do a blood test. Nurse!",                                                     0),
            ],
            "hint": "Explaining the examination builds patient trust."
        },
        {
            "npc": "Ow — that spot is very tender when you press it!",
            "choices": [
                ("A) Thank you for letting me know. I'm concerned it could be appendicitis. I'd like to refer you for an urgent ultrasound.",  2),
                ("B) Rebound tenderness noted. I'll order tests.",                                        1),
                ("C) It's fine, probably just gas.",                                                     0),
            ],
            "hint": "McBurney's point tenderness is a red flag — act on it."
        },
        {
            "npc": "Appendicitis? That sounds serious… what happens next?",
            "choices": [
                ("A) I understand this is worrying. We'll get an ultrasound to confirm. If it is appendicitis, surgery is common and very safe.",  2),
                ("B) Don't panic. We need to confirm first.",                                            1),
                ("C) It'll be fine. We'll sort it.",                                                    0),
            ],
            "hint": "Calm reassurance with a clear plan reduces patient anxiety."
        },
        {
            "npc": "Okay, Doctor. Thank you for explaining everything. I feel a bit better knowing what to expect.",
            "choices": [
                ("A) You're very welcome, Mr. Tan. I'll arrange the ultrasound now and check in on you shortly.",  2),
                ("B) Good. The nurse will take you through.",                                            1),
                ("C) Alright. Next!",                                                                   0),
            ],
            "hint": "A warm closing statement leaves the patient feeling cared for."
        },
    ],
}

CLINIC_PSYCH = {
    "role":    "Psychologist",
    "setting": "The Clinic – Therapy Room",
    "intro":   (
        "Welcome, {name}. Your first client is here. "
        "She's a university student referred for anxiety. Create a safe space — "
        "your words matter more than you know."
    ),
    "npc_name":  "Client (Mei, 20)",
    "context":   "Mei is a 2nd-year student. She's been struggling with exam anxiety and sleep issues for 3 months.",
    "turns": [
        {
            "npc": "Hi… I've never done therapy before. I'm not really sure what to say.",
            "choices": [
                ("A) That's completely okay, Mei. There's no right or wrong way to start. Take your time.",  2),
                ("B) Just tell me what's been going on.",                                                    1),
                ("C) Let's begin. What are your main symptoms?",                                             0),
            ],
            "hint": "Normalising uncertainty helps first-time clients feel safe."
        },
        {
            "npc": "I've just been really stressed about exams. I can't sleep and I keep thinking the worst.",
            "choices": [
                ("A) That sounds exhausting. How long has this been going on for you?",                  2),
                ("B) What kind of thoughts come up?",                                                    1),
                ("C) Have you tried breathing exercises?",                                               0),
            ],
            "hint": "Acknowledge the feeling before probing for details."
        },
        {
            "npc": "About three months. It gets worse the week before any assessment.",
            "choices": [
                ("A) So it's closely tied to assessments. What goes through your mind in those moments?",  2),
                ("B) Three months is a while. Are you eating properly?",                                   1),
                ("C) That's normal for students. It'll pass.",                                             0),
            ],
            "hint": "Linking the pattern helps the client gain insight."
        },
        {
            "npc": "I keep thinking I'm going to fail and disappoint everyone — my parents especially.",
            "choices": [
                ("A) That sounds like a lot of pressure. Tell me more about those expectations — are they coming from your parents, or from yourself?",  2),
                ("B) Why do you think you'll fail?",                                                                                                    1),
                ("C) You should try not to think like that.",                                                                                           0),
            ],
            "hint": "Exploring the source of the pressure is key."
        },
        {
            "npc": "Both, I think. But I also just… feel like I'm not good enough.",
            "choices": [
                ("A) What you're describing sounds like it might be connected to self-worth beyond just grades. Has this feeling of 'not being good enough' come up in other areas of your life?",  2),
                ("B) What evidence do you have for that?",                                                                                                                                          1),
                ("C) Lots of people feel that way. You'll be fine.",                                                                                                                               0),
            ],
            "hint": "Widening the inquiry can reveal deeper patterns."
        },
        {
            "npc": "Yeah… I guess I feel it with friendships too. Like people will leave if I'm not doing well.",
            "choices": [
                ("A) That's a really important insight, Mei. It sounds like your sense of belonging feels conditional. That's something we can work on together.",  2),
                ("B) That's a cognitive distortion. We can address it.",                                                                                           1),
                ("C) Your friends won't leave you over grades.",                                                                                                   0),
            ],
            "hint": "Validating the insight encourages the client's self-awareness."
        },
        {
            "npc": "I've never really thought about it that way. It's… kind of a relief to say it out loud.",
            "choices": [
                ("A) I'm glad it feels that way. Naming it is the first step. We'll keep exploring this together — you're not alone in this.",  2),
                ("B) Good. We'll continue next session.",                                                                                      1),
                ("C) Okay. Homework: write down three positive things about yourself.",                                                        0),
            ],
            "hint": "A warm, forward-looking close builds therapeutic alliance."
        },
    ],
}

HOTEL_SCRIPT = {
    "role":    "Hotel Front Desk",
    "setting": "The Grand Hotel – Reception",
    "intro":   (
        "Welcome to the Grand Hotel, {name}! ✨ "
        "Your first guest has just walked up to the front desk. "
        "Smile, stay professional, and make them feel at home."
    ),
    "npc_name":  "Guest (Ms. Rivera)",
    "context":   "Ms. Rivera booked a Deluxe room for 2 nights. She looks tired from a long flight.",
    "turns": [
        {
            "npc": "Hi, I have a reservation. Rivera. I'm absolutely exhausted from my flight.",
            "choices": [
                ("A) Good evening, Ms. Rivera! Welcome. I'll get you checked in right away — you must be ready for some rest.",  2),
                ("B) Sure. Can I see your ID and booking confirmation?",                                                        1),
                ("C) Name?",                                                                                                    0),
            ],
            "hint": "Acknowledge the guest's state before jumping into process."
        },
        {
            "npc": "Thank you. Here's my booking. I requested a high floor — I really hope that's available.",
            "choices": [
                ("A) Let me check for you right now. *types* Great news — I can offer you Room 1204, a Deluxe on the 12th floor with a city view.",  2),
                ("B) I'll check. We can't always guarantee floor preference.",                                                                       1),
                ("C) Whatever's available — we're nearly full.",                                                                                     0),
            ],
            "hint": "Deliver good news warmly; manage expectations kindly."
        },
        {
            "npc": "Oh, the 12th floor! That's perfect. Does it have a view?",
            "choices": [
                ("A) It faces the city skyline — you'll have a beautiful view, especially at night!",   2),
                ("B) Yes, city-facing.",                                                                 1),
                ("C) I think so.",                                                                       0),
            ],
            "hint": "Specific, enthusiastic detail enhances the guest experience."
        },
        {
            "npc": "Lovely. Is there a spa in the hotel? I could really use a massage.",
            "choices": [
                ("A) We do! The Serenity Spa is on Level 3 — open until 10 PM tonight, so you still have time. Shall I book you a slot?",  2),
                ("B) Yes, Level 3. Closes at 10.",                                                                                        1),
                ("C) I'm not sure. You can check the brochure.",                                                                           0),
            ],
            "hint": "Proactively offering to help is the hallmark of great hospitality."
        },
        {
            "npc": "A slot at 8:30 PM would be wonderful. Oh — and where's the nearest good restaurant?",
            "choices": [
                ("A) Booked! For dinner, I'd recommend Ember on the ground floor — it's our award-winning restaurant. Shall I make a reservation there too?",  2),
                ("B) We have a restaurant downstairs. Or there are places nearby.",                                                                             1),
                ("C) There's a map in your room.",                                                                                                             0),
            ],
            "hint": "Going the extra mile with an offer builds real loyalty."
        },
        {
            "npc": "You're making this so easy! One last thing — what time is checkout?",
            "choices": [
                ("A) Checkout is 11 AM, but if you need a late checkout I can arrange 1 PM at no extra charge — just let me know by morning.",  2),
                ("B) 11 AM. Late checkout may incur a fee.",                                                                                   1),
                ("C) 11 AM sharp.",                                                                                                            0),
            ],
            "hint": "A proactive offer of late checkout is a classic hospitality win."
        },
        {
            "npc": "Late checkout at 1 PM — yes please! Thank you so much, you've been incredibly helpful.",
            "choices": [
                ("A) It's my pleasure, Ms. Rivera! I've noted the late checkout. Enjoy your spa session and dinner — sleep well!",  2),
                ("B) You're welcome. Enjoy your stay.",                                                                            1),
                ("C) No problem. Elevators are on the left.",                                                                      0),
            ],
            "hint": "A personalised farewell completes the impression."
        },
    ],
}

REALESTATE_SCRIPTS = [
    {
        "role":    "Real Estate Salesperson",
        "setting": "The Avenue – House 1 (Starter Cottage)",
        "intro":   (
            "Welcome to The Avenue, {name}! 🏡 "
            "Your first client has just arrived. "
            "They're a young couple looking for their first home. Show them what this cottage has to offer!"
        ),
        "npc_name":  "Client (The Lees – young couple)",
        "context":   "House 1: Cosy 2-bed starter cottage. Pros: affordable, quiet street, garden. Cons: small kitchen, no garage.",
        "turns": [
            {
                "npc": "Hi! We've been looking for ages. What can you tell us about this one?",
                "choices": [
                    ("A) Welcome! This is a charming 2-bedroom cottage — perfect for a first home. It's on a quiet street with a lovely garden out back.",  2),
                    ("B) It's a 2-bed. Good price point for the area.",                                                                                    1),
                    ("C) It's on the listing. Did you read it?",                                                                                           0),
                ],
                "hint": "Paint a picture — buyers buy with emotion first."
            },
            {
                "npc": "A garden! We love that. What's the kitchen like?",
                "choices": [
                    ("A) The kitchen is compact but well laid out — great for cooking together! And honestly, the garden is big enough to add a summer outdoor kitchen one day.",  2),
                    ("B) It's a bit small, not going to lie.",                                                                                                                    1),
                    ("C) Standard.",                                                                                                                                               0),
                ],
                "hint": "Acknowledge the downside but pivot to the upside."
            },
            {
                "npc": "We do need space to cook. We love hosting. Is there a garage?",
                "choices": [
                    ("A) There's no garage, but there's a large driveway for two cars, and the shed is surprisingly spacious — storage sorted!",  2),
                    ("B) No garage, sorry.",                                                                                                     1),
                    ("C) Nope.",                                                                                                                  0),
                ],
                "hint": "Reframe the negative into an alternative positive."
            },
            {
                "npc": "What's the neighbourhood like?",
                "choices": [
                    ("A) It's a really lovely, quiet street — mostly families and young professionals. There's a café two minutes' walk away and a park around the corner.",  2),
                    ("B) Quiet. Residential.",                                                                                                                                1),
                    ("C) It's fine.",                                                                                                                                          0),
                ],
                "hint": "Sell the lifestyle, not just the property."
            },
            {
                "npc": "It sounds really nice. What's the asking price?",
                "choices": [
                    ("A) It's listed at $480,000 — which is genuinely strong value for this street. Properties here have appreciated 8% in the last year.",  2),
                    ("B) $480k.",                                                                                                                            1),
                    ("C) It's on the sheet.",                                                                                                                0),
                ],
                "hint": "Back up the price with market context."
            },
            {
                "npc": "That's a stretch for us. Is there any flexibility?",
                "choices": [
                    ("A) I completely understand. The vendors are motivated — I'd be happy to present a strong offer. What figure were you thinking?",  2),
                    ("B) Maybe. I can ask.",                                                                                                           1),
                    ("C) Probably not.",                                                                                                               0),
                ],
                "hint": "Keep negotiation open — it builds trust."
            },
            {
                "npc": "Around $455k. What do you think?",
                "choices": [
                    ("A) That's a reasonable opening. I'll present it to the vendors today and call you by end of day — I think we have a real shot.",  2),
                    ("B) I'll pass it on.",                                                                                                            1),
                    ("C) They'll probably say no.",                                                                                                    0),
                ],
                "hint": "Close with confidence and a clear next step."
            },
        ],
    },
    {
        "role":    "Real Estate Salesperson",
        "setting": "The Avenue – House 2 (Family Home)",
        "intro":   (
            "House 2 is up, {name}! A family of four is here looking for more space. "
            "This is a 4-bed family home — show them it has everything they need."
        ),
        "npc_name":  "Client (The Nguyens – family of 4)",
        "context":   "House 2: Spacious 4-bed family home. Pros: large yard, 2 bathrooms, near schools. Cons: needs kitchen renovation.",
        "turns": [
            {
                "npc": "We have two kids — space is our top priority. Does this place deliver?",
                "choices": [
                    ("A) Absolutely! Four bedrooms, a huge backyard — the kids will love it. And you're in the catchment for Riverside Primary.",  2),
                    ("B) Yeah, it's a 4-bed. Good yard.",                                                                                        1),
                    ("C) It's fairly spacious.",                                                                                                  0),
                ],
                "hint": "Address the client's stated priority directly and enthusiastically."
            },
            {
                "npc": "Riverside Primary — that's where we're hoping to send them! What about the kitchen?",
                "choices": [
                    ("A) The kitchen needs some updating, but that's actually an opportunity — you could design it exactly how you want. The bones of the house are fantastic.",  2),
                    ("B) It's a bit dated, needs work.",                                                                                                                        1),
                    ("C) Old kitchen, yeah.",                                                                                                                                   0),
                ],
                "hint": "A weakness can be reframed as personalisation potential."
            },
            {
                "npc": "How many bathrooms? With two kids, one is a disaster.",
                "choices": [
                    ("A) Two full bathrooms — one ensuite off the master, one for the kids. Morning chaos: solved!",  2),
                    ("B) Two bathrooms.",                                                                             1),
                    ("C) Two.",                                                                                       0),
                ],
                "hint": "Relate the feature to their daily life."
            },
            {
                "npc": "That backyard — is it safe for young children?",
                "choices": [
                    ("A) It's fully fenced, flat, and faces north for sun. There's even a big shade tree — perfect for a swing set!",  2),
                    ("B) Yeah it's fenced.",                                                                                          1),
                    ("C) It's a normal yard.",                                                                                        0),
                ],
                "hint": "Specific details (fenced, flat, north-facing) build confidence."
            },
            {
                "npc": "It's looking promising. What would renovation on the kitchen roughly cost?",
                "choices": [
                    ("A) A mid-range kitchen refresh typically runs $15–25k. Given the property value, it adds more than it costs. I can refer you to a great local builder if you'd like.",  2),
                    ("B) Maybe $20k? Depends what you want.",                                                                                                                                 1),
                    ("C) No idea — that's up to you.",                                                                                                                                       0),
                ],
                "hint": "Showing expertise and offering a resource builds credibility."
            },
            {
                "npc": "That's helpful. What's the price?",
                "choices": [
                    ("A) Listed at $720,000 — very competitive for a 4-bed in this school zone. Similar homes have gone for $750k+.",  2),
                    ("B) $720k.",                                                                                                     1),
                    ("C) It's on the brochure.",                                                                                      0),
                ],
                "hint": "Comparative market data justifies the price."
            },
            {
                "npc": "We'll need to talk it over, but we're very interested.",
                "choices": [
                    ("A) That's completely understandable — it's a big decision! Take your time. I'll send you a full info pack tonight and I'm here if any questions come up.",  2),
                    ("B) Okay. Let me know.",                                                                                                                                   1),
                    ("C) Don't wait too long — there's interest from others.",                                                                                                  0),
                ],
                "hint": "Respect the client's process — pressure closes doors."
            },
        ],
    },
    {
        "role":    "Real Estate Salesperson",
        "setting": "The Avenue – House 3 (Luxury Home)",
        "intro":   (
            "The big one, {name}! House 3 is a luxury property. "
            "Your client is a professional couple looking to upgrade. Bring your A-game."
        ),
        "npc_name":  "Client (The Chens – executive couple)",
        "context":   "House 3: Luxury 5-bed with pool and home office. Pros: premium finishes, prestigious street. Cons: high strata/maintenance.",
        "turns": [
            {
                "npc": "We've seen a lot of properties. This needs to wow us. What makes it stand out?",
                "choices": [
                    ("A) This is one of the finest homes on The Avenue — five bedrooms, a heated pool, and a dedicated home office with natural light. It's built for executives.",  2),
                    ("B) It's a 5-bed with pool. High-end finishes.",                                                                                                              1),
                    ("C) It's one of our more expensive listings.",                                                                                                                0),
                ],
                "hint": "Match the client's energy — they expect confidence."
            },
            {
                "npc": "We both work from home a lot. Tell me about the office.",
                "choices": [
                    ("A) It's a dedicated room on the northern side — soundproofed, fibre-ready, with floor-to-ceiling windows and garden views. Productivity and calm in one space.",  2),
                    ("B) It's a separate room, good size.",                                                                                                                            1),
                    ("C) There's a room you could use as an office.",                                                                                                                  0),
                ],
                "hint": "Luxury clients want details that match their lifestyle."
            },
            {
                "npc": "The pool is heated? Year-round use?",
                "choices": [
                    ("A) Yes — gas-heated with a smart controller. Summer or winter, it's ready whenever you are. The pool deck is Merbau hardwood too.",  2),
                    ("B) Yes, heated. Good pool.",                                                                                                        1),
                    ("C) I believe so.",                                                                                                                   0),
                ],
                "hint": "Technical specifics (gas-heated, smart controller) signal expertise."
            },
            {
                "npc": "What are the ongoing costs like? We've heard pool maintenance is a headache.",
                "choices": [
                    ("A) Great question. Pool servicing runs around $150/month with a local company I can recommend — and the smart system flags any issues early, so no nasty surprises.",  2),
                    ("B) Maybe $100–200 a month. Standard.",                                                                                                                               1),
                    ("C) There will be some costs, yeah.",                                                                                                                                 0),
                ],
                "hint": "Honesty about costs + a solution = trust."
            },
            {
                "npc": "Is the street quiet? We need privacy.",
                "choices": [
                    ("A) This is one of the most private streets in the area — low traffic, mature tree-lined boundary, and the neighbours are long-term residents who value their space.",  2),
                    ("B) Pretty quiet, yeah.",                                                                                                                                              1),
                    ("C) It's a normal suburban street.",                                                                                                                                   0),
                ],
                "hint": "Privacy and exclusivity are top triggers for luxury buyers."
            },
            {
                "npc": "Price? We've seen similar homes quoted north of $1.5M.",
                "choices": [
                    ("A) This is listed at $1.45M — actually under some comparable sales on this street. Given the pool, office, and finishes, it's priced to sell.",  2),
                    ("B) $1.45M. Fair for the area.",                                                                                                               1),
                    ("C) $1.45M.",                                                                                                                                   0),
                ],
                "hint": "Anchoring to comparables validates the price."
            },
            {
                "npc": "We'd like to make an offer. What's the process?",
                "choices": [
                    ("A) Wonderful! I'll prepare the offer documents today. I'd recommend a strong opening given the interest — shall we discuss the figure that works for you?",  2),
                    ("B) I'll send you the paperwork.",                                                                                                                           1),
                    ("C) You fill in the form and I submit it.",                                                                                                                  0),
                ],
                "hint": "Guide the process confidently — close with momentum."
            },
        ],
    },
]


def get_score_rating(score: int, max_score: int) -> tuple:
    """Returns (label, wage, colour_key) based on score percentage."""
    pct = score / max_score if max_score > 0 else 0
    if pct >= 0.75:
        return ("⭐ Outstanding!", 500, "green")
    elif pct >= 0.45:
        return ("👍 Solid Work", 250, "yellow")
    else:
        return ("📈 Keep Practising", 100, "red")


def get_feedback(score: int, max_score: int, role: str) -> list[str]:
    """Returns a list of feedback lines tailored to role and score."""
    pct = score / max_score if max_score > 0 else 0
    if pct >= 0.75:
        return [
            f"Excellent {role} communication!",
            "You showed empathy & clear information.",
            "Your tone was professional and warm.",
            "The client/patient felt genuinely heard.",
        ]
    elif pct >= 0.45:
        return [
            "Good overall, with room to grow.",
            "Try to add more empathy in your openers.",
            "Providing more detail builds more trust.",
            "You're on the right track — keep at it!",
        ]
    else:
        return [
            "This role needs more practice.",
            "Remember: listen before you advise.",
            "Avoid short or dismissive replies.",
            "Empathy and detail are your best tools.",
        ]
