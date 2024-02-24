from typing import List
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from ocr import get_ocr
#from ocr import get_ocr


class RapidOCRLoader(UnstructuredFileLoader):
    def _get_elements(self) -> List:
        def img2text(filepath):
            resp = ""
            ocr = get_ocr()
            result, _ = ocr(filepath)
            if result:
                ocr_result = [line[1] for line in result]
                resp += "\n".join(ocr_result)
            return resp

        text = img2text(self.file_path)
        from unstructured.partition.text import partition_text
        return partition_text(text=text, **self.unstructured_kwargs)


if __name__ == "__main__":
    loader = RapidOCRLoader(file_path="F:\pythonProject1\semantic_kernel\data\samples\ocr_test.jpg")
    txt_path=""
    docs = loader.load()
    print(docs)
    result = docs[0].page_content
    print(result)
    # 打开txt文件，写入数据
    with open(txt_path, "w", encoding="utf-8") as txt_file:

        txt_file.write(result + "\n")
    #<class 'list'>
