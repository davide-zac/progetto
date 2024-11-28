import llm
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transform', methods=['POST'])
def transform():
    data = request.json
    headings = data.get('headings', [])
    paragraphs = data.get('paragraphs', [])
    
    # Simulate LLM simplification (replace with actual LLM logic)
    #simplified_headings = [f"Simplified: {heading}" for heading in headings]
    #simplified_paragraphs = [f"Simplified: {paragraph}" for paragraph in paragraphs]
    print('running')
    simplified_content = llm.simplify_content(headings,paragraphs)
    print('runned')
    
    return jsonify({
        "headings": simplified_content['headings'],
        "paragraphs": simplified_content['paragraphs']
    })

if __name__ == '__main__':
    app.run(debug=True)
