import os


if __name__ == '__main__':
    if not os.path.exists('backend/send_to_chef_files'):
        os.makedirs('backend/send_to_chef_files')
    if not os.path.exists('frontend/order_files'):
        os.makedirs('frontend/order_files')

    os.system('python3 backend/be_server.py &')
    os.system('python3 frontend/fe_server.py &')
