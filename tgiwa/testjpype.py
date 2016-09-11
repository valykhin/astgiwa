from jpype import *

startJVM(getDefaultJVMPath(), "-Djava.class.path=D:\\studing\\django\\astgiwa\\tgiwa\\fighting-layout-bugs.jar")
FirefoxDriver = JClass('org.openqa.selenium.firefox.FirefoxDriver')
driver = FirefoxDriver();
testPageUrl = "http://127.0.0.1:8000/"; 
driver.get(testPageUrl); 
WebPage = JClass('com.googlecode.fightinglayoutbugs.WebPage')
webPage = WebPage(driver);
FightingLayoutBugs = JClass('com.googlecode.fightinglayoutbugs.FightingLayoutBugs')
flb = FightingLayoutBugs(); 
layoutBugs = flb.findLayoutBugsIn(webPage); 
print type(layoutBugs)
print layoutBugs[0].getUrl()
driver.quit()
shutdownJVM()