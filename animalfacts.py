import re
import praw
import random
import time
import sys
import string
from pygame import mixer
# from '/' import lists

BLACKLIST = (
    'suicidewatch',
    'depression',
    'snakes',
    'mturk',
    'babyelephantgifs',
    'learnprogramming',
    'cscareerquestions',
    'python',
    'japan')

mixer.init()
alert = mixer.Sound('bird.wav')
bell = mixer.Sound('bell.wav')
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
    reddit = praw.Reddit('animal-facts-bot', user_agent='/u/AnimalFactsBot')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit


def check_messages(reddit):
    print("Checking my messages...\n")
    for comment in reddit.inbox.comment_replies(limit=number_of_messages):
        print("Checking comment ID " + comment.id, end='\r')
        if unsubscribed_author_check(comment):
            if not comment.subreddit.user_is_banned:
                file_obj_r = open(reply_history, 'r')
                if comment.id not in file_obj_r.read().splitlines():
                    comment_body = comment.body.lower()
                    if 'good bot' in comment_body:
                        comment.reply(
                            'Thanks! You can ask me for more facts any time. Beep boop.')
                        print('     Thanked someone for "good bot"\n')
                        record_already_replied(file_obj_r, comment)
                    elif 'bad bot' in comment_body or 'unsubscribe' in comment_body:
                        comment.reply(
                            comment.author.name +
                            " has been unsubscribed from AnimalFactsBot. I won't reply to your comments any more.")
                        print('     Unsubbed ' + comment.author.name + '\n')
                        unsubscribe(comment.author)
                        record_already_replied(file_obj_r, comment)
                    elif 'more' in comment_body:
                        comment.reply(
                            "It looks like you asked for more animal facts! " +
                            random_fact())
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
                        comment.reply(
                            "It sounds like you called me the 'best bot'. That's awesome!")
                        print('     Replied to a "best bot"\n')
                        record_already_replied(file_obj_r, comment)
                    elif re.search('(fuck)|(bitch)|(shit)', comment_body):
                        comment.reply(
                            "https://www.youtube.com/watch?v=hpigjnKl7nI")
                        print('     WATCH YO PROFANITY\n')
                        record_already_replied(file_obj_r, comment)
                    elif re.search('(\scats?\s)|(\sdogs?\s)', ' ' + comment_body + ' '):
                        comment.reply(
                            "Did you ask for cat or dog facts? I'm sorry, if I did cat or dog facts I'd be spamming every thread on reddit. Reply 'more' if you'd like a random animal fact.")
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
                        comment.reply(
                            "You said my name! Would you like to know more about me? I am written in Python. I am running from a computer in Seattle. I have given an animal fact to redditors " +
                            str(
                                number_of_facts_given()) +
                            " times!")
                        print('     Told someone about myself.\n')
                        record_already_replied(file_obj_r, comment)
                    else:
                        commented_obj_r = open(history, 'r')
                        if comment.id not in commented_obj_r.read().splitlines():
                            check_comment_for_animal(comment, reddit)
                        commented_obj_r.close()
                file_obj_r.close()


def number_of_facts_given():
    commented_obj_r = open(history, 'r')
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
    file_obj_w = open(reply_history, 'a+')
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
    fact_collection = random.choice(ALL_FACTS)
    return random.choice(fact_collection)


def botengine(animal, regex, reddit, facts, comment):
    text = ' '.join(word.strip(string.punctuation)
                    for word in comment.body.lower().split())
    text = ' ' + text + ' '
    match = re.findall(regex, text)
    if match:
        print(
            animal.upper() +
            " found in comment with comment ID: " +
            comment.id)
        if comment.subreddit.display_name.lower() not in BLACKLIST:
            if comment.subreddit.user_is_banned:
                print("     Not commenting because I am banned from " +
                      comment.subreddit.display_name + "\n")
            else:
                if not unsubscribed_author_check(comment):
                    print("     Not commenting because author is unsubscribed.")
                else:
                    file_obj_r = open(history, 'r')
                    if comment.id not in file_obj_r.read().splitlines():
                        if comment.author.name == reddit.user.me():
                            print('     Skipping my own comment...\n')
                        else:
                            print(
                                '     by ' +
                                comment.author.name +
                                ' in ' +
                                comment.subreddit.display_name +
                                '\n      commenting a fact...')
                            comment.reply(random.choice(facts))
                            alert.play()
                            file_obj_r.close()
                            file_obj_w = open(history, 'a+')
                            file_obj_w.write(comment.id + '\n')
                            file_obj_w.close()
                            time.sleep(wait_time)
                    else:
                        print('     Already commented on this!\n')

# ANIMALS = ('alligator', 'ant', 'beaver', 'badger', 'camel', 'cheetah', 'crab', 'dolphin', 'elephant', 'flamingo', 'frog', 'giraffe', 'gorilla', 'hedgehog','hippo', 'horse', 'jellyfish', 'koala', 'lion', 'lepoard', 'monkey', 'octopus', 'otter', 'owl', 'panda', 'parrot', 'penguin', 'pig', 'scorpion', 'shark', 'sloth', 'snake', 'tiger', 'turtle', 'wolf', 'whale', 'zebra')


