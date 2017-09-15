import re
import praw
import random
import time
import sys
import string
from pygame import mixer
# from '/' import lists

BLACKLIST = ('suicidewatch', 'depression', 'snakes', 'mturk', 'babyelephantgifs', 'learnprogramming', 'cscareerquestions', 'python', 'japan')

mixer.init()
alert=mixer.Sound('bird.wav')
bell=mixer.Sound('bell.wav')
history = 'commented.txt'
reply_history = 'repliedto.txt'
unsubscribed_list = 'unsubscribed.txt'
if len(sys.argv) > 1:
    wait_time = int(sys.argv[1])
else:
    wait_time = 90


if len(sys.argv) > 2:
    number_of_messages = int(sys.argv[2])
else:
    number_of_messages = 50

def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('animal-facts-bot', user_agent = '/u/AnimalFactsBot')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def check_messages(reddit):
    print("Checking my messages...\n")
    for comment in reddit.inbox.comment_replies(limit=number_of_messages):
        print("Checking comment ID " + comment.id, end='\r')
        if unsubscribed_author_check(comment):
            if not comment.subreddit.user_is_banned:
                file_obj_r = open(reply_history,'r')
                if comment.id not in file_obj_r.read().splitlines():
                    comment_body = comment.body.lower()
                    if 'good bot' in comment_body:
                        comment.reply('Thanks! You can ask me for more facts any time. Beep boop.')
                        print('     Thanked someone for "good bot"\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'bad bot' in comment_body or 'unsubscribe' in comment_body:
                        comment.reply(comment.author.name + " has been unsubscribed from AnimalFactsBot. I won't reply to your comments any more.")
                        print('     Unsubbed ' + comment.author.name + '\n')
                        unsubscribe(comment.author)
                        record_already_replied(file_obj_r, comment)
                    elif 'more' in comment_body:
                        comment.reply("It looks like you asked for more animal facts! " + random_fact())
                        print('     Gave someone more facts!\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'thank' in comment_body:
                        print('Thanks found in commment ' + comment.id)
                        comment.reply('You are most welcome. Beep boop.')
                        print('     Replied to a thank you\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'TIL' in comment.body:
                        comment.reply("I'm always happy to help people learn!")
                        print('     Replied to a TIL\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'best bot' in comment_body:
                        comment.reply("It sounds like you called me the 'best bot'. That's awesome!")
                        print('     Replied to a "best bot"\n')
                        record_already_replied(file_obj_r, comment)
                    elif re.search('(fuck)|(bitch)|(shit)', comment_body):
                        comment.reply("https://www.youtube.com/watch?v=hpigjnKl7nI")
                        print('     WATCH YO PROFANITY\n')
                        record_already_replied(file_obj_r, comment)
                    elif re.search('(\scats?\s)|(\sdogs?\s)', ' ' + comment_body + ' '):
                        comment.reply("Did you ask for cat or dog facts? I'm sorry, if I did cat or dog facts I'd be spamming every thread on reddit. Reply 'more' if you'd like a random animal fact.")
                        print('     Explained why I cant do cat or dog facts\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'silly' in comment_body:
                        comment.reply('I am programmed to be silly!')
                        print('     Explained why I am silly\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'hate' in comment_body:
                        comment.reply("Please don't hate. Beep boop.")
                        print('     Replied to a "hate" comment\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'animalfactsbot' in comment_body:
                        print('found my name')
                        comment.reply("You said my name! Would you like to know more about me? I am written in Python. I am running from a computer in Seattle. I have given an animal fact to redditors " + str(number_of_facts_given()) + " times!")
                        print('     Told someone about myself.\n')
                        record_already_replied(file_obj_r, comment)
                    else:
                        commented_obj_r = open(history,'r')
                        if comment.id not in commented_obj_r.read().splitlines():
                            check_comment_for_animal(comment, reddit)
                        commented_obj_r.close()
                file_obj_r.close()

def number_of_facts_given():
    commented_obj_r = open(history,'r')
    count = len(commented_obj_r.read().splitlines())
    commented_obj_r.close()
    return count

def number_of_facts(ALL_FACTS):
    count = 0
    for array in ALL_FACTS:
        count += len(array)
    return count

def record_already_replied(read_file, comment):
    read_file.close()
    file_obj_w = open(reply_history,'a+')
    file_obj_w.write(comment.id + '\n')
    file_obj_w.close()
    time.sleep(wait_time)

def unsubscribe(redditor):
    unsub_w = open(unsubscribed_list, 'a+')
    unsub_w.write(redditor.name + '\n')
    unsub_w.close()

def unsubscribed_author_check(comment):
    unsub_r = open(unsubscribed_list, 'r')
    if comment.author and comment.author.name in unsub_r.read().splitlines():
        unsub_r.close()
        return False
    else:
        unsub_r.close()
        return True

def random_fact():
    fact_collection =  random.choice(ALL_FACTS)
    return random.choice(fact_collection)

def botengine(animal, regex, reddit, facts, comment):
    text = ' '.join(word.strip(string.punctuation) for word in comment.body.lower().split())
    text = ' ' + text + ' '
    match = re.findall(regex, text)
    if match:
        print(animal.upper() + " found in comment with comment ID: " + comment.id)
        if comment.subreddit.display_name.lower() not in BLACKLIST:
            if comment.subreddit.user_is_banned:
                print("     Not commenting because I am banned from " + comment.subreddit.display_name + "\n")
            else:
                if not unsubscribed_author_check(comment):
                    print("     Not commenting because author is unsubscribed.")
                else:
                    file_obj_r = open(history,'r')
                    if comment.id not in file_obj_r.read().splitlines():
                        if comment.author.name == reddit.user.me():
                            print('     Skipping my own comment...\n')
                        else:
                            print('     by ' + comment.author.name + ' in ' + comment.subreddit.display_name + '\n      commenting a fact...')
                            comment.reply(random.choice(facts))
                            alert.play()
                            file_obj_r.close()
                            file_obj_w = open(history,'a+')
                            file_obj_w.write(comment.id + '\n')
                            file_obj_w.close()
                            time.sleep(wait_time)
                    else:
                        print('     Already commented on this!\n')

# ANIMALS = ('alligator', 'beaver', 'badger', 'camel', 'cheetah', 'crab', 'dolphin', 'elephant', 'flamingo', 'frog', 'giraffe', 'gorilla', 'hedgehog','hippo', 'horse', 'jellyfish', 'koala', 'lion', 'lepoard', 'monkey', 'octopus', 'otter', 'owl', 'panda', 'parrot', 'penguin', 'pig', 'scorpion', 'shark', 'sloth', 'snake', 'tiger', 'turtle', 'wolf', 'whale', 'zebra')

def check_comment_for_animal(comment, reddit):
    botengine('alligator', '\salligators?\s', reddit, ALLIGATOR_FACTS, comment)
    botengine('badger', '\sbadgers?\s', reddit, BADGER_FACTS, comment)
    botengine('beaver', '\sbeavers?\s', reddit, BEAVER_FACTS, comment)
    botengine('camel', '\scamels?\s', reddit, CAMEL_FACTS, comment)
    botengine('cheetah', '\scheetahs?\s', reddit, CHEETAH_FACTS, comment)
    botengine('cow', '\scows?\s', reddit, COW_FACTS, comment)
    botengine('crab', '\scrabs?\s', reddit, CRAB_FACTS, comment)
    botengine('dolphin', '\sdolphins?\s', reddit, DOLPHIN_FACTS, comment)
    botengine('dragon', '\sdragons?\s', reddit, DRAGON_FACTS, comment)
    botengine('eagle', '\seagles?\s', reddit, EAGLE_FACTS, comment)
    botengine('echidna', '\sechidnas?\s', reddit, ECHIDNA_FACTS, comment)
    botengine('elephant', '\selephants?\s', reddit, ELEPHANT_FACTS, comment)
    botengine('emu', '\semus?\s', reddit, EMU_FACTS, comment)
    botengine('flamingo', '\sflamingos?\s', reddit, FLAMINGO_FACTS, comment)
    botengine('fox', '\sfoxe?s?\s', reddit, FOX_FACTS, comment)
    botengine('frog', '\sfrogs?\s', reddit, FROG_FACTS, comment)
    botengine('giraffe', '\sgiraffes?\s', reddit, GIRAFFE_FACTS, comment)
    botengine('gorilla', '\sgorillas?\s', reddit, GORILLA_FACTS, comment)
    botengine('hamster', '\shamsters?\s', reddit, HAMSTER_FACTS, comment)
    botengine('hedgehog', '\shedgehogs?\s', reddit, HEDGEHOG_FACTS, comment)
    botengine('hippo', '\shippos?\s', reddit, HIPPO_FACTS, comment)
    botengine('horse', '\shorses?\s', reddit, HORSE_FACTS, comment)
    botengine('hummingbird', '\shummingbirds?\s', reddit, HUMMINGBIRD_FACTS, comment)
    botengine('jellyfish', '\sjellyfish\s', reddit, JELLYFISH_FACTS, comment)
    botengine('kangaroo', '\skangaroos?\s', reddit, KANGAROO_FACTS, comment)
    botengine('koala', '\skoalas?\s', reddit, KOALA_FACTS, comment)
    botengine('lion', '\slions?\s', reddit, LION_FACTS, comment)
    botengine('leopard', '\sleopards?\s', reddit, LEOPARD_FACTS, comment)
    botengine('lizard', '\slizards?\s', reddit, LIZARD_FACTS, comment)
    botengine('monkey', '\smonkeys?\s', reddit, MONKEY_FACTS, comment)
    botengine('narwhal', '\snarwhals?\s', reddit, NARWHAL_FACTS, comment)
    botengine('ocelot', '\socelots?\s', reddit, OCELOT_FACTS, comment)
    botengine('octopus', '\soctopus?\s', reddit, OCTOPUS_FACTS, comment)
    botengine('otter', '\sotters?\s', reddit, OTTER_FACTS, comment)
    botengine('owl', '\sowls?\s', reddit, OWL_FACTS, comment)
    botengine('parrot', '\sparrots?\s', reddit, PARROT_FACTS, comment)
    botengine('panda', '\spandas?\s', reddit, PANDA_FACTS, comment)
    botengine('panther', '\spanthers?\s', reddit, PANTHER_FACTS, comment)
    botengine('peacock', '\speacocks?\s', reddit, PEACOCK_FACTS, comment) 
    botengine('penguin', '\spenguins?\s', reddit, PENGUIN_FACTS, comment)
    botengine('pig', '\spigs?\s', reddit, PIG_FACTS, comment)
    botengine('pigeon', '\spigeons?\s', reddit, PIGEON_FACTS, comment)
    botengine('scorpion', '\sscorpions?\s', reddit, SCORPION_FACTS, comment)
    botengine('seagull', '\sseagulls?\s', reddit, SEAGULL_FACTS, comment)
    botengine('shark', '\ssharks?\s', reddit, SHARK_FACTS, comment)
    botengine('sloth', '\ssloths?\s', reddit, SLOTH_FACTS, comment)
    botengine('snake', '\ssnakes?\s', reddit, SNAKE_FACTS, comment)
    botengine('tiger', '\stigers?\s', reddit, TIGER_FACTS, comment)
    botengine('turtle', '\sturtles?\s', reddit, TURTLE_FACTS, comment)
    botengine('wolf', '\swolf\s', reddit, WOLF_FACTS, comment)
    botengine('whale', '\swhales?\s', reddit, WHALE_FACTS, comment)
    botengine('zebra', '\szebras?\s', reddit, ZEBRA_FACTS, comment)

def animalfactsbot(reddit):
    check_messages(reddit)
    print("Pulling 1000 comments...")
    comment_list = reddit.subreddit('all').comments(limit = 1000)
    print("     checking each comment for " + str(len(ALL_FACTS)) + " different animals\n")
    for comment in comment_list:
        check_comment_for_animal(comment, reddit)


ALLIGATOR_FACTS = (
    'Alligators have been living on Earth for millions of years and are sometimes described as ‘living fossils’.',
    'There are two different species of alligator, the American alligator and the Chinese alligator.',
    'American alligators live in south-eastern areas of the United States such as Florida and Louisiana.',
    'Chinese alligators are found in the Yangtze River but they are critically endangered and only a few remain in the wild.',
    'Like other reptiles, alligators are cold-blooded.',
    'Alligators can weigh over 450 kg (1000 lb).',
    'Alligators have a powerful bite but the muscles that open the jaw are relatively weak. An adult human could hold the jaws of an alligator shut with their bare hands.',
    'Alligators eat a range of different animals such as fish, birds, turtles and even deer.',
    'Alligator eggs become male or female depending on the temperature, male in warmer temperatures and female in cooler temperatures.',
    'Like crocodiles, alligators are part of the order ‘Crocodylia’.'
    )

BADGER_FACTS = (
    'Badgers are part of the family Mustelidae this is the same family as otters, ferret, polecats, weasels and wolverines.',
    'There are 11 species of badger, grouped into 3 types, the Melinae (Eurasian badgers), Mellivorinae (Honey badger) and Taxideinae (American badger).',
    'Badgers are found in North America, Ireland, Great Britain and most of Europe. There are species in Japan, China, Indonesia and Malaysia. The honey badger is found in sub-Saharan Africa, the Arabian Desert, Turkmenistan, and India.',
    'Badgers have stocky bodies with short legs that are suitable for digging. They digs burrows underground called a sett. Their sett are often a maze of tunnels and chambers for sleeping around 6 badgers, setts are kept very clean.',
    'The badger has an elongated head with small ears and a distinctive black and white face, their body has greyish fur with black and white areas underneath.',
    'Badgers can grow to nearly a meter in length. The European badger is larger than the American badger and the Honey badger.',
    'Badgers on average weigh around 9 - 11 kg (20 - 24 lbs).',
    'The badger can run up to 30 km/h (19 mph) for a short period of time.',
    'A male badger is called a boar, the female is called a sow and the young are called cubs.',
    'A group of badgers is called a cete, although they are often called clans. There are usually 2 - 15 badgers in a cete.',
    'The honey badger is a carnivorous species that has the reputation of being the most fearless and vicious of all mammals.',
    'Badgers were eaten in Britain during World War II and were once part of the Native American and settlers diets in the US. Russia still eats badger meat today.',
    "Badgers have featured in lots of British literature over the years, such as Brian Jacques' Redwall series, 'Tommy Brock' in Beatrix Potter's The Tale of Mr. Tod, 'Bill Badger' in Mary Tourtel's Rupert Bear, 'Mr. Badger' in Kenneth Grahame's The Wind in the Willows and 'Trufflehunter' in C. S. Lewis's Chronicles of Narnia."
    )

BEAVER_FACTS = (
    'There are two species of beaver. The European or Eurasian beaver (Castor fiber) and the North American beaver (Castor canadensis).',
    'Beavers are the second largest rodent in the world after the capybara.',
    'The beaver is mainly a nocturnal animal.',
    'The large front teeth of the beaver never stop growing. The beavers constant gnawing on wood helps to keep their teeth from growing too long.',
    'Together beaver colonies create dams of wood and mud to provide still, deep water in order to protect against predators such as wolves, coyotes, bears or eagles, and also so they can float food and building material to their homes.',
    'Once the dams are completed and ponds formed, beavers will work on building their homes called lodges in the middle. The dome shaped lodges, like the dams, are constructed with branches and mud. Lodges have underwater entrances, making entry tough for most other animals.',
    'There are usually two dens within the lodge, one is for drying off after entering from the water and another, drier one, is where the family of up to four adults and six to eight young live.'
    'There were once more than 60 million North American beaver. But due to hunting for its fur, its glands for medicine and because the beavers tree-felling and dams affect other land uses, the population has declined to around 12 million.',
    'The beaver has a good sense of hearing, smell, and touch. It has poor eyesight, but does have a set of transparent eyelids which allow them to see under water.',
    'Using their broad, scaly tail, beavers will forcefully slap the water as an alarm signal to other beavers in the area that a predator is approaching.',
    'Beavers are slow on land but using their webbed feet they are very good swimmers. A beaver can stay under water for up to 15 minutes.',
    'Beavers are herbivores. They like to eat the wood of trees such as the aspen, cottonwood, willow, birch, maple, cherry and also eat pondweed and water lilies.',
    'Adult beavers are around 3 feet long and have been known to weigh over 25 kg (55 lb). Females are as large or larger than males of the same age.',
    'Beavers can live up to 24 years in the wild.',
    'The beaver is the national animal of Canada, and features on the Canadian five-cent piece.',
    'Beavers like to keep themselves busy, they are prolific builders during the night. Hence the saying "As busy as a beaver".'
    )

CAMEL_FACTS = (
    'There are two species of true camel. The dromedary, is a single humped camel that lives in the Middle East and the Horn of Africa area. The bactrian, is a two-humped camel that lives in areas of Central Asia.',
    'There are four camel-like mammals that live in South America, llama and alpaca are called "New World camels", while guanaco and vicuna are called "South American camels".',
    'Camels have been domesticated by humans for thousands of years. Used mostly for transport or to carry heavy loads, they also provide a source of milk, meat, and hair/wool.',
    'Camels live on average for 40 to 50 years.',
    'Camels are 1.85 m (6 ft 1 in) at shoulder level and 2.15 m (7 ft 1 in) at the hump.',
    'Camels are capable of running as fast as 65 km/h (40 mph) for a short period of time, and can maintain a speed of around 40 km/h (25 mph).',
    'Dromedary camels weigh 300 to 600 kg (660 to 1,320 lb) and bactrian camels weigh 300 to 1,000 kg (660 to 2,200 lb).',
    'Camels do not actually hold liquid water in their humps. The humps contain fatty tissue reserves, which can be converted to water or energy when required. They can survive up to six months without food or water by using up these fatty stores.',
    'Camels are well suited to the hot sandy deserts they roam in. Their thick coat insulates them from heat and also lightens during summer to help reflect heat.',
    'A camels long legs help its body to be high from the hot desert surface and a pad of thick tissue called a pedestal raises the body slightly when the camel sits so cool air can pass underneath.',
    'A large camel can drink around 30 gallons (113 liters) in just 13 minutes, making them able to rehydrate faster than any other mammal.',
    'Long eyelashes, ear hair, and closable nostrils keep sand from affecting the camel, while their wide feet help them move without sinking into sand.',
    'Camels have long been used in wartimes. Romans used camels for their ability to scare off horses who are afraid of their scent, and in recent times camels have been used to carry heavy gear and troops across hot sandy deserts.',
    'There are estimated to be over 14 million camels in the world. Camels introduced to desert areas of Australia are the worlds largest populations of feral camels.'
    )

CHEETAH_FACTS = (
    'The cheetah is the fastest land animal in the world. They can reach a top speed of around 113 km per hour.',
    'A cheetah can accelerate from 0 to 113 km in just a few seconds.',
    'Cheetahs are extremely fast however they tire quickly and can only keep up their top speed for a few minutes before they are too tired to continue.',
    'Cheetahs are smaller than other members of the big cat family, weighing only 45 – 60 kilograms.',
    'One way to always recognise a cheetah is by the long, black lines which run from the inside of each eye to the mouth. These are usually called “tear lines” and scientists believe they help protect the cheetah’s eyes from the harsh sun and help them to see long distances.',
    'Cheetahs are the only big cat that cannot roar. They can purr though and usually purr most loudly when they are grooming or sitting near other cheetahs.',
    'While lions and leopards usually do their hunting at night, cheetahs hunt for food during the day.',
    'A cheetah has amazing eyesight during the day and can spot prey from 5 km away.',
    'Cheetahs cannot climb trees and have poor night vision.',
    'With their light body weight and blunt claws, cheetahs are not well designed to protect themselves or their prey. When a larger or more aggressive animal approaches a cheetah in the wild, it will give up its catch to avoid a fight.',
    'Cheetahs only need to drink once every three to four days.'
    )

COW_FACTS = (
    'There are well over 1 billion cattle in the world.',
    'Cattle are sacred in India. There are an estimated 300 million cattle in India.',
    'Young cattle are generally known as calves. Adult females are generally called cows. Adult males that are not castrated are generally called bulls.',
    'Cattle are red/green color blind.',
    'In the sometimes controversial sport of bull fighting, bulls are angered by the movement of the cape rather than its red color.',
    'Cattle trained to be draft animals are known as oxen (ox).',
    'Cows are social animals, and they naturally form large herds. Like people, they will make friends and bond to some herd members, while avoiding others',
    'Cows can hear lower and higher frequencies better than humans.',
    'An average dairy cow weighs about 1,200 pounds.',
    'A cows normal body temperature is 101.5°F.',
    'The average cow chews at least 50 times per minute.',
    'The typical cow stands up and sits down about 14 times a day.',
    'An average cow has more than 40,000 jaw movements in a day.',
    'Cows actually do not bite grass; instead they curl their tongue around it.',
    'Cows have almost total 360-degree panoramic vision.',
    'Cows have a single stomach, but four different digestive compartments.',
    'Cows are pregnant for 9 months just like people',
    'A dairy cow can produce 125 lbs. of saliva a day'
    )

CRAB_FACTS = (
    'Crabs are decapods from the crustacean family.',
    'Crabs have 10 legs, however, the first pair are its claws which are called chelae.',
    'Crabs have a thick external skeleton called an exoskeleton. It is a shell made of calcium carbonate and provides protection for the soft tissue underneath.',
    "Crabs live in all the world's oceans, in fresh water, and on land. There are over 4500 species of crabs.",
    "Other animals with similar names such as hermit crabs, king crabs, porcelain crabs, horseshoe crabs and crab lice, are not true crabs.",
    'Crabs usually have a distinct sideways walk. However, some crabs can walk forwards or backwards, and some are capable of swimming.',
    'The collective name for a group of crabs is a "cast".',
    'Crabs communicate with each other by drumming or waving their pincers.',
    'Male crabs tend to often fight with each other over females or hiding holes.',
    'The Pea Crab is the smallest known species at just a few millimetres wide. The largest species is the Japanese Spider Crab, with a leg span of up to 4 m (13 ft).',
    'Crabs are omnivores, they feed mainly on algae, but also bacteria, other crustaceans, molluscs, worms, and fungi.',
    'Some crab species can naturally autotomise (shed) limbs such as their claws, which then regenerate after about a year.',
    'Crabs make up 20% of all marine crustaceans caught by humans each year. This adds up to a total of 1.5 million ton annually',
    'The most consumed species of crab in the world is the Japanese Blue Crab.'
    )

DOLPHIN_FACTS = (
    'Compared to other animals, dolphins are believed to be very intelligent.',
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
    )

DRAGON_FACTS = (
    'The word “dragon” comes from the Greek word “draconta,” which means “to watch.” The Greeks saw dragons as beasts that guarded valuable items. In fact, many cultures depict dragons as hoarding treasure.',
    'Ancient Greeks and Sumerians spoke of giant “flying serpents” in their scrolls and lectures. Dragons are depicted as snake- or reptile-like.',
    'The Komodo dragon is a type of monitor lizard, which is aggressive and deadly. They can be 10 feet long and use toxic bacteria in their mouths to wound their prey.',
    'In medieval times, dragons were considered very real, but demonic. Religions had widely different views of dragons: some loved them and some feared them.',
    'In many cultural stories, dragons exhibit features of other animals, like the head of elephants, claws of lions and beaks of predatory birds. Their body colors are widely different – red, blue, green, gold, but usually earth tones. In some cultures, the colors have specific meanings.',
    '“Dragon” is actually a family term that includes other mythological creatures, such as cockatrices, gargoyles, wyverns, phoenix, basilisks, hydras, and even some hybrid man-dragon creatures.'
    )

EAGLE_FACTS = (
    'Eagles build their nests on high cliffs or in tall trees.',
    'There are over 60 different species of eagle.',
    'Eagles feature prominently on the coat of arms of a large number of countries, such as Germany, Mexico, Egypt, Poland and Austria.',
    'Golden eagles have been known to hunt foxes, wild cats and even young deer and goats.',
    'Female golden eagles usually lay between one and four eggs each breeding season.',
    'The Great Seal of the United States features a bald eagle. The bald eagle is the national bird of the United States.',
    'Female bald eagles are larger than male bald eagles.',
    'Bald eagles eat mostly fish, swooping down to the water and catching them with their powerful talons.',
    'Bald eagles live for around 20 years in the wild.',
    'Bald eagles build very large nests, sometimes weighing as much as a ton!',
    'The bald eagle was added to the list of endangered species in the United States in 1967 and its numbers have recovered well since.'
    )

ECHIDNA_FACTS = (
    'Male echidnas have a bizarre 4-headed penis.',
    "Echidnas are covered with fur and spiky spines. These spines are modified hairs, similar to that of the porcupines. There are tiny muscle bundles connected to the base of each spine so the echidna can control the spine's movement and direction.",
    'A mother echidna lays a single leathery egg in her pouch, then carries it for about ten days before it hatches. The baby echidna, called a puggle, is born hairless and spineless - but with formidable claws.',
    "Female echidnas produce milk, but they have no nipples. Instead, they secrete milk in two small, hairy areas known as aerola patches, which are connected to the milk glands. A baby echidna suckles milk straight out of its mom's skin.",
    'Echidna is Named After the Greek "Mother of Monsters".',
    "Echidnas are weird - they have a mish-mash of reptilian and mammalian features, which was recognized early on by biologists. In 1802, British anatomist Everard Home named the curious animal after the Greek goddess Ekhidna (meaning 'she viper') who was half-snake and half-woman.",
    'Echidnas are egg-laying mammals. Along with the platypus, the echidna is a member of the monotremes, an order of egg-laying mammals found in Australia.',
    'At the end of their slender snouts, echidnas have tiny mouths and toothless jaws. They use their long, sticky tongues to feed on ants, termites, worms, and insect larvae.',
    "The echidna has a very large brain for its body size. Part of this might be due to their enlarged neocortex, which makes up half of the echidna's brain (compare this to about 30 percent in most other mammals and 80 percent in humans)."
    )

ELEPHANT_FACTS = (
    'There are two types of elephant, the Asian elephant and the African elephant (although sometimes the African Elephant is split into two species, the African Forest Elephant and the African Bush Elephant).',
    'Elephants are the largest land-living mammal in the world.',
    'Both female and male African elephants have tusks but only the male Asian elephants have tusks. They use their tusks for digging and finding food.',
    'Female elephants are called cows. They start to have calves when they are about 12 years old and they are pregnant for 22 months.',
    'An elephant can use its tusks to dig for ground water. An adult elephant needs to drink around 210 litres of water a day.',
    'Elephants have large, thin ears. Their ears are made up of a complex network of blood vessels which help regulate their temperature. Blood is circulated through their ears to cool them down in hot climates.',
    'Elephants have no natural predators. However, lions will sometimes prey on young or weak elephants in the wild. The main risk to elephants is from humans through poaching and changes to their habitat.',
    'The elephant’s trunk is able to sense the size, shape and temperature of an object. An elephant uses its trunk to lift food and suck up water then pour it into its mouth.',
    'An elephant’s trunk can grow to be about 2 meters long and can weigh up to 140 kg. Some scientists believe that an elephant’s trunk is made up of 100,000 muscles, but no bones.',
    'Female elephants spend their entire lives living in large groups called herds. Male elephant leave their herds at about 13 years old and live fairly solitary lives from this point.',
    'Elephants can swim – they use their trunk to breathe like a snorkel in deep water.',
    'Elephants are herbivores and can spend up to 16 hours days collecting leaves, twigs, bamboo and roots.'
    )

EMU_FACTS = (
    'Emus are very docile and curious, and are easily tamed in captivity.',
    "Emus feed on grains, flowers, berries, soft shoots, insects, grubs and whatever else they can find. They even eat stones, dirt and tin cans by accident.",
    "When food is plentiful, emus store large amounts of fat in their bodies. They use these fat stores to survive while looking for more food.",
    'The emu belongs to a family of flightless birds called Ratites. Most Ratites are now extinct, and only the emu, ostrich, cassowary, kiwi and rhea are alive today.',
    'Emus pair in summer and breed in the cooler months. The female develops blue skin on her neck and her feathers turn a darker brown. She struts around the male making special noises to say that she is ready to mate.',
    'Emus are found only in Australia. They live in most of the less-populated areas of the continent and although they can survive in most regions, they avoid dense forest and severe desert.',
    'Emus can grow to between 5 to 6.5 feet (1.5 – 2 metres) in height and weigh up to 130 pounds (60 kg). Males are slightly smaller than females. Males make a grunting sound like a pig and females make a loud booming sound.',
    "The emu is the largest bird in Australia, and the second largest in the world after the ostrich.",
    'Emu chicks grow very quickly, up to 2 pounds (1 kg) a week, and are full-grown in 12 to 14 months. They stay with their family group for another six months or so before they split up to breed in their second season.',
    'Emus must drink every day, and they don’t waste water. On very hot days they breathe rapidly, using their lungs as evaporative coolers. Their large nasal passages have multiple folds inside. In cooler weather they use these folds to recycle air and create moisture for reuse.'
    )

FLAMINGO_FACTS = (
    'Flamingos are a type of wading bird that live in areas of large shallow lakes, lagoons, mangrove swamps, tidal flats, and sandy islands.',
    'The word "flamingo" comes from the Spanish word "flamenco" which came from the earlier Latin word "flamma" meaning flame or fire.',
    'There are six species of flamingo in the world. Two are found in the Old World and four species live in the New World - Americas.',
    'The most widespread flamingo is the Greater flamingo found in areas of Africa, Southern Europe and South, Southwest Asia. The Lesser flamingo is the most numerous and lives in the Great Rift Valley of Africa through to Northwest India.',
    "The four species in the New World include the Chilean flamingo, found in temperate South American areas, the Andean Flamingo and James's flamingo found in the high Andes mountains in Peru, Chile, Bolivia and Argentina and the American flamingo of the Caribbean islands, Belize and Galapagos islands.",
    'The Greater flamingo is the largest species, at up to 1.5 m (5 ft) tall and weighing up to 3.5 kg (8 lbs). The Lesser flamingo is just 90 cm (3 ft) tall, weighing 2.5 kg (5.5 lbs).',
    'In the wild flamingos live 20 - 30 years and sometimes over 50 years in captivity.',
    "Flamingo legs can be longer than their entire body. The backward bending 'knee' of a flamingo's leg is actually its ankle, the knee is out of sight further up the leg.",
    'Quite often flamingos will stand on one leg, with the other tucked under the body. Its not fully understood why they do this but it is believed to conserve body heat.',
    'The flamingo is a filter-feeder, holding its curved beak upside down in the water it sucks in the muddy water and pushes the mud and silt out the side while tiny hair-like filters along the beak called lamellae sieve food from the water.',
    "The pink to reddish color of a flamingo's feathers comes from carotenoids (the pigment that also makes carrots orange) in their diet of plankton, brine shrimp and blue-green algae.",
    'Flamingos are social birds, they live in colonies of sometimes thousands, this helps in avoiding predators, maximizing food intake, and is better for nesting.',
    'Flamingo colonies split into breeding groups of up to 50 birds, who then perform a synchronized ritual "dance" whereby they stand together stretching their necks upwards, uttering calls while waving their heads and then flapping their wings.',
    'The flamingo is the national bird of the Bahamas.'
    )

FOX_FACTS = (
     'A group of foxes is called a "skulk" or "leash".',
     'Grey foxes can retract their claws like cats do',
     'A male is called a ‘dog fox’ while a female is called a ‘vixen’',
     'Foxes are generally solitary animals; unlike wolves, they hunt on their own rather than in packs',
     "Foxes' pupils are vertical, similar to a cat, helping them to see well at night",
     "The tip of a red fox’s tail is white, whereas swift foxes have a black-tipped tail",
    "Foxes have excellent hearing. Red foxes can reportedly hear a watch ticking 40 yards away!",
    'Foxes stink, their funny ‘musky’ smell comes from scent glands at the base of their tail'
    )

FROG_FACTS = (
    'A frog is an amphibian. They lay their eggs in water. The eggs hatch into a tadpole which lives in water until it metamorphoses into an adult frog.',
    'Tadpoles look more like fish than frogs, they have long finned tails and breathe through gills.',
    'An amphibian can live both on land and in water.',
    'Although frogs live on land their habitat must be near swamps, ponds or in a damp place. This is because they will die if their skin dries out.',
    'Instead of drinking water, frogs soak it into their body through their skin.',
    'Frogs breathe through their nostrils while also absorbing about half the air they need through their skin.',
    'Frogs use their sticky, muscular tongue to catch and swallow food. Unlike humans, their tongue is not attached to the back of its mouth. Instead it is attached to the front, enabling the frog to stick its tongue out much further.',
    'The common pond frog is ready to breed when it is only three years old.',
    'Frogs in the wild face many dangers and are lucky to survive several years. In captivity however, frogs can live for much longer.',
    'Frogs can see forwards, sideways and upwards all at the same time. They never close their eyes, even when they sleep.',
    "Remarkably, frogs actually use their eyes to help them swallow food. When the frog blinks, its eyeballs are pushed downwards creating a bulge in the roof of its mouth. This bulge squeezes the food inside the frog's mouth down the back of its throat."
    )

GIRAFFE_FACTS = (
    'A male giraffe can weigh as much as a pick up truck! That’s about 1400 kilograms.',
    'Although a giraffe’s neck is 1.5 – 1.8 meters, it contains the same number of vertebrae at a human neck.',
    "A giraffe's habitat is usually found in African savannas, grasslands or open woodlands.",
    'The hair that makes up a giraffes tail is about 10 times thicker than the average strand of human hair.',
    'The distinctive spots that cover a giraffe’s fur act as a good camouflage to protect the giraffe from predators. When the giraffe stands in front of trees and bushes the light and dark colouring of its fur blends in with the shadows and sunlight.',
    'It is possible to identify the sex of the giraffe from the horns on its head. Both males and females have horns but the females are smaller and covered with hair at the top. Male giraffes may have up to 3 additional horns.',
    'Giraffes are ruminants. This means that they have more than one stomach. In fact, giraffes have four stomachs, the extra stomachs assisting with digesting food.',
    'Drinking is one of the most dangerous times for a giraffe. While it is getting a drink it cannot keep a look out for predators and is vulnerable to attack.',
    'Male giraffes sometimes fight with their necks over female giraffes. This is called “necking”. The two giraffes stand side by side and one giraffe swings his head and neck, hitting his head against the other giraffe. Sometimes one giraffe is hit to the ground during a combat.',
    'A female giraffe gives birth while standing up. The calf drops approximately 6 feet to the ground, but it is not hurt from the fall.',
    'Giraffes have bluish-purple tongues which are tough and covered in bristly hair to help them with eating the thorny Acacia trees.',
    )

GORILLA_FACTS = (
    'There are only about 700 mountain gorillas and they live high in the mountains in two protected parks in Africa. Lowland gorillas live in central Africa.',
    'You may have seen baby gorillas being carried on the back of their mothers, but for the first few months after birth the mother holds the baby gorilla to her chest.',
    'An adult male gorilla is called a silverback because of the distinctive silvery fur growing on their back and hips. Each gorilla family has a silverback as leader who scares away other animals by standing on their back legs and beating their chest!',
    'Young male gorillas usually leave their family group when they are about 11 years old and have their own family group by the age of 15 years old. Young female gorillas join a new group at about 8 years old.',
    'Gorillas are herbivores. They spend most of their day foraging for food and eating bamboo, leafy plants and sometimes small insects. Adult gorillas can eat up to 30 kilograms of food each day.'
    'An adult gorilla is about 1 meter tall to their shoulders when walking on all fours using their arms and their legs.',
    'A gorilla can live for 40 – 50 years.',
    'Gorillas are considered to be very intelligent animals. They are known for their use of tools and their varied communication. Some gorillas in captivity at a zoo have been taught to use sign language.',
    'Gorillas are endangered animals. Their habitat is destroyed when people use the land for farming and the trees for fuel. Gorillas are also killed by poachers and sometimes get caught in poacher’s snares meant for other animals.'
    )

HAMSTER_FACTS = (
    "Hamsters are rodents from the subfamily Cricetinae.",
    "There are 25 species of hamster.",
    "Hamsters have thick silky fur, short tails, small ears, short legs, wide feet and large eyes.",
    "Hamsters usually live in burrows underground during the day, they are crepuscular which means they come out at twilight to feed.",
    "Wild hamsters feed mainly on seeds, fruits, vegetables and sometimes insects.",
    "Hamsters are very good diggers, they will create burrows in the soil that can be over half a meter deep, containing various rooms for different purposes.",
    "Hamsters have large cheek in which they carry food back to their burrows. Full pouches can make their heads double or triple in size.",
    "Hamsters do not have good eyesight, they are nearsighted and also colour-blind.",
    "The hamster relies on scent to find their way. They have scent glands which they rub on objects along a path.",
    "Depending on the species hamsters can be black, grey, honey, white, brown, yellow, red, or a combination of these colors.",
    "Hamsters are great as pets because they are easy to breed in captivity, easy to care for and interact well with people. They are also used as laboratory animals.",
    "The Syrian hamster is the most popular and well known breed kept as pets. All Syrian hamsters as pets are believed to have descended from one pair in 1930.",
    "Syrian hamsters live 2 - 3 years in captivity, and less in the wild. Other popular pet types such as Russian dwarf hamsters live about 2- 4 years in captivity.",
    "Hamsters range in size from the largest breed, the European hamster at 13.4 in (34 cm) long, to the smallest, the dwarf hamster at 2 - 4 in (5.5 - 10.5 cm) long."
    )

HEDGEHOG_FACTS = (
    'There are 17 species of hedgehog. They are found in parts of Europe, Asia, Africa and were introduced in New Zealand by settlers.',
    'Hedgehogs are nocturnal animals, often sleep during the day in a nest or under bushes and shrubs before coming out to feed at night.',
    'Hedgehogs are not related to other spine covered creatures such as the porcupine or echidna.',
    'The spines of a hedgehogs, are stiff hollow hairs, they are not poisonous or barbed and cannot be easily removed, they fall out naturally when a hedgehog sheds its baby spines and grows adult spines a process called "quilling".',
    'Hedgehogs have about 5,000 to 6,500 spines at any one time.',
    'Most hedgehog species will roll into a tight ball if threatened, making it hard for its attacker to get past the spiky defences.',
    'A baby hedgehog is called a hoglet.',
    'Hedgehogs communicate through a combination of snuffles, grunts and squeals.',
    'Hedgehogs have weak eyesight but a strong sense of hearing and smell. They can swim, climb and run surprising quickly over short distances.',
    'For their size hedgehogs have a relatively long lifespan. They live on average for 4-7 years in the wild and longer in captivity.',
    'Hedgehogs in colder climates such as the UK will hibernate through winter.',
    'If hedgehogs come in contact with humans they can sometimes pass on infections and diseases.',
    'The hedgehog is a pest in countries such as New Zealand where it has been introduced, as it does not have many natural predators and eats native species of insects, snails, lizards and baby ground-nesting birds.'
    )

HIPPO_FACTS = (
    'The name hippopotamus means ‘river horse’ and is often shortened to hippo.',
    'The hippopotamus is generally considered the third largest land mammal (after the white rhinoceros and elephant).',
    'Hippopotamuses spend a large amount of time in water such as rivers, lakes and swamps.',
    'Resting in water helps keep hippopotamuses temperature down.',
    'Hippopotamuses give birth in water.',
    'Hippopotamuses have short legs, a huge mouth and a body shaped like a barrel.',
    'The closest relations of the hippopotamus are surprisingly cetaceans such as whales and dolphins. Scientists believe this family of animals diverged in evolution around 55 million years ago.',
    'Although hippos might look a little chubby, they can easily outrun a human.',
    'Hippos can be extremely aggressive, especially if they feel threatened. They are regarded as one of the most dangerous animals in Africa.',
    'Hippos are threatened by habitat loss and poachers who hunt them for their meat and teeth.',
    'A male hippopotamus is called a ‘bull’. A female hippopotamus is called a ‘cow’. A baby hippo is called a ‘calf’.',
    'A group of hippos in known as a ‘herd’, ‘pod’, ‘dale’ or ‘bloat’.',
    'Hippos typically live for around 45 years.',
    )

HORSE_FACTS = (
    'Horses can sleep both lying down and standing up.',
    'Horses can run shortly after birth.',
    'You can generally tell the difference between male and female horses by their number of teeth: males have 40 while females have 36 (but honestly, most us are going to use the much “easier” way).',
    'Domestic horses have a lifespan of around 25 years.',
    'The Przewalski’s horse is the only truly wild horse species still in existence. The only wild population is in Mongolia. There are however numerous populations across the world of feral horses e.g. mustangs in North America.',
    'A 19th century horse named ‘Old Billy’ is said to have lived 62 years.',
    'Horses have around 205 bones in their skeleton.',
    'Horses have been domesticated for over 5000 years.',
    'Horses have bigger eyes than any other mammal that lives on land.',
    'Because horse’s eyes are on the side of their head they are capable of seeing nearly 360 degrees at one time.',
    'Horses gallop at around 44 kph (27 mph).',
    'The fastest recorded sprinting speed of a horse was 88 kph (55 mph).',
    'Estimates suggest that there are around 60 million horses in the world.',
    'Scientists believe that horses have evolved over the past 50 million years from much smaller creatures.',
    'A male horse is called a stallion. A female horse is called a mare.',
    'A young male horse is called a colt. A young female horse is called a filly.',
    'An adult horse’s brain weights 22 oz, about half that of a human.',
    'The first cloned horse was a Haflinger mare in Italy in 2003.',
    'Horses with pink skin can get a sunburn.',
    'A group of horses will not go to sleep at the same time - at least one of them will stay awake to look out for the others.'
    )

HUMMINGBIRD_FACTS = (
    'Hummingbirds are New World birds found only in the Americas',
    'There are more than 340 species of hummingbirds.',
    'Hummingbirds are one of the smallest kinds of bird in the world. With most species 7.5 - 13 cm (3 - 5 in) in length. The Bee hummingbird is the smallest at just 5 cm (2 in). The largest is the Giant Hummingbird reaching over 20 cm (8 in).',
    'They are called hummingbirds due to the sound created by their rapidly beating wings.',
    "Depending on the species a hummingbird's wings can flap on average around 50 times per second, and can reach as high as 200 times per second. This allows them to fly faster than 15 m/s (54 km/h or 34 mph).",
    'The hummingbird can hover, fly forwards, backwards and even upside down.',
    'Hummingbirds drink the nectar of flowers which gives them a good source of glucose energy, they will catch insects every now and again for a protein boost.',
    "A hummingbird's bill varies dramatically depending on the species. Most have a fairly long, thin bill that allows them to reach down to the nectar of a flower. With the bill slightly open they use their tongue to quickly lap up the nectar inside.",
    'Apart from insects, hummingbirds have the highest metabolism of all animals due to the need to keep their wings rapidly beating. Because of this the hummingbird visits hundreds of flowers each day and consuming more than their own weight in nectar each day.'
    'Because they need to conserve energy hummingbirds do not spend all day flying, they spend the majority of their time perched digesting their food.',
    'To conserve energy overnight a hummingbird enters a hibernation-like sleep state called torpor.',
    'Depending on the species hummingbirds live on average 3 to 5 years but have been known to live as long as 12 years.',
    'Most hummingbirds of the United States and Canada migrate over 3000km south in fall to spend winter in Mexico or Central America. Some South American species also move north to these areas during the southern winter.',
    'Before migrating, the hummingbird will store up a layer of fat equal to half its body weight in order to slowly use up this energy source while flying.'
    )

JELLYFISH_FACTS = (
    'Jellyfish live in the sea and are found in all oceans.',
    'Some jellyfish live in fresh water.',
    'Jellyfish can be large and brightly colored. They can often be transparent or translucent.',
    'Some jellyfish can be very hard to see, nearly invisible to the human eye. Box jellyfish are almost transparent.',
    'Although the word is mentioned in their name, jellyfish are not fish.',
    'A group of jellyfish is called a ‘bloom’, ‘swarm’ or ‘smack’. Large blooms can feature over 100,000 jellyfish.',
    'Jellyfish don’t have brains.',
    'Jellyfish use their tentacles to sting. Most are harmless to humans but stings from some species, such as the box jellyfish, can be very painful and sometimes kill.',
    'Jellyfish eat plankton. Some sea turtles eat jellyfish.'
    )

LEOPARD_FACTS = (
    'Leopards are part of the cat family, Felidae. The scientific name for a leopard is Panthera pardus.',
    'Leopards are well known for their cream and gold spotted fur, but some leopards have black fur with dark spots. These black leopards are often mistaken for panthers.',
    'Adult leopards are solitary animals. Each adult leopard has its own territory where it lives and, although they often share parts of it, they try to avoid one another.',
    'A leopard’s body is built for hunting. They have sleek, powerful bodies and can run at speeds of up to 57 kilometers per hour. They are also excellent swimmers and climbers and can leap and jump long distances.',
    'A leopard’s tail is just about as long as its entire body. This helps it with balance and enables it to make sharp turns quickly.',
    'Leopards are mostly nocturnal, hunting prey at night.',
    'Leopards protect their food from other animals by dragging it high up into the trees. A leopard will often leave their prey up in the tree for days and return only when they are hungry!',
    'Female leopards give birth to a litter of two or three cubs at a time. By the time a cub is two years old it will leave the company of its mother and live on their own.',
    'When a female leopard is ready to mate she will give a scent and rub her body on the trees to leave her smell there. Male leopards either smell the females scent or hear her call to know that she is ready to mate.',
    'Some people believe that the bones and whiskers of leopards can heal sick people. Many leopards are killed each year for their fur and body parts and this is one reason why the leopard is an endangered animal. While they were previously found in the wild in a number of areas around the world, their habitat is largely restricted to sub-Saharan Africa with small numbers also found in India, Pakistan, Malaysia, China and Indochina.'
    )


LION_FACTS = (
    'Lions are the second largest big cat species in the world (behind tigers).',
    'The average male lion weighs around 180 kg (400 lb) while the average female lion weighs around 130 kg (290 lb).',
    'The heaviest lion on record weighed an amazing 375 kg (826 lb).',
    'Lions can reach speeds of up to 81 kph (50 mph) but only in short bursts because of a lack of stamina.',
    'The roar of a lion can be heard from 8 kilometers (5.0 miles) away.',
    'Most lions found in the wild live in southern and eastern parts of Africa.',
    'Lions are very social compared to other cat species, often living in prides that feature females, offspring and a few adult males.',
    'Male lions are easy to recognize thanks to their distinctive manes. Males with darker manes are more likely to attract female lions (lionesses).',
    'Lions are the national animal of Albania, Belgium, Bulgaria, England, Ethiopia, Luxembourg, the Netherlands and Singapore.',
    'Lions in the wild live for around 12 years.',
    'When lions breed with tigers the resulting hybrids are known as ligers and tigons. There are also lion and leopard hybrids known as leopons and lion and jaguar hybrids known as jaglions.',
    'Lionesses are better hunters than males and do most of the hunting for a pride.',
    'In the wild, lions rest for around 20 hours a day.',
    )

LIZARD_FACTS = (
    'Some lizards can detach their tails if caught by predators.',
    'The upper and lower eyelids of chameleons are joined, leaving just a small hole for them to see through. They can move their eyes independently however, allowing them to look in two different directions at the same time.',
    'Chameleons have long tongues which they rapidly extend from their mouth, too fast for human eyes to see properly.',
    'Chameleons generally eat insects.',
    'Some chameleons have the ability to change color. This helps them communicate with each other and can also be used for camouflage.',
    'Geckos have no eyelids.',
    'Geckos have unique toes which allow them to be good climbers.',
    'Iguanas have a row of spines which run down their back and tail.',
    'The Komodo dragon is the largest type of lizard, growing up to 3 meters (10 feet) in length.',
    'Komodo dragons are found on a number of different Indonesian Islands.',
    'Komodo dragons are carnivores and can be very aggressive.'
    )

MONKEY_FACTS = (
    'There are currently 264 known monkey species.',
    'Monkeys can be divided into two groups, Old World monkeys that live in Africa and Asia, and New World monkeys that live in South America.',
    'A baboon is an example of an Old World monkey, while a marmoset is an example of a New World monkey.',
    'Apes are not monkeys. Most monkeys have tails.',
    'Some monkeys live on the ground, while others live in trees.',
    'Different monkey species eat a variety of foods, such as fruit, insects, flowers, leaves and reptiles.',

    'Groups of monkeys are known as a ‘tribe’, ‘troop’ or ‘mission’.',
    'The Pygmy Marmoset is the smallest type of monkey, with adults weighing between 120 and 140 grams.',
    'The Mandrill is the largest type of monkey, with adult males weighing up to 35 kg.',
    'Capuchin monkeys are believed to be one of the smartest New World monkey species. They have the ability to use tools, learn new skills and show various signs of self-awareness.',
    'Spider monkeys get their name because of their long arms, legs and tail.',
    'The monkey is the 9th animal that appears on the Chinese zodiac, appearing as the zodiac sign in 2016.'
    )

NARWHAL_FACTS = (
    'Unlike some whale species that migrate, narwhals spend their lives in the Arctic waters of Canada, Greenland, Norway and Russia. Most narwhals winter for up to five months under sea ice in the Baffin Bay-Davis Strait area.',
    'Narwhals feed on Greenland halibut, Arctic and polar cod, squid and shrimp. They do their chomping at the ice floe edge and in the ice-free summer waters.',
    'Narwhals can dive a mile-and-a-half deep in the ocean. Cracks in the sea ice above allow them to pop up for air when they need it.',
    'Narwhals change color as they age. Newborns are a blue-gray, juveniles are blue-black and adults are a mottled gray. Old narwhals are nearly all white.',
    'There are no narwhals in captivity. In the 60s and 70s, several attempts at capturing and keeping narwhals resulted in all of the animals dying within several months.',
    'The narwhal tusk—most commonly found on males—is actually an enlarged tooth with sensory capability and up to 10 million nerve endings inside. Some narwhals have up to two tusks, while others have none. The spiraled tusk juts from the head and can grow as long at 10 feet.'
    "A narwhal tusk's tough core and soft outer layer result in a tusk that is both strong and flexible. It can bend significantly without cracking."
    )


OWL_FACTS = (
    'There are around 200 different owl species.',
    'A group of owls is called a parliament.',
    'Most owls hunt insects, small mammals and other birds.',
    'Some owl species hunt fish. Owls have powerful talons which help them catch and kill prey.',
    'Owls can turn their heads as much as 270 degrees.',
    'Owls are farsighted, meaning they can’t see things close to their eyes clearly.',
    'Owls are very quiet in flight compared to other birds of prey.',
    'The color of owl’s feathers helps them blend into their environment (camouflage).',
    'Barn owls can be recognized by their heart shaped face.'
    )

TURTLE_FACTS = (
    'Turtles have a hard shell that protects them like a shield, this upper shell is called a ‘carapace’.',
    'Turtles also have a lower shell called a ‘plastron’.',
    'Many turtle species (not all) can hide their heads inside their shells when attacked by predators.',
    'Turtles have existed for around 215 million years.',
    'Like other reptiles, turtles are cold blooded.',
    'The largest turtle is the leatherback sea turtle, it can weigh over 900 kg! (2000 lb)',
    'In some species of turtle the temperature determines if the egg will develop into a male or female, lower temperatures lead to a male while higher temperatures lead to a female.',
    'Some turtles lay eggs in the sand and leave them to hatch on their own. The young turtles make their way to the top of the sand and scramble to the water while trying to avoid predators.',
    'Sea turtles have special glands which help remove salt from the water they drink.',
    )

KANGAROO_FACTS = (
    'Kangaroos are marsupial animals that are found in Australia as well as New Guinea.',
    'There are four different kangaroo species, the red kangaroo, eastern grey kangaroo, western grey kangaroo and antilopine kangaroo.',
    'Kangaroos can hop around quickly on two legs or walk around slowly on all four.',
    'Kangaroos can’t walk backwards.',
    'Kangaroos can jump very high, sometimes three times their own height.',
    'Kangaroos can swim.',
    'Baby kangaroos are known as ‘joeys’. A group of kangaroos is called a ‘mob’, ‘troop’ or ‘court’.',
    'The red kangaroo is the largest marsupial in the world.',
    'Kangaroos usually live to around six years old in the wild.'
    )

KOALA_FACTS = (
    'Koalas are native to Australia. Koal1as are not bears.',
    'Koala fossils found in Australia have been dated as long ago as 20 million years.',
    'Koalas eat eucalyptus leaves and almost nothing else.',
    'The brain size of modern koalas has reduced substantially from their ancestors, possibly as an adaptation to the low energy they get from their diets.',
    'The closest living relative of the koala is the wombat.',
    'Koalas have sharp claws which help them climb trees.',
    'Koalas have similar fingerprints to humans.',
    'Koalas have large noses that are coloured pink or black.',
    'Outside of breeding seasons, koalas are quiet animals.',
    'A baby koala is called a ‘joey’. Joeys live in their mother’s pouch for around six months and remain with them for another six months or so afterwards.',
    'Koalas cannot be kept legally as pets.',
    )

SLOTH_FACTS = [
    'Sloths are a medium-sized mammal. There are two types of sloth the two-toed sloth and the three-toed sloth, they are classified into six different species.',
    'All sloths actually have three toes, but the two-toed sloth has only two fingers.',
    'Sloths are part of the order Pilosa so they are related to anteaters and armadillos.',
    'Sloths are tree-dwelling animals, they are found in the jungles of Central and South America.',
    "A sloth's body is usually 50 to 60 cm long. Skeletons of now extinct species of sloth suggest some varieties used to be as large as elephants.",
    'Sloths mainly eat the tree buds, new shoots, fruit and leaves, of the Cecropia tree. Some two-toed sloths also eat insects, small reptiles, and birds.',
    'Sloths have a four-part stomach that very slowly digests the tough leaves they eat, it can sometimes take up to a month for them to digest a meal. Digesting this diet means a sloth has very little energy left to move around making it one of the slowest moving animals in the world.',
    'Sloths can move along the ground at just 2 m (6.5 ft) per minute! In the trees they are slightly quicker at 3 m (10 ft) per minute.',
    'The slow-movement and unique thick fur of the sloth make it a great habitat for other creatures such as moths, beetles, cockroaches, fungi, and algae. In fact, this green colored algae provides a camouflage so sloths can avoid predators.',
    'Sloths can extend their tongues 10 to 12 inches out of their mouths.',
    'The sloth has very long, sharp, and strong claws that they use to hold on to tree branches. The claws are also their only natural defense against predators.',
    'Sloths usually only leave the tree they live in to go to the toilet once a week on the ground. This is when they are most vulnerable to being attacked by their main predators such as jaguars, the harpy eagle and snakes.',
    'Two-toed sloths are nocturnal, being most active at night. While three-toed sloths are diurnal which means they are most active during the day.',
    'It used to be thought sloths slept for 15 to 20 hours a day. However, its now believed they only sleep around 10 hours a day.',
    'In the wild, sloths live on average 10 - 16 years and in captivity over 30 years.',
    ]


OTTER_FACTS = [
    'The otter is a carnivorous mammal in a branch of the weasel family called Lutrinae.',
    'There are 13 species of otter found all around the world.',
    'Some otter species spend all their time in the water while others are land and water based animals.',
    "An otter's den is called a 'holt' or a 'couch'.",
    "A group of otters are called a 'bevy', 'family', 'lodge', or 'romp', or, when in water the group is called a 'raft'.",
    'Otters live up to 16 years in the wild.',
    'Otters are very active hunters, spending many hours a day chasing prey through water or scouring the rivers and the sea bed. They mainly eat fish but also frogs, crayfish and crabs, some species carry a rock to help smash open shellfish.',
    'Otter species range in size from the smallest Oriental small-clawed otter at 0.6 m (2 ft) and 1 kg (2.2 lb). Through to the large Giant otter and Sea otters who can reach 1.8 m (5.9 ft) and 45 kg (99.2 lb).',
    'Four of the main otter species include the European otter, the North American river otter, the Sea otter, and the Giant otter.',
    'The European otter or Eurasian otter, are found in Europe, Asia, parts of North Africa and the British Isles.',
    'The North American river otter was one of the most hunted animals for its fur after Europeans arrived. Sea otters have also been hunted in large numbers for their fur.',
    'Unlike most marine mammals, otters do not have a layer of insulating blubber. Instead air is trapped in their fur which keeps them warm.',
    'The Giant otter is found in South America around the Amazon river basin.',
    'The otter is a very playful animal and are believe to take part in some activities just for the enjoyment. Some make waterslides to slide down into the water!',
    'Otters are a popular animal in Japanese folklore where they are called "kawauso". In these tales the smart kawauso often fool humans, kind of like a fox.',
    ]

SEAGULL_FACTS = (
    'Smallest species of seagulls can reach 11.5 inches in length and 4.2 ounces of weight. Large species can reach 30 inches in length and 3.8 pounds of weight.',
    'Body of most seagulls is covered with white plumage. Wingtips are usually black or dark in color. Some species are grey or entirely white.',
    'Seagull has strong body, elongated legs and webbed feet. Beak is slightly hooked and usually yellow in color.',
    'Seagulls are one of the rare animals that are able to drink salt water. They have special glands (located above the eyes) which eliminate excess salt from the body.',
    'Diet of seagulls includes different types of insects, earthworms, small rodents, reptiles and amphibians. They also consume seed, fruit and leftovers of human meals.',
    'Seagulls are very intelligent birds. They use bread crumbs to attract fish and produce rain-like sound with their feet to attract earthworms hidden under the ground. Seagulls transfer all hunting skills and techniques to their offspring.',
    'Seagulls often steal food from other birds, animals and people. They occasionally eat young members of their own species.',
    'Main predators of seagulls are large birds of prey, such as eagles.',
    'Seagulls live in colonies that consist of few pairs of birds or couple of thousands birds.',
    'Seagulls use wide repertoire of sounds and body language for communication.',
    'Seagulls are monogamous creatures (they mate for a lifetime). Mating couple gathers each year during the mating season to reproduce and to take care of their offspring.',
    'Even though they live in large colonies, breeding couples occupy and defends its territory from nearby couple.',
    'Seagull couples collects plant material and build nests together. Nests are cup-shaped and usually located on the ground or hardly accessible cliffs.',
    'Depending on the species, female can lay one, two or three dark brown or olive green eggs. Incubation period lasts 22 to 26 days. Fathers play very important role in feeding of chicks. Young birds live in nursery flocks where they learn all skill required for independent life.',
    'Lifespan of seagulls depends on the species. Most seagulls can survive from 10 to 15 years in the wild.'
    )

SNAKE_FACTS = [
    'Snakes don’t have eyelids.',
    'Snakes can’t chew food so they have to swallow it whole.',
    'Snakes have flexible jaws which allow them to eat prey bigger than their head!',
    'Snakes are found on every continent of the world except Antarctica.',
    'Snakes have internal ears but not external ones.',
    'Snakes used in snake charming performances respond to movement, not sound.',
    'There are around 3000 different species of snake.',
    'Snakes have a unique anatomy which allows them to swallow and digest large prey.',
    'Snakes shed their skin a number of times a year in a process that usually lasts a few days.',
    'Some species of snake, such as cobras and black mambas, use venom to hunt and kill their prey.',
    'Pythons kill their prey by tightly wrapping around it and suffocating it in a process called constriction. This bot is written in Python',
    'Some sea snakes can breathe partially through their skin, allowing for longer dives underwater.',
    'Anacondas are large, non-venomous snakes found in South America that can reach over 5 m (16 ft) in length.',
    'Python reticulates can grow over 8.7 m (28 ft) in length and are considered the longest snakes in the world.'
    ]

SHARK_FACTS = [
    'Sharks do not have a single bone in their bodies. Instead they have a skeleton made up of cartilage; the same type of tough, flexible tissue that makes up human ears and noses.',
    'Some sharks remain on the move for their entire lives. This forces water over their gills, delivering oxygen to the blood stream. If the shark stops moving then it will suffocate and die.',
    'Sharks have outstanding hearing. They can hear a fish thrashing in the water from as far as 500 meters away!',
    'If a shark was put into a large swimming pool, it would be able to smell a single drop of blood in the water.',
    'Although most species of shark are less than one meter long, there are some species such as the whale shark, which can be 14 meters long.',
    'A pup (baby shark) is born ready to take care of itself. The mother shark leaves the pup to fend for itself and the pup usually makes a fast get away before the mother tries to eat it!',
    'Not all species of shark give birth to live pups. Some species lay the egg case on the ocean floor and the pup hatches later on its own.',
    'Great whites are the deadliest shark in the ocean. These powerful predators can race through the water at 30 km per hour.',
    'Unlike other species of shark, the great white is warm-blooded. Although the great white does not keep a constant body temperature, it needs to eat a lot of meat in order to be able to regulate its temperature. ',
    'A shark always has a row of smaller teeth developing behind its front teeth. Eventually the smaller teeth move forward, like a conveyor belt, and the front teeth fall out.'
    ]

TIGER_FACTS = [
    'The tiger is the biggest species of the cat family.',
    'Tigers can reach a length of up to 3.3 meters (11 feet) and weigh as much as 300 kilograms (660 pounds).',
    'Subspecies of the tiger include the Sumatran Tiger, Siberian Tiger, Bengal Tiger, South China Tiger, Malayan Tiger and Indochinese Tiger.',
    'Many subspecies of the tiger are either endangered or already extinct. Humans are the primary cause of this through hunting and the destruction of habitats.',
    'Around half of tiger cubs don’t live beyond two years of age.',
    'Tiger cubs leave their mother when they are around 2 years of age.',
    'A group of tigers is known as an ‘ambush’ or ‘streak’.',
    'Tigers are good swimmers and can swim up to 6 kilometers.',
    'Rare white tigers carry a gene that is only present in around 1 in every 10,000 tigers.',
    'Tigers usually hunt alone at night time.',
    'Tigers have been known to reach speeds up to 40 mph (65 kph).',
    "Less than 10% of hunts end successfully for tigers",
    'Tigers can easily jump over 5 meters in length.',
    'Various tiger subspecies are the national animals of Bangladesh, India, North Korea, South Korea and Malaysia.',
    'There are more tigers held privately as pets than there are in the wild.',
    'Tigers that breed with lions give birth to hybrids known as tigons and ligers.'
    ]

SCORPION_FACTS = [
    'Scorpions are predatory animals of the class Arachnida, making them cousins to spiders, mites and ticks.',
    'Scorpions have eight legs, a pair of pincers (pedipalps) and a narrow segmented tail that often curves over their back, on the end of which is a venomous stinger.',
    'The scorpion uses their pincers to quickly grab prey and then whip their poisonous tail stinger over to kill or paralyze the prey. The tail is also used as a useful defense against predators.',
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

PANDA_FACTS = (
    'The giant panda is native to China. It has a black and white coat that features large black patches around its eyes.',
    'Pandas are an endangered species. Population estimates vary but there may be around 2000 left living in the wild.',
    'A giant panda cub weighs only around 150 grams (5 oz) at birth.',
    'Adult male pandas can weigh up to 150 kg (330 lb).',
    'Giant panda have a lifespan of around 20 years in the wild.',
    'Female pandas raise cubs on their own (the male leaves after mating).',
    'The diet of a panda is made up almost entirely of bamboo.',
    'Giant pandas eat as much as 10 kg (22 lb) of bamboo a day.',
    'Despite their appearance Giant pandas are good climbers.',
    'The scientific name for the giant panda is ‘ailuropoda melanoleuca’.',
    'An animated movie from 2008 named ‘Kung Fu Panda’ features a giant panda called ‘Po’.'
    )

PANTHER_FACTS = (
    'The animal known as a "panther" actually refers to 3 different types of big cats, leopards (Panthera pardus) or jaguars (Panthera onca) that have a black or white color mutation and a subspecies of the cougar (Puma concolor).',
    "The 'black panther' is a black jaguar of the Americas or a black leopard of Asia and Africa. In fact, the black panther actually has normal rosettes (spots), they are often just too hard to see because the animal's fur is so dark. Melanism is the name of the dark color pigmentation mutation in a jaguar or leopard that cause the fur to be blackish, it occurs in about 6% of the population.",
    'The opposite of melanism is albinism which is an even rarer mutation that can occur in most animal species. The extremely rare "white panther" are albino leopards, jaguars or cougars.',
    'Because the melanism gene is a dominant gene in jaguars, a black jaguar may produce either black or spotted cubs, while a pair of spotted jaguars can only have spotted cubs.',
    'Apart from color the black panther is believed to be less fertile than normal-colored big cats and also much more unpredictable and aggressive.',
    'Black panthers are great swimmers and are one of the strongest tree climbing big cats, often pouncing on prey from a tree, they are capable of leaping up to 20 feet to catch their prey which includes medium sized animals like deer and monkeys and smaller rabbits and birds.',
    'Black panthers have good hearing, extremely good eyesight, and a strong jaw.',
    "The black panther is often called 'the ghost of the forest'. It is a smart, stealth-like attacker, its dark coat helps it hide and stalk prey very easily, especially at night.",
    'The light tan colored Florida panther is one of over 30 subspecies of cougar (Puma concolor) found in North America.',
    "The Florida panther has adapted to the subtropical forests and swamp environments of Florida, however they are very rare animals, as of 2013 it is believed only 160 Florida panthers remain in the wild."
    )

PARROT_FACTS = (
    'There are around 372 different parrot species.',
    'Parrots are believed to be one of the most intelligent bird species. Some species are known for imitating human voices.',
    'Most parrot species rely on seeds as food. Others may eat fruit, nectar, flowers or small insects.',
    'Parrots such as the budgerigar (budgie) and cockatiel are popular as pets.',
    'Some parrot species can live for over 80 years.',
    'There are 21 different species of cockatoo.',
    'Cockatoos usually have black, grey or white plumage (feathers).',
    'Keas are large, intelligent parrots that live in alpine areas of New Zealand’s South Island. They are the world’s only alpine parrot and are known for their curious and sometimes cheeky behaviour near ski fields where they like to investigate bags, steal small items and damage cars.',
    'Kakapos are critically endangered flightless parrots, as of 2010 only around 130 are known to exist. They are active at night (nocturnal) and feed on a range of seeds, fruit, plants and pollen. Kakapos are also the world’s heaviest parrot.',
    'The flag of Dominica features the sisserou parrot.'
    )

PEACOCK_FACTS = (
    '"Peacock" is commonly used as the name for a peafowl of the pheasant family. But in fact "peacock" is the name for the colorfully plumaged male peafowl only. The females are called peahens, they are smaller and grey or brown in color. The name of a baby peafowl is a peachick.',
    'Peacocks are best known for their amazing eye-spotted tail feathers or plumage. During a display ceremony the peacock will stand its tail feathers up to form a fan that stretches out nearly 2 m in length.',
    "A peacock's colourful display is believed to be a way to attract females for mating purposes, and secondly to make the peacock look bigger and intimidating if he feels threatened by predators.",
    'There are 3 varieties of peafowl, the Indian, the Green and the Congo.',
    'The most common type of peafowl found in many zoos and parks around the world is the Indian peafowl. The head and neck of which is covered in shining, blue feathers arranged like scales. It is native to South Asia areas of Pakistan, Sri Lanka and India (where it is the national bird).',
    "The Congo peafowl is native to central Africa. It doesn't have a large plumage like other varieties. It is the national bird of the Democratic Republic of Congo.",
    "The Green peafowl is native to Southeast Asia, it has chrome green and bronze feathers. It lives in areas such as Myanmar (its national symbol) and Java. It is regarded as an endangered species due to hunting and a reduction in its habitat.",
    "White varieties of peacocks are not albinos, they have a genetic mutation that causes the lack of pigments in the plumage.",
    "Peacock feathers accounts for 60 percent of the bird's total body length and with a wingspan measuring 5 feet, it is one of the largest flying birds in the world.",
    "A peafowl can live to over the age of 20 years, the peacocks plumage looks its best when the male reaches the age of 5 or 6.",
    "Peacocks have spurs on their feet that are primarily used to fight with other males.",
    "Peafowl are omnivorous, they eat many types of plants, flower petals, seeds, insects and small reptiles such as lizards.",
    "In Hindu culture, Lord Karthikeya, the god of war, is said to ride a peacock."
    )

SQUID_FACTS = (
    'Many species of squid have a life span that is only about one year',
    'The Humboldt squid is very aggressive and will even attack sharks in the water.',
    'The only predators that giant squid have are sperm whales.'
    )

OCTOPUS_FACTS = (
    'There are around 300 species of octopus, usually located in tropical and temperate ocean waters. They are divided into finned deep-sea varieties that live on the ocean floor and finless, shallow water varieties found around coral reefs.',
    'Octopuses have two eyes in a globe-shaped head (mantle) off which protrude eight long limbs called tentacles that have two rows of sucker senses.',
    'Octopuses can squeeze into tight spaces as they are invertebrates which means they have no skeleton, (some species have a protective casing in their mantles).',
    'An octopus has a hard beak, like a parrot beak, which they use to break into and eat their pray such as crabs and shellfish.',
    'Octopuses have three hearts.',
    'The largest octopus is believed to be the giant Pacific octopus, Enteroctopus dofleini which weigh about 15 kg (33 lb), and has an arm span up to 4.3 m (14 ft).',
    'Octopuses are believed to be highly intelligent compared to other invertebrates.',
    "An octopus's main defense against predators such as sharks is to hide and camouflage itself by using certain skin cells to change its color. This can also be used to talk with or warn other octopuses.",
    'Octopuses can eject a thick, blackish ink in a large cloud to distract a predator while the octopus uses a siphon jet propulsion system to quickly swim away headfirst, with arms trailing behind.',
    'A last ditch defense is for the octopus to shed a tentacle similar to how a gecko or lizard can discard a tale. An octopus is able to regenerate a lost tentacle.',
    'Octopuses have very good eyesight and an excellent sense of touch.',
    'A female octopus can lay on average about 200,000 eggs, however, fending for themselves only a handful of the hatchlings will survive to adulthood.',
    'Octopuses usually live for 6 - 18 months. Males only live a few months after mating, and females die of starvation shortly after their protected eggs hatch.',
    'Humans eat octopus in many cultures and it is also a popular fish bait.'
    )

OCELOT_FACTS = (
    'Ocelot is two times bigger than domestic cat. It can reach 28 to 35 inches in length and between 24 and 35 pounds of weight. Males are bigger than females. Length of a tail measures half of the body size.',
    'Ocelots have beautiful fur which is the reason why people hunt them. Color of the fur is usually tawny, yellow or brown-grayish, covered with black rosettes and stripes.',
    'Ocelot has pointed teeth that are used for biting and blade-like teeth that are used for tearing of the food. It does not have teeth for chewing so it swallows chunks of food.',
    'Ocelot has raspy tongue, which successfully removes every little piece of meat from bones.',
    'Ocelots are carnivores (meat-eaters). They eat rodents, monkeys, tortoises, armadillos, rabbits, birds, lizards, fish, snakes…',
    'Ocelot has excellent eyesight (adapted to night vision) and sense of hearing, which are used for detection of the prey.',
    'Ocelots are nocturnal animals. During the day, they rest in the hollow trees, on the branches or dense vegetation.',
    'Due to smaller size, ocelot is an easy prey of larger cats (such as jaguars and pumas), birds of prey (eagles) and large snakes (anaconda).',
    'Unlike other cat species, ocelots are not afraid of the water. They are excellent swimmers.',
    'Ocelots are territorial and solitary creatures. Males usually live on the territory of 30 square meters. Females occupy territory that is two times smaller.',
    'Ocelots are active 12 hours per day. During that time, ocelot may travel up to 7 miles while it searches for the food.',
    'Average lifespan of ocelot is 10 to 13 years in the wild and up to 20 years in captivity.'
    )

WHALE_FACTS = [
    'Many whales are toothless. They use a plate of comb-like fibre called baleen to filter small crustaceans and other creatures from the water.',
    'There are 79 to 84 different species of whale. They come in many different shapes and sizes!',
    'A baby whale is called a calf. Whales form groups to look after calves and feed together. These groups are often made up of all female or all male whales.',
    'Whales that are found in both Northern and Southern hemisphere never meet or breed together. Their migration is timed so that they are never in breeding areas at the same time.',
    'The arched lower lip of a whale can often make it look like it is smiling! However, this isn’t a “real” smile as the blubber in the head of the whale prevents the muscles of the face from reaching the surface.',
    'You can tell the age of a whale by looking at the wax plug in its ear. This plug in the ear has a pattern of layers when cut lengthwise that scientists can count to estimate the age of the whale.',
    'Whales love to sing! They use this as a call to mates, a way to communicate and also just for fun! After a period of time they get bored of the same whale song and begin to sing a different tune.',
    'Sometimes whales make navigation mistakes during migrations. Although they may have made the mistake days before, they don’t realise it until they becoming stranded.',
    'Whales support many different types of life. Several creatures, such as barnacles and sea lice, attach themselves to the skin of whales and live there.'
    ]

WOLF_FACTS = [
    'Wolves are excellent hunters and have been found to be living in more places in the world than any other land mammal except humans.',
    'The wolf is the ancestor of all breeds of domestic dog. It is part of a group of animals called the wild dogs which also includes the dingo and the coyote.',
    'Most wolves weigh about 40 kilograms but the heaviest wolf ever recorded weighed over 80 kilograms!',
    'Adult wolves have large feet. A fully grown wolf would have a paw print nearly 13 centimeters long and 10 centimeters wide.',
    'Wolves live and hunt in groups called a pack. A pack can range from two wolves to as many as 20 wolves depending on such factors as habitat and food supply. Most packs have one breeding pair of wolves, called the alpha pair, who lead the hunt.',
    'Wolf pups are born deaf and blind while weighing around 0.5 kg (1 lb). It takes about 8 months before they are old enough to actively join in wolf pack hunts.',
    'Wolves in the Arctic have to travel much longer distances than wolves in the forest to find food and will sometimes go for several days without eating.',
    'When hunting alone, the wolf catches small animals such as squirrels, hares, chipmunks, raccoons or rabbits. However, a pack of wolves can hunt very large animals like moose, caribou and yaks.',
    'When the pack kills an animal, the alpha pair always eats first. As food supply is often irregular for wolves, they will eat up to 1/5th of their own body weight at a time to make up for days of missed food.',
    'Wolves have two layers of fur, an undercoat and a top coat, which allow them to survive in temperatures as low at minus 40 degrees fahrenheit! In warmer weather they flatten their fur to keep cool.',
    'A wolf can run at a speed of 40 miles per hour during a chase. Wolves have long legs and spend most of their time trotting at a speed of 7-10 miles per hour. They can keep up a reasonable pace for hours and have been known to cover distances of 55 miles in one night.'
    ]

PIG_FACTS = [
    'Pigs are intelligent animals. Some people like to keep pigs as pets.',
    'A pig’s snout is an important tool for finding food in the ground and sensing the world around them.',
    'Pigs have an excellent sense of smell.',
    'There are around 2 billion pigs in the world.',
    'Humans farm pigs for meat such as pork, bacon and ham.',
    'Wild pigs (boar) are often hunted in the wild.',
    'In some areas of the world, wild boars are the main source of food for tigers.',
    'Feral pigs that have been introduced into new areas can be a threat to the local ecosystem.',
    'Pigs can pass on a variety of diseases to humans.',
    'Relative to their body size, pigs have small lungs.'
    ]

PIGEON_FACTS = (
    'The size of a of pigeon depends on the species. Large pigeons can reach 19 inches in length and 8.8 pounds of weight. Small pigeons can reach 5 inches in length and up to 0.8 ounces of weight.',
    'Pigeons can have dull or colorful plumage, depending on the habitat and type of diet. The most common type of pigeon (that lives in the cities) has grayish plumage. On average, a pigeon has 10,000 feathers on their body.',
    'Pigeons have strong muscles used for flying. They can fly at the altitude of 6000 feet.',
    'Pigeons can move their wings ten times per second and maintain heartbeats at the rate of 600 times per minute.',
    'Pigeons can fly at the speed of 50 to 60 miles per hour. Fastest known pigeon managed to reach speed on 92 miles per hour.',
    'Because of their incredible speed and endurance, pigeons are used for racing. Winners of 400 mile long races can earn million dollars.',
    "Pigeons were used as mail carriers during the First and Second World War. They saved numerous lives by delivering information under enemy fire.",
    'Pigeons are herbivores. Their diet consists of seeds, fruit and various plants.',
    'Pigeons are highly intelligent animals. They are able to recognize themselves in the mirror, to find same people on two different pictures and to recognize all letters of the English alphabet.'
    'Pigeons have exceptional eyesight and ability to identify objects at a distance of 26 miles.',
    'Pigeons have very sensitive sense of hearing. They are able to detect distant storms, earthquakes and volcanic eruptions.',
    'Pigeons are social animals that live in the groups (flocks) composed of 20 to 30 animals.',
    'Pigeons are monogamous creatures. Couples of pigeons can produce up to 8 broods per year when food is abundant.',
    'Female lays 2 eggs that hatch after incubation period of 18 days. Young birds depend on their parents during the first two months of their life. Both parents take care of the chicks (called squabs).',
    'Pigeons can survive more than 30 years in the wild.'
    )


PENGUIN_FACTS = [
    'While other birds have wings for flying, penguins have adapted flippers to help them swim in the water.',
    'Most penguins live in the Southern Hemisphere.',
    'The Galapagos Penguin is the only penguin specie that ventures north of the equator in the wild.',
    'Large penguin populations can be found in countries such as New Zealand, Australia, Chile, Argentina and South Africa.',
    'No penguins live at the North Pole.',
    'Penguins eat a range of fish and other sealife that they catch underwater.',
    'Penguins can drink sea water.',
    'Penguins spend around half their time in water and the other half on land.',
    'The Emperor Penguin is the tallest of all penguin species, reaching as tall as 120 cm (47 in) in height.',
    'Emperor Penguins can stay underwater for around 20 minutes at a time.',
    'Emperor Penguins often huddle together to keep warm in the cold temperatures of Antarctica.',
    'King Penguins are the second largest penguin specie. They have four layers of feathers to help keep them warm on the cold subantarctic islands where they breed.',
    'Chinstrap Penguins get their name from the thin black band under their head. At times it looks like they’re wearing a black helmet, which might be useful as they’re considered the most aggressive type of penguin.',
    'Crested penguins have yellow crests, as well as red bills and eyes.',
    'Yellow eyed penguins (or Hoiho) are endangered penguins native to New Zealand. Their population is believed to be around 4000.',
    'Little Blue Penguins are the smallest type of penguin, averaging around 33 cm (13 in) in height.',
    'Penguin’s black and white plumage serves as camouflage while swimming. The black plumage on their back is hard to see from above, while the white plumage on their front looks like the sun reflecting off the surface of the water when seen from below.',
    'Penguins in Antarctica have no land based predators.'
    ]

ZEBRA_FACTS = [
    'Zebra are part of the equidae family along with horse and donkeys.',
    'Every zebra has a unique pattern of black and white stripes.',
    'There are a number of different theories which attempt to explain zebra’s unique stripes with most relating to camouflage.',
    'Common plain zebras have tails around half a meter in length (18 inches).',
    'Zebra crossings (pedestrian crossings) are named after the black and white stripes of zebras.',
    'Zebras run from side to side to being chased by a predator.',
    'Zebras have excellent eyesight and hearing.',
    'Zebras stand up while sleeping.',
    'Zebras eat mostly grass.',
    'The ears of a zebra show its mood.',
    'A zebra named Marty starred in the 2005 animated film Madagascar.',
    ]

ALL_FACTS = (
    ALLIGATOR_FACTS,
    BADGER_FACTS,
    BEAVER_FACTS,
    CAMEL_FACTS,
    COW_FACTS,
    CHEETAH_FACTS,
    CRAB_FACTS,
    DOLPHIN_FACTS,
    EAGLE_FACTS,
    ECHIDNA_FACTS,
    EMU_FACTS,
    FLAMINGO_FACTS,
    FOX_FACTS,
    FROG_FACTS,
    ELEPHANT_FACTS,
    GIRAFFE_FACTS,
    GORILLA_FACTS,
    HAMSTER_FACTS,
    HEDGEHOG_FACTS,
    HIPPO_FACTS,
    HORSE_FACTS,
    HUMMINGBIRD_FACTS,
    JELLYFISH_FACTS,
    KANGAROO_FACTS,
    KOALA_FACTS,
    LION_FACTS,
    LEOPARD_FACTS,
    MONKEY_FACTS,
    NARWHAL_FACTS,
    OCTOPUS_FACTS,
    OTTER_FACTS,
    OWL_FACTS,
    OCELOT_FACTS,
    PANDA_FACTS,
    PANTHER_FACTS,
    PARROT_FACTS,
    PENGUIN_FACTS,
    PEACOCK_FACTS,
    PIG_FACTS,
    PIGEON_FACTS,
    SCORPION_FACTS,
    SEAGULL_FACTS,
    SHARK_FACTS,
    SLOTH_FACTS,
    SNAKE_FACTS,
    TIGER_FACTS,
    TURTLE_FACTS,
    WOLF_FACTS,
    WHALE_FACTS,
    ZEBRA_FACTS
    )

def main():
    reddit = authenticate()
    while True:
        print("Wait time after commenting will be " + str(wait_time) + " seconds.\n")
        animalfactsbot(reddit)

if __name__ == '__main__':
    main()
