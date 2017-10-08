# animal-facts-bot

A Reddit bot that searches for comments on reddit that contain the name of the animal and then replies to the comment with a fact about that animal.

You can see the bot in action at https://www.reddit.com/user/AnimalFactsBot/comments/

### Current supported animals:
* alligator
* badger
* beaver
* camel
* cheetah
* cow
* crab
* dolphin
* eagle
* echidna
* elephant
* flamingo
* fox
* frog
* giraffe
* gorilla
* hedgehog
* hippo
* horse
* jellyfish
* koala
* lion
* leopard
* lizard
* monkey
* ocelot
* octopus
* otter
* owl
* panda
* penguin
* pig
* scorpion
* seagull
* shark
* sloth
* snake
* tiger
* turtle
* wolf
* whale
* zebra

### AnimalFactsBot will reply to its replies if they contain the phrases:
* good bot
* bad bot
* thank
* more
* silly
* TIL
* AnimalFactsBot

AnimalFactsBot gets these fairly often.


## How to contribute (Teach AnimalFactsBot a new animal): 

* Fork/clone the repo
* Add a tuple of strings of facts (to animalfacts.py) pertaining to a particular animal. Name the tuple variable following the format 'NAMEOFANIMAL_FACTS'. Put the tuple in alphabetical order with the other tuples.
* Add your tuple to the ALL_FACTS tuple.
* Add a line to the check_comment_for_animal() function for your animal following the format.
* Make sure to tag joel-g in the pull request to master.

Please: Don't add a very small set of facts (this will cause the bot to be repetetive regarding your animal).
        Only add TRUE facts. Please no trolling with 'alternative facts'.
