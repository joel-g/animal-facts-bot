import re
import praw
import random
import time
from pygame import mixer
# from '/' import lists

BLACKLIST = {'asoiaf'}

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
    'Horses are herbivores.',
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

DOLPHIN_FACTS = [
    'Compared to other animals, dolphins are believed to be very intelligent.',
    'Dolphins are carnivores.',
    'The Killer Whale (also known as Orca) is actually a type of dolphin.',
    'Bottlenose dolphins are the most common and well known type of dolphin.',
    'Female dolphins are called cows, males are called bulls and young dolphins are called calves.',
    'Dolphins live in schools or pods of up to 12 individuals.',
    'Dolphins often display a playful attitude which makes them popular in human culture. They can be seen jumping out of the water, riding waves, play fighting and occasionally interacting with humans swimming in the water.',
    'Dolphins use a blowhole on top of their heads to breathe.',
    'Dolphins have excellent eyesight and hearing as well as the ability to use echolocation for finding the exact location of objects.',
    'Dolphins communicate with each other by clicking, whistling and other sounds.',
    'Some dolphin species face the threat of extinction, often directly as a result of human behavior. The Yangtze River Dolphin is an example of a dolphin species which may have recently become extinct.',
    'Some fishing methods, such as the use of nets, kill a large number of dolphins every year.'
    ]

WHALE_FACTS = [
    'Many whales are toothless. They use a plate of comb-like fibre called baleen to filter small crustaceans and other creatures from the water.',
    'There are 79 to 84 different species of whale. They came in many different shapes and sizes!',
    'A baby whale is called a calf. Whales form groups to look after calves and feed together. These groups are often made up of all female or all male whales.',
    'Whales that are found in both Northern and Southern hemisphere never meet or breed together. Their migration is timed so that they are never in breeding areas at the same time.',
    'The arched lower lip of a whale can often make it look like it is smiling! However, this isn’t a “real” smile as the blubber in the head of the whale prevents the muscles of the face from reaching the surface.',
    'You can tell the age of a whale by looking at the wax plug in its ear. This plug in the ear has a pattern of layers when cut lengthwise that scientists can count to estimate the age of the whale.',
    'Whales love to sing! They use this as a call to mates, a way to communicate and also just for fun! After a period of time they get bored of the same whale song and begin to sing a different tune.',
    'Sometimes whales make navigation mistakes during migrations. Although they may have made the mistake days before, they don’t realise it until they becoming stranded.',
    'Whales support many different types of life. Several creatures, such as barnacles and sea lice, attach themselves to the skin of whales and live there.'
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
                    elif animal == 'scorpion':
                        comment.reply(random.choice(SCORPION_FACTS))
                    elif animal == 'horse':
                        comment.reply(random.choice(HORSE_FACTS))
                    elif animal == 'dolphin':
                        comment.reply(random.choice(DOLPHIN_FACTS))
                    elif animal == 'whale':
                        comment.reply(random.choice(WHALE_FACTS))
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
    botengine('dolphin', reddit)
    # botengine('horse', reddit)
    botengine('scorpion', reddit)
    botengine('snake', reddit)
    botengine('whale', reddit)

def main():
    reddit = authenticate()
    while True:
        animalfactsbot(reddit)

if __name__ == '__main__':
    main()
