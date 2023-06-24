import store.models as models
import json

class CartItem:
    def __init__(self, id, name, priceCents, salePrice, qty, total, image):
        self.id = id
        self.name = str(name)
        self.priceCents = int(priceCents)
        self.salePrice = int(salePrice)
        self.qty = int(qty)
        self.total = int(total)
        self.image = image


class Cart():
   
    def __init__(self):
        self.items = {}
        self.grandTotal = 0
        
        print("\n\n#####initialized#####\n\n")

    def __str__(self):
        s = f"Cart = [{self.item_count}  \n" 
        for x in self.items:
            ci = self.items[x]
            s += f"    cart item= [{ci.id}, {ci.name}, {ci.qty}, {ci.priceCents},{ci.salePrice}, {ci.total}, {ci.image}]\n"
        s += f"  Grand total: {self.grandTotal}]" 
        return s;
    
    def item_count(self):
        s = 0
        for x in self.items:
            ci = self.items[x]
            s += ci.qty
        return s
    
    def cart_add(self, id):
        itemType = models.ItemType.objects.get(id = id)
        item_id = str(itemType.id)
        if(item_id in self.items):
            self.items[item_id].qty = self.items[item_id].qty + 1
            self.items[item_id].total = self.items[item_id].total + int(itemType.salePrice)
            self.grandTotal = self.grandTotal + int(itemType.salePrice)
        else:
           cart_item = CartItem(itemType.id, itemType.name, itemType.priceCents,itemType.salePrice, 1, itemType.salePrice, itemType.image)
           self.grandTotal = self.grandTotal + int(itemType.salePrice)
           self.items[item_id] = cart_item  #doesn't currently handle out-of-stock case
           
    def cart_remove(self, id):
        itemType = models.ItemType.objects.get(id = id)
        item_id = str(itemType.id)
        if(item_id in self.items):
            self.items[item_id].qty = self.items[item_id].qty - 1
            self.items[item_id].total = self.items[item_id].total - int(itemType.salePrice)
            self.grandTotal = self.grandTotal - int(itemType.salePrice)
            if(self.items[item_id].qty == 0):
                self.items.pop(item_id, None)
   
    def grandTotal(self):
        return self.grandTotal