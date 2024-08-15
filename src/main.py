from sharepoint import final_download
from process_data import final_process
from sendgrid_mail import final_send, final_send_test

def test_unity():
    final_download()
    final_process()
    final_send_test()

def run_unity():
    final_download()
    final_process()
    final_send()

if __name__ == "__main__":
    test_unity()
    # run_unity()