def check_comment_for_animal(comment, reddit):
    botengine('albatross', '\salbatross(es)?\s', reddit, ALBATROSS_FACTS, comment)
    botengine('alligator', '\salligators?\s', reddit, ALLIGATOR_FACTS, comment)
    botengine('ant', '\sants?\s', reddit, ANT_FACTS, comment)
    botengine('badger', '\sbadgers?\s', reddit, BADGER_FACTS, comment)
    botengine('beaver', '\sbeavers?\s', reddit, BEAVER_FACTS, comment)
    botengine('camel', '\scamels?\s', reddit, CAMEL_FACTS, comment)
    botengine('chameleon', '\schameleons?\s', reddit, CHAMELEON_FACTS, comment)
    botengine('cheetah', '\scheetahs?\s', reddit, CHEETAH_FACTS, comment)
    botengine('cow', '\scows?\s', reddit, COW_FACTS, comment)
    botengine('crab', '\scrabs?\s', reddit, CRAB_FACTS, comment)
    botengine('crocodile', '\scrocodiles?\s', reddit, CROCODILE_FACTS, comment)
    botengine('cuttlefish', '\scuttlefish(es)?\s', reddit, CUTTLEFISH_FACTS, comment)
    botengine('dingo', '\sdingos?\s', reddit, DINGO_FACTS, comment)
    botengine('dolphin', '\sdolphins?\s', reddit, DOLPHIN_FACTS, comment)
    # botengine('dragon', '\sdragons?\s', reddit, DRAGON_FACTS, comment)   Disabled because this was only a temp feature during Game of Thrones season. Dragons aren't real.
    botengine('eagle', '\seagles?\s', reddit, EAGLE_FACTS, comment)
    botengine('echidna', '\sechidnas?\s', reddit, ECHIDNA_FACTS, comment)
    botengine('elephant', '\selephants?\s', reddit, ELEPHANT_FACTS, comment)
    botengine('emu', '\semus?\s', reddit, EMU_FACTS, comment)
    botengine('falcon', '\sfalcons?\s', reddit, FALCON_FACTS, comment)
    botengine('flamingo', '\sflamingos?\s', reddit, FLAMINGO_FACTS, comment)
    botengine('fox', '\sfox(es)?\s', reddit, FOX_FACTS, comment)
    botengine('frog', '\sfrogs?\s', reddit, FROG_FACTS, comment)
    botengine('giraffe', '\sgiraffes?\s', reddit, GIRAFFE_FACTS, comment)
    botengine('grasshopper', '\sgrasshoppers?\s', reddit, GRASSHOPPER_FACTS,comment)
    botengine('goat', '\sgoats?\s', reddit, GOAT_FACTS, comment)
    botengine('goose', '\s(goose|geese)\s', reddit, GOOSE_FACTS, comment)
    botengine('gopher', '\sgophers?\s', reddit, GOPHER_FACTS, comment)
    botengine('gorilla', '\sgorillas?\s', reddit, GORILLA_FACTS, comment)
    botengine('hamster', '\shamsters?\s', reddit, HAMSTER_FACTS, comment)
    botengine('hedgehog', '\shedgehogs?\s', reddit, HEDGEHOG_FACTS, comment)
    botengine('hippo', '\shippos?\s', reddit, HIPPO_FACTS, comment)
    botengine('honeybee', '\shoney bees?\s', reddit, HONEYBEE_FACTS, comment)
    botengine('horse', '\shorses?\s', reddit, HORSE_FACTS, comment)
    botengine('hummingbird', '\shummingbirds?\s', reddit, HUMMINGBIRD_FACTS, comment)
    botengine('husky', '\shusk(y|ies)\s', reddit, HUSKY_FACTS, comment)
    botengine('jellyfish', '\sjellyfish(es)\s', reddit, JELLYFISH_FACTS, comment)
    botengine('kangaroo', '\skangaroos?\s', reddit, KANGAROO_FACTS, comment)
    botengine('koala', '\skoalas?\s', reddit, KOALA_FACTS, comment)
    botengine('lion', '\slions?\s', reddit, LION_FACTS, comment)
    botengine('leopard', '\sleopards?\s', reddit, LEOPARD_FACTS, comment)
    botengine('lizard', '\slizards?\s', reddit, LIZARD_FACTS, comment)
    botengine('llama', '\sllamas?\s', reddit, LLAMA_FACTS, comment)
    botengine('meerkat', '\smeerkats?\s', reddit, MEERKAT_FACTS, comment)
    botengine('monkey', '\smonkeys?\s', reddit, MONKEY_FACTS, comment)
    botengine('narwhal', '\snarwhals?\s', reddit, NARWHAL_FACTS, comment)
    botengine('newt', '\snewts?\s', reddit, NEWT_FACTS, comment)
    botengine('ocelot', '\socelots?\s', reddit, OCELOT_FACTS, comment)
    botengine('oryx', '\soryx(es)?\s', reddit, ORYX_FACTS, comment)
    botengine('octopus', '\socto(pus|puses|pusses|pi)\s', reddit, OCTOPUS_FACTS, comment)
    botengine('orca', '\sorcas?\s', reddit, ORCA_FACTS, comment)
    botengine('otter', '\sotters?\s', reddit, OTTER_FACTS, comment)
    botengine('owl', '\sowls?\s', reddit, OWL_FACTS, comment)
    botengine('parrot', '\sparrots?\s', reddit, PARROT_FACTS, comment)
    botengine('panda', '\spandas?\s', reddit, PANDA_FACTS, comment)
    botengine('pangolin', '\spangolins?\s', reddit, PANGOLIN_FACTS, comment)
    botengine('panther', '\spanthers?\s', reddit, PANTHER_FACTS, comment)
    botengine('peacock', '\speacocks?\s', reddit, PEACOCK_FACTS, comment)
    botengine('penguin', '\spenguins?\s', reddit, PENGUIN_FACTS, comment)
    botengine('pig', '\spigs?\s', reddit, PIG_FACTS, comment)
    botengine('pigeon', '\spigeons?\s', reddit, PIGEON_FACTS, comment)
    botengine('platypus', '\splatypuse?s?\s', reddit, PLATYPUS_FACTS, comment)
    botengine('rabbit', '\srabbits?\s', reddit, RABBIT_FACTS, comment)
    botengine('scorpion', '\sscorpions?\s', reddit, SCORPION_FACTS, comment)
    botengine('seagull', '\sseagulls?\s', reddit, SEAGULL_FACTS, comment)
    botengine('sea cucumber', '\ssea cucumbers?\s', reddit, SEA_CUCUMBER_FACTS, comment)
    botengine('shark', '\ssharks?\s', reddit, SHARK_FACTS, comment)
    botengine('sheep', '\ssheep?\s', reddit, SHARK_FACTS, comment)
    botengine('skunk', '\sskunks?\s', reddit, SKUNK_FACTS, comment)
    botengine('sloth', '\ssloths?\s', reddit, SLOTH_FACTS, comment)
    botengine('snail', '\ssnails?\s', reddit, SNAIL_FACTS, comment)
    botengine('snake', '\ssnakes?\s', reddit, SNAKE_FACTS, comment)
    botengine('tarantula', '\starantulas?\s', reddit, TARANTULA_FACTS, comment)
    botengine('squirrel', '\ssquirrels?\s', reddit, SQUIRREL_FACTS, comment)
    botengine('stingray', '\sstingrays?\s', reddit, STINGRAY_FACTS, comment)
    botengine('tiger', '\stigers?\s', reddit, TIGER_FACTS, comment)
    botengine('turtle', '\sturtles?\s', reddit, TURTLE_FACTS, comment)
    botengine('wallaby', '\swallab(y|ies)\s', reddit, WALLABY_FACTS, comment)
    botengine('walrus', '\swalrus\s', reddit, WALRUS_FACTS, comment)
    botengine('whale', '\swhales?\s', reddit, WHALE_FACTS, comment)
    botengine('wolf', '\swol(f|ves)\s', reddit, WOLF_FACTS, comment)
    botengine('zebra', '\szebras?\s', reddit, ZEBRA_FACTS, comment)


def animalfactsbot(reddit):
    check_messages(reddit)
    print("Pulling 1000 comments...")
    comment_list = reddit.subreddit('all').comments(limit=1000)
    print("     checking each comment for " +
          str(len(ALL_FACTS)) + " different animals\n")
    for comment in comment_list:
        check_comment_for_animal(comment, reddit)


ALBATROSS_FACTS = (
    'Albatrosses are known to live until their fifties sixties.',
    'The Wandering albatross has a wingspan that measures up to 11 feet 4 inches from end to end, the largest of any living bird.',
    'When albatrosses find a mate they will pair for life, a union that will often last for 50 years.',
    'The top albatros predator is the tiger shark, that will prey on young chicks shortly after nesting season',
    'Simply using thermal currents, albatrosses can glide for several hundred miles without flapping.',
    'Albatrosses can smell out prey from over 12 miles away.',
    'Of the 22 regognised species of albatrosses, all are listed as at some level of concern; 3 species are Critically Endangered, 5 species are Endangered, 7 species are Near Threatened, and 7 species are Vulnerable.',
    'The scientific name for the albatross is Diomedeidae.',
    'Albatrosses perform dances to attract a mate, these are then repeated each time they meet.',
    'The body of an albatross is covered with white, black, brown, red or yellow feathers. They were used for decoration of hats in the past.',
    'Albatrosses can reach the speed of 40 miles per hour.')

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
    'Like crocodiles, alligators are part of the order ‘Crocodylia’.')

ANT_FACTS = (
	'There are more than 12,000 species of ants all over the world.',
	'An ant can lift 20 times its own body weight. If a second grader was as strong as an ant, she would be able to pick up a car!',
	'Some queen ants can live for many years and have millions of babies!',
	'Ants don’t have ears. Ants "hear" by feeling vibrations in the ground through their feet.',
	'Ants are the longest living of all insects, living for up to 30 years.',
	'When ants fight, it is usually to the death!',
	'When foraging, ants leave a pheromone trail so that they know where they’ve been.',
	'One ant species (Trap-Jaw Ants) owns the record for the fastest movement within the animal kingdom.',
	'The largest ant colony ever found was over 6000 Km or 3750 miles wide.',
	'All worker, soldier and queen ants are female.',
	'Some ant species are asexual, they clone themselves and do not require any males.',
	'Ants and humans are the only creatures that farm other creatures.',
	'Some ants can swim.',
	'Ants can be found on every continent accept antarctica.'
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
    'Beavers like to keep themselves busy, they are prolific builders during the night. Hence the saying "As busy as a beaver".')

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
    'There are estimated to be over 14 million camels in the world. Camels introduced to desert areas of Australia are the worlds largest populations of feral camels.')

CHAMELEON_FACTS = (
    'Chameleons are a very unique branch of the lizard group of reptiles.',
    'There are around 160 species of chameleon.',
    'Chameleons live in warm varied habitats from rainforests through to deserts.',
    'Almost half of the world’s chameleon species are native to Madagascar.',
    'Special color pigment cells under the skin called chromatophores allow some chameleon species to change their skin color, creating combined patterns of pink, blue, red, orange, green, black, brown, yellow and purple.',
    'Chameleon change color for camouflage but this is not always the main reason. Some show darker colors when angry, or when trying to scare others',
    'Male chameleons show light multi-colored patterns when vying for female attention.',
    'Chameleons living in the desert change to black when its cooler to absorb heat, then to a light grey to reflect heat.',
    'Chameleons have amazing eyes. The bulging upper and lower eyelids are joined and the pupil peaks out from a pinhole sized gap.',
    'The chameleons’ eyes can rotate and focus separately on 180-degree arcs, so they can see two different objects at the same time. This gives them a full 360-degree field of vision.',
    'Chameleons feed by ballistically projecting their tongues often over twice the length of their body to catch prey, forming a suction cup as it hits its target.',
    'Chameleons are not deaf but they do not actually have ear openings.',
    'Chameleons eat insects and birds.',
    'Chameleons are different from many reptiles because some of the species, like the Jackson’s chameleon, have live births. These species can give birth to eight to 30 young at one time',
    'According to International Union for Conservation of Nature’s Red List of Threatened Species, many species of chameleon are endangered.'
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
    'Cheetahs only need to drink once every three to four days.')

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
    'A dairy cow can produce 125 lbs. of saliva a day')

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
    'The most consumed species of crab in the world is the Japanese Blue Crab.')

