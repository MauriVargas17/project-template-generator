import time
from src.utils.config import get_settings
from src.utils.models import Sentiment
from transformers import pipeline

SETTINGS = get_settings()

class TemplateSentiment:
    def __init__(self):
        self.model = SETTINGS.models["Sentiment"]
        # Length of one half of the scale! Scales must be symmetrical
        self.pipe = pipeline("text-classification", model=self.model)
        self.scale_length = SETTINGS.sentiment_scale_length
        self.categories = SETTINGS.sentiment_categories
        self.number_of_categories = len(self.categories)
        self.categories_dict = self.set_categories()
    
    def analyze(self, text: str) -> Sentiment:
        initial_time = time.time()
        result = self.pipe(text)
        #print(result)
        label = result[0]["label"]
        score = result[0]["score"]
        category: str
        #print(f"Original label: {label} and score: {score}")
        if label == "negative":
            score = -score
        if label == "neutral":
            category = "neutral"
        else:
            #print(f"Here we see the score {score} before transforming it")
            score_transformed = self.transform_to_scale(score)
            category = self.predict_category(score_transformed)
        final_time = time.time()
        return Sentiment(
            confidence=f"{round(abs(score)*100, 2)}%",
            category=category,
            value_in_range=score_transformed,
            time_ms=round((final_time - initial_time) * 1000, 2)
        )
    
    def predict_category(self, score: float) -> str:
        return self.categories_dict[min(self.categories_dict, key=lambda x: abs(x - score))]


    def set_categories(self) -> dict[float, str]:
        if self.number_of_categories % 2 != 0:
            elements_inside_one_half = (self.number_of_categories - 3)/2
            step = self.scale_length/(elements_inside_one_half + 1)
        range_values = self.custom_range(-self.scale_length, self.scale_length, step)
        print(range_values)
        return dict(zip(range_values, self.categories))

    def transform_to_scale(self, value: float, old_scale: tuple = (0, 1)) -> float:
        old_min, old_max = old_scale
        new_min, new_max = (-self.scale_length, self.scale_length)
        value = max(min(value, old_max), old_min)
       # print(f"Old max: {old_max}, old min: {old_min}, new max: {new_max}, new min: {new_min}, value: {value}")
        old_range = old_max - old_min
        new_range = new_max - new_min
        scaled_value = (((value - old_min) * new_range) / old_range) + new_min
        #print(f"scaled value: {scaled_value}")
        return scaled_value

    def custom_range(self, start, stop, step):
        result = []
        current = start
        while current <= stop:
            result.append(current)
            current += step
        return result
