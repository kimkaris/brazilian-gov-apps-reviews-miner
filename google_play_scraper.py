from google_play_scraper import reviews_all
import pandas as pd
import re

APP_IDS = [
    "br.gov.serpro.cnhe",
    "br.gov.meugovbr",
    "br.gov.dataprev.meuinss"
]


def clean_text(text):
    if text is None:
        return ""
    return re.sub(r"[\x00-\x08\x0B-\x1F\x7F-\x9F]", "", text)


def collect_reviews(app_ids, max_stars=None):
    results = []

    for app_id in app_ids:
        print(f"\n🔍 Collecting reviews for app: {app_id}")
        reviews = reviews_all(
            app_id,
            lang='pt',
            country='br'
        )

        print(f"  → Total reviews found: {len(reviews)}")

        for idx, review in enumerate(reviews, 1):
            score = review['score']
            text = review.get('content')

            if text is None:
                continue

            if max_stars is not None and score > max_stars:
                continue

            results.append({
                "app_id": app_id,
                "stars": score,
                "review": clean_text(text)
            })

            if idx % 100 == 0:
                print(f"    → Processed {idx} reviews...")

    return results


def save_to_split_xlsx(reviews, base_name="app_reviews"):
    max_rows = 1_000_000
    total = len(reviews)
    parts = (total // max_rows) + (1 if total % max_rows else 0)

    for i in range(parts):
        part_df = pd.DataFrame(reviews[i * max_rows : (i + 1) * max_rows])
        file_name = f"{base_name}_part_{i+1}.xlsx"
        part_df.to_excel(file_name, index=False, columns=["app_id", "stars", "review"])
        print(f"File saved: {file_name} ({len(part_df)} reviews)")


try:
    stars_input = input("Maximum number of stars (1 to 5) or leave empty for all: ").strip()
    max_stars = int(stars_input) if stars_input else None
    if max_stars not in [1, 2, 3, 4, 5, None]:
        raise ValueError()
except:
    print("Invalid input. Getting all reviews.")
    max_stars = None


collected_reviews = collect_reviews(APP_IDS, max_stars)
save_to_split_xlsx(collected_reviews)