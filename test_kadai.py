from playwright.sync_api import Page
import pytest
import datetime


class TestHotelPlanisphere(object):

    @pytest.fixture(scope="function", autouse=True)
    def page_fixture(self, page: Page):
        self.page = page
        self.page.goto("https://hotel.testplanisphere.dev/ja/reserve.html?plan-id=0", wait_until="networkidle")
        yield
        self.page.close()

#  ①当日日付以前を設定すると予約できないこと
    def test_before_today(self):
        page = self.page

    #  宿泊日
        textbox_date = page.locator("#date")
        date_list = page.input_value("#date").split("/")
        year = date_list[0]
        month = date_list[1]
        day = date_list[2]
        year_today = str(datetime.date.today().year)
        month_today = str(datetime.date.today().month)
        day_today = str(datetime.date.today().day)

        if (year == year_today) and (month == month_today) and (day == day_today):
            print("宿泊日：", year, "年", month, "月", day, "日")
        else:
            textbox_date.fill(year_today + "/" + month_today + "/" + day_today)
            textbox_date.press("Tab")

        #  宿泊数

            page.fill("#term", "1")

        #  宿泊数
            page.fill("#term", "1")

        #  宿泊数
            page.fill("#term", "1")

        #  宿泊人数
            page.fill("#head-count", "1")

        #  追加プラン
            page.check("#breakfast")

        #  氏名
            page.fill("#username", "古賀")

        #  確認のご連絡
            page.select_option("#contact", "email")

        #  予約内容を確認する
            page.click("#submit-button")

        #  スクリーンショット
            page.screenshot(path="kadai_test1.png")

        #  確認
            assert False
#  ②名前が空の状態では予約できないこと。

    def test_noname(self):
        page = self.page

        #  宿泊日
        textbox_date = page.locator("#date")
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        year_tomorrow = str(tomorrow.year)
        month_tomorrow = str(tomorrow.month)
        day_tomorrow = str(tomorrow.day)

        textbox_date.fill(year_tomorrow + "/" + month_tomorrow + "/" + day_tomorrow)
        textbox_date.press("Tab")

        page.evaluate("document.querySelector('#date').blur()")

        #  宿泊数
        page.fill("#term", "1")

        #  宿泊人数
        page.fill("#head-count", "1")

        #  追加プラン
        page.check("#breakfast")

        #  氏名を入力しない

        #  確認のご連絡
        page.select_option("#contact", "email")

        #  予約内容を確認する
        page.click("#submit-button")

        #  スクリーンショット
        page.screenshot(path="kadai_test2.png")

        #  確認
        assert page.text_content("#username ~ div") == "このフィールドを入力してください。", "名前を入力していなければエラーが出ること"

#  ③3か月以上先の日付では予約できないこと。
    def test_90days(self):
        page = self.page

    #  宿泊日を91日後にする
        textbox_date = page.locator("#date")
        after_90_days = datetime.date.today() + datetime.timedelta(days=91)
        year_90 = str(after_90_days.year)
        month_90 = str(after_90_days.month)
        day_90 = str(after_90_days.day)

        textbox_date.fill(year_90 + "/" + month_90 + "/" + day_90)
        textbox_date.press("Tab")

        #  宿泊数

        page.fill("#term", "1")

        #  宿泊人数
        page.fill("#head-count", "1")

        #  追加プラン
        page.check("#breakfast")

        #  氏名
        page.fill("#username", "古賀")

        #  確認のご連絡
        page.select_option("#contact", "email")

        #  予約内容を確認する
        page.click("#submit-button")

        #  スクリーンショット
        page.screenshot(path="kadai_test3.png")

        #  確認
        assert page.text_content("#date ~ div") == "3ヶ月以内の日付を入力してください。", "3か月以上先の日付を入力するとエラーが出ること。"
