from langchain.llms import OpenAI
from langchain.schema import Document
from langchain.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain

from tt_bot.logger import get_logger


logger = get_logger(__name__)


class DocQA:
    def __init__(self):
        llm = OpenAI(temperature=0.0)
        self.chain = load_qa_chain(llm, chain_type="stuff")

    def get_answer(self, sim_chunks: list[dict], query_text: str) -> str:
        sim_docs = [
            Document(page_content=chunk["text"]) for chunk in sim_chunks
        ]

        with get_openai_callback() as callback:
            answer = self.chain.run(
                input_documents=sim_docs,
                question=query_text,
            )

            logger.info(callback)

        ref = [
            {
                "link": chunk["link"],
                "relevance": chunk["relevance"],
                "sim_score": chunk["sim_score"],
            }
            for chunk in sim_chunks
        ]

        response = {
            "answer": answer.strip(),
            "ref": ref,
        }

        return response
