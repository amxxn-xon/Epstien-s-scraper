"""
Step 1: Scrape full email text from jmail.world API
- The search endpoint already returns full body in matchedEmail.content_markdown
- No need for a separate detail endpoint
- Saves raw data with body text to JSON
"""
import requests
import json
import time

API_BASE = "https://jmail.world/api"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json'
}


def search_emails(query, num_pages=5):
    """Search and collect emails WITH their body text from the search API."""
    all_emails = []
    seen_ids = set()

    for page in range(1, num_pages + 1):
        params = {'q': query, 'limit': 50, 'page': page, 'source': 'all'}
        print(f"[*] Searching page {page}...")
        resp = requests.get(f"{API_BASE}/emails/search", headers=HEADERS, params=params)

        if resp.status_code != 200:
            print(f"[-] Search failed on page {page}: {resp.status_code}")
            break

        data = resp.json()
        items = data.get('results', [])
        if not items:
            print(f"[*] No more results at page {page}.")
            break

        for item in items:
            thread = item.get('thread', {})
            matched = item.get('matchedEmail', {})

            doc_id = thread.get('doc_id', '')
            if not doc_id or doc_id in seen_ids:
                continue
            seen_ids.add(doc_id)

            # The full body is in matchedEmail.content_markdown
            body = matched.get('content_markdown', '')
            subject = thread.get('subject', '')
            sender = (matched.get('sender', '')
                      or thread.get('latest_sender_name', ''))

            all_emails.append({
                'id': doc_id,
                'sender': sender,
                'subject': subject,
                'body': body
            })

        print(f"[+] Got {len(items)} results from page {page} "
              f"({len(all_emails)} unique emails so far)")
        time.sleep(1)

    return all_emails


def main():
    # Search queries — add more to widen your corpus
    # Use food items and code words as queries too
    queries = [
        "jeffrey epstein",
        "pizza",
        "party",
        "massage",
        "island",
        "girl",
        "model",
        "beef jerky",
        "milk",
        "pasta",
        "muffin",
        "grape juice",
    ]

    all_emails = []
    seen_ids = set()

    for query in queries:
        print(f"\n{'='*50}")
        print(f"[*] Query: '{query}'")
        results = search_emails(query, num_pages=5)

        for email in results:
            if email['id'] not in seen_ids:
                seen_ids.add(email['id'])
                all_emails.append(email)

        print(f"[+] Running total: {len(all_emails)} unique emails")

    # Stats
    with_body = sum(1 for e in all_emails if e.get('body', '').strip())
    print(f"\n{'='*50}")
    print(f"[+] Total unique emails: {len(all_emails)}")
    print(f"[+] Emails with body text: {with_body}")

    # Save
    with open("epstein_raw_data.json", "w", encoding="utf-8") as f:
        json.dump(all_emails, f, indent=4, ensure_ascii=False)
    print("[+] Saved to epstein_raw_data.json")


if __name__ == "__main__":
    main()
