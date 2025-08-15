import datetime
import requests
from bs4 import BeautifulSoup


def summarize_with_ollama(
    text: str,
    model: str = "llama3.1:latest",
    base_url: str = "http://192.168.1.8:11434",
    length: str = "medium",
    language: str = "Tiếng Việt",
    temperature: float = 0.2,
    timeout: int = 120,
) -> str:
    """
    Call Ollama's /api/generate endpoint to summarize text.
    Returns the summary string.
    """
    url = f"{base_url.rstrip('/')}/api/generate"
    prompt = build_prompt(text, length, language)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
        },
    }

    try:
        resp = requests.post(url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # For /api/generate, the text is under the "response" key when stream=False
        summary = data.get("response", "").strip()
        if not summary:
            raise ValueError("Empty summary returned. Check model name or input text.")
        return summary
    except requests.exceptions.ConnectionError as e:
        raise SystemExit(
            "❌ Không kết nối được tới Ollama. Hãy chắc chắn Ollama đang chạy tại http://localhost:11434.\n"
            "   Gợi ý: mở terminal và chạy: ollama serve"
        ) from e
    except requests.HTTPError as e:
        # Capture helpful error content if available
        try:
            err_msg = resp.json()
        except Exception:
            err_msg = resp.text
        raise SystemExit(f"❌ Lỗi HTTP từ Ollama: {e}\nChi tiết: {err_msg}") from e
    except requests.RequestException as e:
        raise SystemExit(f"❌ Lỗi gọi API Ollama: {e}") from e


def build_prompt(text: str, length: str, language: str) -> str:
    """Create a simple, robust instruction for summarization."""
    length_map = {
        "short": "1-2 câu, ≤ 50 từ",
        "medium": "khoảng 3-5 câu, ≤ 120 từ",
        "long": "khoảng 1 đoạn, ≤ 200 từ",
    }
    length_req = length_map.get(length, length_map["medium"])
    return (
        f"Hãy tóm tắt nội dung này nhưng đừng quá ngắn nhé: {text}"
    )

def get_url_to_summary(url: str) -> str:
    # print(f"Bắt đầu chạy vào lúc {datetime.datetime.now()}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Lấy tiêu đề
    title = soup.find('h1', class_='title-detail').text.strip()

    # Lấy nội dung chính
    article_body = soup.find('article', class_='fck_detail')
    paragraphs = article_body.find_all(['p', 'h2'])

    content = '\n'.join(p.get_text(strip=True) for p in paragraphs)

    print(f"Tiêu đề: {title} - link: {url}")
    summary = summarize_with_ollama(content)
    # print(f"Kết quả: {summary}")

    # print(f"Kết thúc chạy vào lúc {datetime.datetime.now()}")