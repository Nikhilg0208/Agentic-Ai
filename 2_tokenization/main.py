import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

sentence = "Hello, I am learning tokenization with tiktoken."

tokens = enc.encode(sentence)
print(tokens)

decoded_sentence = enc.decode(tokens)
print(decoded_sentence)