CROCODILE_FACTS = (
    'There are 23 different species of crocodiles that live on this planet.',
    'Crocodiles do not chew their food! Instead, they swallow stones to grind their food inside their stomachs.',
    'Crocodiles with open motuhs is not necessarily a sign of aggression. Instead, that is their only way cooling off.',
    'Crocodiles do not possess any sweat glands.',
    "The muscles responsible for opening a crocodile's jaws are weak, such that even humans can keep a crocdile's mouth closed.",
    'However, opening their mouth when it is closed is almost impossible',
    'After mating, a female crocodile can lay between 20 to 80 eggs.',
    'Crocodiles can have a lifespan of up to 80 years.',
    'The skin on the back of the crocodile is so hard and tough, not even a bullet can pierce it.',
    'The closest relatives of the crocodile in the animal kingdom are rather disparate: Birds and Dinosaurs.',
    'Crocodiles normally drown their prey by dragging them underwater before cutting their meat into smaller chunks.',
    'Crocodiles can shoot out from the water at almost 12 meters per second!'
    )

CUTTLEFISH_FACTS = (
    "Cuttlefish are cephalopods, not fish. Cephalopods include octopus, squid and nautilus.",
    "Cuttlefish, along with most cephalopods, are the ocean’s most intelligent invertebrates.",
    "Cuttlebone, found in the body of a cuttlefish, is used by pet birds to get calcium.",
    "Cuttlefish have green-blue blood and 3 hearts!",
    "A cuttlefish’s camouflage is so good that it can take on a checkerboard pattern placed beneath it.",
    "Cuttlefish are color blind.",
    'Cuttlefish taste with their suckers.',
    "Cuttlefish have 8 arms and 2 long tentacles used for feeding.",
    "The largest cuttlefish is the Australian giant cuttlefish, which is the size and shape of an American football.",
    "Cuttlefish have W shaped eyelids so they can see in front of them and behind them at the same time.")

DINGO_FACTS = (
    'Dingoes actually originate from Southeast Asia, where they can still be found today.',
    'Dingoes mate once per year, from March to June.',
    'Dingoes cannot bark, but they can howl.',
    'Dingoes have permanently erect ears.',
    'Dingoes arrived in Australia from the Asian mainland about 5,000 years ago.',
    'Dingoes live to five or six years of age in the wild and fifteen years in captivity.')
	
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
    'Some fishing methods, such as the use of nets, kill a large number of dolphins every year.')

DRAGON_FACTS = (
    'The word “dragon” comes from the Greek word “draconta,” which means “to watch.” The Greeks saw dragons as beasts that guarded valuable items. In fact, many cultures depict dragons as hoarding treasure.',
    'Ancient Greeks and Sumerians spoke of giant “flying serpents” in their scrolls and lectures. Dragons are depicted as snake- or reptile-like.',
    'The Komodo dragon is a type of monitor lizard, which is aggressive and deadly. They can be 10 feet long and use toxic bacteria in their mouths to wound their prey.',
    'In medieval times, dragons were considered very real, but demonic. Religions had widely different views of dragons: some loved them and some feared them.',
    'In many cultural stories, dragons exhibit features of other animals, like the head of elephants, claws of lions and beaks of predatory birds. Their body colors are widely different – red, blue, green, gold, but usually earth tones. In some cultures, the colors have specific meanings.',
    '“Dragon” is actually a family term that includes other mythological creatures, such as cockatrices, gargoyles, wyverns, phoenix, basilisks, hydras, and even some hybrid man-dragon creatures.')

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
    "The echidna has a very large brain for its body size. Part of this might be due to their enlarged neocortex, which makes up half of the echidna's brain (compare this to about 30 percent in most other mammals and 80 percent in humans).")

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
    'Elephants are herbivores and can spend up to 16 hours days collecting leaves, twigs, bamboo and roots.')

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

FALCON_FACTS = (
    'Peregrine falcons have been clocked at reaching speeds of 242 miles per hour while diving for prey, making them the fastest recorded animal ever.',
    'Falcon is a carnivore. Its diet is based on rodents, frogs, fish, bats and small birds.',
    'Falcons have a lifespan between 12 and 20 years in the wild, depending on species. Some species can live up to 25 years in captivity.',
    'The gyrfalcon (Falco rusticolus) is the largest falcon species. It is up to 61 centimeters (24 inches) long withwingspan up to 130 centimeters (51 inches) and weight up to 1,350 grams (47.6 ounces).',
    'The Seychelles kestrel (Falco araea) is the smallest falcon species. It is 18–23 centimeters 7-9 inches long with a wingspan of 40–45 centimeters (16-18 inches) and weight 73-87 grams (2.5-3 unces).',
    'Falcons have excellent eyesight which they use to locate their prey. They can see up to 8 times more clearly than the sharpest human eye.',
    'Most species of falcon are dark brown or grey-colored with white, yellow and black spots and markings on the body.',
    'Falcons are strong, fast fliers with great aerial agility, which makes them successful hunters capable of taking prey 6 times their own body weight! Usually they kill cleanly, breaking the back of their victims.',
    'The falcon is a bird of prey that, typically sitting close to the top of the food chain, has few predators. Falcons may be killed by other large birds of prey, such as eagles and owls. The eggs and chicks are vulnerable to mammals that may climb into the nest if it is too low to the ground.',
    'Falcons can process four types of light while humans can only process three. This means that the falcon has a very good night vision and can also see ultraviolet rays.'
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
    'The flamingo is the national bird of the Bahamas.')

FOX_FACTS = (
    'A group of foxes is called a "skulk" or "leash".',
    'Grey foxes can retract their claws like cats do',
    'A male is called a ‘dog fox’ while a female is called a ‘vixen’',
    'Foxes are generally solitary animals; unlike wolves, they hunt on their own rather than in packs',
    "Foxes' pupils are vertical, similar to a cat, helping them to see well at night",
    "The tip of a red fox’s tail is white, whereas swift foxes have a black-tipped tail",
    "Foxes have excellent hearing. Red foxes can reportedly hear a watch ticking 40 yards away!",
    'Foxes stink, their funny ‘musky’ smell comes from scent glands at the base of their tail')

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

GOAT_FACTS = (
    'Goats do not have teeth on their upper jaw',
    'Goats have the uncanny ability to yell like humans. Their calls are known as bleating.',
    'A baby goat is a kid and giving birth is called kidding.',
    'According to Norse mythology, during a thunderstorm Thor, the god of thunder, rode in a chariot pulled by two goats, Tanngrisni and Tanngnost.',
    'Goat population is roughly 600 million maintained worldwide (not including feral populations).',
    'Goats are fussy eaters that take a lot of time to search out the best snacks. Goats will often stand on their hind legs to reach the best part of foliage that may be out of reach of sheep.',
    'Goat Milk is alkaline and cow milk is acid. Goat milk is lower in cholesterol and higher in calcium, phosphorus and vitamins A.',
    'The largest number of goats in the United States resides in Texas. Goats can be raised, however, anywhere in the United States.',
    'Goats are members of the Bovidae family, which also includes antelopes, cattle and sheep.',
    'There are two types of goats: domestic goats (Capra hircus), which are raised and bred as farm animals; and mountain goats (Oreamnos americanus), which live in steep, rocky areas in the American Northwest.',
    'There are about 200 breeds of domestic goat, according to the Smithsonian Institution.',
    'Mountain goats are found in the Rocky Mountains, typically in Alaska, western Montana, central Idaho, South Dakota, Colorado and Washington. The wide spread of their cloven hooves allows them to climb steep mountain sides with ease.',
    'Goats and sheep are different species, and there are several physical and behavioral differences.',
    'Mountain goats have bright white coats that help them blend into the snowy areas of their home ranges. Domestic goats have coats that are yellow, chocolate or black.',
    'Goats were one of the first domesticated animals and were first domesticated around 9,000 years ago, according to the Smithsonian.',
    'In bright light, the pupil in a goat\'s eye is rectangular rather than round.',
    'Goat meat — called chevon or cabrito — is eaten all over the world.',
    'More people consume goat milk than the milk from any other animal.',
    'The phrase "Judas goat" is a term that has been used to describe a goat that is trained to herd other animals to slaughter while its own life is spared.')

GOOSE_FACTS = (
    'Some geese migrate every year. Others stay in the same place year round.',
    'Geese eat seeds, nuts, grass, plants and berries. They love blueberries.',
    'Geese can live almost anywhere. They like fields, parks and grassy areas near water.',
    'Geese fly in a “V” formation. If one goose is injured, other geese will stay with it until it dies or can rejoin the flock.',
    'Geese are sometimes raised like chickens for their meat or eggs.',
    'Male geese protect the nest while the female geese sit on the eggs.',
    'Goose is actually the term for female geese, male geese are called ganders. A group of geese on land or in water are a gaggle, while in the air they are called a skein.',
    ' European geese descend from wild greylag geese, birds with short necks and round bodies. Asian geese, the breeds now known as African and Chinese, descend from the swan goose and have long, elegant necks and a distinct knob on their beaks.',
    'Geese can live up to twenty years if well cared for.',
    'A baby goose is called a gosling.',
    'A group of geese is called a gaggle')


