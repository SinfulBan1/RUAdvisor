import requests
import json
import time

RMP_GRAPHQL_URL = "https://www.ratemyprofessors.com/graphql"
HEADERS = {
    "Authorization": "Basic dGVzdDp0ZXN0",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
}
SCHOOL_ID = "U2Nob29sLTgyNQ=="
PAGE_SIZE = 100

TEACHERS_QUERY = """
query NewSearchTeachersQuery($text: String!, $schoolID: ID!, $count: Int!, $cursor: String) {
  newSearch {
    teachers(query: { text: $text, schoolID: $schoolID }, first: $count, after: $cursor) {
      edges {
        cursor
        node {
          id
          firstName
          lastName
          department
          avgRating
          avgDifficulty
          numRatings
          wouldTakeAgainPercent
        }
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      resultCount
    }
  }
}
"""


def fetch_all_professors():
    all_professors = []
    cursor = None
    total = None
    page = 0

    while True:
        page += 1
        variables = {
            "text": "",
            "schoolID": SCHOOL_ID,
            "count": PAGE_SIZE,
            "cursor": cursor,
        }

        for attempt in range(3):
            try:
                resp = requests.post(
                    RMP_GRAPHQL_URL,
                    json={"query": TEACHERS_QUERY, "variables": variables},
                    headers=HEADERS,
                    timeout=30,
                )
                resp.raise_for_status()
                data = resp.json()
                break
            except Exception as e:
                print(f"  Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    time.sleep(2)
                else:
                    print("  Giving up on this page.")
                    return all_professors

        teachers_data = data["data"]["newSearch"]["teachers"]

        if total is None:
            total = teachers_data["resultCount"]
            print(f"Total professors to scrape: {total}")

        edges = teachers_data["edges"]
        for edge in edges:
            node = edge["node"]
            all_professors.append({
                "id": node["id"],
                "first_name": node["firstName"],
                "last_name": node["lastName"],
                "department": node["department"],
                "avg_rating": node["avgRating"],
                "avg_difficulty": node["avgDifficulty"],
                "num_ratings": node["numRatings"],
                "would_take_again_pct": node["wouldTakeAgainPercent"],
            })

        print(f"  Page {page}: fetched {len(edges)} professors ({len(all_professors)}/{total})")

        if not teachers_data["pageInfo"]["hasNextPage"]:
            break

        cursor = teachers_data["pageInfo"]["endCursor"]
        time.sleep(0.5)

    return all_professors


if __name__ == "__main__":
    print("Scraping Rate My Professor data for Rutgers University - New Brunswick...")
    print()

    professors = fetch_all_professors()

    output_path = "lib/Data/rutgers_professors.json"
    with open(output_path, "w") as f:
        json.dump(professors, f, indent=2)

    print()
    print(f"Done! Saved {len(professors)} professors to {output_path}")
