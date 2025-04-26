import random


class Mahdi:
    def __init__(self, name:list):
        self.name = name
        self.sucsses_rate = 0.7

    def wink(self, target_name = None):
        if not target_name:
            target_name = random.choice(self.name)
        if random.random() < self.sucsses_rate:
            print(f'{target_name}بیا برات بخورم 💋')
        else:
            print(f'{target_name}  به کیرشم حسابت نکرد🤣')


    def multi_wink(self, number):
        for _ in range(number):
            self.wink()

    
    def add_name(self, new_name):
        self.name.append(new_name)
        print(f'{new_name}به لیست علاقه مندیا اضافه شد')

    def remove(self, old_name):
        self.name.remove(old_name)
        print(f'{old_name} با موفقیت حذف شد')


    def show_name(self):
        print(f'لیست کسای که مهدی دوست داره بهشون بده')

        r = 0
        for n in self.name:
            r+=1
            print(f'{r}_ {n}')
    

l_mahdi = ['sara', 'saba', 'ali', 'abolfazl']

mehdi = Mahdi(l_mahdi)

# mehdi.add_name('mohsen')
# mehdi.wink()
# mehdi.show_name()
# mehdi.remove('ali')
mehdi.multi_wink(3)
