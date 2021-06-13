from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import math
# Create your models here.

#class MainCycle(models.Model):
    #user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)

class MainCycle(models.Model):
    user = models.ForeignKey(User, related_name='cycle', null=False, on_delete=models.CASCADE)

    coinsCount = models.IntegerField(default=0)
    auto_click_power = models.IntegerField(default=0)
    clickPower = models.IntegerField(default=1)
    level = models.IntegerField(default=0)
    toNextLevel = models.IntegerField(default=10)

    def Click(self):
        self.coinsCount += self.clickPower
        return self.check_level()

    def check_level(self):
        #if(self.coinsCount > (self.level**2 + 1) * 1000):
        if(self.coinsCount > self.toNextLevel):
            self.level += 1
            boost_type = 1
            if self.level % 3 == 0:
                boost_type = 0
            self.toNextLevel = ((self.level+1)**3)*5
            boost = Boost(mainCycle = self, boost_type=boost_type, level = self.level)
            boost.save()
            return True
        return False

    def set_main_cycle(self, coins_count):
        self.coinsCount = coins_count
        return self.check_level()


class Boost(models.Model):
    #id = 1
    mainCycle = models.ForeignKey(MainCycle, related_name='boosts', null=False, on_delete=models.CASCADE)
    level = models.IntegerField(null=False)
    power = models.IntegerField(default=1)
    price = models.IntegerField(default=10)
    boost_type = models.IntegerField(default=1)

    def upgrade(self):
        self.mainCycle.coinsCount -= self.price
        if self.boost_type == 1:
            self.mainCycle.clickPower += self.power
            self.price *= (self.level + 1)*3
            if (self.level < 4):
                self.power *= ((self.level + 1)**(math.log(self.level, 2)))
            else:
                self.power *= int((self.level + 1)*(math.log(self.level, 2)))
        else:
            self.mainCycle.auto_click_power += self.power
            self.price *= 10
            self.power *= int((self.level + 1) / 2)
        #self.power *= 2
        self.save()
        self.mainCycle.save()
        return (self.mainCycle,
        self.level,
        self.price,
        self.power)

    def update_coins_count(self, current_coins_count):
        self.mainCycle.coinsCount += current_coins_count
        return self.mainCycle
