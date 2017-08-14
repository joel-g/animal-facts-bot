import re
import praw
import random
import time
from pygame import mixer
# from '/' import lists


mixer.init()
alert=mixer.Sound('bird.wav')
history = 'commented.txt'

HORSE_FACTS = [
    'Horses can sleep both lying down and standing up.',
    'Horses can run shortly after birth.',
    'Domestic horses have a lifespan of around 25 years.',
    'A 19th century horse named ‘Old Billy’ is said to have lived 62 years.',
    'Horses have around 205 bones in their skeleton.',
    'Horses have been domesticated for over 5000 years.',
    'Horses are herbivores (plant eaters).',
    'Horses have bigger eyes than any other mammal that lives on land.',
    'Because horse’s eyes are on the side of their head they are capable of seeing nearly 360 degrees at one time.',
    'Horses gallop at around 44 kph (27 mph).',
    'The fastest recorded sprinting speed of a horse was 88 kph (55 mph).',
    'Estimates suggest that there are around 60 million horses in the world.',
    'Scientists believe that horses have evolved over the past 50 million years from much smaller creatures.',
    'A male horse is called a stallion.',
    'A female horse is called a mare.',
    'A young male horse is called a colt.',
    'A young female horse is called a filly.'
    ]

SNAKE_FACTS = [
    'Snakes are carnivores',
    'Snakes don’t have eyelids.',
    'Snakes can’t bite food so have to swallow it whole.',
    'Snakes have flexible jaws which allow them to eat prey bigger than their head!',
    'Snakes are found on every continent of the world except Antarctica.',
    'Snakes have internal ears but not external ones.',
    'Snakes used in snake charming performances respond to movement, not sound.',
    'There are around 3000 different species of snake.',
    'Snakes have a unique anatomy which allows them to swallow and digest large prey.',
    'Snakes are covered in scales.',
    'Snakeskin is smooth and dry.',
    'Snakes shed their skin a number of times a year in a process that usually lasts a few days.',
    'Some species of snake, such as cobras and black mambas, use venom to hunt and kill their prey.',
    'Snakes smell with their tongue.','Pythons kill their prey by tightly wrapping around it and suffocating it in a process called constriction.',
    'Some sea snakes can breathe partially through their skin, allowing for longer dives underwater.',
    'Anacondas are large, non-venomous snakes found in South America that can reach over 5 m (16 ft) in length.',
    'Python reticulates can grow over 8.7 m (28 ft) in length and are considered the longest snakes in the world.'
    ]

SCORPION_FACTS = [
    'Scorpions are predatory animals of the class Arachnida, making them cousins to spiders, mites and ticks.',
    'Scorpions have eight legs, a pair of pincers (pedipalps) and a narrow segmented tail that often curves over their back, on the end of which is a venomous stinger.',
    'The scorpion uses their pincers to quickly grab prey and then whip their poisonous tail stinger over to kill or paralyze the prey. The tail is also used as a useful defence against predators.',
    'Scorpion species range in size from 0.09 cm to 20 cm.',
    'Scorpions can be found on all continents except for Antarctica.',
    'There are over 1750 known species of scorpion. While humans generally fear the scorpion and its poisonous sting only about 25 of the species have venom capable of killing a human.',
    'Under UV light such as a black light scorpions are known to glow due to the presence of fluorescent chemicals in their exoskeleton.',
    'The scorpion is nocturnal, often hiding during the day under rocks and in holes in the ground before emerging at night to feed.',
    'Scorpions can eat a massive amount of food in one meal. Their large food storage organs, together with a low metabolism rate and an inactive lifestyle means that if necessary they can survive 6-12 months without eating again.',
    'Areas of China have a traditional dish of fried scorpion, and scorpion wine features in Chinese medicine.',
    'The scorpion is one of the 12 signs of the Zodiac, with the Scorpio constellation identified in the stars.',
    'Scorpions moult, they shed their exoskeleton up to 7 times as they grow to full size. They become vulnerable to predators each time until their new protective exoskeleton hardens.'
    ]


def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('animal-facts-bot', user_agent = '/u/AnimalFactsBot')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def botengine(animal, reddit):
    time.sleep(10)
    print("Checking 500 comments for " + animal + "...\n")
    for comment in reddit.subreddit('all').comments(limit = 500):
        match = re.findall(animal, comment.body)

        if match:
            print(animal + " found in comment with comment ID: " + comment.id)
            file_obj_r = open(history,'r')
            if comment.id not in file_obj_r.read().splitlines():
                if comment.author.name == reddit.user.me():
                    print('     Skipping my own comment...\n')
                else:
                    print('     Found new comment by ' + comment.author.name + '\n')
                    if animal == 'snake':
                        comment.reply(random.choice(SNAKE_FACTS))
                    if animal == 'scorpion':
                        comment.reply(random.choice(SCORPION_FACTS))
                    if animal == 'horse':
                        comment.reply(random.choice(HORSE_FACTS))
                    alert.play()

                    file_obj_r.close()
                    file_obj_w = open(history,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                    print('Waiting 1 minute before commenting again')
                    time.sleep(60)
            else:
                print('Already commented on this!\n')

def animalfactsbot(reddit):
    botengine('horse', reddit)
    botengine('snake', reddit)
    botengine('scorpion', reddit)

def main():
    reddit = authenticate()
    while True:
        animalfactsbot(reddit)

if __name__ == '__main__':
    main()
