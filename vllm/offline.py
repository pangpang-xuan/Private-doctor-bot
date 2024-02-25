from vllm import LLM, SamplingParams
from semantic_kernel.Rubbish.testwordtoyuyin import text_to_speech, API_KEY, SECRET_KEY

class Offline_vllm():

    def __init__(self,model_path, tensor_parallel_size=1,
                 gpu_memory_utilization=0.90,
                 dtype='float16',
                 quantization=None):

        self.sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
        self.llm= LLM(model=model_path,
                    tensor_parallel_size=tensor_parallel_size,
                    trust_remote_code=True,
                    quantization=quantization,
                    gpu_memory_utilization=gpu_memory_utilization, # 0.6
                    dtype=dtype)

    def chat(self,query):

        prompts=dict(query)

        output = self.llm.generate(prompts, self.sampling_params)

        # Print the outputs.
        prompt = output.prompt
        response = output.outputs[0].text
        print(response)
        text_to_speech(response, API_KEY, SECRET_KEY)

