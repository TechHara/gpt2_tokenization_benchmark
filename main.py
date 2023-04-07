import argparse
import os
from transformers import GPT2TokenizerFast
from datasets import load_dataset
import blingfire
import tiktoken
import tqdm


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', type=str, choices=['hf', 'bf', 'tt'],
                        help='choose from huggingface(hf), blingfire(bf), or tiktoken(tt)')
    parser.add_argument('--input', type=str, default=None)
    parser.add_argument('--dataset', type=str, choices=['wikitext'])
    parser.add_argument('-n', type=int, default=1000000)

    args = parser.parse_args()
    if not ((args.input is None) ^ (args.dataset is None)):
        print('one of --input or --dataset must be provided')
        exit(-1)

    if args.library == 'hf':
        tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
        def tokenize(s): return tokenizer([s]).input_ids[0]

    elif args.library == 'bf':
        h = blingfire.load_model(os.path.join(
            os.path.dirname(blingfire.__file__), 'gpt2.bin'))

        def tokenize(s): return blingfire.text_to_ids(h, s, 1132, no_padding=True)

    elif args.library == 'tt':
        tokenizer = tiktoken.encoding_for_model('gpt2')
        def tokenize(s): return tokenizer.encode(s)

    if args.input is not None:
        with open(args.input, 'r') as f:
            dataset = f.readlines()
            dataset_length = len(dataset)
    else:  # args.dataset is not None
        if args.dataset == 'wikitext':
            dataset = load_dataset('wikitext', 'wikitext-103-raw-v1')['train']
            dataset_length = len(dataset)
            dataset = map(lambda text: text['text'], dataset)

    total = min(dataset_length, args.n)
    for n, line in tqdm.tqdm(enumerate(dataset), total=total):
        print(' '.join(str(idx) for idx in tokenize(line)))
        if n >= total:
            break


if __name__ == '__main__':
    main()
