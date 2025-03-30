from playwright.sync_api import sync_playwright, Page
import pytest

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture()
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()

# Test 1: Overeni titulu stranky
def test_homepage_title(page: Page):
    page.goto("https://engeto.cz/")
    assert "ENGETO" in page.title()

# Test 2: Otevreni stranky, odkliknuti cookies, kliknuti na 'Prehled IT kurzu', kliknuti na 'Vice informaci' u 'Testing akademie' a overeni ze na strance je 'Kurz testování softwaru na 6, nebo 12 týdnů'

def test_course_overview_button_exists_and_click(page: Page):
    page.goto("https://engeto.cz/")

    cookies_button = page.locator("#cookiescript_accept")
    cookies_button.wait_for(state="visible")
    cookies_button.click()

    prehled_kurzu_tlacitko = page.locator("body > main > div:nth-child(1) > div > div > a")
    prehled_kurzu_tlacitko.click()

    testing_akademie_vice_informaci = page.locator("#akademie > div.has-text-lg-regular-font-size.fullwidth > div > a:nth-child(6) > span")
    testing_akademie_vice_informaci.click()
    # Nacteni stranky
    page.wait_for_load_state("load")
    
    # Nalezeni textu na strance
    h3_locator = page.locator("h3.has-display-sm-bold-font-size:has-text('Testing je perfektní pro start v IT')")
    
    # Overeni ze text je na strance
    assert h3_locator.is_visible(), "Text 'Testing je perfektní pro start v IT' na stránce nenalezen"

  
# Test 3: Overeni presmerovani na stranku kontaku
def test_contact_page_navigation(page):
    page.goto("https://engeto.cz/")
    # Odkliknuti cookies
    cookies_button = page.locator("#cookiescript_accept")
    cookies_button.wait_for(state="visible")
    cookies_button.click()
    # Kliknuti na 'Kontakt'
    page.locator("#top-header > div > a.contact-link.has-text-sm-semibold-font-size.has-white-color").click()
    page.wait_for_load_state("load")
    # Existence 'kontakt' v url stranky
    assert "kontakt" in page.url.lower()
