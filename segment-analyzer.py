import json, re, nltk, statistics
path_checked_video_segments = '/app/data/video_segments_checked.json'


input_transcripts = {}
with open(path_checked_video_segments, 'r', encoding="utf8") as jsonfile:
    input_transcripts = json.load(jsonfile)

sentences = []
tokens = []
for elem in input_transcripts:
    sentences.append(len(nltk.sent_tokenize(input_transcripts[elem])))
    tokens.append(len(nltk.word_tokenize(input_transcripts[elem])))

print(f"Sentence count for each transcript: {sentences}")
print(f"Mean sentence count: {round(statistics.mean(sentences), 3)}")
print(f"Standard deviation sentence count: {round(statistics.stdev(sentences), 3)}")
print(f"Maximum sentence count: {max(sentences)}")
print(f"Minimum sentence count: {min(sentences)}")
print(f"Token count for each transcript: {tokens}")
print(f"Mean token count: {round(statistics.mean(tokens), 3)}")
print(f"Standard deviation token count: {round(statistics.stdev(tokens), 3)}")
print(f"Maximum token count: {max(tokens)}")
print(f"Minimum token count: {min(tokens)}")



