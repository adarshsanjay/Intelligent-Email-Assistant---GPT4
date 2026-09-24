import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_interactions(
    csv_path="data/emails.csv"
):

    df = pd.read_csv(csv_path)

    df["Customer_Email"] = (
        df["Customer_Email"]
        .fillna("")
    )

    df["Subject"] = (
        df["Subject"]
        .fillna("")
    )

    df["Previous_Reply"] = (
        df["Previous_Reply"]
        .fillna("")
    )

    df["search_text"] = (
        df["Subject"]
        + " "
        + df["Customer_Email"]
    )

    return df


def retrieve_similar_email(
    customer_email: str,
    subject: str,
    df
):

    query = (
        subject
        + " "
        + customer_email
    )

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        df["search_text"]
    )

    query_vector = vectorizer.transform(
        [query]
    )

    similarities = cosine_similarity(
        query_vector,
        matrix
    ).flatten()

    best_index = similarities.argmax()

    row = df.iloc[best_index]

    return {
        "previous_email": row["Customer_Email"],
        "previous_reply": row["Previous_Reply"],
        "similarity": float(
            similarities[best_index]
        ),
    }
