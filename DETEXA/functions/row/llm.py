import warnings
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from accelerate import Accelerator
    import torch
    torch.cuda.empty_cache()
    import re
    accelerator = Accelerator()
    model_name = "mistralai/Mistral-7B-Instruct-v0.3"
    model_name = "meta-llama/Llama-2-13b-chat-hf"
    #model_name = "mistralai/Mistral-Nemo-Base-2407"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )
    model = accelerator.prepare(model)
except Exception as e:
    warnings.warn(f"Warning: {str(e)}", UserWarning)


def llm_extract(val): 
    prompt = (
            f"Extract from the text snippet below info about datasets/data AND code/software availability if they exist, "
            f"if the paragraph states that data or software are/can be/will be available on request or an other way, then you should return 'request',"
            f"if data or software is publicly available at a URL or at a public repository then return 'repo',"
            f"if data/software is available within the publication then return 'pulication',"
            f"if data/software exists but cannot be shared then return 'not_shared',"
            f"if data/software does not exist/is not used then return  'N/A',"
            f"if the paragraph does not say anything about data or software availability then return  'unknown',"
            f"Your response should be single line and always use a consistent structured format with only the following: Dataset: 'request or repo or publication or not_shared or N/A or unknown', Software: 'request or repo or publication or not_shared or unknown'"
            f"Paragraph: '''{val}'''\nAnswer:"
        )
       
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    inputs = tokenizer(prompt, return_tensors="pt", add_special_tokens=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items() if k != "token_type_ids"}
    output_ids = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=False,
       # temperature=0.2,
        pad_token_id=tokenizer.eos_token_id
    )

    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    answer = output_text.split("Answer:")[-1].strip()
    yield ('dataset', 'software')
    matches = re.findall(r'^(Dataset|Software):\s*(.+)$', answer, re.MULTILINE)
    if matches:
      result = {key: value for key, value in matches}
      yield (result['Dataset'], result['Software'])
    else:
      yield ("llm error", "llm error")

llm_extract.registered = True
