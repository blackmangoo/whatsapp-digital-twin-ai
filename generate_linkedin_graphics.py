"""
Generates clean, human-designed 1080x1350 (4:5 Vertical) presentation graphics for LinkedIn.
Aesthetic: Modern technical design (Linear / Vercel style) with authentic WhatsApp dark UI elements.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "linkedin_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH = 1080
HEIGHT = 1350

# Modern Technical Palette (Matte Charcoal, Deep Slate, WhatsApp Emerald)
BG_TOP = (11, 15, 23)        # #0B0F17 Deep Tech Obsidian
BG_BOTTOM = (15, 22, 33)     # #0F1621 Dark Slate
CARD_BG = (19, 27, 38)       # #131B26 Clean Matte Slate
CARD_BORDER = (38, 51, 69)   # #263345 Subtle Structural Border
CARD_INNER_BG = (14, 19, 28) # #0E131C Dark Inset Box

# Typography colors
TEXT_PRIMARY = (241, 245, 249)    # Slate 100
TEXT_SECONDARY = (148, 163, 184)  # Slate 400
TEXT_MUTED = (100, 116, 139)      # Slate 500
ACCENT_GREEN = (0, 168, 132)      # WhatsApp Primary Emerald
ACCENT_BLUE = (56, 189, 248)      # Tech Cyan
ACCENT_RED = (248, 113, 113)      # Alert Red

# WhatsApp Dark Bubble Colors
WA_OUTGOING_BG = (0, 92, 75)      # #005C4B Authentic WhatsApp Outgoing
WA_INCOMING_BG = (32, 44, 51)     # #202C33 Authentic WhatsApp Incoming
WA_TIME = (134, 150, 160)         # #8696A0 Muted timestamp color

def safe_save(img, out_path):
    tmp_path = out_path + ".tmp.png"
    img.save(tmp_path)
    if os.path.exists(out_path):
        try:
            os.remove(out_path)
        except Exception:
            pass
    os.replace(tmp_path, out_path)
    print(f"Saved: {out_path}")

def get_font(size: int, bold: bool = False):
    font_names = [
        "segoeuib.ttf" if bold else "segoeui.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "calibrib.ttf" if bold else "calibri.ttf"
    ]
    for name in font_names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()

def draw_gradient_background(draw):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))

def draw_card(draw, x, y, w, h, bg=CARD_BG, border=CARD_BORDER, radius=12):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=bg, outline=border, width=1)

def draw_chat_bubble(draw, x, y, sender, message, timestamp, bg_color, text_color=TEXT_PRIMARY, time_color=WA_TIME):
    font_msg = get_font(16, bold=False)
    font_time = get_font(11, bold=False)

    full_text = f'{sender}: "{message}"' if sender else f'"{message}"'
    bbox_txt = font_msg.getbbox(full_text)
    txt_w = bbox_txt[2] - bbox_txt[0]

    bbox_time = font_time.getbbox(timestamp)
    time_w = bbox_time[2] - bbox_time[0]

    bubble_w = txt_w + time_w + 36
    bubble_h = 42

    draw.rounded_rectangle([x, y, x + bubble_w, y + bubble_h], radius=8, fill=bg_color)
    draw.text((x + 14, y + 10), full_text, font=font_msg, fill=text_color)
    draw.text((x + bubble_w - time_w - 12, y + 18), timestamp, font=font_time, fill=time_color)
    return y + bubble_h + 10

def draw_pill(draw, x, y, text, bg, fg, font, pad_x=12, pad_y=5):
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.rounded_rectangle([x, y, x + tw + pad_x * 2, y + th + pad_y * 2], radius=6, fill=bg)
    draw.text((x + pad_x, y + pad_y - 1), text, font=font, fill=fg)
    return x + tw + pad_x * 2 + 10

def draw_wrapped_text(draw, text, x, y, max_width, font, fill, line_spacing=5):
    words = text.split(" ")
    lines = []
    current_line = []

    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = font.getbbox(test_line)
        line_w = bbox[2] - bbox[0]
        if line_w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]

    if current_line:
        lines.append(" ".join(current_line))

    curr_y = y
    for line in lines:
        draw.text((x, curr_y), line, font=font, fill=fill)
        bbox = font.getbbox(line)
        line_h = bbox[3] - bbox[1]
        curr_y += line_h + line_spacing

    return curr_y

def draw_header(draw, title, subtitle, slide_num, total_slides=3):
    font_mono = get_font(13, bold=True)
    draw_pill(draw, 60, 48, "ENGINEERING SHOWCASE", (26, 36, 51), ACCENT_BLUE, font_mono)

    slide_str = f"0{slide_num} / 0{total_slides}"
    bbox = font_mono.getbbox(slide_str)
    sw = bbox[2] - bbox[0]
    draw.text((WIDTH - 60 - sw, 52), slide_str, font=font_mono, fill=TEXT_MUTED)

    font_title = get_font(36, bold=True)
    font_subtitle = get_font(18, bold=False)
    draw.text((60, 102), title, font=font_title, fill=TEXT_PRIMARY)
    draw.text((60, 155), subtitle, font=font_subtitle, fill=TEXT_SECONDARY)

    draw.line([(60, 195), (WIDTH - 60, 195)], fill=CARD_BORDER, width=1)

def draw_footer(draw):
    font_footer = get_font(14, bold=False)
    draw.line([(60, HEIGHT - 50), (WIDTH - 60, HEIGHT - 50)], fill=CARD_BORDER, width=1)
    draw.text((60, HEIGHT - 38), "github.com/blackmangoo/whatsapp-digital-twin-ai", font=font_footer, fill=TEXT_MUTED)
    draw.text((WIDTH - 190, HEIGHT - 38), "Ammar Akbar", font=get_font(14, bold=True), fill=TEXT_SECONDARY)


# ====================================================================
# SLIDE 1: SYSTEM ARCHITECTURE
# ====================================================================
def generate_slide_1():
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    draw_gradient_background(draw)

    draw_header(
        draw,
        title="WhatsApp Digital Twin AI Architecture",
        subtitle="Decoupling Conversational Cadence (QLoRA) from Memory (pgvector)",
        slide_num=1
    )

    # Tech Chips
    font_chip = get_font(13, bold=True)
    bx = 60
    bx = draw_pill(draw, bx, 215, "Qwen 2.5 7B Instruct", (20, 35, 30), ACCENT_GREEN, font_chip)
    bx = draw_pill(draw, bx, 215, "Unsloth 4-bit QLoRA", (30, 25, 45), (192, 132, 252), font_chip)
    bx = draw_pill(draw, bx, 215, "Supabase pgvector (HNSW)", (20, 35, 30), ACCENT_GREEN, font_chip)
    bx = draw_pill(draw, bx, 215, "llama.cpp Engine", (35, 30, 20), (251, 191, 36), font_chip)

    card_w = WIDTH - 120
    card_h = 225
    gap = 20
    start_y = 275

    stages = [
        {
            "num": "01",
            "name": "Data Engineering & Burst Fusion",
            "layer": "PREPROCESSING",
            "color": ACCENT_BLUE,
            "summary": "Real WhatsApp messaging occurs in bursts of 3-5 rapid lines per minute.",
            "action": "Engineered a 90-second sliding time-window aggregator that cleans 2.5k media placeholders and merges fragments into 3,024 clean, strictly alternating ChatML turns."
        },
        {
            "num": "02",
            "name": "Knowledge & Episodic RAG",
            "layer": "GROUNDING LAYER",
            "color": ACCENT_GREEN,
            "summary": "Model weights cannot reliably memorize dynamic facts (e.g. assignment status).",
            "action": "Supabase PostgreSQL with pgvector HNSW cosine search. Embeds known entities and past conversations to eliminate conversational amnesia before generation."
        },
        {
            "num": "03",
            "name": "Fine-Tuned LLM (Tone & Voice)",
            "layer": "VOICE ENGINE",
            "color": (192, 132, 252),
            "summary": "Base models default to overly formal corporate assistant English.",
            "action": "Fine-tuned Qwen 2.5 7B via 4-bit QLoRA (Rank=16, Alpha=32). Nails authentic bilingual Roman Urdu, casual university vocabulary, and authentic sentence length."
        },
        {
            "num": "04",
            "name": "Human Latency & Bubble Splitter",
            "layer": "AGENT POST-PROCESSING",
            "color": (251, 146, 60),
            "summary": "Instant paragraph replies immediately reveal bot automation.",
            "action": "Simulates natural human typing latency (2-5s) based on character length, splits responses into 2-3 snappy bubbles, and enforces safety guardrails."
        }
    ]

    font_num = get_font(24, bold=True)
    font_name = get_font(20, bold=True)
    font_layer = get_font(12, bold=True)
    font_lbl = get_font(14, bold=True)
    font_body = get_font(15, bold=False)

    for i, s in enumerate(stages):
        cy = start_y + i * (card_h + gap)
        draw_card(draw, 60, cy, card_w, card_h)

        # Left subtle colored line
        draw.rectangle([60, cy, 64, cy + card_h], fill=s["color"])

        # Number & Layer
        draw.text((85, cy + 18), s["num"], font=font_num, fill=s["color"])
        draw.text((128, cy + 24), s["layer"], font=font_layer, fill=TEXT_MUTED)

        # Title
        draw.text((85, cy + 54), s["name"], font=font_name, fill=TEXT_PRIMARY)

        # Inset divider
        draw.line([(85, cy + 88), (60 + card_w - 25, cy + 88)], fill=CARD_BORDER, width=1)

        # Problem line
        draw.text((85, cy + 102), "• Bottleneck: ", font=font_lbl, fill=TEXT_MUTED)
        draw_wrapped_text(draw, s["summary"], 185, cy + 102, card_w - 130, font_body, TEXT_MUTED)

        # Solution line
        draw.text((85, cy + 138), "• Architecture: ", font=font_lbl, fill=ACCENT_GREEN)
        draw_wrapped_text(draw, s["action"], 195, cy + 138, card_w - 140, font_body, TEXT_SECONDARY, line_spacing=4)

    draw_footer(draw)
    out_path = os.path.join(OUTPUT_DIR, "1_architecture_overview.png")
    safe_save(img, out_path)


# ====================================================================
# SLIDE 2: 3 PRODUCTION HURDLES & ENGINEERING FIXES
# ====================================================================
def generate_slide_2():
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    draw_gradient_background(draw)

    draw_header(
        draw,
        title="3 Production Hurdles & Engineering Fixes",
        subtitle="Technical constraints encountered during edge deployment and how we solved them",
        slide_num=2
    )

    card_w = WIDTH - 120
    card_h = 305
    gap = 25
    start_y = 235

    hurdles = [
        {
            "num": "CHALLENGE 01",
            "title": "The WhatsApp 'Burst' Noise",
            "problem": "Real humans don't text in single clean essays. They send 4 rapid disjointed lines in 30 seconds. Training on raw exported lines produces fragmented, chaotic model output.",
            "fix_title": "Sliding Time-Window Aggregation",
            "fix": "Engineered a timestamp parser in Python that groups consecutive messages from the same sender within 90 seconds into one coherent turn, refining 9.4k raw logs into 3,024 balanced ChatML turns.",
            "color": ACCENT_BLUE
        },
        {
            "num": "CHALLENGE 02",
            "title": "The 20GB Cloud Storage Ceiling",
            "problem": "Merging 7B weights and quantizing full models requires ~30.5GB of temporary disk space during GGUF conversion, causing Kaggle kernels to crash with disk-quota errors.",
            "fix_title": "Decoupled Runtime LoRA Loading",
            "fix": "Exported only the fine-tuned LoRA weights in GGUF format (78MB instead of 30GB). Attached the adapter at runtime using llama-server with zero cloud disk penalty.",
            "color": (251, 191, 36)
        },
        {
            "num": "CHALLENGE 03",
            "title": "Conversational 'Amnesia' & Filler Collapse",
            "problem": "Fine-tuning alone memorized syntax but failed on relational facts ('What is the assignment status?'). The model collapsed into 2-word filler responses like 'Hm' or 'Kia hua'.",
            "fix_title": "Hybrid Supabase pgvector RAG",
            "fix": "Built an external entity and episodic memory layer in Supabase with HNSW indexing. Grounding facts are dynamically injected before generation, eliminating hallucination.",
            "color": ACCENT_GREEN
        }
    ]

    font_tag = get_font(12, bold=True)
    font_h_title = get_font(21, bold=True)
    font_lbl = get_font(14, bold=True)
    font_body = get_font(15, bold=False)

    for i, h in enumerate(hurdles):
        cy = start_y + i * (card_h + gap)
        draw_card(draw, 60, cy, card_w, card_h)

        # Inset header bar
        draw.rounded_rectangle([60, cy, 60 + card_w, cy + 38], radius=12, fill=CARD_INNER_BG)
        draw.rectangle([60, cy + 20, 60 + card_w, cy + 38], fill=CARD_INNER_BG)
        draw.text((85, cy + 11), h["num"], font=font_tag, fill=h["color"])

        # Main Title
        draw.text((85, cy + 54), h["title"], font=font_h_title, fill=TEXT_PRIMARY)

        # Problem Section
        draw.text((85, cy + 96), "PROBLEM:", font=font_lbl, fill=ACCENT_RED)
        draw_wrapped_text(draw, h["problem"], 165, cy + 96, card_w - 110, font_body, TEXT_MUTED, line_spacing=4)

        # Divider
        draw.line([(85, cy + 175), (60 + card_w - 25, cy + 175)], fill=CARD_BORDER, width=1)

        # Fix Section
        draw.text((85, cy + 190), "SOLUTION:", font=font_lbl, fill=ACCENT_GREEN)
        draw.text((165, cy + 190), h["fix_title"], font=get_font(15, bold=True), fill=TEXT_PRIMARY)
        draw_wrapped_text(draw, h["fix"], 85, cy + 220, card_w - 50, font_body, TEXT_SECONDARY, line_spacing=4)

    draw_footer(draw)
    out_path = os.path.join(OUTPUT_DIR, "2_hurdles_and_solutions.png")
    safe_save(img, out_path)


# ====================================================================
# SLIDE 3: COMPARATIVE EVALUATION (REALISTIC WHATSAPP CHAT UI)
# ====================================================================
def generate_slide_3():
    img = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)
    draw_gradient_background(draw)

    draw_header(
        draw,
        title="Comparative Evaluation: LoRA vs. RAG",
        subtitle="Testing factual entity recall & conversational depth on authentic university queries",
        slide_num=3
    )

    card_w = WIDTH - 120

    # 1. Incoming query card (Authentic WhatsApp Incoming Bubble)
    draw_card(draw, 60, 220, card_w, 135)
    draw.text((85, 235), "INCOMING WHATSAPP MESSAGE", font=get_font(12, bold=True), fill=TEXT_MUTED)

    # Incoming chat bubble
    draw.rounded_rectangle([85, 260, 60 + card_w - 25, 335], radius=10, fill=WA_INCOMING_BG)
    draw.text((105, 275), 'Sameer: "Ammar kal subah AI lab ka code submit karna hai,', font=get_font(18, bold=False), fill=TEXT_PRIMARY)
    draw.text((180, 303), 'assignment 5 complete hai tumhara?"', font=get_font(18, bold=False), fill=TEXT_PRIMARY)
    draw.text((60 + card_w - 105, 310), "11:24 PM", font=get_font(12, bold=False), fill=WA_TIME)

    card_h = 395

    # -------------------------------------------------------------
    # 2. Panel 1: WITHOUT RAG (Pure LoRA Fine-Tuning)
    # -------------------------------------------------------------
    cy1 = 380
    draw_card(draw, 60, cy1, card_w, card_h)

    # Header bar
    draw.rounded_rectangle([60, cy1, 60 + card_w, cy1 + 36], radius=12, fill=CARD_INNER_BG)
    draw.rectangle([60, cy1 + 18, 60 + card_w, cy1 + 36], fill=CARD_INNER_BG)
    draw.text((85, cy1 + 10), "WITHOUT RAG (Pure LoRA Fine-Tuning)", font=get_font(13, bold=True), fill=ACCENT_RED)

    # WhatsApp Bubbles (Outgoing)
    draw_chat_bubble(draw, 85, cy1 + 52, "Twin", "Hm", "11:25 PM", CARD_INNER_BG)
    draw_chat_bubble(draw, 85, cy1 + 102, "Twin", "Room may ja ke krta", "11:25 PM", CARD_INNER_BG)

    # Defect Analysis Box
    draw_card(draw, 85, cy1 + 165, card_w - 50, 205, bg=CARD_INNER_BG, border=CARD_BORDER)
    draw.text((105, cy1 + 180), "DEFECT ANALYSIS:", font=get_font(13, bold=True), fill=ACCENT_RED)
    defects = [
        "• Model has zero factual memory of university deadlines or lab tasks.",
        "• Defaults to low-entropy casual filler ('Hm') without addressing the prompt.",
        "• Does not know what Assignment 5 is or whether code was written.",
        "• Fails to provide actionable status, requiring human intervention."
    ]
    dy = cy1 + 208
    for d in defects:
        draw.text((105, dy), d, font=get_font(14, bold=False), fill=TEXT_SECONDARY)
        dy += 27

    # -------------------------------------------------------------
    # 3. Panel 2: WITH SUPABASE RAG (Our Approach)
    # -------------------------------------------------------------
    cy2 = 800
    draw_card(draw, 60, cy2, card_w, card_h)

    # Header bar
    draw.rounded_rectangle([60, cy2, 60 + card_w, cy2 + 36], radius=12, fill=CARD_INNER_BG)
    draw.rectangle([60, cy2 + 18, 60 + card_w, cy2 + 36], fill=CARD_INNER_BG)
    draw.text((85, cy2 + 10), "WITH SUPABASE PGVECTOR RAG (Grounded Digital Twin)", font=get_font(13, bold=True), fill=ACCENT_GREEN)

    # WhatsApp Bubbles (Outgoing - Authentic WhatsApp Green)
    draw_chat_bubble(draw, 85, cy2 + 52, "Twin", "No, abhi lab mai hi baitha hun", "11:25 PM", WA_OUTGOING_BG, time_color=(160, 200, 190))
    draw_chat_bubble(draw, 85, cy2 + 102, "Twin", "Task 1 ho gya hai, baki raat ko push karta hun", "11:25 PM", WA_OUTGOING_BG, time_color=(160, 200, 190))

    # Advantage Analysis Box
    draw_card(draw, 85, cy2 + 165, card_w - 50, 205, bg=CARD_INNER_BG, border=CARD_BORDER)
    draw.text((105, cy2 + 180), "ENGINEERING ADVANTAGE:", font=get_font(13, bold=True), fill=ACCENT_GREEN)
    advantages = [
        "• pgvector retrieves context on FAST NUCES AI lab and 'task1.cpp'.",
        "• Correctly identifies current location ('lab mai') and progress status.",
        "• Communicates in authentic Roman Urdu with natural burst cadence.",
        "• Grounded truth eliminates conversational amnesia and robotic replies."
    ]
    ay = cy2 + 208
    for a in advantages:
        draw.text((105, ay), a, font=get_font(14, bold=False), fill=TEXT_SECONDARY)
        ay += 27

    draw_footer(draw)
    out_path = os.path.join(OUTPUT_DIR, "3_comparative_eval.png")
    safe_save(img, out_path)

if __name__ == "__main__":
    generate_slide_1()
    generate_slide_2()
    generate_slide_3()
    print("All 3 refined vertical LinkedIn graphics generated successfully!")
