import subprocess, os

# from backend.be_server import be_server
#
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

os.sys.path.insert(0, "backend/be_server")
os.sys.path.insert(0, "frontend/fe_server")
# import be_server
if __name__ == '__main__':
    os.system('python3 be_server.py &')
    # subprocess.check_output(run_backend_srver)
    # subprocess.check_output(run_frontend_srver)
