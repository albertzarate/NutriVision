from __future__ import print_function


from flask import Flask, request, render_template
import flask
import os
import subprocess
import nutrition_api
import predict
import sys

import json

app = Flask(__name__)


@app.route("/get_nutrition_info/<food_label>")
def get_nutrition_api(food_label):
    food = nutrition_api.FoodItem(str(food_label))
    return food.get_food_nutrition()



@app.route('/identify_food', methods=['POST', 'GET'])
def load_image():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', food=result)


@app.route('/ml')
def load_ml_ui():
    return render_template('camera_test.html')


@app.route('/result/get_nutri/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        food = nutrition_api.FoodItem(str(result.items()[0][1]))
        food_info = str(food.get_food_nutrition())
        return render_template("result.html", food=food_info)

@app.route('/predict', methods=['POST'])
def load_result_ajax():
    os.system("rm -f result.txt")
    os.system("rm -f request.json")
    try:
        base64data = request.form['data']
        json_content = dict({"payload": {"image": {"imageBytes": "image_bytes"}}})
        json_content['payload']['image']['imageBytes'] = base64data

        print(json_content)
        with open("request.json", "w") as jsonfile:
            json.dump(json_content, jsonfile)
        jsonfile.close()
        output = subprocess.check_output(
            """curl -X POST -H "Content-Type: application/json"   -H "Authorization: Bearer $(gcloud auth application-default print-access-token)"   https://automl.googleapis.com/v1beta1/projects/nutrivision-221719/locations/us-central1/models/ICN4042215275664663461:predict -d @request.json""",
            shell=True)
        result = json.loads(output)
        food_label = result['payload'][0]["displayName"]
        food = nutrition_api.FoodItem(food_label)

        food_info = str(food.get_food_nutrition())

        print(food_info)

        if food_info == None:
            return render_template("error.html")

        with open("result.txt", "w") as f:
            f.write(food_info)
            f.close()

        print(food_info, file=sys.stdout)
        return food_info
    except:
        return render_template("error.html")


@app.route('/get_final_result')
def get_final():
    try:
        with open("result.txt", "r") as f:
            res = f.read()
            f.close()

        food_list = res.split("\n")

        return render_template("final_result.html", food_info= food_list)
    except:
        return render_template("error.html")


@app.route('/predict_fast')
def load_predict_curl():
    output = subprocess.check_output(
        """curl -X POST -H "Content-Type: application/json"   -H "Authorization: Bearer $(gcloud auth application-default print-access-token)"   https://automl.googleapis.com/v1beta1/projects/nutrivision-221719/locations/us-central1/models/ICN4042215275664663461:predict -d @request.json""",
        shell=True)
    result = json.loads(output)
    food_label = result['payload'][0]["displayName"]
    food = nutrition_api.FoodItem(food_label)
    food_info = str(food.get_food_nutrition())
    # return render_template('result.html', food=food_info)
    return food_info

@app.route('/error/not_found')
def error_handle():
    return render_template("error.html")

@app.route('/predict/<base64data>')
def load_prediction(base64data):
    json_content = dict({"payload": {"image": {"imageBytes": "image_bytes"}}})
    json_content['payload']['image']['imageBytes'] = base64data

    print(json_content)
    with open("request.json", "w") as jsonfile:
        json.dump(json_content, jsonfile)
    jsonfile.close()
    output = subprocess.check_output(
        """curl -X POST -H "Content-Type: application/json"   -H "Authorization: Bearer $(gcloud auth application-default print-access-token)"   https://automl.googleapis.com/v1beta1/projects/nutrivision-221719/locations/us-central1/models/ICN4042215275664663461:predict -d @request.json""",
        shell=True)
    result = json.loads(output)
    food_label = result['payload'][0]["displayName"]
    food = nutrition_api.FoodItem(food_label)
    food_info = str(food.get_food_nutrition())

    return food_info


@app.route('/')
def static_page():
    os.system("rm -f result.txt")
    os.system("rm -f request.json")
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, threaded=True)
