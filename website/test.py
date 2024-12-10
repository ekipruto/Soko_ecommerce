from intasend import APIService

API_PUBLISHABLE_KEYS='ISPubKey_test_e88ee3d1-c8b8-43cf-bc2d-c9a3110f8b13'
API_TOKEN='ISSecretKey_test_f3eee4d6-2af1-4978-bd9d-3a1eb3db0cbc'

service=APIService(token=API_TOKEN, publishable_key=API_PUBLISHABLE_KEYS, test=True)

create_order=service.collect.mpesa_stk_push(phone_number='0714431840',email='test@gmail.com',amount='1'
                                             ,narrative='purchase of items')
print(create_order)
