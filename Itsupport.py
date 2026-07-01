from functions import Functions
import config
from stream_flow import stream_flow
from orchflow import orch_flow

class it_support_task:
    @staticmethod
    def stream_flow(driver, tenant):
        stream_flow(driver)

    @staticmethod
    def orch_flow(driver, tenant):
        orch_flow(driver)

    @staticmethod
    def it_support(driver, tenant):
        Functions.append_to_notepad(config.file_path, "Stream Flow")
        it_support_task.stream_flow(driver, tenant)
        Functions.append_to_notepad(config.file_path, "Orch Flow")
        it_support_task.orch_flow(driver, tenant)