GOPHER_FACTS = (
    'Pocket gophers, commonly referred to as gophers, are burrowing rodents of the family Geomyidae.',
    'The gopher has large cheek pouches lined with fur which it uses to carry food and nesting material.',
    'About 35 species of gophers live in Central and North America.',
    'Gophers are commonly known for their extensive tunneling activities.',
    'Gophers weigh around 0.5 lb (230 g), and are about 6–8 in (150–200 mm) in body length, with a tail 1–2 in (25–51 mm) long.',
    'A gophers daily intake of food is equal to 60% of its body weight.',
    'Mating season of gophers takes place during the spring.',
    'Gopher can survive 2 to 3 years (rarely up to 5) in the wild.',
    'Natural enemies of gophers are owls, hawks, coyotes, weasels and snakes.',
    'The gopher is an iconic mascot and one of the most distinctive features of the Go programming language.')

GRASSHOPPER_FACTS = (
    'Grasshoppers have typanal organs on their bellies, but no ears.',
    'Grasshoppers make music by stridulating or crepitating.',
    'Grasshoppers cause billions of dollars of damage to crops annually.',
    'Grasshoppers existed as early as 300 million years ago.',
    'Grasshoppers can jump twenty times the length of their bodies.',
    'Grasshoppers go through three stages of development: egg, nymph, and adult.',
    'In Africa, Central America, and South America, grasshoppers are eaten as a source of protein.',
    'Grasshoppers can grow up to five inches. Females are usually bigger than males.',
    'There are 11,000 known species of grasshoppers.',
    'A single grasshopper can eat half its bodyweight in a day.',)


GORILLA_FACTS = (
    'There are only about 700 mountain gorillas and they live high in the mountains in two protected parks in Africa. Lowland gorillas live in central Africa.',
    'You may have seen baby gorillas being carried on the back of their mothers, but for the first few months after birth the mother holds the baby gorilla to her chest.',
    'An adult male gorilla is called a silverback because of the distinctive silvery fur growing on their back and hips. Each gorilla family has a silverback as leader who scares away other animals by standing on their back legs and beating their chest!',
    'Young male gorillas usually leave their family group when they are about 11 years old and have their own family group by the age of 15 years old. Young female gorillas join a new group at about 8 years old.',
    'Gorillas are herbivores. They spend most of their day foraging for food and eating bamboo, leafy plants and sometimes small insects. Adult gorillas can eat up to 30 kilograms of food each day.'
    'An adult gorilla is about 1 meter tall to their shoulders when walking on all fours using their arms and their legs.',
    'A gorilla can live for 40 – 50 years.',
    'Gorillas are considered to be very intelligent animals. They are known for their use of tools and their varied communication. Some gorillas in captivity at a zoo have been taught to use sign language.',
    'Gorillas are endangered animals. Their habitat is destroyed when people use the land for farming and the trees for fuel. Gorillas are also killed by poachers and sometimes get caught in poacher’s snares meant for other animals.')

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
    'Hedgehogs have about 5,000 to 6,500 spines at any one time, each which last about a year',
    'Its illegal to sell hedgehogs in Georgia, USA'
    'Most hedgehog species will roll into a tight ball if threatened, making it hard for its attacker to get past the spiky defences.',
    'A baby hedgehog is called a hoglet.',
    'Hedgehogs communicate through a combination of snuffles, grunts and squeals.',
    'Hedgehogs have weak eyesight but a strong sense of hearing and smell. They can swim, climb and run surprising quickly over short distances.',
    'For their size hedgehogs have a relatively long lifespan. They live on average for 4-7 years in the wild and longer in captivity.',
    'Hedgehogs in colder climates, such as the UK, will hibernate through winter.',
    'If hedgehogs come in contact with humans they can sometimes pass on infections and diseases.',
    'The hedgehog is a pest in countries such as New Zealand where it has been introduced, as it does not have many natural predators and eats native species of insects, snails, lizards and baby ground-nesting birds.')

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

HONEYBEE_FACTS = (
    'The honey bee has been around for millions of years.',
    'Honey bees, scientifically also known as Apis mellifera, which mean "honey-carrying bee", are environmentally friendly and are vital as pollinators.',
    'Honey bee is the only insect that produces food eaten by man.',
    'Honey is the only food that includes all the substances necessary to sustain life, including enzymes, vitamins, minerals, and water; and it\'s the only food that contains "pinocembrin", an antioxidant associated with improved brain functioning.',
    'Honey bees have 6 legs, 2 compound eyes made up of thousands of tiny lenses (one on each side of the head), 3 simple eyes on the top of the head, 2 pairs of wings, a nectar pouch, and a stomach.',
    'Honey bees have 170 odorant receptors, compared with only 62 in fruit flies and 79 in mosquitoes. Their exceptional olfactory abilities include kin recognition signals, social communication within the hive, and odor recognition for finding food. Their sense of smell is so precise that it could differentiate hundreds of different floral varieties and tell whether a flower carried pollen or nectar from meters away.',
    'The honey bee\'s wings stroke incredibly fast, about 200 beats per second, thus making their famous, distinctive buzz. A honey bee can fly for up to six miles, and as fast as 15 miles per hour.',
    'The average worker bee produces only about 1/12th teaspoon of honey in her lifetime. Doesn\'t this fact make you love every drop of honey? Read and you will understand why it makes so much sense to say: "as busy as a bee".',
    'A hive of bees will fly 90,000 miles, the equivalent of three orbits around the earth to collect 1 kg of honey.',
    'It takes one ounce of honey to fuel a bee\'s flight around the world (National Honey Board).',
    'A honey bee visits 50 to 100 flowers during a collection trip.',
    'The bee\'s brain is oval in shape and only about the size of a sesame seed (iflscience.com), yet it has remarkable capacity to learn and remember things and is able to make complex calculations on distance travelled and foraging efficiency.',
    'A colony of bees consists of 20,000-60,000 honeybees and one queen. Worker honey bees are female, live for about 6 weeks and do all the work.',
    'Each honey bee colony has a unique odour for members\' identification.'    )

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
    'A group of horses will not go to sleep at the same time - at least one of them will stay awake to look out for the others.')

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
    'Before migrating, the hummingbird will store up a layer of fat equal to half its body weight in order to slowly use up this energy source while flying.')

HUSKY_FACTS = (
    'Huskies have a double-layer coat that can keep them warm in temperatures as low as -60 degrees Fahrenheit.',
    'A husky\'s howl can be heard up to ten miles away.',
    'Huskies were brought to the US from Siberia during the Nome Gold Rush in 1909.',
    'Huskies\' coats come in six different shades.',
    'Heterochromia, a condition in which each eye is a different color, is common in huskies.',
    'Huskies were bred by the Chukchi Eskimos of northeastern Siberia.',
    'The color of a husky\'s nose depends on the color of its coat.',
    'Huskies have hair between their toes to keep their feet warm.',
    'When diptheria broke out in Nome, Alaska in 1925, a sled dog team led by the husky, Balto, transported medicine to the town before the epidemic could spread any further. The dogs made the trip during a blizzard, braving strong winds and temperatures as low as -23 degrees Fahrenheit.',
    'They\'re good dogs, Brent.')

JELLYFISH_FACTS = (
    'Jellyfish live in the sea and are found in all oceans.',
    'Some jellyfish live in fresh water.',
    'Jellyfish can be large and brightly colored. They can often be transparent or translucent.',
    'Some jellyfish can be very hard to see, nearly invisible to the human eye. Box jellyfish are almost transparent.',
    'Although the word is mentioned in their name, jellyfish are not fish.',
    'A group of jellyfish is called a ‘bloom’, ‘swarm’ or ‘smack’. Large blooms can feature over 100,000 jellyfish.',
    'Jellyfish don’t have brains.',
    'Jellyfish use their tentacles to sting. Most are harmless to humans but stings from some species, such as the box jellyfish, can be very painful and sometimes kill.',
    'Jellyfish eat plankton. Some sea turtles eat jellyfish.')

KANGAROO_FACTS = (
    'Kangaroos are marsupial animals that are found in Australia as well as New Guinea.',
    'There are four different kangaroo species, the red kangaroo, eastern grey kangaroo, western grey kangaroo and antilopine kangaroo.',
    'Kangaroos can hop around quickly on two legs or walk around slowly on all four.',
    'Kangaroos can’t walk backwards.',
    'Kangaroos can jump very high, sometimes three times their own height.',
    'Kangaroos can swim.',
    'Baby kangaroos are known as ‘joeys’. A group of kangaroos is called a ‘mob’, ‘troop’ or ‘court’.',
    'The red kangaroo is the largest marsupial in the world.',
    'Kangaroos usually live to around six years old in the wild.')

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
    'Komodo dragons are carnivores and can be very aggressive.')

