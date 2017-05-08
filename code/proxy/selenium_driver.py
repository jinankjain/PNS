import argparse

from alexa_fetcher import get_top_domains
from selenium import webdriver, common


def run(args):
    PROXY = "localhost:" + str(args.proxy_port)
    # Create a copy of desired capabilities object.
    desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    # Change the proxy properties of that copy.
    desired_capabilities['proxy'] = {
        "httpProxy": PROXY,
        "sslProxy": PROXY,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    }

    driver = webdriver.Remote("http://localhost:9515", desired_capabilities)

    try:
        for (idx, domain) in enumerate(get_top_domains(args.n,
                                                       args.start_from)):
            url = "http://" + domain
            print("Fetching %s. (%d out of %d) " % (url, idx + 1, args.n))
            try:
                driver.get(url)
            except common.exceptions.TimeoutException:
                print("Fetching %s timed out." % url)
            except common.exceptions.RemoteDriverServerException as exc:
                print("Caught remote driver server exception: %s" % str(exc))
            except Exception as exc:
                print("Caught generic exception: %s" % unicode(exc))
    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", type=int, required=True)
    parser.add_argument("--start-from", type=int, default=0)
    parser.add_argument("--proxy-port", type=int, default=8080)
    args = parser.parse_args()
    run(args)
