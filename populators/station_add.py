from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("http://127.0.0.1:8000/add_station")

stations = {
    'Dhaka': ['Kamalapur Railway Station','Dhaka Airport Railway Station','Tangail Railway Station','Bhairab Bazar Railway Station','Narsingdi Railway Station','Joydebpur Railway Station','Kishoreganj Railway Station','Narayanganj Railway Station','Gazipur Railway Station','Gopalganj Railway Station','Faridpur Railway Station','Tongi Railway Station','Tejgaon Railway Station','B.B. East Railway Station','Rajbari Railway Station'],
    'Rajshahi' : ['Akkelpur Railway Station','Joypurhat Railway Station','Sonatola Railway Station','Natore Railway Station','Pabna Railway Station','Ishwardi Railway Station','Ullapara Railway Station','Hili Railway Station','Santahar Railway Station','Panchbibi Railway Station','Bogra Railway Station','Raninagar Railway Station','Singra Railway Station','Faridpur Railway Station','Sirajganj Railway Station','Rajshahi Railway Station','Ahsanganj Railway Station','Amnura Railway Station'],
    'Rangpur' : ['Parbatipur Railway Station','Dinajpur Railway Station','Gaibandha Railway Station','Birampur Railway Station','Domar Railway Station','Panchagarh Railway Station','Pirganj Railway Station','Pirgachha Railway Station','Bonarpara Railway Station','Phulbari Railway Station','Chapai Nawabganj Railway Sation','Lalmonirhat Railway Station','Nilphamari Railway Station','Saidpur Railway Station','Kaunia Railway Station','Rangpur Railway Station','Bamondanga Railway Station','Chilahati Railway Station'],
    'Mymensingh' : ['Dewanganj Railway Station','Gaforgaon Railway Station','Bahadurbad Railway Station','Jamalpur Railway Station','Mymensingh Railway Station','Mohanganj Railway Station'],
    'Chittagong' : ['Akhaura Railway Station','Ashuganj Railway Station','Chandpur Railway Station','Comilla Railway Station','Feni Railway Station','Nabinagar Railway Station','Brahmanbaria Railway Station','Chittagong Railway Station','Laksam Railway Station'],
    'Khulna' : ['Khulna Railway Station', 'Jessore Railway Station','Phultala Railway Station','Darshana Railway Station','Mirpur Railway Station','Kustia Railway Station','Chuadanga Railway Station','Daulatpur Railway Station','Noapara Railway Station','Poradah Railway Station','Bheramara Railway Station','Pakshi Railway Station'],
    'Sylhet' : ['Sylhet Railway Station','Kulaura Railway Station','Sreemangal Railway station','Shaistaganj Railway Station'],
}

# stations = ['Kamalapur Railway Station','Dhaka Airport Railway Station','Tangail Railway Station','Bhairab Bazar Railway Station','Narsingdi Railway Station','Joydebpur Railway Station','Kishoreganj Railway Station','Narayanganj Railway Station','Gazipur Railway Station','Gopalganj Railway Station','Faridpur Railway Station','Tongi Railway Station','Tejgaon Railway Station','B.B. East Railway Station','Rajbari Railway Station','Akkelpur Railway Station','Joypurhat Railway Station','Sonatola Railway Station','Natore Railway Station','Pabna Railway Station','Ishwardi Railway Station','Ullapara Railway Station','Hili Railway Station','Santahar Railway Station','Panchbibi Railway Station','Bogra Railway Station','Raninagar Railway Station','Singra Railway Station','Faridpur Railway Station','Sirajganj Railway Station','Rajshahi Railway Station','Ahsanganj Railway Station','Amnura Railway Station','Parbatipur Railway Station','Dinajpur Railway Station','Gaibandha Railway Station','Birampur Railway Station','Domar Railway Station','Panchagarh Railway Station','Pirganj Railway Station','Pirgachha Railway Station','Bonarpara Railway Station','Phulbari Railway Station','Chapai Nawabganj Railway Sation','Lalmonirhat Railway Station','Nilphamari Railway Station','Saidpur Railway Station','Kaunia Railway Station','Rangpur Railway Station','Bamondanga Railway Station','Chilahati Railway Station','Dewanganj Railway Station','Gaforgaon Railway Station','Bahadurbad Railway Station','Jamalpur Railway Station','Mymensingh Railway Station','Mohanganj Railway Station','Akhaura Railway Station','Ashuganj Railway Station','Chandpur Railway Station','Comilla Railway Station','Feni Railway Station','Nabinagar Railway Station','Brahmanbaria Railway Station','Chittagong Railway Station','Laksam Railway Station','Khulna Railway Station', 'Jessore Railway Station','Phultala Railway Station','Darshana Railway Station','Mirpur Railway Station','Kustia Railway Station','Chuadanga Railway Station','Daulatpur Railway Station','Noapara Railway Station','Poradah Railway Station','Bheramara Railway Station','Pakshi Railway Station','Sylhet Railway Station','Kulaura Railway Station','Sreemangal Railway station','Shaistaganj Railway Station']

for key,value in stations.items():
    for station in value:
        station_name = driver.find_element(By.XPATH, '//*[@id="station_name"]')
        station_location = driver.find_element(By.XPATH, '//*[@id="station_location"]')
        station_description = driver.find_element(By.XPATH, '//*[@id="station_description"]')
        add_button = driver.find_element(By.XPATH, '/html/body/form/input[5]')
        station_name.send_keys(f'{station}')
        station_location.send_keys(f'{station.split(" ")[0]}')#use station.split(" ")[0] + ", " + key for jila, division format
        add_button.click()
        print(f'added {station} located in {station.split(" ")[0]}')
        time.sleep(0.15)