MEERKAT_FACTS = (
    'Meerkats can spot an eagle in flight more than a thousand feet away.',
    'Meerkats, or suricates, are a type of mongoose that live in the southern African plains.',
    'When foraging for food, a few meerkats will stand guard while the rest look for insects, lizards, birds, and fruit.',
    'Female meerkats give birth to two to four young each year. They are cared for by fathers and siblings who teach them to play and forage.',
    'Meerkat mobs sleep in a single furry pile inside a burrow. Each burrow is an extensive tunnel-and-room system that stays cool under the African sun.',
    'Meerkats have strictly defined roles in their societies including sentry, babysitter, hunter, and teacher.',
    'Meerkat coats can be gold, silver, orange, or brown. Their tails are 7.5 to 9.5 inches (19 to 24 cm) long.',
    'Meerkat burrows can be up to 6.5 feet (2 meters) deep and can have as many as 15 entrances. Mobs of meerkats live in more than one burrow at a time.',
    'Meerkats start their mornings by grooming and lying in the sun.',
    'Meerkats can eat scorpions. Adult meerkats have some immunity to scorpion venom. Mothers will cut off the the tail of a scorpion before feeding it to their young.',
    'Baby meerkats, called pups, are born under ground. They weigh 25 to 36 grams (0.9 to 1.3 ounces) and are blind, deaf, and almost hairless.',
    'A membrane covers and protects a meerkat\'s eyes while they dig. They can also close their ears to keep them free of soil.',
    'Meerkats live in groups of up to 40. These groups are called gangs or mobs.',
    'Meerkats are vicious fighters that often kill each other in skirmishes. Both sides line up across a field before charging forward with leaps and bounds. Before attacking, they try to psych out their opponents with aggressive posturing and bluffing to avoid serious conflict if possible.')

LLAMA_FACTS = (
    'Llamas are members of the camelid, or camel, family.',
    'Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago by Indians in the Peruvian highlands.',
    'Llamas can grow as much as 6 feet tall.',
    'Llamas weigh 280 to 450 pounds and can carry about a quarter of their body weight, so a 400-pound male llama can carry about 100 pounds on a trek of 10 to 12 miles with no problem.',
    'In the Andes Mountains of Peru, llama fleece has been shorn and used in textiles for about 6,000 years. Llama wool is light, warm and water-repellent.',
    'Llamas are hardy and well suited to harsh environments.',
    'Llamas are smart and easy to train.',
    'Llamas are vegetarians and have efficient digestive systems.',
    'Llama poop has almost no odor. Llama farmers refer to llama manure as "llama beans." It makes great, eco-friendly fertilizer. The Incas in Peru burned dried llama poop for fuel.',
    'Llamas live to be about 20 years old.',
    'A baby llama is called a "cria." It\'s pronounced KREE-uh. Mama llamas usually only have one baby at a time. Llama twins are incredibly rare. Pregnancy lasts for about 350 days—nearly a full year. Crias weigh 20 to 35 pounds at birth.',
    'Llamas come in a range of solid and spotted colors including black, gray, beige, brown, red and white.',
    'Llamas are social animals and prefer to live with other llamas or herd animals.',
    'A group of llamas is called a herd.',
    'Llamas don\'t bite. They spit when they\'re agitated, but that\'s mostly at each other.',
    'Yarn made from llama fiber is soft and lightweight, yet remarkably warm.'
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
    'The monkey is the 9th animal that appears on the Chinese zodiac, appearing as the zodiac sign in 2016.')

NARWHAL_FACTS = (
    'Unlike some whale species that migrate, narwhals spend their lives in the Arctic waters of Canada, Greenland, Norway and Russia. Most narwhals winter for up to five months under sea ice in the Baffin Bay-Davis Strait area.',
    'Narwhals feed on Greenland halibut, Arctic and polar cod, squid and shrimp. They do their chomping at the ice floe edge and in the ice-free summer waters.',
    'Narwhals can dive a mile-and-a-half deep in the ocean. Cracks in the sea ice above allow them to pop up for air when they need it.',
    'Narwhals change color as they age. Newborns are a blue-gray, juveniles are blue-black and adults are a mottled gray. Old narwhals are nearly all white.',
    'There are no narwhals in captivity. In the 60s and 70s, several attempts at capturing and keeping narwhals resulted in all of the animals dying within several months.',
    'The narwhal tusk—most commonly found on males—is actually an enlarged tooth with sensory capability and up to 10 million nerve endings inside. Some narwhals have up to two tusks, while others have none. The spiraled tusk juts from the head and can grow as long at 10 feet.'
    "A narwhal tusk's tough core and soft outer layer result in a tusk that is both strong and flexible. It can bend significantly without cracking.")

NEWT_FACTS = (
    'Newts are a type of salamander.',
    'There are more than 100 known species of newts found in North America, Europe, North Africa, and Asia.',
    'Unlike other members of the salamander family, Newts are semi-aquatic, spending part of their lives on land and part in the water.',
    'During their terrestrial juvenile phase, newts are called "efts" (after the Old English name for newts).',
    'At least once species of newt has gone extinct: the Yunnan lake newt.',
    'The Old English name for the newt was "efte," which later became "euft" or "ewt(e)." The term "newt" came from merging in the article "an" (i.e. "an ewte" --> "a newt").',
    'Newts can regenerate their limbs, eyes, spinal cords, hearts, intestines, and upper and lower jaws.',
    'Newts are born as tadpoles, then undergo metamorphosis where they develop legs and their gills are absorbed and replaced by lungs.',
    'Many newts produce toxins, and some produce enough to kill a human, but the toxins are only dangerous if ingested.',
    'Newts are also known as Tritones in historical literature, after the mythological figure Triton.',
    'Alhough newts have air-breathing lungs, they also absorb oxygen and other substances through their water-permeable skin.',
    'The newt\'s thin, sensitive, water-permeable skin make it an excellent bioindicator (i.e. indicator of the health of an ecosystem or environment).',
    'One of the characteristis distinguishing newts from other salamanders is its relatively rougher skin.',
    'Several species of newt are considered threatened or endangered, including the Edough ribbed newt, Kaiser\'s spotted net, and the Montseny brook newt.',
    'In the UK, it is illegal to catch, possess, or handle great crested newts without a license.'
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
    'Average lifespan of ocelot is 10 to 13 years in the wild and up to 20 years in captivity.')

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
    'Humans eat octopus in many cultures and it is also a popular fish bait.')

ORYX_FACTS = (
    'Oryxes are species of antelope native to Africa and the Arabian Peninsula.',
    'The Arabian oryx was only saved from extinction through a captive breeding program and reintroduction to the wild.',
    'Small populations of several oryx speciies, such as the scimitar oryx, exist in Texas and New Mexico in wild game ranches.',
    'White oryxes are known to dig holes in the sand for the sake of coolness.',
    'The smallest species of oryx is the Arabian oryx. It became extinct in the wild in 1972, but was reintroduced in 1982 in Oman.',
    "The Arabian oryx was the first speicies to have its threat category downgraded from 'Extinct in the Wild' to 'Vulnerable'.",
    'All oryx specicies prefer near-desert conditions and can survive without water for long periods of time.',
    'Oryxes live in herds in numbers up to 600.',
    'Newborn oryx calves are able to run with their herd immediately after birth.',
    'Oryxes have been known to kill lions with their horns.',
    'Oryx horns make the animals a prized game trophy, which has led to the near-extinction of the two northern species.'
    )

ORCA_FACTS = (
    "The orca's large size and strength make it among the fastest marine mammals, able to reach speeds in excess of 55 km/h.",
    "Many orcas live with their mothers for their entire lives.",
    "The orca is not a fish, but a mammal. However it is not a whale, as it is part of the dolphin family.",
    "The largest orca caught was 10 meters long and weighted 10 tons, as heavy as an African elephant.",
    "Orcas live in groups of related females, led by the oldest female, called pods. A pod can have as few as three members or as many as a hundred or more.",
    "Orcas do not have smelling organs or a lobe in the brain dedicated to smelling, so it is believed they cannot smell.",
    "Orcas can sleep with one eye open, like dolphins, as they cannot completely go to sleep, having to go to the surface to get air from time to time.",
    "In captivity, an orca's dorsal fin often flops. This is possible as the fin is not made up of bones, but of large connective tissue."
    "Orcas are the most widely distributed animals in the world, not counting humans. They can be found in all oceans, both in warm and cold waters and even in freezing waters.",
    "The oldest known orca lived to be 103.",
    "There is no record of a wild orca ever attacking a human.",
    "There are fifty-two orcas in captivity all over the world.",
    "Mother orcas give birth every three to ten years, after a 17-month pregnancy.",
    "In Argentina, orcas hurl themselves on-shore to grab sea lion pups.",
    "Whalers call the orca the 'killer of whales'. It preys on sperm, gray, fin, humpback and other whales.",
    "Orcas can weigh up to 6 tons.",
    "An orca's teeth can grow to be 4 inches (10 cm) long.",
    "The orca can reach speeds in excess of 30 knots (about 34 mph, or 56 kph)."
    )

OTTER_FACTS = (
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
)

OWL_FACTS = (
    'Owls are nocturnal and hunt in the night.',
    'There are around 200 different owl species.',
    'A group of owls is called a parliament.',
    'Most owls hunt insects, small mammals and other birds.',
    'Some owl species hunt fish. Owls have powerful talons which help them catch and kill prey.',
    'Owls can turn their heads as much as 270 degrees.',
    'Owls are farsighted, meaning they can’t see things close to their eyes clearly.',
    'Owls are very quiet in flight compared to other birds of prey.',
    'The color of owl’s feathers helps them blend into their environment (camouflage).',
    'Barn owls can be recognized by their heart shaped face.')

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
    'An animated movie from 2008 named ‘Kung Fu Panda’ features a giant panda called ‘Po’.')

