"""
Step 4: Export corpus for AntConc and Voyant Tools
- AntConc: needs individual .txt files (one per email) in a folder
- Voyant: needs a single combined .txt file (or upload the folder)
- Also exports a POS-tagged version for linguistic analysis
"""
import json
import os


def main():
    with open("epstein_clean_data.json", "r", encoding="utf-8") as f:
        clean_data = json.load(f)

    # --- AntConc: one .txt file per email ---
    antconc_dir = "corpus_antconc"
    os.makedirs(antconc_dir, exist_ok=True)

    for email in clean_data:
        filename = f"{email['id']}.txt"
        filepath = os.path.join(antconc_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Subject: {email['subject']}\n")
            f.write(f"Sender: {email['sender']}\n")
            f.write(f"---\n")
            f.write(email['body'])

    print(f"[+] AntConc corpus: {len(clean_data)} files saved to '{antconc_dir}/'")
    print(f"    -> Open AntConc > File > Open Dir > select '{antconc_dir}'")

    # --- Voyant: single combined file ---
    with open("corpus_voyant.txt", "w", encoding="utf-8") as f:
        for email in clean_data:
            f.write(f"=== EMAIL: {email['id']} ===\n")
            f.write(f"Subject: {email['subject']}\n")
            f.write(f"Sender: {email['sender']}\n\n")
            f.write(email['body'])
            f.write("\n\n")

    print(f"[+] Voyant corpus: saved to 'corpus_voyant.txt'")
    print(f"    -> Go to https://voyant-tools.org/ > Upload 'corpus_voyant.txt'")

    # --- POS-tagged export (word/TAG format for linguistic tools) ---
    if os.path.exists("epstein_annotated.json"):
        with open("epstein_annotated.json", "r", encoding="utf-8") as f:
            annotated = json.load(f)

        with open("corpus_pos_tagged.txt", "w", encoding="utf-8") as f:
            for email in annotated:
                f.write(f"=== {email['id']} ===\n")
                for sent in email.get('pos_tagged', []):
                    tagged_str = ' '.join(f"{word}/{tag}" for word, tag in sent)
                    f.write(tagged_str + "\n")
                f.write("\n")
        print(f"[+] POS-tagged corpus: saved to 'corpus_pos_tagged.txt'")

    # --- Flagged terms summary (for quick reference) ---
    if os.path.exists("epstein_annotated.json"):
        with open("epstein_annotated.json", "r", encoding="utf-8") as f:
            annotated = json.load(f)

        with open("flagged_terms_report.txt", "w", encoding="utf-8") as f:
            f.write("FLAGGED CODED LANGUAGE REPORT\n")
            f.write("=" * 50 + "\n\n")
            for email in annotated:
                if email['flag_count'] > 0:
                    f.write(f"Email: {email['id']}\n")
                    f.write(f"Subject: {email['subject']}\n")
                    f.write(f"Flags: {email['flag_count']}\n")
                    for flag in email['flagged_terms']:
                        f.write(f"  [{flag['category']}] \"{flag['word']}\" -> {flag['sentence']}\n")
                    f.write("\n")
        print(f"[+] Flagged terms report: saved to 'flagged_terms_report.txt'")


if __name__ == "__main__":
    main()
