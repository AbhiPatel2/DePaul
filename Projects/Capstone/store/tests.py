import random
import string

import store.interaction as interaction
from django.test import TestCase

import store.models as models  # this is how we can query

stringEdgeCases = ["", " ", "\\", "null", "NULL", "    a    ", "long string " * (300 // 12),
    "admin", "username", "test", "new", "NULL", "!@#$%^&*(){?+|_", "\"a\""
    "\u200B", "a\u200Ba", "\u200Ba\u200B", "گچپژ", "表", "Üß", "\u0000"]

safeChars = string.ascii_letters
anyChar = string.__all__ # see string.py for every option

def randomString(minLen=1, maxLen=50, charOptions=anyChar):
    return random.choices(k=random.randint(minLen, maxLen))

# usernames probably shouldn't start or end with any space and can only contain latin alphabet or symbols

class BasicPassingTest(TestCase):

    def test_interactions(self):
        registerRes: tuple[interaction.Status, models.Customer] = interaction.signUp("rp_88", "Rohan Panchal", "rp@depaul.edu", "+1(630)987-1234", "bleh8888")
        # print(registerRes)
        self.assertEqual(registerRes[0], interaction.Status.SUCCESS)

        customer: models.Customer = registerRes[1]

        self.assertEqual(interaction.loginVerify("rp_88", "bleh8888")[0], interaction.Status.SUCCESS)

        createAddressRes = interaction.createAddress("22 Ashland Ave", "Chicago", "Illinois", "60614")
        self.assertEqual(createAddressRes[0], interaction.Status.SUCCESS)

        customer.linkCustomerAddress(createAddressRes[1])
        assert (customer.address == createAddressRes[1])


class CartTest(TestCase):

    def test_cart(self):

        item1 = interaction.addItemType("Bleu", "Perfum Spray", "Chanel", "17800", "17800", "3.4", "M",
                "The most intense of the BLEU DE CHANEL fragrances. Powerful and refined, the Parfum for men reveals the essence of independence and determination. A timeless scent with a strong masculine signature.",
                "https://dybskkbnjb5ca.cloudfront.net/img/prod/mp-5028.webp",
                [("Power", .8), ("Masculinity", .75), ("Freshness", .7), ("Wooden", .65), ("Warmth", .6)])
        self.assertEqual(item1[0], interaction.Status.SUCCESS)
        item1 = item1[1]

        item2 = interaction.addItemType("Skunk", "Perfum Spray", "Chanel", "1100", "500", "9.5", "F", "The best Chanel fragrance", "",
                [("Power", .9), ("Masculinity", .1), ("Freshness", -.98), ("Warmth", .6), ("Pleasant", -1.0)])[1]
        item3 = interaction.addItemType("Jaoeuuaoe", "Lotion", "Deeeee", "5599", "5599", "1.3", "U", "", "",
                [("Femininity", .3), ("Freshness", 0)])[1]

        customers: list[models.Customer] = []
        for i in range(4):
            itemRes = interaction.signUp("customer_" + str(i), "Customer " + chr(i + 65), "email" + str(i) + "@email.com", "0000000000" + str(i), "PASSWORD")
            self.assertEqual(itemRes[0], interaction.Status.SUCCESS)
            customers.append(itemRes[1])

        models.Item.make(item1)
        self.assertEqual(models.Item.objects.count(), 1) # A

        self.assertEqual(models.OrderItem.objects.count(), 0)
        self.assertEqual(models.Order.objects.count(), 0)

        self.assertEqual(customers[0].addItemToCart(item1)[0], interaction.Status.SUCCESS) # +A
        self.assertEqual(models.OrderItem.objects.count(), 1)
        self.assertEqual(models.Order.objects.count(), 1)

        self.assertEqual(customers[0].addItemToCart(item1)[0], interaction.Status.FAILURE)
        self.assertEqual(models.OrderItem.objects.count(), 1)
        self.assertEqual(customers[0].removeItemFromCart(item1)[0], interaction.Status.SUCCESS) # -A
        self.assertEqual(models.OrderItem.objects.count(), 0)
        self.assertEqual(models.Order.objects.count(), 0)

        self.assertEqual(customers[0].removeItemFromCart(item1)[0], interaction.Status.FAILURE)
        self.assertEqual(models.OrderItem.objects.count(), 0)
        self.assertEqual(models.Order.objects.count(), 0)

        models.Item.make(item1) # B|C
        models.Item.make(item1) # B|C
        self.assertEqual(models.Item.objects.count(), 3)

        self.assertEqual(customers[0].addItemToCart(item1)[0], interaction.Status.SUCCESS) # +B
        self.assertEqual(models.OrderItem.objects.count(), 1)
        self.assertEqual(models.Order.objects.count(), 1)

        self.assertEqual(customers[1].addItemToCart(item1)[0], interaction.Status.SUCCESS) # +C
        self.assertEqual(models.OrderItem.objects.count(), 2)
        self.assertEqual(models.Order.objects.count(), 2)

        models.Item.make(item2) # D
        self.assertEqual(customers[0].addItemToCart(item2)[0], interaction.Status.SUCCESS) # +D
        self.assertEqual(models.OrderItem.objects.count(), 3)
        self.assertEqual(models.Order.objects.count(), 2)

        models.Item.make(item3) # E
        self.assertEqual(customers[0].addItemToCart(item3)[0], interaction.Status.SUCCESS) # +E
        self.assertEqual(models.OrderItem.objects.count(), 4)
        self.assertEqual(customers[0].addItemToCart(item2)[0], interaction.Status.FAILURE)
        self.assertEqual(models.OrderItem.objects.count(), 4)

        self.assertEqual(customers[2].addItemToCart(item1)[0], interaction.Status.SUCCESS) # +A
        self.assertEqual(models.OrderItem.objects.count(), 5)
        self.assertEqual(models.Order.objects.count(), 3)

        self.assertEqual(customers[3].addItemToCart(item1)[0], interaction.Status.FAILURE)
        self.assertEqual(models.OrderItem.objects.count(), 5)
        self.assertEqual(models.Order.objects.count(), 3)

        self.assertEqual(customers[0].removeItemFromCart(item2)[0], interaction.Status.SUCCESS) # -D
        self.assertEqual(models.OrderItem.objects.count(), 4)

        self.assertEqual(customers[2].removeItemFromCart(item1)[0], interaction.Status.SUCCESS) # -A
        self.assertEqual(models.OrderItem.objects.count(), 3)
        self.assertEqual(models.Order.objects.count(), 2)

        self.assertEqual(customers[0].removeItemFromCart(item3)[0], interaction.Status.SUCCESS) # -E
        self.assertEqual(models.OrderItem.objects.count(), 2)
        self.assertEqual(customers[0].removeItemFromCart(item3)[0], interaction.Status.FAILURE)
        self.assertEqual(models.OrderItem.objects.count(), 2)

        self.assertEqual(customers[0].removeItemFromCart(item1)[0], interaction.Status.SUCCESS) # -B
        self.assertEqual(models.OrderItem.objects.count(), 1)
        self.assertEqual(models.Order.objects.count(), 1)

        self.assertEqual(customers[1].removeItemFromCart(item1)[0], interaction.Status.SUCCESS) # -C

        self.assertEqual(models.OrderItem.objects.count(), 0) # reset
        self.assertEqual(models.Order.objects.count(), 0)

        self.assertEqual(customers[0].addItemToCart(item1)[0], interaction.Status.SUCCESS)
        self.assertEqual(customers[0].addItemToCart(item1)[0], interaction.Status.SUCCESS)
        self.assertEqual(customers[1].addItemToCart(item1)[0], interaction.Status.SUCCESS)
        self.assertEqual(customers[0].addItemToCart(item3)[0], interaction.Status.SUCCESS)
        self.assertEqual(models.OrderItem.objects.count(), 4)
        self.assertEqual(customers[0].shipOrder(), interaction.Status.SUCCESS)
        self.assertEqual(models.OrderItem.objects.count(), 1)
        self.assertEqual(customers[2].shipOrder(), interaction.Status.FAILURE)

class CorrelationTest(TestCase):

    def setUp(self):
        self.customer1: models.Customer = interaction.signUp("abc", "Alpha Bet", "a@b.c", "+1(234)567-9999", "5xyzabcxyz5")[1]
        self.item1 = interaction.addItemType("A", "a", "a", "0", "0", "0", "U", "", "",
                [("Power", .8), ("Masculinity", .75), ("Freshness", .7), ("Wooden", .65), ("Warmth", .6)])[1]
        self.item2 = interaction.addItemType("B", "b", "b", "0", "0", "0", "U", "", "",
                [("Power", .9), ("Masculinity", .1), ("Freshness", -.98), ("Warmth", .6), ("Pleasant", -1.0)])[1]
        self.item3 = interaction.addItemType("C", "c", "c", "0", "0", "0", "U", "", "",
                [("Femininity", .3), ("Freshness", 0)])[1]


    def test_correlation(self):

        interaction.addQualitiesCustomer(
            [("Power", .8), ("Masculinity", .5), ("Wooden", .02), ("Warmth", .8888888888888)],
            self.customer1
        )

        # print(list(models.QualityItemTypeJoin.objects.all()))

        print(interaction.getCorrelations(self.customer1)) # A then B, no C
        print(interaction.getCorrelations(self.customer1, False)) # A then B; C preferably last