PANGOLIN_FACTS = (
    'The name "pangolin" comes from the Malay word pengguling, meaning "one who rolls up".',
    'Pangolins can also emit a noxious-smelling chemical from glands near the anus, similar to the spray of a skunk.',
    'Large pangolins can extend their tongues as much as 40 cm (16 in), with a diameter of only 0.5 cm (0.20 in).',
    'A pangolin can consume 140 to 200 g (4.9 to 7.1 oz) of insects per day.',
    'Pangolins have a very poor sense of vision, so they rely heavily on smell and hearing.',
    'Pangolins lack teeth, so also lack the ability to chew.',
    'The weight of a pangolin at birth is 80 to 450 g (2.8 to 15.9 oz) and the average length is 150 mm (5.9 in).',
    'Pangolin meat is considered a delicacy in southern China and Vietnam.',
    'Pangolin is the most trafficked animal in the world.',
    'All eight species of pangolin are categorized on IUCN Red List of Threatened Species.')

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
    "The Florida panther has adapted to the subtropical forests and swamp environments of Florida, however they are very rare animals, as of 2013 it is believed only 160 Florida panthers remain in the wild.")

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
    'The flag of Dominica features the sisserou parrot.')

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
    "In Hindu culture, Lord Karthikeya, the god of war, is said to ride a peacock.")

PENGUIN_FACTS = (
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
    'Penguins in Antarctica have no land based predators.')

PIG_FACTS = (
    'Pigs are intelligent animals. Some people like to keep pigs as pets.',
    'A pig’s snout is an important tool for finding food in the ground and sensing the world around them.',
    'Pigs have an excellent sense of smell.',
    'There are around 2 billion pigs in the world.',
    'Humans farm pigs for meat such as pork, bacon and ham.',
    'Wild pigs (boar) are often hunted in the wild.',
    'In some areas of the world, wild boars are the main source of food for tigers.',
    'Feral pigs that have been introduced into new areas can be a threat to the local ecosystem.',
    'Pigs can pass on a variety of diseases to humans.',
    'Relative to their body size, pigs have small lungs.',
    'Contrary to popular belief, pigs are actually considered to be very clean animals.',
    'Pigs cannot sweat, so they bathe in water and mud to cool themselves off.',
    'When pigs have ample space, they will try not to soil in the areas where they sleep and eat.' )

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
    'Female pigeons lay 2 eggs that hatch after incubation period of 18 days. Young birds depend on their parents during the first two months of their life. Both parents take care of the chicks (called squabs).',
    'Pigeons can survive more than 30 years in the wild.')

PLATYPUS_FACTS = (
    "Platypuses have no stomach",
    "A platypus' bill is comprised of thousands of cells that can detect the electric fields generated by all living things, giving them a sixth sense",
    "Researchers have discovered a pre-historic platypus that was over 1 meter long, double the size of the modern animal.",
    "Platypuses nurse without nipples, milk oozing from the mammary glands on the abdomen of females and babies drink it by sucking on their mother's fur.",
    "Platypus males have venomous spurs that only activate during mating season, indicating it is meant to fend off competing males",
    "When the first platypus specimen was sent back to England from Australia, scientists thought it was a hoax and someone was playing a trick on them.",
    "Platypuses use gravel as makeshift teeth as they lack teeth inside their bill, making it hard to chew.",
    "A platypus' tail holds half of the animal's body fat in case of food shortage. ",
    "Platypuses have dense, thick fur that helps them stay warm underwater. Most of the fur is dark brown, except for a patch of lighter fur near each eye, and lighter-colored fur on the underside.",
    "Platypuses only live in the freshwater areas that glow through the island of Tasmania, and the eastern and southeastern coast of Australia.",
    "Platypuses are the only mammals that lay eggs, a category called monotremes.",
    "Platypus fur, being very thick and waterproof, used to be very in the fur trade until Australia banned platypus hunting to protect the species.",
    "Platypuses is the correct plural form, although platypi and platypodes are also accepted."
    )

RABBIT_FACTS = (
    'A rabbit’s teeth never stop growing, which is why it is very important to provide chews and treats for them to keep their teeth from becoming overgrown.',
    'Rabbits have 28 teeth.',
    'When rabbits are happy they can jump and twist. This is commonly called a "binky."',
    'The average size of a rabbit litter is usually between 4 and 12 babies, just after a short 30-day pregnancy.',
    'More than half of the world’s rabbits live in North America.',
    'Jackrabbits, which belong to the genus “Lepus,” have been clocked at speeds of 45 miles per hour.',
    'Rabbits have a life span about 8 years, though sterilized rabbits (those who are spayed/neutered) can live as long as 10-12 years.'
    'A rabbit can run between 25-45miles per hour.',
    'Rabbits sleep about 8 hours a day.',
    'Rabbits cannot vomit. They don’t have enough muscles in their stomach.',
    'A male rabbit is called a buck, a female is a doe, and a baby is a kit/kitten.',
    )

SCORPION_FACTS = (
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
    'Scorpions moult, they shed their exoskeleton up to 7 times as they grow to full size. They become vulnerable to predators each time until their new protective exoskeleton hardens.')

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
    'Lifespan of seagulls depends on the species. Most seagulls can survive from 10 to 15 years in the wild.')

SEA_CUCUMBER_FACTS = (
    'Sea cucumbers can reproduce both sexually and asexually.',
    'Sea cucumbers breathe through a branched network of hollow tubules circulating through the anus.',
    'Sea cucumbers have no brain, but they do have a ring of neural tissue surrounding the oral cavity.',
    'At depths below 5.5 miles (8.9 km) under the sea, sea cucumbers can comprise up to 90 percent of the total mass of macrofauna.',
    'Many small animals, such as the pearl fish and many species of shrimp, can live in symbiosis with sea cucumbers.',
    'Sea cucumbers are scavengers, feeding on debris found on the ocean floor.',
    'Sea cucumbers are closely related to starfish and sea urchins.',
    'There are over 1,250 known species of sea cucumber.',
    'As a defense mechanism, sea cucumbers can expel some of their internal organs from their anus. These internal organs can regenerate relatively quickly.',
    'Most species of sea cucumber are around 4-12 inches long',
    'Sea cucumbers can easily get into and out of small crevices',
    'Sea cucumbers communicate by sending hormones through the water',
    'Some species of sea cucumber can emit a sticky substance that can tangle up predators')

SHARK_FACTS = (
    'Sharks do not have a single bone in their bodies. Instead they have a skeleton made up of cartilage; the same type of tough, flexible tissue that makes up human ears and noses.',
    'Some sharks remain on the move for their entire lives. This forces water over their gills, delivering oxygen to the blood stream. If the shark stops moving then it will suffocate and die.',
    'Sharks have outstanding hearing. They can hear a fish thrashing in the water from as far as 500 meters away!',
    'If a shark was put into a large swimming pool, it would be able to smell a single drop of blood in the water.',
    'Although most species of shark are less than one meter long, there are some species such as the whale shark, which can be 14 meters long.',
    'A pup (baby shark) is born ready to take care of itself. The mother shark leaves the pup to fend for itself and the pup usually makes a fast get away before the mother tries to eat it!',
    'Not all species of shark give birth to live pups. Some species lay the egg case on the ocean floor and the pup hatches later on its own.',
    'Great whites are the deadliest shark in the ocean. These powerful predators can race through the water at 30 km per hour.',
    'Unlike other species of shark, the great white is warm-blooded. Although the great white does not keep a constant body temperature, it needs to eat a lot of meat in order to be able to regulate its temperature. ',
    'A shark always has a row of smaller teeth developing behind its front teeth. Eventually the smaller teeth move forward, like a conveyor belt, and the front teeth fall out.')

SHEEP_FACTS = (
    'There are over 1 billion sheep in the world!',
    'Sheep have a field of vision (FOV) of around 300 degrees allowing them to look behind themselves without turning their head!',
    'Sheeps have four stomachs!',
    'Ancient egyptians believed that sheep were sacred to society. When a sheep died, it would be mummified just like a human.',
    'Sheep have 24 molar teeth and 8 incisor teeth.',
    'A collection or group of sheep is called a flock.',
    'Most sheep live between 6-11 years.',
    'A lamb is considered a sheep less than one year old.',
    )

