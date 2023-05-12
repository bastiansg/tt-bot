import numpy as np

from tt_bot.logger import get_logger
from tt_bot.utils.json_data import group_by_key

from tt_bot.search_engine import SearchEngine
from tt_bot.text_encoders import OpenAIEncoder


logger = get_logger(__name__)


class Retrieval:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.text_encoder = OpenAIEncoder()

    def merge_chunk_group(self, chunk_group: list[dict]) -> dict:
        sim_score = max(chunk["similarity"] for chunk in chunk_group)
        mrged_text = " ".join(chunk["text"] for chunk in chunk_group)
        merged_group = {
            "text": mrged_text,
            "link": chunk_group[0]["link"],
            "relevance": len(chunk_group),
            "sim_score": sim_score,
        }

        return merged_group

    async def retrieve(
        self,
        query_text: str,
        sim_tresh: float = 0.8,
        top_k: int = 3,
    ) -> dict:
        se_results = await self.search_engine.search(query_text)
        if not (len(se_results)):
            return {}

        doc_texts = [doc["text"] for doc in se_results]
        doc_embeddings = self.text_encoder.batch_encode(doc_texts, contexts=[])
        logger.info(f"doc_embeddings => {doc_embeddings.shape}")

        q_embedding = self.text_encoder.encode(
            [query_text],
            contexts=[],
            encoder_type="",
        )

        sims = np.inner(q_embedding, doc_embeddings).ravel()
        sims_idx = np.nonzero(sims >= sim_tresh)[0]
        if not len(sims_idx):
            logger.info("no good enough answers")
            return []

        sim_chunks = (
            doc | {"similarity": sims[idx]}
            for idx, doc in enumerate(se_results)
            if idx in sims_idx
        )

        chunk_groups = group_by_key(
            sim_chunks,
            group_key="link",
            sort_key="link",
        )

        sim_chunks = map(self.merge_chunk_group, chunk_groups)
        sim_chunks = sorted(
            sim_chunks,
            key=lambda x: (x["relevance"], x["sim_score"]),
            reverse=True,
        )[:top_k]

        return sim_chunks
