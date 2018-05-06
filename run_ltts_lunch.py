import subprocess, os

#
# run_backend_srver = [['screen', '-S', 'backend'],
#                      ['cd', 'backend/'],
#                      ['python3', 'be_server.py', '&']]
#
# run_frontend_srver = [['screen', '-S', 'backend'],
#                       ['cd', 'frontend/'],
#                       ['python3', 'fe_server.py', '&']]

run_backend_srver = ['python3', 'be_server.py', '&']
run_frontend_srver = ['python3', 'fe_server.py', '&']

if __name__ == '__main__':
    subprocess.check_output(run_backend_srver)
    subprocess.check_output(run_frontend_srver)
