from urllib.parse import urlparse
import requests
import concurrent.futures
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logging.basicConfig(level=logging.INFO)

# ReadTheDocs projects and API endpoints
RTD_PROJECTS = {
    "canonical-juju": (
        "https://canonical-juju.readthedocs-hosted.com/_/api/v3/search/"
    ),
    "canonical-terraform-provider-juju": (
        "https://canonical-terraform-provider-juju.readthedocs-hosted.com"
        "/_/api/v3/search/"
    ),
    "pythonlibjuju": ("https://pythonlibjuju.readthedocs.io/_/api/v3/search/"),
    "canonical-jaas-documentation": (
        "https://canonical-jaas-documentation.readthedocs-hosted.com"
        "/_/api/v3/search/"
    ),
    "canonical-charmcraft": (
        "https://canonical-charmcraft.readthedocs-hosted.com/_/api/v3/search/"
    ),
    "ops": "https://ops.readthedocs.io/_/api/v3/search/",
}

# Domain information mapping, title for chips, weight for relevance
DOMAIN_INFO = {
    "canonical-juju.readthedocs-hosted.com": {"title": "Juju", "weight": 0.6},
    "canonical-terraform-provider-juju.readthedocs-hosted.com": {
        "title": "Terraform Juju",
        "weight": 0.5,
    },
    "pythonlibjuju.readthedocs.io": {"title": "Python Libjuju", "weight": 0.4},
    "canonical-jaas-documentation.readthedocs-hosted.com": {
        "title": "JAAS",
        "weight": 0.3,
    },
    "canonical-charmcraft.readthedocs-hosted.com": {
        "title": "Charmcraft",
        "weight": 0.2,
    },
    "ops.readthedocs.io": {"title": "Ops", "weight": 0.1},
}


def fetch_search_results(project, url, query):
    """
    Fetch search results synchronously from ReadTheDocs API
    and log responses.
    """
    params = {
        "q": f"project:{project} {query}",
        "page_size": 10,  # fetch the first 10 results from each domain
    }

    logging.info(f"Sending API Request to {url}")
    logging.info(f"Query Parameters: {params}")

    try:
        response = requests.get(url, params=params, timeout=5)
        logging.info(f"Response Status: {response.status_code}")
        logging.info(f"Response Body: {response.json()}")

        if response.status_code == 200:
            return response.json()
        else:
            logging.warning(f"API request failed: {response.status_code}")
            logging.warning(f"Response text: {response.text}")

            return {"results": []}

    except requests.exceptions.RequestException as e:
        logging.error(f"Network error fetching {project}: {e}")
        return {"results": []}


def search_all_docs(query):
    """Run API searches concurrently using ThreadPoolExecutor."""
    results = []

    # use ThreadPoolExecutor to make requests in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_project = {
            executor.submit(fetch_search_results, project, url, query): project
            for project, url in RTD_PROJECTS.items()
        }

        for future in concurrent.futures.as_completed(future_to_project):
            try:
                search_results = future.result()
                results.extend(search_results.get("results", []))
            except Exception as e:
                print(f"Error fetching search results: {e}")

    return results


def calculate_relevance(result, query):
    """Calculate relevance using TF-IDF with scaled domain weighting."""
    title = result.get("title", "").lower()
    content = " ".join(
        block["content"] for block in result.get("blocks", [])
    ).lower()

    parsed_domain = urlparse(result.get("domain", "")).hostname or result.get(
        "domain", ""
    )

    search_results = [query, title, content]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(search_results)

    query_vector = tfidf_matrix[0]
    title_vector = tfidf_matrix[1]
    content_vector = tfidf_matrix[2]

    title_score = (query_vector * title_vector.T).sum() * 1.5
    content_score = (query_vector * content_vector.T).sum()

    # Boost "How to..." articles
    how_to_boost = 0.5 if title.startswith("how to") else 0

    # Normalize domain weight
    domain_weight = DOMAIN_INFO.get(parsed_domain, {}).get("weight", 1)
    domain_multiplier = 1 + (
        domain_weight / 5
    )  # Convert weight into a multiplier

    # Final score with domain multiplier
    return (title_score + content_score + how_to_boost) * domain_multiplier


def process_and_sort_results(results, query, max_length=200, limit=20):
    """
    Merge, truncate, and sort search results based on relevance,
    limiting to top 20 results.
    """
    processed_results = []

    for result in results:
        parsed_domain = urlparse(
            result.get("domain", "")
        ).hostname or result.get("domain", "")
        project_name = DOMAIN_INFO.get(parsed_domain, {}).get(
            "title", parsed_domain
        )

        full_content = " ".join(
            block["content"] for block in result.get("blocks", [])
        )
        short_content = (
            full_content[:max_length] + "..."
            if len(full_content) > max_length
            else full_content
        )

        relevance_score = calculate_relevance(result, query)

        processed_results.append(
            {
                "title": result.get("title", "Untitled"),
                "url": f"https://{parsed_domain}{result.get('path', '')}",
                "domain": parsed_domain,
                "project_name": project_name,
                "short_content": short_content,
                "relevance_score": relevance_score,
            }
        )

    return sorted(
        processed_results, key=lambda x: x["relevance_score"], reverse=True
    )[:limit]
