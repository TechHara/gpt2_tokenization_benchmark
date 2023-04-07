# GPT2 Tokenizer Benchmark
Compare GPT2 tokenization speed among HuggingFace, BlingFire, and Tiktoken's implementations.

## Setup
```sh
pip install -r requirement.txt
```

## Run
```sh
for library in hf bf tt; do time taskset -c 0 python main.py --library $library --dataset wikitext > output.$library; done
bash calc_parity.sh output.[hb]f
bash calc_parity.sh output.{bf,tt}
bash calc_parity.sh output.{hf,tt}
```

## Result
Ran on Ubuntu x64. Lower the better.
![](benchmark.webp)