SKUNK_FACTS = (
    'Skunks are omnivores, which mean that they eat both plants and animals. They like to eat fruits, insects, worms, reptiles and rodents.',
    'Skunks often attack beehive because they eat honeybees.',
    'Before it sprays the victim, skunk will turn its back, lift its tail, start hissing and stumping with its feet. Those are the warning signs that precede spraying.',
    'Skunk can spray its oily and smelly substance up to 10 feet distance.',
    "Skunks's worst predators are coyotes, bobcats and owls.",
    'Skunks live up to 3 years in the wild. They can survive up to 10 years in captivity.',
    'Skunks can transmit rabies.'
    'Skunks are typically around the size of house cats. They grow to 8 to 19 inches long and weigh around 7 ounces to 14 lbs.',
    'Skunks appeared 40 million years ago, evolving from common ancestors with weasels and polecats.',
    'Skunks are found in the United States, Canada, South America and Mexico.',
    'Skunks live in forest edges, woodlands, grasslands and deserts. They typically make their homes in abandoned burrows, but will also live in abandoned buildings, under large rocks and in hollow logs.',
    'Though they typically prefer to dine on insects and grubs, skunks are omnivores, consuming a vast diet of both plant and animal matter. Skunks are opportunistic eaters, and their diets are flexible, often shifting with the seasons.',
    'Skunks have strong forefeet and long nails, which make them excellent diggers. When no other form of shelter is available they may even burrow underneath buildings by entering foundation openings.',
    'Skunks are known to release a powerful smell through their anal glands when threatened. Skunks will usually only attack when cornered or defending their young, and spraying is not the first method of defense. A skunk will growl, spit, fluff its fur, shake its tail, and stamp the ground.',
    'Although skunks have very poor eyesight, they have excellent senses of smell and hearing.',
    'Skunks are nocturnal, which means they search for food at night and sleep in dens lined with leaves during the day.',
    'Skunks are slow and can run only 10 miles per hour.',
    'Skunks are immune to rattlesnake venom, bee stings and scorpions.',
    'Females can bear 3-10 young and male skunks reach sexual maturity from 4-6 months after birth while females reach sexual maturity nine months to a year after birth.'
    )

SLOTH_FACTS = (
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
)

SNAIL_FACTS = (
    'Snails are gastropod mollusks, members of the ‘phylum Mollusca’ and the class ‘Gastropoda’.',
    'Snails have no back bone. When they feel threatened, they usually retreat into their shell to protect themselves.',
    'The largest land snail is the ‘Achatina achatina’, the Giant African Snail.',
    'Some land snails feed on other terrestrial snails.',
    'Most snails live from 2 to 5 years, but in captivity, some have exceeded 10 or 15 years of age.',
    'The mucus of the garden snail is used to treat wrinkles, spots, and scars on the skin.',
    'Most snail species are hermaphrodites, so they have both male and female reproductive organs.',
    'The speed of snails is around 0.5-0.8 inches per second. If they moved without stopping, it would take more than a week to complete 1 kilometer.',
    'Snails do not change shells when they grow up. Instead, the shell grows along with them.',
    'Snails host several types of parasites that, while may not kill them, they are capable of affecting or killing their predators or animals that eat the snails. Even humans who eat poorly cooked snails can become seriously ill.',
    'A single garden snail (Helix aspersa) can have up to 430 hatchlings after a year.', 
    'Many snails are in danger of extinction. Among these are the species ‘Aaadonta constricta’ and ‘Aaadonta fuscozonata’, and others of the ‘genus Aaadonta’ and ‘Achatinella’ are in critical danger of extinction.',
    'The size of the shell of a snail reflects its age.',
    'Land snails do not chew their food. They scrape it.',
    'Calcium carbonate is the main component of the snail shells.',
    'Snails can have lungs or gills depending on the species and their habitat. Some marine snails actually can have lungs and some land based snails can have gills.',
    'Most snail species have a ribbon-like tongue called a radula that contains thousands of microscopic teeth. The radula works like a file, ripping food up into tiny pieces.',
    'The majority of snails are herbivores eating vegetation such as leaves, stems and flowers, some larger species and marine based species can be predatory omnivores or even carnivores.',
    'The giant African land snail grows to about 38 cm (15 in) and weigh 1 kg (2lb).',
    "The largest living sea snail species is the Syrinx aruanus who's shell can reach 90 cm (35 in) in length and the snail can weigh up to 18 kg (40lbs)!",
    'Common garden snails have a top speed of 45 m (50 yards) per hour.',
    'As they move along snails leave behind a trail of mucus which acts as a lubricant to reduce surface friction. This also allows the snail to move along upside down.',
    'Depending on the species snails can live 5 - 25 years.',
    'Snail is a common name for gastropod molluscs that can be split into three groups, land snails, sea snails and freshwater snails.',
    'North America has about 500 native species of land snails.',
    'Snails do not change shells when they grow. Instead, the shell grows along with them.',
    'A single garden snail (Helix aspersa) can have up to 430 hatchlings after a year.',
    'Most land snails have two set of tentacles, the upper one carry the eyes, while the lower one has the olfactory organs. However, they do not have ears or ear canal.',
    'Snails are strong and can lift up to 10 times their body weight in a vertical position.',
    'The snail Lymnaea makes decisions by using only two types of neuron: one deciding whether the snail is hungry, and the other deciding whether there is food in the vicinity.')

SNAKE_FACTS = (
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
    'Python reticulates can grow over 8.7 m (28 ft) in length and are considered the longest snakes in the world.')

SQUID_FACTS = (
    'Many species of squid have a life span that is only about one year',
    'The Humboldt squid is very aggressive and will even attack sharks in the water.',
    'The only predators that giant squid have are sperm whales.',
    'Squid are strong swimmers and certain species can "fly" for short distances out of the water.',
    'The majority of squid are no more than 60 cm (24 in) long, although the giant squid may reach 13 m (43 ft).',
    'The smallest squid is the pygmy squid which can be less than 2.5 centimeters (1 inch) long.',
    'It wasn\'t until 2004 that researchers in Japan took the first images ever of a live giant squid.',
    'Giant squid have the largest eyes in the animal kingdom, measuring up to 10 inches in diameter.',
    'Squid, like cuttlefish, have eight arms arranged in pairs, and two longer tentacles with suckers.',
    'Squids belong to a particularly successful group of mollusks called the cephalopods, which have been around for about 500 million years.',
    'Giant squid mostly eat deep water fishes and other squids including other giant squids.',
    'The only predators that giant squid have are sperm whales.')

SQUIRREL_FACTS = (
    'In fall, squirrels bury more food than they will recover.',
    'Squirrels can find food buried beneath a foot of snow.',
    'A squirrel’s front teeth never stop growing.',
    'Squirrels may lose 25% of their buried food to thieves.',
    'Squirrels zigzag to escape predators.',
    'Squirrels may pretend to bury a nut to throw off potential thieves.',
    'A newborn squirrel is about an inch long.',
    'Humans introduced squirrels to most of our major city parks.',
    'Squirrels are acrobatic, intelligent and adaptable.',
    'Squirrels get bulky to stay warm during the winter.',
    'Squirrels don’t dig up all of their buried nuts, which results in more trees!')
	
STINGRAY_FACTS = (
     'Stingrays are diverse group of fish characterized by flattened bodies.',
     'The largest species of stingray measure 6.5 feet in length and can weigh up to 790 pounds.',
     'Stingrays are closely related to sharks. Stingrays don’t have bones.',
     'Stringrays flattened body ends with long tail that usually contains spine and venom. Spines can be serrated in some species.',
     'There are more than 70 Species of stingray.',
     'Stringray mouths are located on the bottom side of their body. When they catch clams, shrimps, and mussels, they will crash and eat them using their powerful jaws.',
     'Stringray`s long tails usually have a spine and venom.',
     'Stingrays Use camouflage for protection and hunting.',
     'Stingrays don’t use their eyes to find prey. They use their electro-sensors to locate their prey',
     'Stingrays are solitary, but can also live in groups.',
     'Stingrays have a lifespan of 15-25 years.',
     'Stringrays can be found in oceans in tropical and subtropical areas around the world. Stingrays like warm and shallow water.',
     'Stingrays are found both in freshwater and ocean.',
     'Stingrays give birth to 2-6 young stingrays each year.',
     'Baby stingrays are born fully developed; they look like miniature versions of adult animals. Babies take care of themselves from the moment of birth.')

TARANTULA_FACTS = (
    'Female tarantulas can live 30 years or longer in the wild.',
    'The largest tarantulas have a leg span the size of a dinner table.',
    'Tarantulas are quite docile and rarely bite people.',
    'Tarantulas defend themselves by throwing needle-like hairs at their attackers.',
    'A fall can be fatal for a tarantula.',
    'Tarantulas have retractable claws on each leg, much alike a cat.',
    'Though tarantulas do not spin webs, they do use silk',
    'Most tarantulas wander during the summer months.',
    'Tarantulas cannot regenerate lost legs.',
    "Because tarantulas molt throughout their lives, replacing their exoskeletons as they grow, they have the ability to repair any damage they've sustained.",
    'If a tarantula does feel threatened, it uses its hind legs to scrape barbed hairs from its abdomen and flings them in the direction of the threat.',
    'Tarantulas do not use webs to capture prey, they do it the hard way – hunting on foot. ',
    'Like other spiders, tarantulas paralyze their prey with venom, then use digestive enzymes to turn the meal into a soupy liquid.',
    'Since falls can be so dangerous for tarantulas, it is important for them to get a good grip when climbing.')

