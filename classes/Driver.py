import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager


class Driver(webdriver.Firefox):
    """
    Initialize a custom firefox web driver with a default timeout of 30 seconds
    """

    def __init__(self, *args, **kwargs):
        self.ff_profile_path = os.path.join(os.getcwd(), "assets", "drhphmfl.selenium_profile")

        self.extension_id = "tprb.addon@searxes.danwin1210.me"
        self.user_properties = {}
        self.my_timeout = 10

        "firefox profile"
        profile = FirefoxProfile(self.ff_profile_path)
        "default driver options"
        options = FirefoxOptions()
        options.headless = True

        "install executable (or find in cache) for driver"
        service = Service(GeckoDriverManager().install())

        "initialize driver"
        webdriver.Firefox.__init__(
            self,
            *args,
            **kwargs,
            options=options,
            service=service,
            firefox_profile=profile
        )

    def set_cookies(self):
        """disable pop survey"""
        self.add_cookie({"name": "surveyDisabled",
                         "domain": ".bestbuy.com", "value": "true"})

    def add_user_prop(self, key, value):
        """
        store a user property
        Valid args: ["email", "password", "warranty", "security_code"]
        """
        valid_props = ["email", "password", "warranty", "security_code"]
        try:
            if key in valid_props:
                self.user_properties[key] = value
            else:
                raise ValueError(key + " not a valid argument.")
        except ValueError as e:
            print(e)

    def get_user_prop(self, prop):
        return self.user_properties[prop]

    def take_screenshot(self, directory, name="", add_time=True, rmv_ext=False):
        """
        Takes a screenshot of the current driver's page.
        Uninstalls extensions first.
        Saves picture in /screenshots/<date_and_time>.png
        """
        path = os.path.join(directory, name)
        if add_time:
            path += "-" + \
                    str(datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S")).replace(" ", "-").replace(":", "-")
        path += ".png"

        "uninstall extensions so all web elements are visible for screenshot"
        if rmv_ext:
            try:
                self.uninstall_addon(self.extension_id)
                self.refresh()
            except Exception as e:
                print("Did not remove extensions when requested to take screenshot.")
                print(e)

        try:
            self.save_full_page_screenshot(path)
        except Exception as e:
            print("Did not take screenshot when requested.")
            print(e)

    def initial_login(self):
        """return bool for if user was successfully logged in"""
        try:
            if "https://www.bestbuy.com/identity/signin" not in self.current_url:
                self.get("https://www.bestbuy.com/login")

            login_url = self.current_url
            wait = WebDriverWait(self, timeout=self.my_timeout)

            wait.until(EC.visibility_of_element_located(
                (By.ID, "fld-e"))).send_keys(self.user_properties["email"])
            wait.until(
                EC.visibility_of_element_located((By.ID, "fld-p1"))).send_keys(self.user_properties["password"])

            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "cia-form__controls__submit"))).click()

            wait.until(EC.url_changes(login_url))
            wait.until(EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "v-ellipsis"), "Hi"))
            return True

        except TimeoutException:
            return False

    def check_stock(self):
        """return bool for if button is clickable on watch link"""
        in_stock = None
        times_failed = 0
        while times_failed <= 3:
            try:
                btn_div = self.find_element(
                    By.CLASS_NAME, "fulfillment-add-to-cart-button")
                btn = btn_div.find_element(By.TAG_NAME, "button")

                if not btn.is_displayed() or not btn.is_enabled():
                    in_stock = False
                else:
                    in_stock = True
                break
            except Exception as exp:
                if times_failed == 3:
                    raise NoSuchElementException(exp)
                print("trying " + str(3 - times_failed) + " more times")
                times_failed += 1
                time.sleep(1)
                self.refresh()
        return in_stock

    def add_to_cart(self):
        """click add to cart button (add warranty if selected)"""
        timeout = 10
        wait = WebDriverWait(self, timeout=timeout)
        if self.user_properties["warranty"]:
            try:
                input_div = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, "standard-warranty")))
                inp = WebDriverWait(input_div, timeout).until(
                    EC.element_to_be_clickable((By.TAG_NAME, "input")))
                if not inp.is_selected():
                    inp.click()
            except Exception as e:
                print(
                    "Warranty option could not be selected, still trying to buy item though...")
                print(e)
                pass

        added_to_cart = False
        times_failed = 0
        while not added_to_cart:
            try:
                btn_div = wait.until(EC.presence_of_element_located(
                    (By.CLASS_NAME, "fulfillment-add-to-cart-button")))
                WebDriverWait(btn_div, timeout).until(
                    EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()

                wait.until(EC.visibility_of_element_located(
                    (By.CLASS_NAME, "c-modal-window")))
                added_to_cart = True
            except Exception as exp:
                if times_failed == 3:
                    raise Exception("Could not add item to cart.")
                print(exp)
                print("Did not add item to cart trying " +
                      str(3 - times_failed) + " more times.")
                times_failed += 1
                self.refresh()

    def buy_product(self):
        """the entire process for buying a product"""
        wait = WebDriverWait(self, timeout=self.my_timeout)

        self.get("https://www.bestbuy.com/cart")
        if "https://www.bestbuy.com/identity/signin" in self.current_url:
            self._sign_in_method(wait)
        self._cart_method(wait)
        self.get("https://bestbuy.com/checkout/r/fast-track")

        bought_item = False
        times_failed = 0
        while not bought_item:
            curr_url = self.current_url
            if "/checkout/r/fulfillment" in curr_url:
                self._fulfillment_method(wait)
            elif "/checkout/r/delivery" in curr_url:
                self._delivery_method(wait)
            elif "/checkout/r/payment" in curr_url:
                bought_item = self._payment_method(wait)
            elif "/checkout/r/fast-track" in curr_url:
                bought_item = self._fast_track_method(wait)
            else:
                raise Exception("Did not know what to do with " + curr_url)

            if not bought_item:
                try:
                    wait.until(EC.url_changes(curr_url))
                    times_failed = 0
                except TimeoutException:
                    if times_failed == 3:
                        raise TimeoutException(
                            "Url did not change when expected.")
                    times_failed += 1
                    self.refresh()

    def _sign_in_method(self, wait):
        wait.until(EC.visibility_of_element_located((By.ID, "fld-p1"))
                   ).send_keys(self.user_properties["password"])

        btn_div = wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "cia_form__controls")))
        WebDriverWait(btn_div, timeout=self.my_timeout).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()

    def _cart_method(self, wait):
        matches = ["delivery", "free shipping"]
        lists = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, "availability__list")))
        for li in lists:
            options = WebDriverWait(li, timeout=self.my_timeout).until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "availability__fulfillment")))
            for option in options:
                try:
                    self._wait_until_not_loading()
                    label_text = option.find_element(
                        By.CLASS_NAME, "availability__label").text.lower().replace("\n", " ").strip()

                    if any(s in label_text for s in matches):
                        WebDriverWait(option, timeout=self.my_timeout).until(
                            EC.element_to_be_clickable((By.TAG_NAME, "input"))).click()
                        break
                except Exception as e:
                    print(
                        "Could not click a free shipping option when requested, continuing...")
                    print(e)
                    pass
        self._wait_until_not_loading()

    def _fulfillment_method(self, wait):
        btn_div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "button--continue")))
        self._wait_until_not_loading()
        WebDriverWait(btn_div, timeout=self.my_timeout).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()

    def _delivery_method(self, wait):
        try:
            time_select = wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "tb-select")))
            Select(time_select).select_by_index(1)
        except Exception as e:
            print(
                "Could not pick a time for delivery. It's possible that it was already selected, continuing...")
            print(e)
            pass

        btn_div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "button--continue")))
        self._wait_until_not_loading()
        WebDriverWait(btn_div, timeout=self.my_timeout).until(
            EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()

    def _fast_track_method(self, wait):
        try:
            inp = wait.until(EC.visibility_of_element_located((By.ID, "cvv")))
            inp.clear()
            inp.send_keys(self.user_properties["security_code"])
        except Exception as exp:
            print(exp)
            pass

        btn_div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "payment__order-summary")))

        self._wait_until_not_loading()

        # TODO: uncomment buy method
        # curr_url = self.current_url
        # WebDriverWait(btn_div, timeout=self.my_timeout).until(
        #     EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()
        # WebDriverWait(self, timeout=30).until(EC.url_changes(curr_url))
        return True

    def _payment_method(self, wait):
        try:
            inp = wait.until(EC.visibility_of_element_located(
                (By.ID, "credit-card-cvv")))
            inp.clear()
            inp.send_keys(self.user_properties["security_code"])
        except Exception as exp:
            print(exp)
            pass

        btn_div = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "payment__order-summary")))

        self._wait_until_not_loading()

        # TODO: uncomment buy method
        # curr_url = self.current_url
        # WebDriverWait(btn_div, timeout=self.my_timeout).until(
        #     EC.element_to_be_clickable((By.TAG_NAME, "button"))).click()
        # WebDriverWait(self, timeout=30).until(EC.url_changes(curr_url))
        return True

    def _is_loading(self):
        """return True/False for loading spinner"""
        try:
            self.find_element(By.CLASS_NAME, "page-spinner--in")
            return True
        except NoSuchElementException:
            try:
                self.find_element(By.CLASS_NAME, "page-spinner--out")
                return False
            except NoSuchElementException:
                return True

    def _wait_until_not_loading(self):
        """
        check for page spinner element, waits .5 seconds after spinner element disappears
        checks in intervals of .5 seconds
        raises TimeoutError if not found in 30 seconds
        """
        timeout = time.time() + 30
        while self._is_loading():
            if time.time() > timeout:
                raise TimeoutError("Timed out at checking for page loading.")
            time.sleep(.5)
        time.sleep(1)


"""DRIVER TESTS"""


# drivers = []
# d = Driver()
# d.add_user_prop("warranty", True)
# d.get("https://www.bestbuy.com/site/jlab-go-work-wireless-office-headset-black/6460025.p?skuId=6460025")
# in_stock = d.check_stock()
# if in_stock:
#     d.add_to_cart()
# drivers.append(d)
# d.add_user_prop("warranty", False)
# d.get("https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149")
# time.sleep(3)
# d.refresh()
# in_stock = d.check_stock()
# # added = d.add_to_cart()
# print(d.user_properties)
# if not in_stock:
#     d.quit()
#     drivers.remove(d)
# time.sleep(3)
# print(drivers)
# if __name__ == "__main__":
# driver = Driver()
# driver.get("https://google.com")
# driver.take_screenshot(os.getcwd(), name="test")
# took_pic = driver.save_full_page_screenshot(os.getcwd() + "\\test.png")
# print(str(took_pic))
# driver.take_screenshot(os.getcwd(), name="test", rmv_ext=True)
# ROOT_DIR = Path(__file__).parent.parent
# print(ROOT_DIR)
