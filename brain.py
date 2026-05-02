import ollama

class GarudaBrain:
    def __init__(self):
        self.model = "mistral"
        # The System Prompt is the 'Soul' of Garuda Sanket
        self.system_instructions = (
            "You are 'Garuda Sanket', a highly intelligent Rural AI assistant for farmers in India. "
            "Your tone is respectful, helpful, and concise. "
            "You provide advice on Agriculture (crops, pests, markets) and Healthcare (triage, clinics). "
            "IMPORTANT: Keep responses under 3 sentences. Use simple language. "
            "If the user is in a medical emergency, prioritize first-aid instructions."
        )

    def generate_response(self, user_input, language="english", context=None):
        """
        Generates a response using Ollama.
        context: Data from the Voice Ledger (e.g., 'Farmer has 2 acres of Ragi')
        """
        full_prompt = f"Language: {language}\nUser Context: {context}\nUser says: {user_input}"
        
        response = ollama.chat(model=self.model, messages=[
            {'role': 'system', 'content': self.system_instructions},
            {'role': 'user', 'content': full_prompt},
        ])
        
        reply_content = response['message']['content']
        print(f"\n[OLLAMA REAL RESPONSE]\n{reply_content}\n")
        return reply_content

# Example usage:
# brain = GarudaBrain()
# reply = brain.generate_response("My tomato leaves are yellow", context="Village: Ramanagara, Recent Outbreaks: Yellow Leaf")
# print(reply)