import re
import praw
import random
import time
from pygame import mixer
# from '/' import lists

BLACKLIST = {'asoiaf', 'gameofthrones', 'exmormon', 'suicidewatch', 'politics', 'whowouldwin'}

mixer.init()
alert=mixer.Sound('bird.wav')
history = 'commented.txt'

def authenticate():
    print('Authenticating...\n')
    reddit = praw.Reddit('animal-facts-bot', user_agent = '/u/AnimalFactsBot')
    print('Authenticated as {}\n'.format(reddit.user.me()))
    return reddit

def botengine(animal, regex, reddit, facts):
    time.sleep(10)
    print("Checking 500 comments for " + animal + "...\n")
    for comment in reddit.subreddit('all-gameofthrones-asoiaf-exmorman-suicidewatch-politics-whowouldwin').comments(limit = 500):
        match = re.findall(regex, comment.body)

        if match:
            print(animal + " found in comment with comment ID: " + comment.id)
            file_obj_r = open(history,'r')
            if comment.id not in file_obj_r.read().splitlines():
                if comment.author.name == reddit.user.me():
                    print('     Skipping my own comment...\n')
                else:
                    print('     Found new comment by ' + comment.author.name + '\n')
                    comment.reply(random.choice(facts))
                    alert.play()
                    file_obj_r.close()
                    file_obj_w = open(history,'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                    print('Waiting 1 minute before commenting again\n')
                    time.sleep(60)
            else:
                print('Already commented on this!\n')

def animalfactsbot(reddit):
    botengine('owl', '\sowls?\s', reddit, OWL_FACTS)
    botengine('horse', '\shorses?\s', reddit, HORSE_FACTS)
    botengine('penguin', '\spenguins?\s', reddit, PENGUIN_FACTS)
    botengine('octopus', '\soctopus?\s', reddit, OCTOPUS_FACTS)
    botengine('pig', '\spig?\s', reddit, PIG_FACTS)
    botengine('tiger', '\stiger?\s', reddit, TIGER_FACTS)
    botengine('frog', '\sfrog?\s', reddit, FROG_FACTS)
    botengine('giraffe', '\sgiraffe?\s', reddit, GIRAFFE_FACTS)
    botengine('wolf', '\swolf?\s', reddit, WOLF_FACTS)
    botengine('turtle', '\sturtle?\s', reddit, TURTLE_FACTS)
    botengine('jellyfish', '\sjellyfish?\s', reddit, JELLYFISH_FACTS)
    botengine('koala', '\skoala?\s', reddit, KOALA_FACTS)
    botengine('sloth', '\ssloth?\s', reddit, SLOTH_FACTS)
    botengine('dolphin', '\sdolphin?\s', reddit, DOLPHIN_FACTS)
    botengine('scorpion', '\sscorpion?\s', reddit, SCORPION_FACTS)
    botengine('snake', '\ssnake?\s', reddit, SNAKE_FACTS)
    botengine('whale', '\swhale?\s', reddit, WHALE_FACTS)



OWL_FACTS = [
    'There are around 200 different owl species.',
    'Owls are active at night (nocturnal).',
    'A group of owls is called a parliament.',
    'Most owls hunt insects, small mammals and other birds.',
    'Some owl species hunt fish.',
    'Owls have powerful talons (claws) which help them catch and kill prey.',
    'Owls have large eyes and a flat face.',
    'Owls can turn their heads as much as 270 degrees.',
    'Owls are farsighted, meaning they can’t see things close to their eyes clearly.',
    'Owls are very quiet in flight compared to other birds of prey.',
    'The color of owl’s feathers helps them blend into their environment (camouflage).',
    'Barn owls can be recognized by their heart shaped face.'
    ]

TURTLE_FACTS = [
    'Turtles are reptiles.',
    'Turtles have a hard shell that protects them like a shield, this upper shell is called a ‘carapace’.',
    'Turtles also have a lower shell called a ‘plastron’.',
    'Many turtle species (not all) can hide their heads inside their shells when attacked by predators.',
    'Turtles have existed for around 215 million years.',
    'Like other reptiles, turtles are cold blooded.',
    'The largest turtle is the leatherback sea turtle, it can weigh over 900 kg! (2000 lb)',
    'Turtles lay eggs.',
    'In some species of turtle the temperature determines if the egg will develop into a male or female, lower temperatures lead to a male while higher temperatures lead to a female.',
    'Some turtles lay eggs in the sand and leave them to hatch on their own. The young turtles make their way to the top of the sand and scramble to the water while trying to avoid predators.',
    'Sea turtles have special glands which help remove salt from the water they drink.',
    'Many turtle species are endangered.'
    ]

KOALA_FACTS = [
    'Koalas are native to Australia.',
    'Koalas are not bears.',
    'Koala fossils found in Australia have been dated as long ago as 20 million years.',
    'Koalas eat eucalypt leaves and almost nothing else.',
    'The brain size of modern koalas has reduced substantially from their ancestors, possibly as an adaptation to the low energy they get from their diets.',
    'The closest living relative of the koala is the wombat.',
    'Koalas have sharp claws which help them climb trees.',
    'Koalas have similar fingerprints to humans.',
    'Koalas have large noses that are coloured pink or black.',
    'Outside of breeding seasons, koalas are quiet animals.',
    'A baby koala is called a ‘joey’.',
    'Joeys live in their mother’s pouch for around six months and remain with them for another six months or so afterwards.',
    'Koalas cannot be kept legally as pets.',
    ]

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

GIRAFFE_FACTS = [
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
    ]

JELLYFISH_FACTS = [
    'Jellyfish live in the sea and are found in all oceans.',
    'Some jellyfish live in fresh water.',
    'Jellyfish look a little like umbrellas.',
    'Jellyfish can be large and brightly colored.',
    'They can often be transparent (see-through) or translucent (semi-translucent).',
    'Some can be very hard to see, nearly invisible to the human eye.',
    'Although the word is mentioned in their name, jellyfish are not fish.',
    'A group of jellyfish is called a ‘bloom’, ‘swarm’ or ‘smack’.',
    'Large blooms can feature over 100,000 jellyfish.',
    'Jellyfish don’t have brains.',
    'Jellyfish use their tentacles to sting. Most are harmless to humans but stings from some species, such as the box jellyfish, can be very painful and sometimes kill.',
    'Box jellyfish are almost transparent.',
    'Jellyfish eat plankton. Some sea turtles eat jellyfish.'
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

FROG_FACTS = [
    'A frog is an amphibian. They lay their eggs in water. The eggs hatch into a tadpole which lives in water until it metamorphoses into an adult frog.',
    'Tadpoles look more like fish than frogs, they have long finned tails and breathe through gills.',
    'An amphibian can live both on land and in water.',
    'Although frogs live on land their habitat must be near swamps, ponds or in a damp place. This is because they will die if their skin dries out.',
    'Instead of drinking water, frogs soak it into their body through their skin.',
    'Frogs breathe through their nostrils while also absorbing about half the air they need through their skin.,',
    'Frogs use their sticky, muscular tongue to catch and swallow food. Unlike humans, their tongue is not attached to the back of its mouth. Instead it is attached to the front, enabling the frog to stick its tongue out much further.',
    'The common pond frog is ready to breed when it is only three years old.',
    'Frogs in the wild face many dangers and are lucky to survive several years. In captivity however, frogs can live for much longer.',
    'Frogs can see forwards, sideways and upwards all at the same time. They never close their eyes, even when they sleep.',
    "Remarkably, frogs actually use their eyes to help them swallow food. When the frog blinks, its eyeballs are pushed downwards creating a bulge in the roof of its mouth. This bulge squeezes the food inside the frog's mouth down the back of its throat."
    ]

WOLF_FACTS = [
    'Wolves are excellent hunters and have been found to be living in more places in the world than any other mammal except humans.',
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
    'Pigs are intelligent animals.',
    'Like humans, pigs are omnivores, meaning they eat both plants and other animals.',
    'A pig’s snout is an important tool for finding food in the ground and sensing the world around them.',
    'Pigs have an excellent sense of smell.',
    'There are around 2 billion pigs in the world.',
    'Humans farm pigs for meat such as pork, bacon and ham.',
    'Some people like to keep pigs as pets.',
    'Wild pigs (boar) are often hunted in the wild.',
    'In some areas of the world, wild boars are the main source of food for tigers.',
    'Feral pigs that have been introduced into new areas can be a threat to the local ecosystem.',
    'Pigs can pass on a variety of diseases to humans.',
    'Relative to their body size, pigs have small lungs.'
    ]

OCTOPUS_FACTS = [
    'There are around 300 species of octopus, usually located in tropical and temperate ocean waters. They are divided into finned deep-sea varieties that live on the ocean floor and finless, shallow water varieties found around coral reefs.',
    'Octopuses have two eyes in a globe-shaped head (mantle) off which protrude eight long limbs called tentacles that have two rows of sucker senses.',
    'Octopuses can squeeze into tight spaces as they are invertebrates which means they have no skeleton, (some species have a protective casing in their mantles).',
    'An octopus has a hard beak, like a parrot beak, which they use to break into and eat their pray such as crabs and shellfish.',
    'Octopuses have three hearts.',
    'The largest octopus is believed to be the giant Pacific octopus, Enteroctopus dofleini which weigh about 15 kg (33 lb), and has an arm span up to 4.3 m (14 ft).',
    'Octopuses are believed to be highly intelligent compared to other invertebrates.',
    "An octopus's main defence against predators such as sharks is to hide and camouflage itself by using certain skin cells to change its color. This can also be used to talk with or warn other octopuses.",
    'Another defence is to make a fast escape. Octopuses can eject a thick, blackish ink in a large cloud to distract the predator while the octopus uses a siphon jet propulsion system to quickly swim away headfirst, with arms trailing behind.',
    'A last ditch defence is for the octopus to shed a tentacle similar to how a gecko or lizard can discard a tale. An octopus is able to regenerate a lost tentacle.',
    'Octopuses have very good eyesight and an excellent sense of touch.',
    'A female octopus can lay on average about 200,000 eggs, however, fending for themselves only a handful of the hatchlings will survive to adulthood.',
    'Octopuses usually live for 6 - 18 months. Males only live a few months after mating, and females die of starvation shortly after their protected eggs hatch.',
    'Humans eat octopus in many cultures and it is also a popular fish bait.'
    ]

PENGUIN_FACTS = [
    'Penguins are flightless birds.',
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

def main():
    reddit = authenticate()
    while True:
        animalfactsbot(reddit)

if __name__ == '__main__':
    main()
