import json, nltk, re, csv, argparse
from enum import Enum

class SegmentationMethod(str, Enum):
    texttiling = "texttiling"
    gpt = "gpt"

parser = argparse.ArgumentParser(description="Analyze the text segmentation results")
parser.add_argument("method", type=SegmentationMethod)
args = parser.parse_args()

method = args.method
path_checked_video_segments = '/app/data/video_segments_checked.json'
path_results = '/app/data/video_transcripts-gpt.json'
path_output_statistics = '/app/data/results-statistics-gpt.csv'

results = {}
with open(path_results, 'r', encoding="utf8") as jsonfile:
    results = json.load(jsonfile)

# load all input transcripts as dict; key are the segmentids, values the segments
input_transcripts = {}
with open(path_checked_video_segments, 'r', encoding="utf8") as jsonfile:
    input_transcripts = json.load(jsonfile)


def get_average_length_per_segment(segments):
    segments_as_list = []
    for elem in segments.split("\n\n"):
        segments_as_list.append(elem)
    avg_chars = sum(map(len, segments_as_list)) / len(segments_as_list)
    avg_token_per_segment = []
    for elem in segments_as_list:
        avg_token_per_segment.append(len(nltk.word_tokenize(elem)))
    avg_tokens = sum(avg_token_per_segment) / len(avg_token_per_segment)
    avg_sentences_per_segment = []
    for elem in segments_as_list:
        avg_sentences_per_segment.append(len(nltk.sent_tokenize(elem)))
    avg_sentences = sum(avg_sentences_per_segment) / len(avg_sentences_per_segment)
    return avg_sentences, avg_tokens, avg_chars

def get_statistics(results_as_list):
    result_dict = {}
    for elem in results_as_list:
        present_segments = results_as_list[elem]
        present_dict = {}
        present_dict["id"] = elem
        present_dict["video_transcript"] = input_transcripts[elem]
        present_dict["produced_segments"] = present_segments
        present_dict["number_of_segments"] = len(re.split(r"\n\n", present_segments))
        length_sentences, length_tokens, length_chars = get_average_length_per_segment(present_segments)
        present_dict["avg_length_per_segment_in_sentences"] = round(length_sentences, 3)
        present_dict["avg_length_per_segment_in_tokens"] = round(length_tokens, 3)
        present_dict["avg_length_per_segment_in_chars"] = round(length_chars, 3)
        present_dict["length_of_transcript_in_sentences"] = round(len(nltk.sent_tokenize(input_transcripts[elem])), 3)
        present_dict["length_of_transcript_in_tokens"] = round(len(nltk.word_tokenize(input_transcripts[elem])), 3)
        present_dict["length_of_transcript_in_chars"] = round(len(input_transcripts[elem]), 3)
        result_dict[elem] = present_dict
    return result_dict

