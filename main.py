# This script is an attempt to automate some steps for IPM sever set-up.
# This script requires the following:
#
# Selenium chrome webdriver of appropriate version to be downloaded at
# https://chromedriver.chromium.org/downloads
#
# An excel sheet containing the following information: store number and
# store ups IP address. Currently this script only contain a single,
# static store number and IP address
#
# An implementation to process store numbers into 2 numbers, one for the
# original number, and one for the 4 digit version of the number is also
# necessary. Some places for node subview you need the original number,
# other places like creating EXSi hosts you need the 4 digit conversion
# of the number. BOTH HAS TO BE IN STRING FORMAT, just use for each,
# str(x)
#
# The transformation of columns into lists and its usage in this script
# are yet to be implemented. Please see my Bell Webscraper scripts for
# an example of pandas, and put the whole script in a "for x in range(
# len(store_list)).
#
# To implement fail safe features, you can implement flow control over
# each step along with a console interface. For example, once each step
# done, user has to press enter to continue to the next step. Furthermore,
# include a console prompt at the beginning for user to indicate which
# step to begin on. In case a step fails, you can resume at the step
# where it failed.
#
# If you encounter a element is stale error in future inplementation,
# quit the current driver and relaunch the page. That is the only fix.
#
# There is a slight possibility that element with //*[@id="ext-gen32"]
# will stop working. It should work but in case it doesn't, it is fine
# to replace it with /html/body/div[2]/div[2]/div/ul/
#
# Good luck!

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


import re
import time
import supporting_css

######################################################
# Default chrome options to bypass "Connection not private" flag

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')

#####################################################
# Launches webdriver, see & change url in supporting_css module
driver = supporting_css.reload(chrome_options)

action = ActionChains(driver)

######################################################
######################################################
######################################################
# Part 1: Node discovery
# Requires: Store UPS IP Address

######################################################
######################################################
######################################################

# Allow additional time to wait for load.
time.sleep(10)

# Clicks on the discovery tab on the left panel. If this part fails to work, replace the XPATH with a FULL PATH from
# inspect page.
discovery_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="ext-gen32"]/div/li[4]/ul/li[1]/div/a/span')
discovery_button.click()

#####################################################

# Clicks on address scan on the right panel
address_scan = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[2]/div/div/ul/li[3]/a')
address_scan.click()

# Locates the input bar for IP address and clears the pre-filled input
input_bar = supporting_css.exp_wait(driver, By.CLASS_NAME, 'x-form-element').find_element_by_tag_name('input')
input_bar.clear()

time.sleep(3)

# Enters new input
input_bar.send_keys("10.122.149.75")
input_bar = None

# Submit button (since this is the first step, body/div[14] is usually the case.
# In case it fails, replace XPATH by identifying the class name of the pop up window.
submit_button = driver.find_element_by_xpath('/html/body/div[14]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
submit_button.click()
submit_button = None

######################################################
######################################################
######################################################
# Part 2: Create sub-view & filter
# Requires:
# Store Number (Original and 4 digit)
#
# This step must be completely clean (there can not be
# subviews already created for the store.)

######################################################
######################################################
######################################################

time.sleep(10)

# Clicks on the "node" button on the left panel
node_list_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="ext-gen32"]/div/li[1]/ul/li[1]/div/a/span')
node_list_button.click()

time.sleep(3)

# Right clicks on the same button to bring up "Create a sub view"
action.context_click(node_list_button).perform()

create_sub_view = driver.find_element_by_link_text("Create a sub view")
create_sub_view.click()

time.sleep(3)

# Find the input bar and clears the pre-filled entry
input_bar = supporting_css.exp_wait(driver, By.CLASS_NAME, 'x-form-element').find_element_by_tag_name('input')
input_bar.clear()

time.sleep(3)

# Original store number
input_bar.send_keys("Store " + "245")

input_bar = None

