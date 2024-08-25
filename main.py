from amazon import getWishlistData, getDataLink
from bestbuy import getItemData

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

while True:
        try:
            itemData = getItemData(link)
            break
        except Exception as e:
            print(e)
print("Wishlist saved")

