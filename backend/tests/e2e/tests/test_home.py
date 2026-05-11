from  tests.e2e.pages.home_page import HomePage


def test_hero_section(driver):
    page = HomePage(driver)

    assert "Ibn Al-Haitham GPA Assistant" in page.get_heading_text()

def test_github_link(driver):
    page = HomePage(driver)

    page.open_github()
    assert "github.com/ibrahimhabibeg/gpa-assistant" in driver.current_url

def test_trello_link(driver):
    page = HomePage(driver)

    page.open_trello()
    assert "trello.com/b/THUbWFxZ/gpa-assistant" in driver.current_url
def test_jira_link(driver):
    page = HomePage(driver)

    page.open_jira()
    assert "https://gpaassistant.atlassian.net/jira" in driver.current_url