# Finds the submit button for creating sub view
submit_button = driver.find_element_by_xpath('/html/body/div[23]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
submit_button.click()

submit_button = None

# Allow changes to save
time.sleep(5)

# The webdriver needs to quit at this moment to allow changes to reflect in a more "normal" way
driver.quit()

# Restarts the login
driver = supporting_css.reload(chrome_options)

action = ActionChains(driver)

#
time.sleep(5)

# Now goes back to the node list and finds the newly created node by taking the whole list of nodes first
node_list = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/ul/div/li[1]/ul/li[1]/ul').find_elements_by_tag_name('a')

# Loops through to find the newly created node
for element in node_list:
    node_name = element.find_element_by_tag_name('span').text
    # Original store number
    if node_name == ("Store " + "245"):
        print("found")
        # Right clicks the created sub view
        action.context_click(element).perform()
        break

node_filter = driver.find_element_by_link_text('Edit filter view')
node_filter.click()

time.sleep(1)

# Add rule button
add_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div[1]/div/div/div[1]/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
add_button.click()

time.sleep(0.5)

# Clicks on the "Name" field
input_bar = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[2]')
input_bar.click()

time.sleep(0.5)

# Clicks on an input receiver element created as a result of the previous click and brings up the drop down menu
input_bar_2 = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[2]/div')
input_bar_2.click()

input_bar = None

time.sleep(1)

# Clicks on "Name" in the drop down menu
input_bar = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-layer x-combo-list "]/div/div[10]')
input_bar.click()

input_bar = None

# Finds the operator field
input_bar = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[3]/div/div')
input_bar.click()

# Clicks on the resulting input receiver and brings up drop down menu
input_bar_2 = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[3]/div')
input_bar_2.click()

input_bar = None

time.sleep(1)

# Clicks on "contains" in the drop down menu
input_bar = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-layer x-combo-list "][2]/div/div[7]')
input_bar.click()

input_bar = None

# Clicks on the input field
input_bar = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[1]/div/table/tbody/tr/td[4]/div/div')
input_bar.click()

# Finds the resulting input receiver and enters the 4 digit version of store number.
input_bar_2 = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/div[4]/input')
input_bar_2.send_keys("0245")

# Saves the filter view.
submit_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
submit_button.click()

######################################################
######################################################
######################################################
# Part 3: Adding ESXi Hosts
# Requires:
# Store Number (4 digit)
#
# This step must be completely clean (there can not be
# hosts already created for the store.)

######################################################
######################################################
######################################################

time.sleep(10)

# Finds and clicks the connector button
connector_button = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[2]/div[2]/div/ul/div/li[4]/ul/li[3]/div/a/span')
connector_button.click()

time.sleep(3)

# To create connector 03 and 04
for x in range(3,5):
    # Add connector button
    add_connector = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[2]/div/div/ul/li[1]/a')
    add_connector.click()

    time.sleep(2)

    # Selects the input field and select ESXi Hosts in drop down,
    input_bar = supporting_css.exp_wait(driver, By.CLASS_NAME, 'x-form-element').find_element_by_tag_name('input')
    input_bar.click()

    input_bar = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-layer x-combo-list "][1]/div/div[3]')
    input_bar.click()

    # Required for page to load
    time.sleep(2)

    # Selects the newly popped up input fields, the first one in this case and enters host name
    input_bar = driver.find_elements_by_class_name('x-form-element')[1].find_element_by_tag_name('input')
    input_bar.click()

    # Four digit store number
    input_bar.send_keys("pe0" + "0245" + "pr0" + str(x))

    # Enters username and password
    input_bar = driver.find_elements_by_class_name('x-form-element')[2].find_element_by_tag_name('input')
    input_bar.click()

    input_bar.send_keys("root")

    input_bar = driver.find_elements_by_class_name('x-form-element')[3].find_element_by_tag_name('input')
    input_bar.click()

    input_bar.send_keys("D!>!ne@889")

    # Submit and creates the node
    submit_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window x-resizable-pinned"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
    submit_button.click()

    # Allowance for waits
    time.sleep(2)

######################################################
######################################################
######################################################
# Part 4: Adding shutdown policy
# Requires:
# Store Number (4 digit and original store number)
#
# This step must be completely clean (there can not be
# hosts already created for the store.)

######################################################
######################################################
######################################################

# Clicks into policies on the left panel
config_policy = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[2]/div[2]/div/ul/div/li[3]/ul/li[3]/div/a/span')
config_policy.click()

time.sleep(5)

# Find the store 1557 reference policy
policy_list = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div').find_elements_by_tag_name('span')

for element in policy_list:
    if element.text == "Store 1557 ESXi Shutdown Policy":
        element.click()
        time.sleep(3)
        break

time.sleep(1)

# Copies store 1557 Policy
copy_policy = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/ul/li[4]/a')
copy_policy.click()

time.sleep(1)

# Enters new name. Original store number.
input_bar = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window"]/div[2]/div[1]/div/div/div/div/div/form/div[1]/div[1]/input')
input_bar.send_keys("Store " + "245 " + "ESXi Shutdown Policy")

# Saves the new policy
submit_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
submit_button.click()

time.sleep(5)

# Quits and relaunches the driver to allow actual creation of the policy or whatever weird stuff it has to do.
driver.quit()

driver = supporting_css.reload(chrome_options)

action = ActionChains(driver)

# Clicks on the policy button on the left panel again just in case.
config_policy = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[2]/div[2]/div/ul/div/li[3]/ul/li[3]/div/a/span')
config_policy.click()

time.sleep(5)

# Now finds the newly created policy in the list.
policy_list = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div').find_elements_by_tag_name('span')

for element in policy_list:
    # Original store number
    if element.text == "Store " + "245" + " ESXi Shutdown Policy":
        element.click()
        time.sleep(3)
        break

time.sleep(1)

# Edits the policy
edit_policy = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/ul/li[2]/a')
edit_policy.click()

time.sleep(1)

# Button to edit nodes
button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window"]/div[2]/div[1]/div/div/div/div/div/form/div[2]/div/div/table/tbody/tr/td[2]/em/button')
button.click()

# Finds the two pre-selected nodes for 1557
deselect_one = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/form/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/div[1]')
deselect_two = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/form/div/div[3]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div/div/div[2]/div[2]')

# Selects both using SHIFT
action.key_down(Keys.SHIFT).click(deselect_one).click(deselect_two).key_up(Keys.SHIFT).perform()

# Move them out/deselect them from list.
deselect_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div/div/table[2]/tbody/tr/td[2]/em/button')
deselect_button.click()

# Saves the node change
time.sleep(2)
save_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
save_button.click()

time.sleep(1)

# Saves the changes for policy
submit_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
submit_button.click()

time.sleep(5)

# Quits and relaunches page for changes to take effect... goes back into the policy... you get the idea now
driver.quit()

driver = supporting_css.reload(chrome_options)

action = ActionChains(driver)

config_policy = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[2]/div[2]/div/ul/div/li[3]/ul/li[3]/div/a/span')
config_policy.click()

time.sleep(5)

policy_list = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div').find_elements_by_tag_name('span')

for element in policy_list:
    # Original store number
    if element.text == "Store " + "245" + " ESXi Shutdown Policy":
        element.click()
        time.sleep(3)
        break

time.sleep(1)

edit_policy = supporting_css.exp_wait(driver, By.XPATH, '/html/body/div[3]/div/div/div/div/div/div[2]/div[2]/div/div[1]/div/div/ul/li[2]/a')
edit_policy.click()

time.sleep(1)

# Opens up the ESXi node selection list again
button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window"]/div[2]/div[1]/div/div/div/div/div/form/div[2]/div/div/table/tbody/tr/td[2]/em/button')
button.click()

# On the left side, performs a complete search (you can restrict this to just the "computer room" section but I wanted to be safe)
left_panel_search = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/form/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div')

# Finds all div child elemnts of that whole list.
search_list = left_panel_search.find_elements_by_tag_name('div')
list_length = len(search_list)

# Selects the first instance of pr03 host it encounters. I've tried to do both in the same for loop but there is
# No way to count how many matches there will be in the whole list (there will be duplicate matches)
for element in search_list:
    if element.text == ("pe" + "00245" + "pr03"):
        action.key_down(Keys.SHIFT).click(element).key_up(Keys.SHIFT).perform()
        time.sleep(3)
        break

# for pr04
for element in search_list:
    if element.text == ("pe" + "00245" + "pr04"):
        action.key_down(Keys.SHIFT).click(element).key_up(Keys.SHIFT).perform()
        time.sleep(3)
        break

# Puts them into the right hand list.
select_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/form/div/div[2]/div/div/table[1]/tbody/tr/td[2]/em/button')
select_button.click()

# Saves the node changes
time.sleep(2)
save_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
save_button.click()

time.sleep(1)

# Edit power source button
edit_power_source = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window"]/div[2]/div[1]/div/div/div/div/div/form/div[4]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div/div[5]/table/tbody/tr/td[4]/div/img')
edit_power_source.click()

# Again, finds the desired power source from the list. Should not be restricted to any individual section of the list
power_source_list = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/form/div/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[2]/div')
search_list = power_source_list.find_elements_by_tag_name('div')

for element in search_list:
    # Four digit version of store number
    if element.text == ("ups0" + "0245" + ".ngco.com"):
        element.click()
        time.sleep(3)
        break

# Saves the power source change
save_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@id="SelectItemsBase-window"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
save_button.click()

# Saves the edited policy
submit_button = supporting_css.exp_wait(driver, By.XPATH, '//*[@class="x-window"]/div[2]/div[1]/div/div/div/div/div/div/div/div/table/tbody/tr/td[1]/table/tbody/tr/td[2]/em/button')
submit_button.click()

time.sleep(5)

# End of step 4


