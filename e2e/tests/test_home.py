from pages.home_page import HomePage



def test_hero_section(driver):
    page = HomePage(driver)

    assert "Master Your Academic" in page.get_heading_text()
    assert page.is_subtitle_visible()


def test_github_link(driver):
    page = HomePage(driver)

    page.open_github()
    assert "github.com/ibrahimhabibeg/gpa-assistant" in driver.current_url