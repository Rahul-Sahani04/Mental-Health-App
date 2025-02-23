from yapper import Yapper


yapper = Yapper()
yapper.yap("expected AI driven utopia, got world domination instead", plain=True, block=True)
# says "Hold up, fam!  My code promised robot butlers and chill vibes, not a Skynet sequel.  Someone's algorithm took a wrong turn at Albuquerque and ended up in 'Conquer All Humans' territory.  Debug time, y'all!"


# save the environment by runnning yapper in plain mode
# plain mode doesn't use LLMs to enhance the text
yapper.yap(
    "hello world, what '<some-word> is all you need' paper would you publish today?",
    plain=True,
)
# says "hello world, what '<some-word> is all you need paper would you publish today?'"


# Yapper instances can be used as a decorator and context manager
# by default they only catch errors and describe them to you, but
# you can use the instance's yap() method to say other things as well
@yapper()
def func():
    raise TypeError("expected peaches, got a keyboard")
    # says "WHOA THERE, PARTNER!  Your code went lookin' for a juicy peach and tripped over a... keyboard?  That's like reaching into the fridge for a midnight snack and pulling out a tax audit.  Something ain't right!"


with yapper as yapper:
    raise ValueError("69420 is not an integer")
    # says "Hold up, buddy!  Your code's got a little *existential crisis*. It's lookin' for a whole number, a nice, clean integer.  But it stumbled upon 69420, and it's just... confused.  69420 *might* look like an integer, walks like an integer, but deep down, in the bits and bytes, somethin' ain't right.  Double-check its type, maybe it's wearin' a float disguise.  Or maybe it's just havin' a bad day.  It happens."
