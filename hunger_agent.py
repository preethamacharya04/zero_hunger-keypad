import random

class ZeroHungerAgent:
    def __init__(self, ledger, brain):
        self.ledger = ledger
        self.brain = brain

    def get_main_menu(self, lang):
        if lang == 'en':
            return "Welcome to Zero Hunger. Press 1 if you are looking for food, or press 2 if you want to check your active requests."
        return "ಜೀರೋ ಹಂಗರ್‌ಗೆ ಸುಸ್ವಾಗತ. ನೀವು ಆಹಾರಕ್ಕಾಗಿ ಹುಡುಕುತ್ತಿದ್ದರೆ 1 ಒತ್ತಿ, ಅಥವಾ ನಿಮ್ಮ ಸಕ್ರಿಯ ವಿನಂತಿಗಳನ್ನು ಪರಿಶೀಲಿಸಲು 2 ಒತ್ತಿ."

    def get_food_type_menu(self, lang):
        if lang == 'en':
            return "What kind of food do you need? Press 1 for Raw Grains, 2 for Cooked Meals, or 3 for Baby Food."
        return "ನಿಮಗೆ ಎಂತಹ ಆಹಾರದ ಅವಶ್ಯಕತೆ ಇದೆ? ಧಾನ್ಯಗಳಿಗಾಗಿ 1, ಬೇಯಿಸಿದ ಆಹಾರಕ್ಕಾಗಿ 2, ಅಥವಾ ಮಗುವಿನ ಆಹಾರಕ್ಕಾಗಿ 3 ಒತ್ತಿ."

    def process_request(self, phone, lang, food_type, city):
        food_names = {
            "grains": "Raw Grains" if lang == 'en' else "ಧಾನ್ಯಗಳು",
            "cooked": "Cooked Meals" if lang == 'en' else "ಬೇಯಿಸಿದ ಆಹಾರ",
            "baby": "Baby Food" if lang == 'en' else "ಮಗುವಿನ ಆಹಾರ"
        }
        food_name = food_names.get(food_type, "Food Request")
        
        if lang == 'en':
            base_text = f"Your request for {food_name} has been broadcast to donors in {city}. Please wait while we find a match."
        else:
            base_text = f"{city}ನಲ್ಲಿರುವ ದಾನಿಗಳಿಗೆ ನಿಮ್ಮ {food_name} ವಿನಂತಿಯನ್ನು ಕಳುಹಿಸಲಾಗಿದೆ. ದಯವಿಟ್ಟು ಕಾಯಿರಿ."

        # Use brain to make it more personalized
        context = f"User phone: {phone}. City: {city}. Food requested: {food_name}."
        prompt = f"Provide a comforting message to a person who just requested {food_name} for their family. Mention that the request is sent to donors in {city}. Base text: {base_text}"
        
        try:
            generated_response = self.brain.generate_response(prompt, lang, context)
            return generated_response
        except:
            return base_text

    def get_donor_acceptance_message(self, donor_name, lang):
        if lang == 'en':
            return f"Good news! A donor has accepted your request. They are located nearby. You can now press 1 to dial them directly."
        return f"ಒಳ್ಳೆಯ ಸುದ್ದಿ! ಒಬ್ಬ ದಾನಿ ನಿಮ್ಮ ವಿನಂತಿಯನ್ನು ಒಪ್ಪಿಕೊಂಡಿದ್ದಾರೆ. ಅವರು ಹತ್ತಿರದಲ್ಲಿದ್ದಾರೆ. ಅವರನ್ನು ನೇರವಾಗಿ ಸಂಪರ್ಕಿಸಲು ಈಗ 1 ಒತ್ತಿ."
