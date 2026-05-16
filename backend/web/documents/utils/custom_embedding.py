
import os
from langchain_core.embeddings import Embeddings
from openai import OpenAI
class CustomEmbeddings(Embeddings):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("API_KEY"),
            base_url=os.getenv("API_BASE")
        )

    def embed_documents(self, texts):
        # Normalize inputs to non-empty strings to satisfy embedding API requirements.
        if not isinstance(texts, (list, tuple)):
            raise TypeError(f"embed_documents expects a list/tuple of strings, got {type(texts)}")
        batch_size = 10
        all_embeddings = []
        cleaned_texts = [str(t).strip() for t in texts if t is not None and str(t).strip()]
        if not cleaned_texts:
            raise ValueError("embed_documents received no valid text inputs after cleaning")
        for i in range(0, len(cleaned_texts), batch_size):
            batch = cleaned_texts[i: i + batch_size]
            if not batch:
                continue
            response = self.client.embeddings.create(
                model="text-embedding-v4",
                input=batch,
                dimensions=1024
            )
            # 保证 response.data 按照输入顺序排列，直接获取每个 embedding
            batch_embeddings = [data.embedding for data in response.data]
            all_embeddings.extend(batch_embeddings)
        return all_embeddings

    def embed_query(self, text):
        return self.embed_documents([text])[0]