TIGER_FACTS = (
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
    'Tigers that breed with lions give birth to hybrids known as tigons and ligers.')

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

WALLABY_FACTS = (
    'Wallabies are members of the kangaroo clan found primarily in Australia and on nearby islands.',
    'Wallabies are marsupials or pouched mammals. Wallaby young are defenseless and develop in the pouch of their mother.',
    'The largest wallabies can reach 6 feet from head to tail.',
    'Wallabies have powerful hind legs they use to bound along at high speeds and jump great distances.',    
    'Wallabies are herbivores and eat mainly roots, grass, tree leaves and ferns. They rest during the day and are active mainly at night.',
    'Nail-tailed wallabies are so-named because of the sharp growth at the end of their tails.',
    'When wallabies fight, they use their hind legs to deliver powerful kicks.',
    'Four species of wallaby have already gone extinct. Many others are endangered, while others are considered vulnerable.',
    'Large species of wallaby tend to live in groups, but smaller species tend to live alone.',
    'A young wallaby is called Joey. The males are called Jack while the females are called Jill.',
    'There are 30 different species of wallabies and all are native to Australia and Tasmania.'
    'The average lifespan of a wallaby is from 9 - 15 years.',
    "A group of wallabies is known as a ‘mob’.",
    'A female typically gives birth to a single wallaby and in very rare cases, twins. The gestation period is one month.',
    'Wallabies have strong back legs that help them hop and move about powerfully. The forearms of the wallaby are small and used mainly for balancing or for feeding.',
    'An adult wallaby weighs about 15 – 26 kg. The males are 77-88 cm in height and the females are about 70-84 cm tall. Their tail is 80 cm long, which is almost the length of their entire body. They use their tail to balance and jump around. They also use it to prop into a sitting position.',
    'Wallabies are pink and furless at birth.',
    )

WALRUS_FACTS = (
    'The scientific name for a walrus is Odobenus Rosmarus. It is latin for tooth walking sea-horse.',
    'A male walrus is called a bull. A female walrus is called a cow. A baby walrus is called a calf.',
    'Walruses spend half their time on land and the other half in water.',
    'There are two sub-species of walruses. The Atlantic Walrus and the Pacific Walrus.',
    'Walruses live in the Northern Hemisphere in the Arctic.',
    'Atlantic Walruses live near Northern Canada to Greenland.',
    'Walruses are grey or brown but turn a pinkish color as they age.',
    'Walruses have thick skin and then a layer of blubber.  Their blubber keeps them warm in icy waters.',
    'Walruses grow to be 7.5 pounds to 11.5ft. Walruses can weigh up to 4,000 pounds',
    'Walruses whiskers are called vibrissae.',
    'Walruses have 450 whiskers. Their whiskers are very sensitive and are used to help them locate food.',
    'Walruses can hold their breath under water for up to 30 minutes.',
    'Walruses live between 30-40 years in the wild.',
    'Female Walruses give birth to their babies on land or on ice floes.',
    'Baby walruses weigh between 100-165 pounds!',
    'There are around 250,000 walruses left in the wild.',
    'Walruses were hunted by humans for their blubber and ivory tusks.',
    'Walruses weigh from 600 to 1,500 kilograms (1,320 to 3,300 lbs.) and can be as long as 3.2 meters (10.5 feet).',
    'Walrus tusks can grow up to 3 feet (1 m). The tusks are canine teeth and stick out from either side of the animal’s mouth.',
    'Walruses use their tusks to break through ice, and to assist in climbing out of the water and onto the ice. The animals also use their tusks to defend themselves from larger predators and to establish dominance and a hierarchy among walruses.',
    'Walruses can swim on average around 4.35 mph (7 km/h) and as fast as 21.74 mph (35 km/h).',
    'A group of walruses is called a herd. They gather by the hundreds to sunbathe on the ice. During mating season, walruses amass by the thousands.',
    'Walruses are carnivores, but they aren’t ferocious hunters. The walrus’ favorite food is shellfish.',
    'There are three subspecies of walrus. Atlantic walruses live in the coastal areas along northeastern Canada to Greenland. Pacific walruses live in the northern seas near Russia and Alaska. Laptev walruses live in the Laptev Sea of Russia.',
    'In the 1950s, the population of walruses was almost eliminated due to commercial hunting, but the population was brought back to a thriving number in the 1980s.',
    'Native people of the Arctic hunt walruses for hides, food, ivory and bones. These natives are now the only people who are allowed to legally hunt walruses.',
    'Odobenus rosmarus, the walruses’ scientific name, is Latin for ‘tooth-walking sea-horse’.',
    'Walruses have only two natural predators: the orca (or killer whale) and the polar bear. Both are more likely to hunt walrus calves than adults.')

WHALE_FACTS = (
    'Many whales are toothless. They use a plate of comb-like fibre called baleen to filter small crustaceans and other creatures from the water.',
    'There are 79 to 84 different species of whale. They come in many different shapes and sizes!',
    'A baby whale is called a calf. Whales form groups to look after calves and feed together. These groups are often made up of all female or all male whales.',
    'Whales that are found in both Northern and Southern hemisphere never meet or breed together. Their migration is timed so that they are never in breeding areas at the same time.',
    'The arched lower lip of a whale can often make it look like it is smiling! However, this isn’t a “real” smile as the blubber in the head of the whale prevents the muscles of the face from reaching the surface.',
    'You can tell the age of a whale by looking at the wax plug in its ear. This plug in the ear has a pattern of layers when cut lengthwise that scientists can count to estimate the age of the whale.',
    'Whales love to sing! They use this as a call to mates, a way to communicate and also just for fun! After a period of time they get bored of the same whale song and begin to sing a different tune.',
    'Sometimes whales make navigation mistakes during migrations. Although they may have made the mistake days before, they don’t realise it until they becoming stranded.',
    'Whales support many different types of life. Several creatures, such as barnacles and sea lice, attach themselves to the skin of whales and live there.')

WOLF_FACTS = (
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
)

ZEBRA_FACTS = (
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
)

ALL_FACTS = (
    ALBATROSS_FACTS,
    ALLIGATOR_FACTS,
    ANT_FACTS,
    BADGER_FACTS,
    BEAVER_FACTS,
    CAMEL_FACTS,
    CHAMELEON_FACTS,
    CHEETAH_FACTS,
    COW_FACTS,
    CRAB_FACTS,
    CROCODILE_FACTS,
    CUTTLEFISH_FACTS,
    DINGO_FACTS,
    DOLPHIN_FACTS,
    EAGLE_FACTS,
    ECHIDNA_FACTS,
    EMU_FACTS,
    FALCON_FACTS,
    FLAMINGO_FACTS,
    FOX_FACTS,
    FROG_FACTS,
    ELEPHANT_FACTS,
    GIRAFFE_FACTS,
    GRASSHOPPER_FACTS,
    GOAT_FACTS,
    GOOSE_FACTS,
    GOPHER_FACTS,
    GORILLA_FACTS,
    HAMSTER_FACTS,
    HEDGEHOG_FACTS,
    HIPPO_FACTS,
    HONEYBEE_FACTS,
    HORSE_FACTS,
    HUMMINGBIRD_FACTS,
    HUSKY_FACTS,
    JELLYFISH_FACTS,
    KANGAROO_FACTS,
    KOALA_FACTS,
    LEOPARD_FACTS,
    LION_FACTS,
    LIZARD_FACTS,
    LLAMA_FACTS,
    MEERKAT_FACTS,
    MONKEY_FACTS,
    NARWHAL_FACTS,
    NEWT_FACTS,
    OCELOT_FACTS,
    OCTOPUS_FACTS,
    ORYX_FACTS,
    ORCA_FACTS,
    OTTER_FACTS,
    OWL_FACTS,
    PANDA_FACTS,
    PANGOLIN_FACTS,
    PANTHER_FACTS,
    PARROT_FACTS,
    PEACOCK_FACTS,
    PENGUIN_FACTS,
    PIG_FACTS,
    PIGEON_FACTS,
    PLATYPUS_FACTS,
    RABBIT_FACTS,
    SCORPION_FACTS,
    SEAGULL_FACTS,
    SEA_CUCUMBER_FACTS,
    SHARK_FACTS,
    SHEEP_FACTS,
    SKUNK_FACTS,
    SLOTH_FACTS,
    SNAIL_FACTS,
    SNAKE_FACTS,
    SQUIRREL_FACTS,
    STINGRAY_FACTS,
    TARANTULA_FACTS,
    TIGER_FACTS,
    TURTLE_FACTS,
    WALLABY_FACTS,
    WALRUS_FACTS,
    WHALE_FACTS,
    WOLF_FACTS,
    ZEBRA_FACTS
)


def main():
    reddit = authenticate()
    while True:
        print(
            "Wait time after commenting will be " +
            str(wait_time) +
            " seconds.\n")
        animalfactsbot(reddit)


if __name__ == '__main__':
    main()
