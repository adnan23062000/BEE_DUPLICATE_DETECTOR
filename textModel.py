from sentence_transformers import SentenceTransformer, util
import json

def calculate_similarity(input_text):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

    embeddings = []

    with open('test.json', 'r', encoding='utf-8') as json_file:
        bug_reports = [json.loads(line) for line in json_file]

    # Calculate the embeddings for all bug reports
    embeddings = model.encode([bug_report.get('originalDescription', '') for bug_report in bug_reports])
    
    input_embedding = model.encode(input_text)

    result = []

    for i, embedding_i in enumerate(embeddings):
        similarity_score = util.pytorch_cos_sim(input_embedding, embedding_i).item()
        result.append({
            'bug_report_id': bug_reports[i]['key'],
            'similarity_score': similarity_score,
            'description': bug_reports[i]['originalDescription']
        })

    sorted_result = sorted(result, key=lambda x: x['similarity_score'], reverse=True)

    return sorted_result


def calculate_embeddings(input):
    try:
        print('dhukse')
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        input_embedding = model.encode(input)
        return input_embedding
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None 