#### Important Notes

This program was made with the assumption that you want  
to scalp products that Best Buy limits to one per user.  
This means that you will need a Best Buy account for each  
individual product at the specified url you want to purchase.  

In example:  
You want 3 items of: <https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149>  
You will need three individual Best Buy accounts

- These accounts must be created with an email and password
- **NOT** an oauth method (such as "Sign Up with Google")
- See [example image](https://www.flickr.com/photos/194329591@N06/51649422194/in/dateposted-public/)

This program will default to buying product with free shipping option. However, will not stop trying to buy if  
no free shipping option is found (this is highly unlikely). This program will give Best Buy access to your  
location and will try to find a store near you. If there is no store near you with availability,  
scalper with not buy product. Best Buy changes there website somewhat frequently.  
This means that this application is susceptible to break and may need necessary updates  
in order to work properly. Here is [Best Buy's Support Page](https://www.bestbuy.com/site/electronics/customer-service/pcmcat87800050001.c?id=pcmcat87800050001)  
that will be helpful if you wish to make any changes  
to orders that were processed (like returns or changes).

#### Before Scalping

1. For every account you are using
    - Go to <https://www.bestbuy.com>
    - Login
    - Go to account settings
    - Set up a valid default payment method
    - Set up a valid default shipping address
    - Clear your cart of any products you do not want to purchase
2. Make sure you do not have anything masking your public ip address
    - This includes a VPN or proxy
    - This [website](https://whatismyipaddress.com) should show you your current valid location
    - If it does not, find out why before continuing
    - Best Buy needs to know your real location for any reason it selects in-store pickup
3. [Download Firefox](https://www.mozilla.org/en-US/firefox/new/) (if you don't have it already)
    - This is the browser that this application uses
4. Set your computer's sleep settings to never sleep/hibernate
    - This will cause application to stop running
    
#### Mac

When trying to launch another instance of the application,  
it will just focus the window you currently have open.  
To get around this you will need to:

1. Go to the location where the app is stored on your computer
2. Right-click on the app
3. Select the option "New Terminal at Folder"
4. Use the command: ***open -n .***
   - Make sure you enter the period and spacing is correct
   - Enter this command for every app you want open
6. Close the terminal window when you have all your apps

#### Troubleshooting

1. Make sure Firefox is downloaded and up-to-date
2. Checking link/logins on Windows:
   - Sometimes web browser does not initialize properly
   - Just try a few more times
   - Once it is running, it is good to go
3. 'Something went wrong error'
   - Sometimes Best Buy forbids requests if too many hits are being made on server
   - More specifically on login
   - Try again later (maybe a couple of hours)