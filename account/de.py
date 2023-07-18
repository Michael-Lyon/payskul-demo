import random

class UniqueRandomNumberGenerator:
    def __init__(self):
        self.generated_numbers = set()

    def generate_unique_random(self):
        while True:
            new_number = random.randint(0, 999999)
            new_number_str = f"{new_number:06d}"
            if new_number_str not in self.generated_numbers:
                self.generated_numbers.add(new_number_str)
                return new_number_str

# Example usage:
if __name__ == "__main__":
    generator = UniqueRandomNumberGenerator()

    # for _ in range(10):
    unique_random_number = generator.generate_unique_random()
    print(unique_random_number)