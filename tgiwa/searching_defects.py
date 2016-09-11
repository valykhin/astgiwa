# -*- coding: utf-8 -*-
from django.db import IntegrityError
from selenium import webdriver
from jpype import *
from models import Defect, Screenshot


def search_defect(url, test_id, browser='Firefox'):
    status = 0
    try:
        startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\\studing\\django\\astgiwa\\tgiwa\\fighting-layout-bugs.jar")
        if browser == 'Firefox':
            FirefoxDriver = JClass('org.openqa.selenium.firefox.FirefoxDriver')
            driver = FirefoxDriver()
        elif browser == 'Chrome':
            ChromeDriver = JClass('org.openqa.selenium.chrome.ChromeDriver')
            java.lang.System.setProperty("webdriver.chrome.driver", "D://chromedriver.exe");
            driver = ChromeDriver()
        elif browser == 'Safari':
            SafariDriver = JClass('org.openqa.selenium.safari.SafariDriver')
            driver = SafariDriver()
        elif browser == 'Internet Explorer':
            InternetExplorerDriver = JClass('org.openqa.selenium.ie.InternetExplorerDriver')
            driver = InternetExplorerDriver()
        elif browser == 'Edge':
            EdgeDriver = JClass('org.openqa.selenium.edge.EdgeDriver')
            driver = EdgeDriver()
        else:
            print "None browser is selected"
            status = 3
        driver.get(url)
        WebPage = JClass('com.googlecode.fightinglayoutbugs.WebPage')
        webPage = WebPage(driver)
        FightingLayoutBugs = JClass('com.googlecode.fightinglayoutbugs.FightingLayoutBugs')
        screenshotDir = java.io.File(JString('D://studing//django//astgiwa//tgiwa//static//tgiwa//screenshots//'))
        #FightingLayoutBugs.setScreenshotDir('D://studing//django//astgiwa//tgiwa//static//tgiwa//screenshots//')
        flb = FightingLayoutBugs()
        flb.setScreenshotDir(screenshotDir)
        layoutBugs = flb.findLayoutBugsIn(webPage)
        driver.quit()
        for layoutBug in layoutBugs:
            try:
                screenshot = Screenshot(file_path=layoutBug.getScreenshot())
                screenshot.save()
            except IntegrityError:
                print IntegrityError.message
                screenshot = None
            try:
                layout_bug = Defect(test_id=test_id, defect_type_id=1, full_url=layoutBug.getUrl(), screenshot=screenshot,
                                defect_description=layoutBug.getDescription())
                layout_bug.save()
            except IntegrityError:
                status = 2
                print IntegrityError.message
                if screenshot is not None:
                    screenshot.delete()
    except JavaException, ex:
        print JavaException.message(ex)
        status = 1
    finally:
        shutdownJVM()
    return status

