import time
from functions import Functions
from Itsupport import it_support_task
import config
from tenant_list import tenant_list

driver = Functions.get_chrome_driver()

for tenant in tenant_list:
    config.tenant = tenant
    config.sub_tenant = tenant.split('.')[0]
    config.full_url = "https://" + tenant
    config.auth_url = config.full_url + "/auth/maintenance/login"
    config.stream = f"https://{config.sub_tenant}-sf.oa.iqvia.com/dashboard/index.html#/streams/list"
    config.orch = f"https://{config.sub_tenant}-orchflow.oa.iqvia.com/dashboard/index.html#/streams/list"
    #config.pipe = config.full_url + "/datapipeline/maintenance/connection-strings/list"

    start_time = time.time()

    Functions.append_to_notepad(config.file_path, config.tenant)

    # Call the modified login_and_verify_loop and check its return value
    skip_current_tenant = Functions.login_and_verify_loop(driver, config.auth_url, config.full_url, config.outlookfolder,
                                                          config.outlooksubfolder, config.email, max_attempts=10, wait_time=10)

    if skip_current_tenant:
        print(f"Skipping further tasks for {config.tenant} due to invalid login.")
        Functions.append_to_notepad(config.file_path, "Skipped due to invalid login attempt.")
        Functions.append_to_notepad(config.file_path, config.new_line)
        continue # Skip the rest of the current loop iteration and move to the next tenant

    it_support_task.it_support(driver,config.tenant)

    end_time = time.time()
    elapsed_time = (end_time - start_time) / 60
    rounded_elapsed_time = round(elapsed_time, 1)
    print("Elapsed time:", rounded_elapsed_time)
    elapsed_time_str = str(rounded_elapsed_time)

    Functions.append_to_notepad(config.file_path, "Total time taken" + elapsed_time_str + " Minutes")
    Functions.append_to_notepad(config.file_path, config.new_line)
    Functions.append_to_notepad(config.file_path, "Stream check done")