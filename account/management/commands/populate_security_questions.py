from django.core.management.base import BaseCommand
from account.models import SecurityQuestion  # Import your SecurityQuestion model

class Command(BaseCommand):
    help = 'Populate SecurityQuestion model with 100 possible security questions'

    def handle(self, *args, **kwargs):
        security_questions = [
            "What is your mother's maiden name?",
            "What is the name of your first pet?",
            "In which city were you born?",
            "What is your favorite book?",
            "What is your favorite movie?",
            "What is the name of your best childhood friend?",
            "What is your favorite color?",
            "What was the make and model of your first car?",
            "What is the name of your favorite teacher?",
            "What is your favorite food?",
            "What is your favorite sports team?",
            "What is the name of the street you grew up on?",
            "What is the name of your first school?",
            "What is your favorite vacation destination?",
            "What is the name of your favorite historical figure?",
            "What is the name of your favorite fictional character?",
            "What is your favorite song?",
            "What is your favorite hobby?",
            "What is the name of your childhood hero?",
            "What is your favorite restaurant?",
            "What is your favorite type of music?",
            "What is your favorite TV show?",
            "What is the name of your favorite actor/actress?",
            "What is the name of your favorite author?",
            "What is your favorite childhood toy?",
            "What is your favorite season of the year?",
            "What is the name of your favorite childhood book?",
            "What is your favorite sports activity?",
            "What is the name of the first company you worked for?",
            "What is the name of your first boss?",
            "What is your favorite type of cuisine?",
            "What is the name of your favorite childhood game?",
            "What is your favorite holiday?",
            "What is your favorite animal?",
            "What is your favorite beverage?",
            "What is your favorite type of dessert?",
            "What is your favorite childhood memory?",
            "What is the name of your favorite childhood movie?",
            "What is your favorite type of weather?",
            "What is the name of your favorite childhood TV show?",
            "What is your favorite outdoor activity?",
            "What is the name of your favorite childhood sports team?",
            "What is your favorite board game?",
            "What is your favorite type of art?",
            "What is the name of your favorite childhood superhero?",
            "What is your favorite mode of transportation?",
            "What is your favorite type of dance?",
            "What is the name of your favorite childhood singer/band?",
            "What is your favorite indoor activity?",
            "What is your favorite type of flower?",
            "What is the name of your favorite childhood park or playground?",
            "What is your favorite ice cream flavor?",
            "What is your favorite type of tree?",
            "What is your favorite type of candy?",
            "What is the name of your favorite childhood teacher?",
            "What is your favorite type of bird?",
            "What is your favorite childhood nickname?",
            "What is your favorite type of insect?",
            "What is the name of your favorite childhood magazine?",
            "What is your favorite type of fish?",
            "What is your favorite childhood cartoon character?",
            "What is your favorite type of reptile?",
            "What is your favorite childhood superhero costume?",
            "What is your favorite type of clothing?",
            "What is the name of your favorite childhood stuffed animal?",
            "What is your favorite type of cloud?",
            "What is your favorite childhood toy vehicle (e.g., toy car, train)?",
            "What is your favorite type of sport equipment?",
            "What is the name of your favorite childhood building or landmark?",
            "What is your favorite type of gemstone?",
            "What is your favorite childhood constellation or star?",
            "What is your favorite type of beverage container (e.g., cup, mug)?",
            "What is the name of your favorite childhood painting or artwork?",
            "What is your favorite type of footwear?",
            "What is your favorite childhood fruit?",
            "What is your favorite type of animal sound?",
            "What is the name of your favorite childhood song or lullaby?",
            "What is your favorite type of space object (e.g., planet, comet)?",
            "What is your favorite childhood bedtime story?",
            "What is your favorite type of natural disaster?",
            "What is the name of your favorite childhood fairy tale?",
            "What is your favorite type of cloud formation?",
            "What is your favorite childhood nickname for a family member?",
            "What is your favorite type of celestial event (e.g., eclipse, meteor shower)?",
            "What is the name of your favorite childhood museum?",
            "What is your favorite type of historical artifact?",
            "What is your favorite childhood flavor of gum or candy?",
            "What is your favorite type of ocean creature?",
            "What is the name of your favorite childhood science experiment?",
            "What is your favorite type of technology gadget?",
            "What is your favorite childhood game to play with friends?",
            "What is your favorite type of dinosaur?",
            "What is the name of your favorite childhood weather phenomenon?",
            "What is your favorite type of book genre?",
            "What is your favorite childhood song to play with friends?",
        ]
        for question_text in security_questions:
            SecurityQuestion.objects.create(question_text=question_text)

        self.stdout.write(self.style.SUCCESS('Successfully populated SecurityQuestion model.'))
