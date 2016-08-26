# -*- coding: utf8 -*

import random

#------------------------------------------------------
# iBrew
#
# Coffee & tea jokes
#
# https://github.com/Tristan79/iBrew
#
# Copyright © 2016 Tristan (@monkeycat.nl)
#
# Kettle Rattle (rev 6)
#------------------------------------------------------



class iBrewJokes:


    teaJokes = [["What do you call a talkative drink?","Chai-tea."],
                ["How long does it take to brew chinese tea?","Oolong time."],
                ["When shouldn’t you drink a hot beverage?","If it’s not your cup of tea."],
                ["How does Moses make his tea?","Hebrews it."],
                ["What drink do goalies hate?","Penal-tea."],
                ["How do you ask a dinosaur to lunch?","Tea Rex?"],
                ["What does a worry wart drink?","Safe-tea."],
                ["Why did the hipster burn his tongue?","Because he drank his tea before it was cool."],
                ["What drink brings you down to earth?","Gravi-tea."],
                ["What do sophisticated fish drink?","Salt-tea."],
                ["Why did the tea bag have to do it’s laundry?","Because it was stained."],
                ["What kind of music do teapots like?","Jasmine."],
                ["Why must you be careful of tea at night?","Because it might mug you."],
                ["What does a tea bag do when it’s tired?","It seeps."],
                ["Why did the teapot get in trouble?","Because he was naugh-tea."],
                ["What did the teapot wear to bed?","A nightea"],
                ["What happens when an old teapot laughs too hard?","It teas its pants."],
                ["It is time to get this par-tea started!","Right?"],
                ["Hello Brew-TEA-Full!!!","Your kettle"],
                ["I love to drink tea each day","It brings out my inner tranquili-tea"],
                ["Today!","Full of creativi-Tea"],
                ["It tends to break the ice very easily","Flirt-tea."],
                ["When your kettle is too","Chat-tea"],
                ["Where there is tea","There is hope!"],
                ["If tea is the drink of love","Then brew on!"],
                ["It really is a serious problem","If tea can’t fix it."],
                ["The study into soaked leafs","Teaology"],
                ["Why I have an iKettle two zero?","So my wife only has to walk, once!"]
                ]
 
 
    coffeeJokes = [["Why is a bad cup of coffee the end of a marriage?","Because it’s grounds for divorce!"],
                ["What do you call sad coffee?","Despresso"],
                ["Did you know it’s a sin for a woman to make coffee?","In the bible it says He-brews"],
                ["Why coffee is better than a Woman?","Coffee goes down easier!"],
                ["They call me ’coffee’ ","Cause I grind so fine."],
                ["Hold the sugar please","You’re sweet enough for the both of us"],
                ["So I’ve been thinking about you a latte","Your coffee grinder"],
                ["How do you look so good before coffee?","Your coffee machine"],
                ["Why are men are like coffee?"," The best ones are rich, hot, and can keep you up all night!"],
                ["Coffee runs to you!","Coffee runs to me!"],
                ["Come to the Darkside™","We have coffee"],
                ["","Pot-head!!!"],
                ["Coffee!","Makes me poop!"],
                ["How does a tech-guy drink coffee?","He installs Java!"],
                ["Why do they call coffee mud?","Because it was ground a couple of minutes ago"],
                ["What’s fat, slimy, and drinks a lot of coffee?","Java the Hut"],
                ["Why don’t snakes drink coffee?","It makes them viperactive!"],
                ["What are you, if you call your cats cream and sugar?","You’re probably drinking too much coffee"],
                ["What’s black and doesn’t work?","Decaffeinated coffee"],
                ["Where is all the coffee?","We were mugged!"],
                ["Energy is...","MilkCoffee²"],
                ["I’m sure all coffee beans are juvenile","They’re always getting grounded!"],
                ["Is coffee your daily grind?","Your coffee machine"]
        ]


    def tea(self):
        return random.choice(self.teaJokes)


    def coffee(self):
        return random.choice(self.coffeeJokes)


    def joke(self):
        return random.choice(self.teaJokes+self.coffeeJokes)


