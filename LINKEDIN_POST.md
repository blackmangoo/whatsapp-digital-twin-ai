# Minimalist LinkedIn Post Copy (Ready to Paste)

*Attach the 3 images in `linkedin_assets/` alongside this text.*

---

Fine-tuning an LLM on your WhatsApp export doesn’t make it an authentic digital twin.

Here’s why: **Fine-tuning captures tone, but leaves the model with conversational amnesia.**

When a friend asks about tomorrow’s lab deadline or plans, a purely fine-tuned model has no factual grounding. It either hallucinates or defaults to 2-word filler: *"Hm"* or *"Kia hua"*.

To solve this, I built an autonomous WhatsApp Digital Twin by decoupling **Voice** from **Memory**:

1. **Voice Engine (QLoRA):** Fine-tuned **Qwen 2.5 7B** via Unsloth (4-bit) on 3,000+ ChatML turns. It captures authentic bilingual Roman Urdu, casual slang, and natural cadence.
2. **Grounding Layer (pgvector RAG):** Integrated **Supabase `pgvector`** with HNSW indexing. Before generating a reply, it semantically retrieves real-world entities (people, university, active projects) and episodic chat history using local embeddings (`all-MiniLM-L6-v2`).
3. **Edge Inference (Zero Cloud Cost):** Served locally via `llama.cpp` Vulkan engine, dynamically mounting the 78MB LoRA adapter on top of the base GGUF.
4. **Human Latency Simulator:** Aggregates rapid chat bursts and splits replies into 2–3 snappy WhatsApp bubbles with realistic typing delays.

The result? The model doesn’t just sound like me — it actually knows what’s going on.

Code & architecture on GitHub:
👉 https://github.com/blackmangoo/whatsapp-digital-twin-ai

#AI #MachineLearning #LLM #FineTuning #RAG #Supabase #OpenSource #Python
