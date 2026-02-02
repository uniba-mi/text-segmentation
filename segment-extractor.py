import json, timeit, re, argparse
from enum import Enum
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.texttiling import TextTilingTokenizer
from codecarbon import track_emissions
from openai import OpenAI

class SegmentationMethod(str, Enum):
    texttiling_default = "texttiling_default"
    texttiling_basic = "texttiling_basic"
    texttiling_all = "texttiling_all"
    gpt = "gpt"

parser = argparse.ArgumentParser(description="Analyze the text segmentation results")
parser.add_argument("method", type=SegmentationMethod)
args = parser.parse_args()

method = args.method
# data must be in JSON-format, {"id":"text","id":"text",[...]}
path_checked_video_segments = '/app/data/video_segments_checked.json'
client = OpenAI(api_key="ADD_YOUR_OPENAI_KEY_HERE")

# load all segment as dict; key are the segmentids, values the segments
checked_segments = {}
with open(path_checked_video_segments, 'r', encoding="utf8") as jsonfile:
    checked_segments = json.load(jsonfile)

# to test different parameter configuration, use these values; caution: very low values result in slower processing times
if method == SegmentationMethod.texttiling_default:
    w = [20]
    k = [10]
elif method == SegmentationMethod.texttiling_basic:
    w = [20, 30]
    k = [5, 10]
else:
    w = [1, 2, 3, 5, 8, 10, 15, 20, 30, 40, 50]
    k = [1, 2, 3, 5, 8, 10, 15, 20, 30, 40, 50]


results = {}
if method == SegmentationMethod.gpt:
    def create_prompt(transcript):
        prompt = f'Die folgenden Absätze stammen aus dem Transkript einer Vorlesung zum Thema Software Engineering:\n\n{transcript}'
        prompt += 'Aufgabe:\nErstelle Segmente basierend auf dem gegebenen Text.\n\n'
        prompt += 'Hinweise zum Ausgabeformat:\nGib ausschließlich die Segmente zurück, mit einer leeren Zeile als Trennung zwischen den Segmenten.\n\n'
        return prompt
    
    print(timeit.timeit(stmt =""))

    start_time = timeit.default_timer()
    for id in checked_segments:
        prompt = create_prompt(checked_segments[id])
        print(f"Starting processing video id: {id}")
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user", "content": f'{prompt}'
                }
            ]
        )
        result = completion.choices[0].message.content
        results[id] = result
        print(f"Finished with video id: {id}")

    print(f"Processing took: {timeit.default_timer() - start_time}")

else:
    stop_words = set(stopwords.words('german'))

    def process_transcript(video_transcript, w, k):
        sentences = sent_tokenize(video_transcript)
        tt = TextTilingTokenizer(demo_mode=False, stopwords=stop_words, w=w, k=k)
        # TextTilingTokenizer requires \n\n linebreaks, otherwise no processing is done, see https://stackoverflow.com/questions/69870891/nltk-texttiling
        input = "\n\n".join(sentences)
        tiles = tt.tokenize(input)
        result = []
        for elem in tiles:
            fixed_elem = re.sub("^\n\n", "", elem)
            fixed_elem = re.sub("\n\n", " ", fixed_elem)
            result.append(fixed_elem)
        return(result)

    @track_emissions(project_name="texttiling")
    def initiate_texttiling(i,j):
        result = {}
        counter = 0
        results_texttiling = {}
        for id in checked_segments:
            segments = process_transcript(checked_segments[id], i, j)
            counter += 1
            print(f"Current Iteration: w:{i},k:{j}, Transcript Counter: {counter}, Number of new Segments: {len(segments)}")
            results_texttiling[id] = "\n\n".join(segments)
        return results_texttiling
    
    for i in w:
        for j in k:
            start_time = timeit.default_timer()
            result = initiate_texttiling(i,j)
            current_id = f"w:{i};k:{j}"
            results[current_id] = result
            print(f"Processing took: {timeit.default_timer() - start_time}")

# save results in JSON file
with open('/app/data/video_transcripts.json', 'w', encoding="utf8") as jsonfile:
    json.dump(results, jsonfile, ensure_ascii=False)
    print(f"done saving segments generated, method(s): {(method.value)}")