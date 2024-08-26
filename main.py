from amazon import getWishlistData, getDataLink
from bestbuy import getItemData, searchItem

# what = input("do you want to import a wishlist or singular item?(Answer W for Wishlist or S for SIngular item):\n")

# if what.upper() == "W":
#     link = input("Paste in the link to your wishlist:\n")
#     while True:
#         try:
#             wishlist = getWishlistData(link)
#             break
#         except Exception as e:
#             print(e)
#     print("Wishlist saved!")
#     items = wishlist
# else:
#     link = input("Paste in the link to your item:\n")
#     while True:
#         try:
#             itemData = getDataLink(link)
#             break
#         except Exception as e:
#             print(e)
#     print("Item saved!")
#     items = itemData
    
    
# print(items)

print(search)
link = "https://www.bestbuy.ca/en-ca/product/asus-rog-swift-32-4k-ultra-hd-240hz-0-03ms-gtg-oled-led-g-sync-gaming-monitor-pg32ucdm/17728627"
while True:
        try:
            itemData = getItemData(link)
            break
        except Exception as e:
            print(e)
print("Wishlist saved")
print(itemData)