def pretty_print_statistics(statistics, model):
    print(f"Statistics for model {model} are as follows: ")
    number_of_segments = []
    avg_length_per_segment_in_sentences = []
    avg_length_per_segment_in_tokens = []
    avg_length_per_segment_in_chars = []
    length_of_transcript_in_sentences = []
    length_of_transcript_in_tokens = []
    length_of_transcript_in_chars = []

    number_segments_single = 0
    avg_length_per_segment_sentences_single = 0
    avg_length_per_segment_tokens_single = 0
    avg_length_per_segment_chars_single = 0
    length_transcript_sentences_single = 0
    length_transcript_tokens_single = 0
    length_transcript_chars_single = 0

    number_segments_all_segments = 0
    avg_length_per_segment_sentences_all = 0
    avg_length_per_segment_tokens_all = 0
    avg_length_per_segment_chars_all = 0
    length_transcript_sentences_all = 0
    length_transcript_tokens_all = 0
    length_transcript_chars_all = 0

    for elem in statistics:
        number_of_segments.append(statistics[elem]["number_of_segments"])
        avg_length_per_segment_in_sentences.append(statistics[elem]["avg_length_per_segment_in_sentences"])
        avg_length_per_segment_in_tokens.append(statistics[elem]["avg_length_per_segment_in_tokens"])
        avg_length_per_segment_in_chars.append(statistics[elem]["avg_length_per_segment_in_chars"])
        length_of_transcript_in_sentences.append(statistics[elem]["length_of_transcript_in_sentences"])
        length_of_transcript_in_tokens.append(statistics[elem]["length_of_transcript_in_tokens"])
        length_of_transcript_in_chars.append(statistics[elem]["length_of_transcript_in_chars"])
    for elem in statistics:
        print(f"For just the first transcript, sample statistics:")
        number_segments_single = statistics[elem]["number_of_segments"]
        print(f'Number of segments for one transcript: {number_segments_single}')
        avg_length_per_segment_sentences_single = statistics[elem]["avg_length_per_segment_in_sentences"]
        print(f'Avg_length_per_segment_in_sentences for one transcript: {avg_length_per_segment_sentences_single}')
        avg_length_per_segment_tokens_single = statistics[elem]["avg_length_per_segment_in_tokens"]
        print(f'Avg_length_per_segment_in_tokens for one transcript: {avg_length_per_segment_tokens_single}')
        avg_length_per_segment_chars_single = statistics[elem]["avg_length_per_segment_in_chars"]
        print(f'Avg_length_per_segment_in_chars for one transcript: {avg_length_per_segment_chars_single}')
        length_transcript_sentences_single = statistics[elem]["length_of_transcript_in_sentences"]
        print(f'Length_of_transcript_in_sentences for one transcript: {length_transcript_sentences_single}')
        length_transcript_tokens_single = statistics[elem]["length_of_transcript_in_tokens"]
        print(f'Length_of_transcript_in_tokens for one transcript: {length_transcript_tokens_single}')
        length_transcript_chars_single = statistics[elem]["length_of_transcript_in_chars"]
        print(f'Length_of_transcript_in_chars for one transcript: {length_transcript_chars_single}')
        print()
        break
    print(f"For all segments produced by model {model}, the combined statistics are: ")
    number_segments_all_segments = round(sum(number_of_segments)/len(number_of_segments), 3)
    print(f"Number of segments averaged across all segments: {number_segments_all_segments}")
    avg_length_per_segment_sentences_all = round(sum(avg_length_per_segment_in_sentences)/len(avg_length_per_segment_in_sentences), 3)
    print(f"Avg_length_per_segment_in_sentences averaged across all segments: {avg_length_per_segment_sentences_all}")
    avg_length_per_segment_tokens_all = round(sum(avg_length_per_segment_in_tokens)/len(avg_length_per_segment_in_tokens), 3)
    print(f"Avg_length_per_segment_in_tokens averaged across all segments: {avg_length_per_segment_tokens_all}")
    avg_length_per_segment_chars_all = round(sum(avg_length_per_segment_in_chars)/len(avg_length_per_segment_in_chars), 3)
    print(f"Avg_length_per_segment_in_chars averaged across all segments: {avg_length_per_segment_chars_all}")
    length_transcript_sentences_all = round(sum(length_of_transcript_in_sentences)/len(length_of_transcript_in_sentences), 3)
    print(f"Length_of_transcript_in_sentences averaged across all segments: {length_transcript_sentences_all}")
    length_transcript_tokens_all = round(sum(length_of_transcript_in_tokens)/len(length_of_transcript_in_tokens), 3)
    print(f"Length_of_transcript_in_tokens averaged across all segments: {length_transcript_tokens_all}")
    length_transcript_chars_all = round(sum(length_of_transcript_in_chars)/len(length_of_transcript_in_chars), 3)
    print(f"Length_of_transcript_in_chars averaged across all segments: {length_transcript_chars_all}")

    print(f"Length_of_transcript_in_sentences total: {sum(length_of_transcript_in_sentences)}")
    print(f"Length_of_transcript_in_tokens total: {sum(length_of_transcript_in_tokens)}")
    print(f"Length_of_transcript_in_chars total: {sum(length_of_transcript_in_chars)}")

    combined_statistics = []
    combined_statistics.append(model)
    combined_statistics.extend([number_segments_single, avg_length_per_segment_sentences_single, avg_length_per_segment_tokens_single, avg_length_per_segment_chars_single, length_transcript_sentences_single, length_transcript_tokens_single, length_transcript_chars_single, number_segments_all_segments, avg_length_per_segment_sentences_all, avg_length_per_segment_tokens_all, avg_length_per_segment_chars_all, length_transcript_sentences_all, length_transcript_tokens_all, length_transcript_chars_all])

    return combined_statistics


csv_statistics = []
csv_statistics.append(["model-name","sample-number_of_segments","sample-avg_length_per_segment_in_sentences","sample-avg_length_per_segment_in_tokens","sample-avg_length_per_segment_in_characters", "sample-length_of_transcript_in_sentences", "sample-length_of_transcript_in_tokens", "sample-length_of_transcript_in_characters","number_of_segments","avg_length_per_segment_in_sentences","avg_length_per_segment_in_tokens","avg_length_per_segment_in_characters", "length_of_transcript_in_sentences", "length_of_transcript_in_tokens", "length_of_transcript_in_characters"])
if method == SegmentationMethod.texttiling:
    for elem in results:
        print(elem)
        current_result = get_statistics(results[elem])
        csv_statistics.append(pretty_print_statistics(current_result, f"texttiling({elem})"))
        print("==========================")
    
    # save all parameter configuration separately
    for elem in results:
        print(elem)
        file = path_results + elem.replace(":","") + ".json"
        with open(file, 'w', encoding="utf8") as jsonfile:
            json.dump(results[elem], jsonfile, ensure_ascii=False)
            print(f"done saving parameter config {elem} segments produced by texttiling")
else :
    statistics_chatgpt = get_statistics(results)
    csv_statistics.append(pretty_print_statistics(statistics_chatgpt, "gpt-4o"))
    print("==========================")

print(csv_statistics)

# save to file
with open(path_output_statistics, 'w', encoding="utf8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_statistics)
