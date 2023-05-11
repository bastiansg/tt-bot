import numpy as np

from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain

from tt_bot.logger import get_logger
from tt_bot.search_engine import SearchEngine
from tt_bot.text_encoders import OpenAIEncoder


logger = get_logger(__name__)


class LLMRetrieval:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.text_encoder = OpenAIEncoder()

        llm = OpenAI()
        self.chain = load_qa_chain(llm, chain_type="stuff")

    async def retrieve(
        self,
        query_text: str,
        sim_tresh: float = 0.8,
        top_k: int = 3,
    ) -> dict:
        docs = await self.search_engine.search(query_text)
        doc_texts = [doc["text"] for doc in docs]

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

        sim_docs = (
            doc | {"similarity": sims[idx]}
            for idx, doc in enumerate(docs)
            if idx in sims_idx
        )

        sim_docs = sorted(
            sim_docs,
            key=lambda x: x["similarity"],
            reverse=True,
        )[:top_k]

        lc_docs = [Document(page_content=doc["text"]) for doc in sim_docs]
        answer = self.chain.run(input_documents=lc_docs, question=query_text)

        ref = []
        links = []
        for doc in sim_docs:
            link = doc["link"]
            if link in links:
                continue

            ref.append(
                {
                    "link": link,
                    "sim": doc["similarity"],
                }
            )

            links.append(link)

        response = {
            "answer": answer.strip(),
            "ref": ref,
        }

        return response
