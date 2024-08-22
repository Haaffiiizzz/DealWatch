from amazon import getWishlistData, getDataLink

while True:
    try:
        getDataLink("https://a.co/d/2PrUwpj")
        break
    except Exception as e:
        print(e.args[0])
        
