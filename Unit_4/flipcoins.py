import random

class Coin(object):
    '''this is a simple fair coin, can be pseudorandomly flipped'''
    sides = ('heads', 'tails')
    last_result = None

    def flip(self):
        '''call coin.flip() to flip the coin and record it as the last result'''
        self.last_result = result = random.choice(self.sides)
        return result

    #auxilliary functions to manipulate the coins:

    def create_coins(number):
        '''create a list of a number of coin objects'''
        return [Coin() for i in xrange(number)]

    def flip_coins(coins):
        '''side effect function, modifies object in place, returns None'''
        for coin in coins:
            coin.flip()

    def coint_heads(flipped_coins):
        return sum(coin.last_result == 'heads' for coin in flipped_coins)

    def count_tails(flipped_coins):
        return sum(coin.last_result == 'tails' for coin in flipped_coins)

    def main():
        coins = create_coins(1000)
        for i in xrange(100):
            flip_coins(coins)
            print count_heads(coins)

    if __name__ == '__main__':
        main()
