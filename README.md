# Vocabulary, Models, and Token Counts for the paper TIMTC

This repository contains the vocabularies and language models to accompany the paper [Tokenization Is More Than Compression](https://aclanthology.org/2024.emnlp-main.40/) by Craig W. Schmidt, Varshini Reddy, Haoran Zhang, Alec Alameddine, Omri Uzan, Yuval Pinter, Chris Tanner.  This paper will be presented at [EMNLP 2024](https://2024.emnlp.org/).

Please direct any questions about this repo to <tokenization-maintainer@kensho.com>

These files are intended to stimulate academic research, but are not being actively developed at Kensho any longer.  

### Abstract of the paper

Tokenization is a foundational step in natural language processing (NLP) tasks, bridging raw text and language models. Existing tokenization approaches like Byte-Pair Encoding (BPE) originate from the field of data compression, and it has been suggested that the effectiveness of BPE stems from its ability to condense text into a relatively small number of tokens. We test the hypothesis that fewer tokens lead to better downstream performance by introducing PathPiece, a new tokenizer that segments a document's text into the minimum number of tokens for a given vocabulary. Through extensive experimentation we find this hypothesis not to be the case, casting doubt on the understanding of the reasons for effective tokenization. To examine which other factors play a role, we evaluate design decisions across all three phases of tokenization: pre-tokenization, vocabulary construction, and segmentation, offering new insights into the design of effective tokenizers. Specifically, we illustrate the importance of pre-tokenization and the benefits of using BPE to initialize vocabulary construction. We train 64 language models with varying tokenization, ranging in size from 350M to 2.4B parameters, all of which are made publicly available.

### Installation

The model files are quite large, so this repo used `git lfs` to store the large `*.bin` model files.  You will first need to install `git lfs`.  The particular instructions depend on your platform, but for example on Debian you would do `sudo apt install git-lfs`.  Then do `git lfs install` to set things up within git.  

When cloning the repo it will first clone the smaller files, and then download the larger model files, which are stored outside the repo.
**Please note that this repo will use 115G of disk space to clone!**  

You may prefer to clone the repository without automatically downloading the large files, to save on time and disk space. 
To do so, set the `GIT_LFS_SKIP_SMUDGE` variable before cloning like this:

```
GIT_LFS_SKIP_SMUDGE=1 git clone git@github.com:kensho-technologies/timtc_vocabs_models.git
```

Then you can download an individual `.bin` file with `git lfs pull --include="path/to/file"`, or all of the files with `git lfs pull`.


### `vocabularies` directory

This contains the 54 vocabulary files used in the experiments.  See Table 1 in the paper for the corresponding runs.  The filenames take the form `bpe_greedy_4_32768.vocab` is a BPE run with Greedy segmentation, where `4` refers to the rank column in Table 1, and `32768` is the vocabulary size. Vocabulary files ending in `.vocab` should be used with the [Huggingface tokenizer](https://huggingface.co/docs/tokenizers/en/index) with byte level pre-tokenization for segmentation. Those ending in `.vocab` should be used with the [PathPiece tokenizer](https://github.com/kensho-technologies/pathpiece), released as a separate repo as part of this paper.  The `.vocab` format just contains a separate token of bytes on each line, encoded in hexadecimal.

All files in this directory are released under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### `models` directory

This directory contains the trained Language Models (LM's), in Huggingface format.  There are subdirectories for the 350M and 1.3B parameter models.  The filenames correspond to the names in the vocabularies directory.

All files in this directory are released under the [AI Pubs Open Rail-M license](https://www.licenses.ai/ai-pubs-open-railm-vz1).

### `tokencounts` directory  

Many intrinsic tokenization metrics can be computed off the counts of each token over a training corpus.  For convenience, we have included the counts of each token for each vocabulary, over the [MiniPile](https://arxiv.org/abs/2304.08442) dataset. This is the same dataset used to train each vocabulary. The hope is to stimulate research into finding a metric that is a function of these counts that correlated better with the downstream performance presented in the paper.  These `.tsv` files contain the token and count separated by a tab, in decreasing order by count.

All files in this directory are released under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### `util` directory

The byte-level tokens in the `tokencounts` directory use the same encoding as the [byte-level pretokenizion used by Hugginface](https://huggingface.co/docs/tokenizers/en/api/pre-tokenizers#tokenizers.pre_tokenizers.ByteLevel). For your convience, this directory has a utility file defining the `frombytes` and `tobytes` function, for converting back and forth between this encoding and a python `bytes` object. It also has the very simple `fromhex` and `tohex` functions to convert the tokens in the`.vocab` files.

The util.py file is released under the [AI Pubs Open Rail-S license](https://www.licenses.ai/ai-pubs-open-rails-vz1).

### License

As already mentioned, the various directories are covered by different licenses.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

© 2023-present Kensho Technologies, LLC. The present date is determined by the timestamp of the most recent commit in the repository.
