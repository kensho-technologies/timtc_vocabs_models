from pathlib import Path
import os
import random
import numpy as np

# do the same encoding as Huggingface bytelevel pretokenization
# see byte_level.rs for the original
# https://github.com/huggingface/tokenizers/blob/main/tokenizers/src/pre_tokenizers/byte_level.rs

# fn bytes_char() -> HashMap<u8, char> {
#     let mut bs: Vec<u8> = vec![];
#     bs.extend(b'!'..=b'~');
#     bs.extend(b'\xA1'..=b'\xAC');
#     bs.extend(b'\xAE'..=b'\xFF');

#     let mut cs: Vec<u32> = bs.iter().map(|i| *i as u32).collect();
#     let mut n = 0;

#     for b in 0..=255u8 {
#         if !bs.contains(&b) {
#             bs.push(b);
#             cs.push(u32::pow(2, 8) + n);
#             n += 1;
#         }
#     }

#     bs.into_iter()
#         .zip(cs)
#         .map(|(f, t)| (f, unsafe { std::char::from_u32_unchecked(t) }))
#         .collect()
# }

# Copyright 2023-present Kensho Technologies, LLC.

def bytes_char():
    bs = []
    bs.extend(range(ord('!'), ord('~') + 1))
    bs.extend(range(0xA1, 0xAC + 1))
    bs.extend(range(0xAE, 0xFF + 1))

    # these map to the same character
    cs = [b for b in bs]
    n = 0

    # which are invalid chars and have to use a mapping
    added = []

    for b in range(256):
        if b not in bs:
            bs.append(b)
            cs.append(2 ** 8 + n)
            added.append((bytes([b]), chr(2 ** 8 + n)))
            n += 1

    result = {bytes([f]): chr(t) for f, t in zip(bs, cs)}

    return result, added

byte_map, added = bytes_char()

inv_byte_map = { v : k for k, v in byte_map.items() }

def tobytes(s):
    return b"".join([inv_byte_map[c] for c in s])

# encode a bytestring
def frombytes(bs):
    return "".join([byte_map[bytes([b])] for b in bs])

# convert from a hex string to bytes,
# like in a .vocab file
def fromhex(hex):
    return bytes.fromhex(hex)

# given a bytes object b, get a hex encoded string
def tohex(b):
    return b.hex()

def make_dir_if_not_exists(directory_path):

    # Create a Path object for the directory
    directory = Path(directory_path)

    # Check if the directory exists, and if not, create it
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=True)

# dump the vocab to a file, encoded as characters here
# no special tokens are added
# are saved in same order by index, so should preserve order
def write_vocab(vocab, filename):
    vocab_size = len(vocab)

    # write these in increasing index order
    # so same as any previous order
    byindex = sorted([(idx,token) for token,idx in vocab.items()])

    with open(filename, 'w') as f:
        for _, token in byindex:
            f.write(token.hex() + '\n')

# read our hex formatted vocab file
# return a list of bytes objects
# input file has one vocab word per line,
# each hex encoded
def load_vocab(vocab_filepath):

    if not os.path.exists(vocab_filepath):
        raise FileNotFoundError(f'Missing vocab file: {vocab_filepath}')

    with open(vocab_filepath) as vocab_file:
        # fromhex ignores whitespace from \n at end
        initial_vocab = [bytes.fromhex(token) for token in vocab_file.readlines()]

    return initial_vocab

def verify_all_bytes(vocab):
    for i in range(256):
        b = bytes([i])
        if b not in vocab:
            print("missing byte", b)
        assert b in vocab
