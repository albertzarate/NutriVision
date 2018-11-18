import requests
import json
import sys

class FoodItem:
    def __init__(self, food_label):
        self.food_found= food_label
        self.food_name = ["Food Type: ", "name"]
        self.id = 0
        self.calories = None
        self.calories_from_fat = None,
        self.total_fat = None,
        self.saturated_fat =  None,
        self.trans_fatty_acid =  None
        self.sodium = None
        self.total_carbohydrate = None,
        self.dietary_fiber = None
        self.sugars = None
        self.protein = None

    def get_item_id(self):
        url = "https://api.nutritionix.com/v1_1/search/{0}?results=0%3A1&fields=item_name%2Citem_id&appId=33316d66&appKey=505db5453af8f8b32a6cdd289a90af1c".format(self.food_found)
        r = requests.get(url)
        info = json.loads(r.text)

        self.food_name[1] = info["hits"][0]["fields"]["item_name"]
        self.id = info["hits"][0]["fields"]["item_id"]


        return self.id

    def get_food_nutrition(self):
        if self.id == 0:
            self.get_item_id()
        url = "https://api.nutritionix.com/v1_1/item?id={0}&appId=33316d66&appKey=505db5453af8f8b32a6cdd289a90af1c".format(self.id)
        r = requests.get(url)

        nut_info = json.loads(r.text)

        self.calories = ["Calories: " , nut_info["nf_calories"]]
        self.calories_from_fat = ["Calories From Fat: ", nut_info["nf_calories_from_fat"]]
        self.total_fat = ["Total Fat: ", nut_info["nf_total_fat"]]
        self.saturated_fat =  ["Saturated Fat: ", nut_info["nf_saturated_fat"]]
        self.trans_fatty_acid =  ["Trans Fat: ", nut_info["nf_trans_fatty_acid"]]
        self.sodium = ["Sodium: ", nut_info["nf_sodium"]]
        self.total_carbohydrate = ["Total Carbohydates: ", nut_info["nf_total_carbohydrate"]]
        self.dietary_fiber = ["Dietary Fiber: " , nut_info["nf_dietary_fiber"]]
        self.sugars = ["Sugars: ", nut_info["nf_sugars"]]
        self.protein = ["Protein: ", nut_info["nf_protein"]]

        temp = [self.food_name, self.calories, self.calories_from_fat, self.total_fat, self.saturated_fat, self.trans_fatty_acid, self.sodium, self.total_carbohydrate, self.dietary_fiber, self.sugars,self.protein]
        result = ""
        for i, info in enumerate(temp):
            if info[1] != None:
                result = result + str(info[0]) + str(info[1])

        return result[:-2]