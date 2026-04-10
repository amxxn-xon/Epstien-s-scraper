"""
Step 3: POS Tagging & Coded Language Annotation
- Tags each email body with Part-of-Speech tags using NLTK
- Flags potential coded language (food items, euphemisms)
- Saves annotated data to JSON

Install first:
    pip install nltk
    python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('punkt_tab'); nltk.download('averaged_perceptron_tagger_eng')"
"""
import json
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

# ---- Coded language / food-item wordlists ----
# These are examples — expand based on your pragmatics research
FOOD_CODE_WORDS = {
    'pizza', 'hotdog', 'hot dog', 'pasta', 'ice cream', 'cheese',
    'burger', 'walnut', 'sauce', 'chicken', 'menu', 'dessert',
    'appetizer', 'entree', 'recipe', 'catering', 'buffet',
    'cookie', 'candy', 'cake', 'pie', 'donut', 'muffin',
    'beef jerky', 'jerky', 'milk', 'grape juice', 'grape'
}

EUPHEMISM_WORDS = {
    'massage', 'party', 'entertainment', 'model', 'modeling',
    'young', 'girl', 'girls', 'friend', 'friends', 'special',
    'arrangement', 'gift', 'package', 'delivery', 'service',
    'visit', 'visitor', 'guest', 'travel', 'trip', 'island',
    'private', 'discreet', 'favor', 'introduce', 'fresh'
}


def annotate_email(email):
    """Tokenize, POS-tag, and flag coded language in one email."""
    body = email['body']
    sentences = sent_tokenize(body)

    tagged_sentences = []
    flagged_words = []

    for sent in sentences:
        tokens = word_tokenize(sent)
        tagged = pos_tag(tokens)  # List of (word, POS) tuples
        tagged_sentences.append(tagged)

        # Check for coded language
        lower_tokens = [t.lower() for t in tokens]
        for word in lower_tokens:
            if word in FOOD_CODE_WORDS:
                flagged_words.append({'word': word, 'category': 'food_code', 'sentence': sent})
            if word in EUPHEMISM_WORDS:
                flagged_words.append({'word': word, 'category': 'euphemism', 'sentence': sent})

    return {
        'id': email['id'],
        'sender': email['sender'],
        'subject': email['subject'],
        'body': body,
        'pos_tagged': [[(w, t) for w, t in sent] for sent in tagged_sentences],
        'flagged_terms': flagged_words,
        'flag_count': len(flagged_words)
    }


def main():
    with open("epstein_clean_data.json", "r", encoding="utf-8") as f:
        clean_data = json.load(f)

    print(f"[*] POS-tagging {len(clean_data)} emails...")

    annotated = []
    total_flags = 0

    for i, email in enumerate(clean_data):
        result = annotate_email(email)
        annotated.append(result)
        total_flags += result['flag_count']
        if result['flag_count'] > 0:
            print(f"  [!] Email {result['id']}: {result['flag_count']} flagged terms")
        if (i + 1) % 10 == 0:
            print(f"  [*] Processed {i+1}/{len(clean_data)}")

    # Sort by flag count (most suspicious first)
    annotated.sort(key=lambda x: x['flag_count'], reverse=True)

    print(f"\n[+] Total flagged terms across corpus: {total_flags}")
    print(f"[+] Emails with at least 1 flag: {sum(1 for a in annotated if a['flag_count'] > 0)}")

    # Save annotated data
    with open("epstein_annotated.json", "w", encoding="utf-8") as f:
        json.dump(annotated, f, indent=4, ensure_ascii=False)
    print("[+] Saved to epstein_annotated.json")


if __name__ == "__main__":
    main()
