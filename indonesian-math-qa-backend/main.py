from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json # Import json for robust parsing
import re   # Import regex module for extracting LaTeX

class QuestionRequest(BaseModel):
    question: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Mengizinkan aplikasi Vue kita terhubung
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/api/ask")
def ask_question(request_body: QuestionRequest):
    # Prompt sistem yang digunakan selama pelatihan, mendorong penalaran Bahasa Indonesia
    # Prompt ini memberitahu model untuk berpikir langkah demi langkah dan melakukannya dalam Bahasa Indonesia.
    system_prompt = "Anda adalah asisten matematika yang membantu. Anda diberikan masalah. Pikirkan masalahnya dan berikan langkah-langkah pengerjaan Anda secara bertahap dalam Bahasa Indonesia. Setelah proses berpikir Anda, berikan jawaban akhir dalam format yang jelas, idealnya menggunakan LaTeX untuk ekspresi matematika."

    # Nama model kustom kita yang dibuat di Ollama
    # Ini harus sesuai dengan nama yang Anda gunakan saat membuat model Ollama Anda
    # (misalnya, di Modelfile Anda: FROM ./your-model.gguf NAME indonesian-reasoning-llm:latest)
    # Diperbarui berdasarkan output `ollama list` Anda:
    model_name = "hf.co/budf93/deepseek-r1-qwen3-8b-indonesian-math-qa:Q4_K_M"

    try:
        # Menggunakan endpoint /api/generate yang lebih umum
        # Payload untuk /api/generate sedikit berbeda dari /api/chat
        payload = {
            "model": model_name,
            "prompt": f"{system_prompt}\n\n{request_body.question}", # Gabungkan system prompt dan pertanyaan
            "stream": False,      # Kita ingin satu respons lengkap
            "options": {
                # Token berhenti ini penting untuk model yang di-finetune dengan format spesifik
                # Ini memberitahu model untuk berhenti menghasilkan setelah mencapai akhir bagian "pemikiran"nya.
                # Sesuaikan jika format output model Anda menggunakan token berhenti yang berbeda.
                "stop": ["</think>"],
                "temperature": 0.2 # Suhu lebih rendah untuk mengurangi keacakan, jawaban lebih terfokus
            }
        }

        # Lakukan permintaan ke API Ollama
        response = requests.post(
            "http://localhost:11434/api/generate", # Mengubah endpoint menjadi /api/generate
            json=payload,
            timeout=300 # Menambahkan timeout untuk permintaan (misalnya, 5 menit)
        )

        # Memicu HTTPError untuk respons yang buruk (4xx atau 5xx)
        response.raise_for_status()

        # Parse respons JSON
        data = response.json()
        print("Raw response from Ollama:", data) # Baris untuk debugging

        model_response_content = None
        # Prioritize extracting content from 'response' (common for /api/generate)
        if 'response' in data:
            model_response_content = data['response']
        # Fallback to 'message.content' (common for /api/chat-like responses)
        elif 'message' in data and 'content' in data['message']:
            model_response_content = data['message']['content']

        if model_response_content:
            # Regex to find LaTeX expressions enclosed in \\( ... \\) or \\[ ... \\]
            # re.DOTALL makes '.' match newlines, important for multi-line LaTeX
            latex_matches = re.findall(r'\\\\\((.*?)\\\\\)|\\\[(.*?)\\\]', model_response_content, re.DOTALL)

            extracted_latex = ""
            if latex_matches:
                # Iterate in reverse to get the last (and likely final answer) LaTeX expression
                for match_tuple in reversed(latex_matches):
                    # match_tuple will be (inline_content, None) or (None, display_content)
                    if match_tuple[0]: # If it's an inline match (from \\( ... \\))
                        extracted_latex = match_tuple[0]
                        break
                    elif match_tuple[1]: # If it's a display match (from \\[ ... \\])
                        extracted_latex = match_tuple[1]
                        break

            if extracted_latex:
                # If a LaTeX expression was successfully extracted, return it
                return {"answer": extracted_latex}
            else:
                # If no LaTeX expression was found in the content
                return {"error": "Model memberikan respons, tetapi tidak ditemukan ekspresi LaTeX yang valid untuk dirender. Respons lengkap: " + model_response_content}
        else:
            # Original error messages for empty content (if no 'response' or 'message.content' was found)
            if data.get('done_reason') == 'load':
                return {"error": "Model dimuat tetapi tidak menghasilkan respons. Mungkin prompt terlalu singkat atau model tidak menghasilkan output untuk input ini."}
            elif data.get('done') and not model_response_content:
                return {"error": "Model selesai memproses tetapi tidak memberikan konten respons. Periksa prompt atau konfigurasi model."}
            else:
                return {"error": "Model tidak memberikan konten respons yang valid atau format respons tidak terduga."}

    except requests.exceptions.ConnectionError:
        # Error spesifik ketika server Ollama tidak berjalan atau tidak dapat dijangkau
        return {"error": "Tidak dapat terhubung ke server Ollama. Pastikan Ollama berjalan di http://localhost:11434."}
    except requests.exceptions.Timeout:
        # Error spesifik ketika permintaan habis waktu
        return {"error": "Permintaan ke Ollama habis waktu. Model mungkin membutuhkan waktu lebih lama untuk merespons."}
    except requests.exceptions.RequestException as e:
        # Menangkap error terkait permintaan lainnya (misalnya, error HTTP)
        return {"error": f"Terjadi kesalahan saat berkomunikasi dengan Ollama: {e}"}
    except json.JSONDecodeError:
        # Error jika respons bukan format JSON yang valid
        return {"error": "Respons dari Ollama bukan format JSON yang valid."}
    except Exception as e:
        # Menangkap error tak terduga lainnya
        return {"error": f"Terjadi kesalahan tak terduga di backend: {e}"}
