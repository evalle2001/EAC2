from django.test import TestCase

# Create your tests here.

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
 
class MySeleniumTests(StaticLiveServerTestCase):
    #carregar una BD de test
    #fixtures = ['testdb.json',]
 
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)
        # creem superusuari
        user = User.objects.create_user("isard", "isard@isardvdi.com", "pirineus")
        user.is_superuser = True
        user.is_staff = True
        user.save()
 
    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l'execució al navegador
        cls.selenium.quit()
        super().tearDownClass()

    def test_check_no_questions_choices(self):
        # anem directament a la pàgina d'accés a l'admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))

        # comprovem que el títol de la pàgina és el que esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )

        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        driver = self.selenium
        elements = 0
        #Creem un superusuari a mà
        driver.find_element(By.XPATH, "//*[@class='model-user']//a[@class='addlink']").click()
        self.assertEqual( self.selenium.title , "Add user | Django site admin")
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('admin123')
        password1_input = self.selenium.find_element(By.NAME, "password1")
        password1_input.send_keys('@€!0U@€!0U')
        password2_input = self.selenium.find_element(By.NAME, "password2")
        password2_input.send_keys('@€!0U@€!0U')
        driver.find_element(By.XPATH, "//input[@value='Save']").click()

        # Posem permisos de staff
        self.assertEqual( self.selenium.title , "admin123 | Change user | Django site admin")
        driver.find_element(By.NAME, "is_staff").click()
        driver.find_element(By.NAME, "_save").click()
        self.assertEqual( self.selenium.title , "Select user to change | Django site admin")
        driver.find_element(By.XPATH, "/html/body/div[1]/header/div[2]/form/button").click()
        self.assertEqual( self.selenium.title , "Logged out | Django site admin" )
        driver.find_element(By.XPATH, "/html/body/div/div/main/div/p[2]/a").click()
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('admin123')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('@€!0U@€!0U')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # Revisem que vegi els choices i questions
        if  driver.find_elements(By.XPATH, "//*[@id='myapp-choice' or @id='myapp-question']"):
          elements = 1
        self.assertEqual(elements, 0, "Hay Choices o Questions")
