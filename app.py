from flask import Flask, jsonify, request 


app = Flask(__name__)




@app.route('/<st>', methods = ['GET']) 
def detect(st): 
  
    return jsonify({'data': st}) 
  

# if __name__ == "__main__":   
#     app.run(debug=False)      