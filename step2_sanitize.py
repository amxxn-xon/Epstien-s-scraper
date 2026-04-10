"""
Step 2: Sanitize and clean the raw scraped data
- Removes HTML tags, extra whitespace, redaction blocks
- Removes duplicates
- Filters out emails with no usable body text
- Saves clean data to JSON
"""
import json
import re


def clean_text(text):
    """Remove HTML, normalize whitespace, strip redaction markers."""
    if not text:
        return ""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Remove redaction blocks (unicode block chars)
    text = re.sub(r'[\u2588]+', '[REDACTED]', text)
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove non-printable characters
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    return text


def main():
    # Load raw data
    with open("epstein_raw_data.json", "r", encoding="utf-8") as f:
        raw = json.load(f)

    print(f"[*] Loaded {len(raw)} raw emails")

    clean_data = []
    seen_texts = set()

    for email in raw:
        body = clean_text(email.get('body', ''))
        subject = clean_text(email.get('subject', ''))
        sender = clean_text(email.get('sender', ''))

        # Skip if no body text
        if len(body) < 20:
            continue

        # Skip duplicates (by body text)
        text_hash = hash(body[:200])
        if text_hash in seen_texts:
            continue
        seen_texts.add(text_hash)

        clean_data.append({
            'id': email.get('id', ''),
            'sender': sender,
            'subject': subject,
            'body': body
        })

    print(f"[+] After cleaning: {len(clean_data)} usable emails")

    # Save clean data
    with open("epstein_clean_data.json", "w", encoding="utf-8") as f:
        json.dump(clean_data, f, indent=4, ensure_ascii=False)
    print("[+] Saved to epstein_clean_data.json")


if __name__ == "__main__":
    main()
