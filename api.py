from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from processing import get_comments, classify_comments, evaluate_comments
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def homepage():
    return 'pagina inicial'

@app.route("/get/<string:product>", methods=['GET'])
@cross_origin()
def process_product(product):
    
    product_data = get_comments(product)
    
    product_image = product_data['imagem-url']
    
    classified_comments = classify_comments(product_data['comentarios'])
    
    polaridades = classified_comments['polaridade']
    
    score, features = evaluate_comments(classified_comments)
    

from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from processing import get_comments, classify_comments, evaluate_comments
import pandas as pd

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def homepage():
    return 'Página inicial'

@app.route("/get/<string:product>", methods=['GET'])
@cross_origin()
def process_product(product):
    product_data = get_comments(product)
    product_image = product_data['imagem-url']
    classified_comments = classify_comments(product_data['comentarios'])
    polaridades = classified_comments['polaridade']
    score, features = evaluate_comments(classified_comments)
    
    # Contar as ocorrências de polaridades
    positivo = polaridades.count('positivo')
    neutro = polaridades.count('neutro')
    negativo = polaridades.count('negativo')
    
    
    response = {
        'product': product,
        'image': product_image,
        'score': score,
        'features': features,
        'positivo': positivo,
        'negativo': negativo,
        'neutro': neutro
    }

    # Retornar a resposta em JSON
    return jsonify(response)
    
    
if __name__ == '__main__':
    app.run()
