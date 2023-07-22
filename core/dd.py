{'method': 'IDENTITY', 
 'callback_type': 'IDENTITY', 
 'callback_code': 'IDENTITY_IS_READY', 
 'type': 'CALLBACK', 
 'code': 'IDENTITY_IS_READY', 
 'callbackURL': 'https://payskul-demo.up.railway.app/core/webhook/', 
 'env': 'production', 
 'status': 'is_success', 
 'started_at': '2023-07-22T01:06:52.508Z', 
 'ended_at': '2023-07-22T01:07:27.525Z', 
 'message': 'Successfully fetched identity',
 'options': {}, 'meta': {}, 
 'bankName': 'Kuda Bank', 'bankType': '5f0cf73e8a8bcc18b8156ad7', 
 'bankId': '5f0cf73e8a8bcc18b8156ad7', 'bankSlug': 'kuda-bank', 
 'record': '64bb2bac1231db003b293684', 'recordId': '64bb2bac1231db003b293684', 'callback_url': 'https://api.okra.ng/v2/callback?record=64bb2bac1231db003b293684&method=IDENTITY', 
 'customerId': '63d43e042e2c240013b94ed5', 
 'customerBvn': '22334507774', 'country': 'NG', 'extras': {}, 
 'identity': 
         {'enrollment': {
             'bank': '033', 'branch': 'Oko Oba', 'registration_date': '2015-09-08'}, 'aliases': [], 'phone': ['07068733754'], 'email': [], 'verified': False, 'next_of_kins': [], 'address': ['33 Fatai Omisakin Street'], 
          'owner': '63f157fbbad20d13e7664894', 
          'record': '64bb2bac1231db003b293684', 
          'bvn_updated': False, 
          'smileId': False, 
          'paystackId': False, 
          'ref_ids': [], 'merged': False, 
          'fbn_fix': False, 'merged_ids': [], 
          'projects': ['63f157fb1a0f603b1b58423f'], 
          '_id': '63d43dfb567faa9d15a8daa8', 'bvn': '22334507774', 
          '__v': 0, 'created_at': '2023-01-27T21:11:23.739Z', 
          'dob': '2001-08-12', 
          'firstname': 'Michael', 'fullname': 'Michael Chinonso Asomugha', 
          'gender': 'Male', 'is_bvn_verified': True, 
          'last_bvn_processed': '2023-01-27T21:11:23.738Z', 
          'last_updated': '2023-07-22T00:56:01.457Z', 
          'lastname': 'Asomugha', 
          'level_of_account': 'Level 1 Low Level Accounts', 
          'lga_of_origin': 'Umuahia South', 
          'lga_of_residence': 'Alimosho', 
          'marital_status': 'Single', 
          'middlename': 'Chinonso', 
          'nationality': 'Nigeria', 
          'nin': None, 'photo_id': [{'_id': '647505f653ccae002f53eb6f', 'url': 'https://dv7b45oo546j4.cloudfront.net/NDQ1OTMzMTAxNw%3D%3D.png', 'image_type': 'bvn_photo'}], 'state_of_origin': 'Abia State', 'state_of_residence': 'Lagos State', 'verification_country': 'NG', 'watch_listed': 'No', 'customer': '63d43e042e2c240013b94ed5', 'employer': []}
 
 }






{'method': 'BALANCE', 
 'callback_type': 'BALANCE', 
 'callback_code': 'BALANCE_SUCCESS', 
 'type': 'CALLBACK', 
 'code': 'BALANCE_SUCCESS', 
 'callbackURL': 'https://payskul-demo.up.railway.app/core/webhook/', 
 'env': 'production', 'status': 'is_success', 'started_at': '2023-07-22T02:21:49.764Z', 'ended_at': '2023-07-22T02:22:37.504Z', 
 'message': 'Successfully fetched balance', 'options': {}, 'meta': {}, 
 'bankName': 'Kuda Bank', 'bankType': '5f0cf73e8a8bcc18b8156ad7', 
 'bankId': '5f0cf73e8a8bcc18b8156ad7', 'bankSlug': 'kuda-bank', 
 'record': '64bb3d3d1231db003b293ec3', 'recordId': '64bb3d3d1231db003b293ec3', 'callback_url': 'https://api.okra.ng/v2/callback?record=64bb3d3d1231db003b293ec3&method=BALANCE', 
 'customerId': '63d43e042e2c240013b94ed5', 
 'customerBvn': '22334507774', 'country': 'NG', 'extras': {}, 
 'nuban': '2007084982', 
 'balance': {
     'nuban': '2007084982', 'name': 'ASOMUGHA, CHINONSO MICHAEL',
     'ledger_balance': 153.37, 'available_balance': 153.37, 'currency': 'NGN', 'status': 'Active', 'accountId': '64ba5a64303403e516f98b3c'
     }}



{'method': 'ACCOUNTS', 
 'callback_type': 'ACCOUNTS', 'callback_code': 'ACCOUNTS_SUCCESS', 
 'type': 'CALLBACK', 'code': 'ACCOUNTS_SUCCESS',
 'callbackURL': 'https://payskul-demo.up.railway.app/core/webhook/', 
 'env': 'production', 'status': 'is_success', 
 'started_at': '2023-07-22T02:21:49.764Z', 
 'ended_at': '2023-07-22T02:22:37.518Z', 
 'message': 'Successfully fetched accounts', 
 'options': {}, 'meta': {}, 'bankName': 'Kuda Bank', 
 'bankType': '5f0cf73e8a8bcc18b8156ad7', 
 'bankId': '5f0cf73e8a8bcc18b8156ad7', 
 'bankSlug': 'kuda-bank', 
 'record': '64bb3d3d1231db003b293ec3', 
 'recordId': '64bb3d3d1231db003b293ec3', 
 'callback_url': 'https://api.okra.ng/v2/callback?record=64bb3d3d1231db003b293ec3&method=ACCOUNTS', 
 'customerId': '63d43e042e2c240013b94ed5',
 'customerBvn': '22334507774', 'country': 'NG', 'extras': {}, 'nuban': '2007084982', 'account': {'nuban': '2007084982', 'name': 'ASOMUGHA, CHINONSO MICHAEL', 'ledger_balance': 153.37, 'available_balance': 153.37, 'currency': 'NGN', 'status': 'Active', 'account': '64ba5a64303403e516f98b3c', 'accountId': '64ba5a64303403e516f98b3c'}
 }




{'method': 'AUTH', 'callback_type': 'AUTH', 'callback_code': 'AUTH_SUCCESS', 'type': 'CALLBACK', 'code': 'AUTH_SUCCESS', 'callbackURL': 'https://payskul-demo.up.railway.app/core/webhook/', 'env': 'production', 'status': 'is_success', 'started_at': '2023-07-22T02:21:49.764Z', 'ended_at': '2023-07-22T02:22:37.397Z', 'message': 'Successfully fetched auth', 'options': {}, 'meta': {}, 'bankName': 'Kuda Bank', 'bankType': '5f0cf73e8a8bcc18b8156ad7', 'bankId': '5f0cf73e8a8bcc18b8156ad7', 'bankSlug': 'kuda-bank', 'record': '64bb3d3d1231db003b293ec3', 'recordId': '64bb3d3d1231db003b293ec3', 'callback_url': 'https://api.okra.ng/v2/callback?record=64bb3d3d1231db003b293ec3&method=AUTH', 'customerId': '63d43e042e2c240013b94ed5', 'customerBvn': '22334507774', 'country': 'NG', 'extras': {}, 'auth': {}}